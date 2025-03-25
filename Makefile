all: mug.svg logo.png
	python3 generate_mugs.py

clean:
	rm -rf out