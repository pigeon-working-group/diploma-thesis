all: render

render: paper.tex
	pdflatex -shell-escape paper.tex 
	bibtex paper
	pdflatex -shell-escape paper.tex 

quick: paper.tex
	python3 quick_paper.py 20 30 quick
	# pdflatex doesn't support piping
	pdflatex -shell-escape quick_paper.tex 
	bibtex quick_paper
	pdflatex -shell-escape quick_paper.tex 
	rm quick_paper.tex

final: paper.tex
	python3 quick_paper.py 80 70 final
	# pdflatex doesn't support piping
	pdflatex -shell-escape final_paper.tex 
	bibtex final_paper
	pdflatex -shell-escape final_paper.tex 
	rm final_paper.tex	
