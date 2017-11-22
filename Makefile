all: render

render: paper.tex
	pdflatex -shell-escape paper.tex 
	bibtex paper
	pdflatex -shell-escape paper.tex 

quick: paper.tex
	python3 quick_paper.py
	# pdflatex doesn't support piping
	pdflatex -shell-escape quick_paper.tex 
	bibtex quick_paper
	pdflatex -shell-escape quick_paper.tex 
	rm quick_paper.tex