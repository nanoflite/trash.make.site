SERVER="johan@smoll.home"
DATA_PATH="/mnt/data"

.PHONY: all build deploy serve build_www build_gopher build_gemini deploy_www deploy_gopher deploy_gemini

all: build deploy

build: build_www build_gopher build_gemini

deploy: deploy_www deploy_gopher deploy_gemini

build_www:
	@echo "Building the www site..."
	@PYTHONUNBUFFERED=1 python -m TrashMakeSite html ./source ./build

build_gopher:
	@echo "Building the gopher site..."
	@PYTHONUNBUFFERED=1 python -m TrashMakeSite gopher ./source ./build_gopher

build_gemini:
	@echo "Building the gemini site..."
	@PYTHONUNBUFFERED=1 python -m TrashMakeSite gemini ./source ./build_gemini

serve:
	@echo "Starting local webserver"
	@python -m http.server --directory ./build

deploy_www:
	@echo "Copying www site to server..."
	@rsync -avzhe ssh --progress ./build/ ${SERVER}:${DATA_PATH}/www --delete

deploy_gopher:
	@echo "Copying gopher site to server..."
	@rsync -avzhe ssh --progress ./build_gopher/ ${SERVER}:${DATA_PATH}/gopher --delete


deploy_gemini:
	@echo "Copying gemini site to server..."
	@rsync -avzhe ssh --progress ./build_gemini/ ${SERVER}:${DATA_PATH}/gemini --delete
