SERVER="johan@vandenbran.de"
REMOTE="johan@vandenbran.de:public"

.PHONY: all build deploy postdeploy serve

all: build deploy postdeploy

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
