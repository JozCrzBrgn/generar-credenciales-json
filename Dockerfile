# ------------------------------ Builder Stage ------------------------------ #
FROM python:3.13-slim-bookworm AS builder

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

# Instalar herramientas necesarias para compilar paquetes
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential gcc libffi-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copiar solo el archivo de dependencias
COPY requirements.txt .

# Crear entorno virtual e instalar dependencias
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# ---------------------------- Production Stage ---------------------------- #
FROM python:3.13-slim-bookworm AS final

ENV PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Copiar entorno virtual y dependencias desde el builder
COPY --from=builder /opt/venv /opt/venv

# Copiar solo el código de aplicación (no requirements.txt)
COPY . .

EXPOSE 8000

# Ejecutar sin --reload (modo producción)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
