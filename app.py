import gradio as gr
import chromadb
import uuid
import json
from typing import List, Tuple

# --- Configuración de ChromaDB ---
try:
    # A colección DEBE ser en memoria (non persistente)
    chroma_client = chromadb.Client()
    COLLECTION_NAME = "documents"
    collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)
    print(f"ChromaDB en memoria inicializada. Colección: {COLLECTION_NAME}")
except Exception as e:
    print(f"ERRO ao inicializar ChromaDB: {e}")
    collection = None
    
# --- Funcións de Lóxica ---

def process_and_add_files(file_list: List[gr.File]) -> str:
    """
    Procesa unha lista de ficheiros subidos, valida se son JSON, 
    extrae o texto e engádeos á colección ChromaDB.
    """
    if not collection:
        return "⚠️ Erro: A base de datos ChromaDB non está dispoñible."
    
    if not file_list:
        return "Non se subiu ningún ficheiro."

    documents = []
    metadatas = []
    ids = []
    success_count = 0
    
    for file_obj in file_list:
        file_path = file_obj.name
        file_name = file_path.split("/")[-1]
        
        # Validación de tipo de ficheiro
        if not file_name.lower().endswith(('.json', '.txt')):
             return f"❌ Erro: O ficheiro '{file_name}' non é un ficheiro JSON ou TXT (Requisito de formato)."

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Intenta parsear como JSON, senón gárdao como texto plano
                try:
                    json_data = json.loads(content)
                    document_text = json.dumps(json_data, indent=2, ensure_ascii=False)
                except json.JSONDecodeError:
                    document_text = content
                
                documents.append(document_text)
                metadatas.append({"filename": file_name, "source": "uploaded_file"})
                ids.append(str(uuid.uuid4()))
                success_count += 1

        except Exception as e:
            print(f"Erro ao procesar '{file_name}': {e}")
            return f"❌ Erro interno ao ler o ficheiro '{file_name}': {e}"
            
    if documents:
        try:
            collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            total_docs = collection.count()
            return f"✅ Subida completada: Engadíronse {success_count} documentos. Total na BD: {total_docs}."
        except Exception as e:
            return f"❌ Erro de ChromaDB ao engadir documentos: {e}"
    else:
        return "Non se puido procesar ningún ficheiro."


def semantic_query(query_text: str) -> Tuple[str, str]:
    """
    Realiza a busca semántica do documento máis relevante na colección.
    """
    if not collection:
        return "⚠️ Erro na Consulta", "A base de datos ChromaDB non está dispoñible."
    
    if not query_text:
        return "⚠️ Consulta baleira", "Por favor, introduce unha pregunta ou termo de busca."
        
    if collection.count() == 0:
        return "⚠️ Sen documentos", "A colección está baleira. Sube ficheiros na pestana 'Subida de Ficheiros'."

    try:
        # Consulta semántica (n_results=1 para obter o máis relevante)
        results = collection.query(
            query_texts=[query_text],
            n_results=1,
            include=['documents', 'metadatas', 'distances']
        )
        
        if not results['documents'] or not results['documents'][0]:
            return f"❓ Resultado non atopado: '{query_text}'", "Non se atopou ningún documento relevante."
        
        document_content = results['documents'][0][0]
        metadata = results['metadatas'][0][0]
        distance = results['distances'][0][0]
        filename = metadata.get('filename', 'Descoñecido')
        
        header = f"✅ Documento máis relevante: {filename} (Distancia: {distance:.4f})"
        return header, document_content
        
    except Exception as e:
        error_msg = f"❌ Erro de ChromaDB durante a consulta: {e}"
        return error_msg, "Erro interno. Verifique a consola para máis detalles."

# 🆕 NOVA FUNCIÓN PARA ELIMINAR DOCUMENTOS
def delete_all_documents() -> str:
    """
    Elimina todos os documentos da colección en memoria.
    """
    if not collection:
        return "⚠️ Erro: A base de datos ChromaDB non está dispoñible."
    
    # Chama ao método delete() sen argumentos para eliminar todo
    collection.delete(where={}) 
    
    # Confirma que a conta é 0
    count = collection.count()
    return f"🗑️ Eliminación completa. A colección '{COLLECTION_NAME}' contén agora {count} documentos."

# --- Interface Gradio (CORRIXIDA con gr.Blocks) ---

if __name__ == "__main__":
    if collection:
        # Usamos gr.Blocks como contexto principal para evitar o erro de Gradio
        with gr.Blocks(title="Buscador Semántico ChromaDB") as demo:
            gr.Markdown("# Ferramenta de Consulta Semántica (ChromaDB + Gradio)")
            
            # Pestana de Subida de Ficheiros
            with gr.Tab("⬆️ Subida de Ficheiros") as upload_tab:
                gr.Markdown("## Subir Documentos para Análise Semántica")
                gr.Markdown("Sube un ou varios ficheiros de texto (preferentemente JSON) á base de datos en memoria.")
                
                file_uploader = gr.File(
                    file_count="multiple", 
                    type="filepath", 
                    file_types=['.json', '.txt'],
                    label="Seleccionar ficheiros JSON/TXT"
                )
                upload_button = gr.Button("Engadir Documentos a ChromaDB", variant="primary")
                
                # Botón de borrado engadido
                delete_button = gr.Button("🗑️ Eliminar TODOS os Documentos da BD", variant="stop")
                
                upload_status = gr.Textbox(label="Estado da Operación / Borrado", lines=2)
                
                # Conexións da pestana de subida
                upload_button.click(
                    fn=process_and_add_files,
                    inputs=file_uploader,
                    outputs=upload_status
                )
                
                # Conexión do botón de borrado
                delete_button.click(
                    fn=delete_all_documents,
                    inputs=None,
                    outputs=upload_status
                )


            # Pestana de Consulta Semántica
            with gr.Tab("🔎 Consulta Semántica") as query_tab:
                gr.Markdown("## Consulta Semántica sobre Documentos Cargados")
                gr.Markdown("Introduce unha pregunta ou termo para atopar o documento máis *semánticamente* relevante.")
                
                query_input = gr.Textbox(label="A túa Pregunta", placeholder="Ex: Cales son os requisitos para traballar nunha empresa tecnolóxica?")
                query_button = gr.Button("Buscar Documento Máis Relevante", variant="primary")
                
                result_header = gr.Textbox(label="Resultado da Busca", lines=1)
                result_document = gr.Textbox(label="Contido do Documento", lines=15, interactive=False)
                
                # Conexión da acción
                query_button.click(
                    fn=semantic_query,
                    inputs=query_input,
                    outputs=[result_header, result_document]
                )
        
        # Lanzamento da aplicación
        demo.launch(share=False, inbrowser=True)
    else:
        print("\nO programa non pode lanzarse sen unha inicialización exitosa de ChromaDB.")