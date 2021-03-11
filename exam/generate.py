#!/usr/bin/env python3

import random
import sys, os, shutil, tempfile

import modloader

import jinja2
from cairosvg import svg2png

def read_seeds():
    with open("seeds.txt", 'r') as seedsfile:
        try:
            seeds = [int(line) for line in seedsfile]
        except ValueError:
            print("Seeds file malformed. Please use only one integer on each line!")
            sys.exit(1)
        return seeds

class Processor:
    def __init__(self, target_dir):
        self.target_dir = target_dir
        self.environment = self.get_environment()

    def get_environment(self):
        raise NotImplementedError

    def process(self, template_file, context):
        raise NotImplementedError


class SVGProcessor(Processor):
    def get_environment(self):
        return jinja2.Environment(
            autoescape=False,
            loader=jinja2.FileSystemLoader(os.path.abspath('tex_base')),
            )

    def process(self, template_file, context):
        template = self.environment.get_template(template_file)
        rendered = template.render(context)
        target_filename = os.path.join(self.target_dir, template_file[:-3] + "png")
        svg2png(bytestring=rendered.encode("utf-8"), write_to=target_filename, dpi=150)

class TEXProcessor(Processor):
    def get_environment(self):
        return jinja2.Environment(
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

    def process(self, template_file, context):
        template = self.environment.get_template(template_file)
        content = template.render(context)
        with open(os.path.join(self.target_dir, template_file), "w") as destination_file:
            destination_file.write(content)



class ExamCreator:
    def __init__(self, seed, generators, pdfdir="out"):
        try:
            os.mkdir(pdfdir)
        except FileExistsError:
            pass
        self.seed = seed
        self.targetdir_obj = tempfile.TemporaryDirectory()
        self.target_dir = self.targetdir_obj.name
        self.maindir = os.getcwd()
        self.rng = random.Random(seed)
        self.generators = generators
        self.pdfdir = os.path.join(os.getcwd(), pdfdir)
        self.processors = {
            "tex": TEXProcessor(self.target_dir),
            "svg": SVGProcessor(self.target_dir),
            }

    def prepare(self):
        shutil.copytree("tex_base", self.target_dir, dirs_exist_ok=True)

    def generate(self):
        for generator in self.generators:
            template_files = generator.FILES
            context = generator.get_context(self.rng)
            self.process_all_templates(template_files, context)

    def process_all_templates(self, template_files, context):
        for template_file in template_files:
            self.process_template(template_file, context)

    def process_template(self, template_file, context):
        extension = template_file[-3:]
        processor = self.processors[extension]
        processor.process(template_file, context)

    def make_exam(self):
        context = {"matrnr": self.seed, "printanswers": "\\noprintanswers"}
        target_file = os.path.join(self.pdfdir, "{}.pdf".format(self.seed))
        self.make(context, target_file)

    def make_solution(self):
        context = {"matrnr": self.seed, "printanswers": "\\printanswers"}
        target_file = os.path.join(self.pdfdir, "{}_sol.pdf".format(self.seed))
        self.make(context, target_file)

    def make(self, context, target_file):
        self.process_template("exam.tex", context)
        os.chdir(self.target_dir)
        os.system("latexmk -pdf exam.tex")
        shutil.copy("exam.pdf", target_file)
        os.chdir(self.maindir)

    def clean(self):
        self.targetdir_obj.cleanup()


if __name__ == "__main__":
    cleanup = True
    seeds = read_seeds()
    generators = sorted(modloader.get_modules('generators', 'get_context'), key=lambda g: g.__name__)
    if len(sys.argv) > 1:
        if sys.argv[1] == "s":
            seeds = seeds[0:1]
        elif sys.argv[1].isnumeric():
            seeds = [int(sys.argv[1])]
    creators = [ExamCreator(seed, generators) for seed in seeds]
    for creator in creators:
        try:
            creator.prepare()
            creator.generate()
            creator.make_exam()
            creator.make_solution()
        finally:
            if cleanup:
                creator.clean()
