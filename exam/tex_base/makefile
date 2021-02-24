DIR=$(notdir ${PWD})

all: compile rename clean

compile:
	latexmk -pdf exam_answers.tex
	latexmk -pdf exam_noanswers.tex
clean:
	latexmk -C
rename:
	mv exam_answers.pdf ${DIR}_sol.pdf
	mv exam_noanswers.pdf ${DIR}.pdf
