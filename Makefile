.PHONY: all


PROJECT_FOLDER = md_translate
WORKING_DIRECTORY = $(shell pwd)
VENV_BIN = .venv/bin/

go_to_project_folder:
	@cd $(WORKING_DIRECTORY)

# Tools section
black:
	@$(VENV_BIN)/black $(PROJECT_FOLDER)

isort:
	@$(VENV_BIN)/isort $(PROJECT_FOLDER)

format: black isort

# Linters section
check_black:
	@$(VENV_BIN)/black --diff --check $(PROJECT_FOLDER)

check_mypy:
	@$(VENV_BIN)/mypy $(PROJECT_FOLDER) --config-file $(WORKING_DIRECTORY)/pyproject.toml

check_isort:
	@$(VENV_BIN)/isort --check-only $(PROJECT_FOLDER)

check_flake8:
	@$(VENV_BIN)/flake8 $(PROJECT_FOLDER)

check: check_black check_mypy check_isort, check_flake8

# Coverage section
tests:
	@$(VENV_BIN)/pytest tests

# Releasing
major_release: bump_major_release commit_version
minor_release: bump_minor_release commit_version
patch_release: bump_patch_release commit_version

commit_version:
	@git commit -a -m "`poetry version`"

bump_major_release:
	@poetry version major

bump_minor_release:
	@poetry version minor

bump_patch_release:
	@poetry version patch

release:
	@poetry build
	@poetry publish -u $(USERNAME) -p $(TOKEN)

# Other
clean:
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf ./coverage.xml htmlcov .coverage .coverage_html
	@rm -rf .mypy_cache .pytest_cache
