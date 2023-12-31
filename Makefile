# Makefile

.PHONY: validate fix test clean dist

REPO_NAME := context-aware-word-vectors
PACKAGE_NAME := context_aware_word_vectors

validate:
	venv/dev_${REPO_NAME}/bin/pylint src/${PACKAGE_NAME} -r n --output-format=parseable --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" --exit-zero --ignore-paths="src/${PACKAGE_NAME}/bak" src/${PACKAGE_NAME} tests | tee validation/pylint-report.txt
	venv/dev_${REPO_NAME}/bin/flake8 --format=pylint --exit-zero --ignore=E501,E800,W503,G001,E305,G004 --max-line-length=89 --extend-exclude="src/${PACKAGE_NAME}/bak" src/${PACKAGE_NAME} tests | tee validation/flake8-report.txt
	venv/dev_${REPO_NAME}/bin/mypy --exclude src/${PACKAGE_NAME}/bak src > validation/mypy.log || (exit 0)
	venv/dev_${REPO_NAME}/bin/python validation/score-with-pylint.py -p src/${PACKAGE_NAME} | grep 'Your\|Threshold'

fix:
	venv/dev_${REPO_NAME}/bin/pre-commit run --all-files

# Generates coverage-reports/coverage.xml, cov-html/
test:
	venv/test_${REPO_NAME}/bin/pytest -m all --capture=tee-sys

dist:
	venv/${REPO_NAME}/bin/python -m build

clean: ## Remove general artifact files
	find . -name '.coverage' -delete
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '.pytest_cache' -type d | xargs rm -rf
	find . -name '__pycache__' -type d | xargs rm -rf
	find . -name '.ipynb_checkpoints' -type d | xargs rm -rf

venv/dev_${REPO_NAME}: ## create virtual environment if venv is not present
	python3 -m venv venv/dev_${REPO_NAME}
	venv/dev_${REPO_NAME}/bin/python -m pip install --upgrade pip
	venv/dev_${REPO_NAME}/bin/python -m pip install pip-tools

venv/test_${REPO_NAME}: ## create virtual environment if venv is not present
	python3 -m venv venv/test_${REPO_NAME}
	venv/test_${REPO_NAME}/bin/python -m pip install --upgrade pip
	venv/test_${REPO_NAME}/bin/python -m pip install pip-tools

venv/${REPO_NAME}: ## create virtual environment if venv is not present
	python3 -m venv venv/${REPO_NAME}
	venv/${REPO_NAME}/bin/python -m pip install --upgrade pip
	venv/${REPO_NAME}/bin/python -m pip install pip-tools

requirements/requirements.txt: venv/${REPO_NAME} pyproject.toml  # generate requirements for release
	venv/${REPO_NAME}/bin/pip-compile -v --resolver=backtracking -o requirements/requirements-pip-compile.txt pyproject.toml
	venv/${REPO_NAME}/bin/pip-sync -v requirements/requirements-pip-compile.txt
	venv/${REPO_NAME}/bin/pip freeze > requirements/requirements.txt

requirements/test-requirements.txt: venv/test_${REPO_NAME} pyproject.toml requirements/requirements.txt ## generate requirements for test
	venv/test_${REPO_NAME}/bin/pip-compile -v --resolver=backtracking --extra test -o requirements/test-requirements-pip-compile.txt pyproject.toml
	venv/test_${REPO_NAME}/bin/pip-sync --force requirements/test-requirements-pip-compile.txt requirements/requirements.txt
	venv/test_${REPO_NAME}/bin/pip freeze > requirements/test-requirements.txt

requirements/dev-requirements.txt: venv/dev_${REPO_NAME} pyproject.toml requirements/test-requirements.txt requirements/requirements.txt ## generate requirements for dev
	venv/dev_${REPO_NAME}/bin/pip-compile -v --resolver=backtracking --extra dev -o requirements/dev-requirements-pip-compile.txt pyproject.toml
	venv/dev_${REPO_NAME}/bin/pip-sync --force requirements/dev-requirements-pip-compile.txt requirements/test-requirements.txt requirements/requirements.txt
	venv/dev_${REPO_NAME}/bin/pre-commit install  # Installs the git-hooks
	venv/dev_${REPO_NAME}/bin/pip freeze > requirements/dev-requirements.txt
