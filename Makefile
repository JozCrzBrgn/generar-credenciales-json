# Verificar si el archivo .env existe
ifeq (,$(wildcard .env))
$(error El archivo .env NO existe.)
endif

# Carga variables desde .env
include .env
export

# Usa las vars de .env
ENV_FILE ?= .env
IMAGE ?= $(DOCKER_IMAGE)
CONTAINER ?= $(DOCKER_CONTAINER)
PORT ?= $(DOCKER_PORT)

# === Docker === #
docker-create:
	@echo "Construyendo y ejecutando la imagen Docker..."
	docker build -t $(IMAGE) .
	docker run -d --env-file $(ENV_FILE) -p $(PORT):$(PORT) --name $(CONTAINER) $(IMAGE)

docker-del:
	@echo "Deteniendo y eliminando el contenedor..."
	docker stop $(CONTAINER)
	docker rm $(CONTAINER)
	docker rmi $(IMAGE)