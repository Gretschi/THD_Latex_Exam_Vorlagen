# exam-framework

A LaTeX/Python-based framework to create individualized Take-Home exams.

It is a significant extension of my LaTeX exam framework available in my
[LaTeX template repository](https://mygit.th-deg.de/afischer/thd-latex-vorlagen) and is based heavily on the [LaTeX exam class](https://www.ctan.org/pkg/exam).

## Requirements

The main requirements are a reasonable LaTeX setup and Python (3) for the
dynamic parts. [Latexmk](https://www.ctan.org/pkg/latexmk/) is used to streamline the LaTeX compilation process.
[Jinja2](https://palletsprojects.com/p/jinja/) is used as template engine.
The DNS example depends on the [`cairosvg`](https://cairosvg.org/) module
to convert the SVG input file to a PNG file usable by LaTeX.

## Usage

Generate an example by calling `python generate.py` in the `exam` folder.
Results will be put in the `out` folder.

To add your own questions, proceed with the following steps: First, create
or copy your own exam `.tex` files into the `tex_base` folder. You can
designate content to be randomized with the TeX expression
`\VAR{variablename}` anywhere in the file. Don't forget to include your
file and set exam metadata (time, duration, etc.) in the `exam.tex` file.

To randomize variables, create a corresponding Python script in the
`generators` directory. This script is expected to have two elements:
* a `FILES` list referencing the TeX files modified by this script 
  (e.g., `FILES = ["myquestion.tex"]`). Usually, you should keep one
  file per script, but sometimes a question may depend on more than one
  file (e.g., if the question itself includes further files).
* a `get_context(rng)` method, which gets a preseeded pseudorandom number
  generator as input. This method is supposed to return a dictionary which
  maps variable names to their contents. This dictionary is used to
  replace the names defined above with `\VAR{variablename}` with the
  respective content.

If your script fulfills these two requirements, it will be detected and used
by the `generate.py` script automatically.

Finally, fill the `seeds.txt` with as many integer seeds as you would like
to generate exams. The original intent of this framework was to fill it with matriculation
numbers, if you want to have one exam for each student. However, if you prefer having
groups of students with the same exam (e.g., groups 1-4, with one exam per group)
you can also use these group numbers as seeds.

See the provided examples for more information.

## Example

![Example of an exam with its solution side-by-side](Example.png "An exam and its solution")

## Customization

The overall layout is based on [THD](https://www.th-deg.de) requirements.
To modify the layout have a look in particular
at `thdstyle.tex` and `titlepage.tex` in the `tex_base` folder.

Suggestions, remarks and constructive criticism are very welcome. HTH

---
© 2021 [Andreas Fischer](mailto:andreas.fischer@th-deg.de)
