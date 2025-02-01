# Usa una imagen base para Python
FROM python:3.12.8-slim


RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    pkg-config \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copia los archivos necesarios
COPY requirements.txt ./

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

ENV DJANGO_KEY="django-insecure-o8znq@&$^!05#bx@))jlscgr$bi&9yb(1rw8z=k+jb8i=a#*0%"

# Copia el resto del código
COPY . .

RUN python manage.py migrate

# Expone el puerto
EXPOSE 8000


# Comando para ejecutar el servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
