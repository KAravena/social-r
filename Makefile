.PHONY: generate test verify preview render

generate:
	python engine/generate.py

test: generate
	python -m unittest discover -s tests -v

verify:
	python engine/verify.py

preview: generate
	cd prototype && quarto preview

render: generate
	cd prototype && quarto render
