all: mug.svg logo.png
	#python3 generate_mugs.py
	python3 render_mugs.py

clean:
	rm -rf out