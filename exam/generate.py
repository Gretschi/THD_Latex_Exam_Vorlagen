#!/usr/bin/env python3

import random
import sys, os, shutil

import modloader

import jinja2
latex_jinja_env = jinja2.Environment(
    block_start_string = '\BLOCK{',
    block_end_string = '}',
    variable_start_string = '\VAR{',
    variable_end_string = '}',
    comment_start_string = '\#{',
    comment_end_string = '}',
    line_statement_prefix = '%-',
    line_comment_prefix = '%#',
    trim_blocks = True,
    autoescape = False,
    loader = jinja2.FileSystemLoader(os.path.abspath('tex_base')),
)

def read_seeds():
    with open("seeds.txt", 'r') as seedsfile:
        try:
            seeds = [int(line) for line in seedsfile]
        except ValueError:
            print("Seeds file malformed. Please use only one integer on each line!")
            sys.exit(1)
        return seeds

class ExamCreator:
    def __init__(self, seed, generators, pdfdir="out"):
        try:
            os.mkdir(pdfdir)
        except FileExistsError:
            pass
        self.seed = seed
        self.targetdir = str(seed)
        self.maindir = os.getcwd()
        self.rng = random.Random(seed)
        self.generators = generators
        self.pdfdir = os.path.join(os.getcwd(), pdfdir)

    def prepare(self):
        shutil.copytree("tex_base", self.targetdir)

    def generate(self):
        for generator in self.generators:
            template_files = generator.FILES
            context = generator.get_context(self.rng)
            self.process_all_templates(template_files, context)

    def process_all_templates(self, template_files, context):
        for template_file in template_files:
            self.process_template(template_file, context)

    def process_template(self, template_file, context):
        template = latex_jinja_env.get_template(template_file)
        rendered_template = template.render(context)
        with open(os.path.join(self.targetdir, template_file), "w") as destination_file:
            destination_file.write(rendered_template)

    def make_exam(self):
        context = {"matrnr": self.seed, "printanswers": "\\noprintanswers"}
        target_file = "{}.pdf".format(self.seed)
        self.make(context, target_file)

    def make_solution(self):
        context = {"matrnr": self.seed, "printanswers": "\\printanswers"}
        target_file = "{}_sol.pdf".format(self.seed)
        self.make(context, target_file)

    def make(self, context, target_file):
        self.process_template("exam.tex", context)
        os.chdir(self.targetdir)
        os.system("latexmk -pdf exam.tex")
        shutil.copy("exam.pdf", target_file)
        os.chdir(self.maindir)

    def move_to_pdfdir(self):
        pdfexam = os.path.join(self.targetdir, "{}.pdf".format(self.seed))
        pdfsol = os.path.join(self.targetdir, "{}_sol.pdf".format(self.seed))
        shutil.copy(pdfexam, self.pdfdir)
        shutil.copy(pdfsol, self.pdfdir)

    def clean(self):
        shutil.rmtree(self.targetdir)


if __name__ == "__main__":
    seeds = read_seeds()
    generators = sorted(modloader.get_modules('generators', 'get_context'), key=lambda g: g.__name__)
    if len(sys.argv) > 1:
        if sys.argv[1] == "s":
            seeds = seeds[0:1]
        elif sys.argv[1].isnumeric():
            seeds = [int(sys.argv[1])]
    creators = [ExamCreator(seed, generators) for seed in seeds]
    for creator in creators:
        creator.prepare()
        creator.generate()
        creator.make_exam()
        creator.make_solution()
        creator.move_to_pdfdir()
        creator.clean()
