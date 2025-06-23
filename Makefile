all: setup-git-hooks
	$(MAKE) -C backend
	$(MAKE) -C frontend
	$(MAKE) build-and-run
	$(MAKE) -C backend migrate-up

.PHONY: build-and-run
build-and-run:
	docker compose build --no-cache
	docker compose up --watch

check:
	$(MAKE) -C backend check

check-types:
	$(MAKE) -C backend check-types

lint: 
	$(MAKE) -C backend lint
	$(MAKE) -C frontend lint

.PHONY: run
run:
	docker compose up --watch

.PHONY: semantic-release
semantic-release:
	uv run semantic-release version --no-changelog --no-push --no-vcs-release --skip-build --no-commit --no-tag
	uv lock
	git add pyproject.toml uv.lock
	git commit --allow-empty --amend --no-edit 

.PHONY: setup-git-hooks
setup-git-hooks:
	chmod +x hooks/pre-commit
	chmod +x hooks/pre-push
	chmod +x hooks/post-commit
	git config core.hooksPath hooks

test:
	$(MAKE) -C backend test
	$(MAKE) -C frontend test
