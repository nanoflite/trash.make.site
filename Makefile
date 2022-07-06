SERVER="johan@smoll.home"
DATA_PATH="/mnt/data"

.PHONY: all build deploy serve build_www build_gopher build_gemini build_finger deploy_www deploy_gopher deploy_gemini deploy_finger clean

all: clean build deploy

build: build_www build_gopher build_gemini build_finger

deploy: deploy_www deploy_gopher deploy_gemini deploy_finger

build_www:
	@echo "Building the www site..."
	@PYTHONUNBUFFERED=1 python -m TrashMakeSite html ./source ./build

build_gopher:
	@echo "Building the gopher site..."
	@PYTHONUNBUFFERED=1 python -m TrashMakeSite gopher ./source ./build_gopher

build_gemini:
	@echo "Building the gemini site..."
	@PYTHONUNBUFFERED=1 python -m TrashMakeSite gemini ./source ./build_gemini

build_finger:
	@echo "Building the finger info..."
	@PYTHONUNBUFFERED=1 python -m TrashMakeSite finger ./source ./build_finger

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

deploy_finger:
	@echo "Copying finger data to server..."
	@rsync -avzhe ssh --progress ./build_finger/ ${SERVER}:${DATA_PATH}/finger --delete

clean:
	@echo "Clean..."
	@rm -rf ./build
	@rm -rf ./build_gopher
	@rm -rf ./build_gemini
	@rm -rf ./build_finger

