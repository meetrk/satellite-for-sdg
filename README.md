# satellite-for-sdg

## Essay template

Repository layout:

- `latex/essay_template.tex` - editable essay source
- `latex/references.bib` - BibLaTeX reference data
- `latex/figures/` - essay images and diagrams
- `reference/` - original sample essay and supporting reference documents
- `build/` - generated PDF and intermediate LaTeX files

Place figures in `latex/figures/` and replace the placeholder content in
`latex/essay_template.tex`.

Compile the essay:

```bash
make essay
```

The resulting PDF is written to `build/essay_template.pdf`.

Remove generated files:

```bash
make clean
```
