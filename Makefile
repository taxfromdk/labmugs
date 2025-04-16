all: 
	python3 render_mugs.py

generate:
	python3 generate_mugs.py
	

clean:
	rm -rf out/*.png out/*.pdf