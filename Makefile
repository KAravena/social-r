.PHONY: generate build test preview render clean

generate:
	python engine/generator/generate_all_modules.py

build: generate
	python engine/generator/build.py

test: build
	python -m unittest discover -s tests -v

preview: build
	quarto preview

render: build
	quarto render

clean:
	python -c "import shutil, os; [shutil.rmtree(d, ignore_errors=True) for d in ['.quarto', '_site', '_freeze', 'tests/screenshots']]"
