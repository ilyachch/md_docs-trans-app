.PHONY: all


PROJECT_FOLDER = md_translate
WORKING_DIRECTORY = $(shell pwd)

go_to_project_folder:
	@cd $(WORKING_DIRECTORY)

# Tools section
black:
	@poetry run black -S $(PROJECT_FOLDER)

isort:
	@poetry run isort $(PROJECT_FOLDER)

# Linters section
check_black:
	@poetry run black -S --diff --check $(PROJECT_FOLDER)

check_mypy:
	@poetry run mypy $(PROJECT_FOLDER)

check_imports:
	@poetry run isort --check-only $(PROJECT_FOLDER)

# Coverage section
coverage:
	@poetry run coverage run -m unittest

coverage_html_report:
	@poetry run coverage html

coverage_xml_report:
	@poetry run coverage xml

coverage_cmd_report:
	@poetry run coverage report

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
	@rm -rf ./coverage.xml
	@rm -rf .mypy_cache
	@rm -rf .coverage
	@rm -rf .coverage_html
