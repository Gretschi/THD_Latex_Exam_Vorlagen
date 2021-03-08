#!/usr/bin/env python

import os
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
    loader = jinja2.FileSystemLoader(os.path.abspath('tex_templates')),
)

def get_basic_ctx(rng):
    return {
        "datarate": rng.randint(10, 100),
        "channels": rng.randint(10, 30),
        "switchingdelay": rng.randint(50, 1000),
        "data": rng.randint(10, 900),
        }

def compute_solution(ctx):
    channelrate = ctx["datarate"]/ctx["channels"]
    transdelay = ctx["data"]/channelrate
    result = ctx["switchingdelay"] + transdelay
    ctx["channelrate"] = round(channelrate, 2)
    ctx["transdelay"] = round(transdelay, 2)
    ctx["result"] = round(result, 2)
    return ctx

def get_rendered(rng):
    ctx = get_basic_ctx(rng)
    ctx = compute_solution(ctx)
    template = latex_jinja_env.get_template('05_Rechnung_Leitungsvermittlung.tex')
    return template.render(ctx)

def write_tex(rng):
    content = get_rendered(rng)
    with open("05_Rechnung_Leitungsvermittlung.tex", "w") as questionfile:
        questionfile.write(content)

def generate(rng):
    write_tex(rng)
    files = ["05_Rechnung_Leitungsvermittlung.tex"]
    return files

if __name__ == "__main__":
    import random
    print(get_rendered(random))
