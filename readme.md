<<<<<<< HEAD
# Instrucciones para Ejecutar el Script y Desplegarlo en Cloud Run

Este README proporciona instrucciones detalladas para construir, subir y desplegar el script de web scraping en Cloud Run utilizando Cloud Build y un archivo `cloudbuild.yaml`.

---

## Descripción del Proyecto

El script realiza las siguientes tareas:
1. **Scraping de Noticias:** Extrae las noticias más recientes de Yogonet.
2. **Procesamiento de Datos:** Limpia y estructura los datos obtenidos.
3. **Carga a BigQuery:** Sube los datos procesados a una tabla en BigQuery.

---

## Requisitos Previos

Antes de continuar, asegúrate de tener lo siguiente configurado:
- **Google Cloud SDK instalado.**
- **Cuenta de servicio con permisos de acceso a BigQuery y Cloud Run.**
- **Proyecto en Google Cloud configurado.**
- **BigQuery Dataset y Tabla disponibles.**

---

## Estructura del Proyecto

El proyecto contiene los siguientes archivos:
- `main.py`: Código principal del script.
- `requirements.txt`: Librerías necesarias para ejecutar el script.
- `Dockerfile`: Configuración para crear una imagen Docker del proyecto.
- `cloudbuild.yaml`: Configuración para la ejecución automatizada de Cloud Build.

---

## Configuración de los Archivos

### 1. **`requirements.txt`**
Lista las dependencias necesarias:
```plaintext
selenium
google-cloud-bigquery
pandas
datetime
pytz
```


### Configura el entorno Docker:

``` Dockerfile
# Imagen base
FROM python:3.9-slim

# Configuración del entorno
WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY main.py .

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]

```


### Configura Cloud Build para construir y desplegar el servicio:

```yaml
steps:
  # Construir la imagen Docker
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/yogonet-scraper', '.']

  # Subir la imagen a Container Registry
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/yogonet-scraper']

  # Desplegar en Cloud Run
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: 'gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'yogonet-scraper'
      - '--image'
      - 'gcr.io/$PROJECT_ID/yogonet-scraper'
      - '--platform'
      - 'managed'
      - '--region'
      - 'us-central1'
      - '--allow-unauthenticated'

images:
  - 'gcr.io/$PROJECT_ID/yogonet-scraper'

```

Asegura estar logueado en gcloud correctamente para usarlo.


---
=======
# Instrucciones para Ejecutar el Script y Desplegarlo en Cloud Run

Este README proporciona instrucciones detalladas para construir, subir y desplegar el script de web scraping en Cloud Run utilizando Cloud Build y un archivo `cloudbuild.yaml`.

---

## Descripción del Proyecto

El script realiza las siguientes tareas:
1. **Scraping de Noticias:** Extrae las noticias más recientes de Yogonet.
2. **Procesamiento de Datos:** Limpia y estructura los datos obtenidos.
3. **Carga a BigQuery:** Sube los datos procesados a una tabla en BigQuery.

---

## Requisitos Previos

Antes de continuar, asegúrate de tener lo siguiente configurado:
- **Google Cloud SDK instalado.**
- **Cuenta de servicio con permisos de acceso a BigQuery y Cloud Run.**
- **Proyecto en Google Cloud configurado.**
- **BigQuery Dataset y Tabla disponibles.**

---

## Estructura del Proyecto

El proyecto contiene los siguientes archivos:
- `main.py`: Código principal del script.
- `requirements.txt`: Librerías necesarias para ejecutar el script.
- `Dockerfile`: Configuración para crear una imagen Docker del proyecto.
- `cloudbuild.yaml`: Configuración para la ejecución automatizada de Cloud Build.

---

## Configuración de los Archivos

### 1. **`requirements.txt`**
Lista las dependencias necesarias:
```plaintext
selenium
google-cloud-bigquery
pandas
datetime
pytz
```


### Configura el entorno Docker:

``` Dockerfile
# Imagen base
FROM python:3.9-slim

# Configuración del entorno
WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY main.py .

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]

```


### Configura Cloud Build para construir y desplegar el servicio:

```yaml
steps:
  # Construir la imagen Docker
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/yogonet-scraper', '.']

  # Subir la imagen a Container Registry
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/yogonet-scraper']

  # Desplegar en Cloud Run
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: 'gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'yogonet-scraper'
      - '--image'
      - 'gcr.io/$PROJECT_ID/yogonet-scraper'
      - '--platform'
      - 'managed'
      - '--region'
      - 'us-central1'
      - '--allow-unauthenticated'

images:
  - 'gcr.io/$PROJECT_ID/yogonet-scraper'

```

Asegura estar logueado en gcloud correctamente para usarlo.


---
>>>>>>> 23d6e1571aa5e29d8ad79a997f1257680be32ac7
Autor: Claudio Carballo