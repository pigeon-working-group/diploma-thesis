all: render

render: paper.tex
	tectonic paper.tex

quick: paper.tex
	python3 quick_paper.py
	# tectonic doesn't support piping
	tectonic quick_paper.tex 
	rm quick_paper.tex