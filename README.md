# exam-framework

A LaTeX/Python-based framework to create individualized Take-Home exams.

It is a significant extension of my LaTeX exam framework available in my
[LaTeX template repository](https://mygit.th-deg.de/afischer/thd-latex-vorlagen) and is based heavily on the [LaTeX exam class](https://www.ctan.org/pkg/exam).

Requirements are a reasonable LaTeX setup and Python for the dynamic parts.
Generate an example by calling `python generate.py` in the exam folder.
Create new dynamic questions by creating a new LaTeX file in `tex_base`,
including it in `exam.tex` and creating an accompanying Python script in
the `generators` directory. See the provided examples for more information.

Suggestions, remarks and constructive criticism are very welcome. HTH

---
© 2021 [Andreas Fischer](mailto:andreas.fischer@th-deg.de)
