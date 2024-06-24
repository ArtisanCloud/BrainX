include .env

# $(eval export $(shell sed -ne 's/ *#.*$$//; /./ s/=.*$$// p' .env))


ifdef DOCKER_IMAGE_PLATFORM
	DOCKER_PLATFORM_FLAG = --platform $(DOCKER_IMAGE_PLATFORM)
else
	DOCKER_PLATFORM_FLAG =
endif

echo-variables:
	echo DOCKER_IMAGE_VERSION=${DOCKER_IMAGE_VERSION}
	echo DOCKER_IMAGE_PLATFORM=${DOCKER_IMAGE_PLATFORM}
	
	
	echo DOCKER_BACKEND_IMAGE_NAME=${DOCKER_BACKEND_IMAGE_NAME}
	echo DOCKER_FRONTEND_IMAGE_NAME=${DOCKER_FRONTEND_IMAGE_NAME}
	echo DOCKER_GATEWAY_IMAGE_NAME=${DOCKER_GATEWAY_IMAGE_NAME}
	
	echo PYTHON_IMAGE=${PYTHON_IMAGE}
	echo PYTHON_VERSION=${PYTHON_VERSION}
	echo DOCKER_PLATFORM_FLAG=${DOCKER_PLATFORM_FLAG}
	echo HOST_PROXY_PORT=${HOST_PROXY_PORT}

	echo POETRY_VERSION=${POETRY_VERSION}
	echo BACKEND_PORT=${BACKEND_PORT}
	echo FRONTEND_PORT=${FRONTEND_PORT}
	echo GATEWAY_PORT=${GATEWAY_PORT}



docker-buildx:docker-buildx-backend docker-buildx-frontend docker-buildx-gateway

# build backend
docker-buildx-backend:

	docker buildx build \
		--build-arg PYTHON_IMAGE=${PYTHON_IMAGE} \
		--build-arg PYTHON_VERSION=${PYTHON_VERSION} \
		--build-arg HOST_PROXY=${HOST_PROXY} \
		${DOCKER_PLATFORM_FLAG} \
		--tag ${DOCKER_BACKEND_IMAGE_NAME}:$(DOCKER_IMAGE_VERSION) \
		--file backend/Dockerfile \
		$(DOCKER_BUILD_OPTS) \
		backend

# build frontend
docker-buildx-frontend:
	docker buildx build \
		--build-arg DOCKER_IMAGE_PLATFORM=${DOCKER_IMAGE_PLATFORM} \
		${DOCKER_PLATFORM_FLAG} \
		--tag ${DOCKER_FRONTEND_IMAGE_NAME}:$(DOCKER_IMAGE_VERSION) \
		--file frontend/Dockerfile \
		$(DOCKER_BUILD_OPTS) \
		frontend

# build gateway
docker-buildx-gateway:
	docker buildx build \
		--build-arg DOCKER_IMAGE_PLATFORM=${DOCKER_IMAGE_PLATFORM} \
		--platform ${DOCKER_IMAGE_PLATFORM} \
		--tag ${DOCKER_GATEWAY_IMAGE_NAME}:$(DOCKER_IMAGE_VERSION) \
		--file gateway/Dockerfile \
		$(DOCKER_BUILD_OPTS) \
		gateway



tag-image-version:
	docker tag artisan-cloud/brainx-backend-app :$(DOCKER_IMAGE_VERSION)
	docker tag artisan-cloud/brainx-frontend-app artisan-cloud/brainx-frontend-app:$(DOCKER_IMAGE_VERSION)
	docker tag artisan-cloud/brainx-gateway-app artisan-cloud/brainx-gateway-app:$(DOCKER_IMAGE_VERSION)