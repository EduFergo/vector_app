# 🚀 Buscador Semántico con ChromaDB e Gradio

## 💡 Descrición do Proxecto

Este proxecto consiste no desenvolvemento dunha aplicación web interactiva para realizar buscas semánticas sobre documentos de texto. Utiliza **ChromaDB** como base de datos vectorial en memoria para xerar e almacenar os *embeddings* dos documentos, e **Gradio** para proporcionar unha interface de usuario amigable.

A aplicación permite:
1.  Subir ficheiros de texto (JSON) á base de datos.
2.  Realizar consultas ou preguntas.
3.  Recuperar o documento máis relevante en función do **significado** (semántica) da consulta.

### Tecnoloxías Principais

* **Python:** Linguaxe de programación principal.
* **ChromaDB:** Base de datos vectorial en modo **en memoria** (non persistente).
* **Gradio:** Framework para crear a interface web interactiva.

## 🛠️ Requisitos e Instalación

### 1. Requisitos Previos

Necesitas ter instalado **Conda** ou **Miniconda** para xestionar o ambiente virtual e **Docker** (opcional) para a execución dockerizada.

### 2. Configuración do Ambiente (Recomendado)

Debido a problemas de compatibilidade coa libraría `pydantic` en Python máis recentes, a aplicación require Python 3.11.

1.  **Crear e Activar o Entorno:**
    ```bash
    conda create --name chroma python=3.11
    conda activate chroma
    ```

2.  **Instalar Dependencias:**
    O ficheiro `requirements.txt` contén as dependencias necesarias:
    ```bash
    pip install -r requirements.txt
    ```

### 3. Ficheiros de Proba

O proxecto inclúe un cartafol `test_files/` con tres documentos JSON de exemplo para demostrar a busca semántica:
* `receita.json`
* `analitica.json`
* `grupo_musical.json`

---

## ⚙️ Instrucións de Execución

Podes executar a aplicación de dúas maneiras: localmente (con Python/Conda) ou usando Docker.

### Opción A: Execución Local (Python/Conda)

1.  **Activar o Entorno:**
    ```bash
    conda activate chroma
    ```
2.  **Lanzar a Aplicación:**
    ```bash
    python app.py
    ```
3.  A aplicación iniciarase e mostrará unha URL na consola (normalmente `http://127.0.0.1:7860`).

### Opción B: Execución con Docker (Opcional)

A execución con Docker garante un ambiente illado e consistente.

1.  **Construír a Imaxe de Docker:**
    Executa este comando no directorio raíz (`vector_app/`) onde se atopa o `Dockerfile`:
    ```bash
    docker build -t buscador-semantico-app .
    ```

2.  **Lanzar o Contedor:**
    Executa a imaxe, mapeando o porto 7860:
    ```bash
    docker run -d -p 7860:7860 --name semantico-container buscador-semantico-app
    ```
3.  Accede á aplicación en `http://localhost:7860`.

---

## 🌐 Uso da Aplicación

Unha vez que a aplicación estea aberta no navegador, segue estes pasos:

### 1. ⬆️ Subida de Ficheiros

1.  Vai á pestana **"⬆️ Subida de Ficheiros"**.
2.  Fai clic en **"Seleccionar ficheiros JSON/TXT"** e selecciona os 3 ficheiros do cartafol `test_files/`.
3.  Fai clic en **"Engadir Documentos a ChromaDB"**.
4.  O estado debe confirmar a adición de **3 documentos**. Os *embeddings* son xerados neste paso.

**Para eliminar todos os documentos (xa que a BD é en memoria), preme o botón:**
* `🗑️ Eliminar TODOS os Documentos da BD`.

### 2. 🔎 Consulta Semántica

1.  Vai á pestana **"🔎 Consulta Semántica"**.
2.  Introduce unha pregunta que se relacione co **significado** dos documentos cargados.
    * Exemplo de consulta: `Que información teño sobre a situación sanitaria dunha persoa?`
3.  Fai clic en **"Buscar Documento Máis Relevante"**.
4.  A aplicación devolverá o contido completo do ficheiro `analitica.json`, xa que é semanticamente o máis próximo á pregunta.

Isto demostra que o motor de ChromaDB está a utilizar a proximidade vectorial para a recuperación de información.