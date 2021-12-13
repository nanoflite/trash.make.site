SERVER="johan@vandenbran.de"
GEMINI_SERVER="gemini@vandenbran.de"
REMOTE="johan@vandenbran.de:public"

.PHONY: all build deploy postdeploy serve

all: build deploy postdeploy build_gopher deploy_gopher build_gemini deploy_gemini

postdeploy:
	ssh ${SERVER} "find ./public -type d -exec chmod g+rx {} \;"
	ssh ${SERVER} "find ./public -type f -exec chmod g+r {} \;"

deploy:
	@echo "Copying site to server..."
	@rsync -avzhe ssh --progress ./build/ ${REMOTE} --delete

build:
	@echo "Building the html site..."
	@PYTHONUNBUFFERED=1 python -m TrashMakeSite html ./source ./build

serve:
	@echo "Starting local webserver"
	@python -m http.server --directory ./build

build_gopher:
	@echo "Building the gopher site..."
	@PYTHONUNBUFFERED=1 python -m TrashMakeSite gopher ./source ./build_gopher

deploy_gopher:
	@echo "Copying gopher site to server..."
	@rsync -avzhe ssh --progress ./build_gopher/ ${SERVER}:/var/gopher --delete

build_gemini:
	@echo "Building the gemini site..."
	@PYTHONUNBUFFERED=1 python -m TrashMakeSite gemini ./source ./build_gemini

deploy_gemini:
	@echo "Copying gemini site to server..."
	@rsync -avzhe ssh --progress ./build_gemini/ ${GEMINI_SERVER}:gemini/content --delete
