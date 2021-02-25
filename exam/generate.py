#!/usr/bin/env python3

import random
import sys, os, shutil

import modloader

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
        with open(os.path.join(self.targetdir, "matrnr.tex"), "w") as matrnrfile:
            matrnrfile.write("\\newcommand{{\\matrnr}}{{{matrnr}}}".format(matrnr=self.seed))

    def generate(self):
        for generator in self.generators:
            files = generator.generate(self.rng)
            for filename in files:
                shutil.move(filename, self.targetdir)

    def make(self):
        os.chdir(self.targetdir)
        os.system("make")
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
    generators = sorted(modloader.get_modules('generators', 'generate'), key=lambda g: g.__name__)
    if len(sys.argv) > 1:
        if sys.argv[1] == "s":
            seeds = seeds[0:1]
        elif sys.argv[1].isnumeric():
            seeds = [int(sys.argv[1])]
    creators = [ExamCreator(seed, generators) for seed in seeds]
    for creator in creators:
        creator.prepare()
        creator.generate()
        creator.make()
        creator.move_to_pdfdir()
        creator.clean()
