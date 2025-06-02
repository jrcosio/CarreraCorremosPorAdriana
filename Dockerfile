FROM python:3.10-slim

WORKDIR /app

# Copiar los archivos de requisitos e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Copiar la carpeta de assets
COPY assets/ ./assets/

# Puerto en el que se ejecutará la aplicación
EXPOSE 80

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]