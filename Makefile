.PHONY: init clean update lint test format package package-upload


init:
	python3.11 -m venv venv
	(source venv/bin/activate; pip install -e .[dev])

clean:
	rm -rf venv/

update: clean init

lint:
	ruff src/cover_image/ tests/

test: lint
	pytest -vv tests/cover_image

format:
	black src/cover_image/ tests/
	isort src/cover_image/ tests/

package:
	(source venv/bin/activate; python3 -m build)

package-upload:
	(source venv/bin/activate; python3 -m twine upload dist/*)