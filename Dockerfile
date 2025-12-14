# Usa unha imaxe base de Python
FROM python:3.11-slim

# Establece o directorio de traballo
WORKDIR /app

# Copia os ficheiros de dependencias e instalaas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto da aplicación
COPY app.py .
COPY test_files/ test_files/

# O porto por defecto de Gradio
EXPOSE 7860

# Comando para executar a aplicación
CMD ["python", "app.py"]