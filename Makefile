.PHONY: essay clean

essay:
	cd latex && latexmk -pdf -bibtex -interaction=nonstopmode -outdir=../build essay_template.tex

clean:
	cd latex && latexmk -C -outdir=../build essay_template.tex
	rmdir build 2>/dev/null || true
