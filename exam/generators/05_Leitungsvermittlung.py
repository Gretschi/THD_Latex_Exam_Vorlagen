#!/usr/bin/env python

TEMPLATE_CMD = """
\\newcommand{{\\datarate}}{{{datarate}}}
\\newcommand{{\\channels}}{{{channels}}}
\\newcommand{{\\switchingdelay}}{{{switchingdelay}}}
\\newcommand{{\\data}}{{{data}}}
\\newcommand{{\\channelrate}}{{{channelrate}}}
\\newcommand{{\\transdelay}}{{{transdelay}}}
\\newcommand{{\\result}}{{{result}}}
"""

def get_ctx(rng):
    return {
        "datarate": rng.randint(10, 100),
        "channels": rng.randint(10, 30),
        "switchingdelay": rng.randint(50, 1000),
        "data": rng.randint(10, 900),
        }

def compute(ctx):
    channelrate = ctx["datarate"]/ctx["channels"]
    transdelay = ctx["data"]/channelrate
    result = ctx["switchingdelay"] + transdelay
    ctx["channelrate"] = round(channelrate, 2)
    ctx["transdelay"] = round(transdelay, 2)
    ctx["result"] = round(result, 2)
    return ctx

def get_cmdstr(ctx):
    return TEMPLATE_CMD.format(**ctx)

def print_tex(rng):
    ctx = get_ctx(rng)
    ctx = compute(ctx)
    print(get_cmdstr(ctx))

def write_tex(rng):
    ctx = get_ctx(rng)
    ctx = compute(ctx)
    with open("Leitungsvermittlung_commands.tex", "w") as commandfile:
        commandfile.write(get_cmdstr(ctx))

def generate(rng):
    write_tex(rng)
    files = ["Leitungsvermittlung_commands.tex"]
    return files

if __name__ == "__main__":
    import random
    print_tex(random)
