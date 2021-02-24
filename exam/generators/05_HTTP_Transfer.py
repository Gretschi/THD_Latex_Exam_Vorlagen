#!/usr/bin/env python

TEMPLATE_CMD = """
\\newcommand{{\\sizeweb}}{{{sizeweb}kByte}}
\\newcommand{{\\sizepa}}{{{sizepa}kByte}}
\\newcommand{{\\sizepb}}{{{sizepb}kByte}}
\\newcommand{{\\rate}}{{{rate}MByte/s}}
\\newcommand{{\\rtt}}{{{rtt}ms}}
\\newcommand{{\\sola}}{{{sola:.2f}ms}}
\\newcommand{{\\solb}}{{{solb:.2f}ms}}
\\newcommand{{\\solc}}{{{solc:.2f}ms}}
\\newcommand{{\\sold}}{{{sold:.2f}ms}}
\\newcommand{{\\sole}}{{{sole:.2f}ms}}
"""

def get_ctx(rng):
    return {
        "sizeweb": rng.randint(2, 20),
        "sizepa": rng.randint(110, 490),
        "sizepb": rng.randint(110, 490),
        "rate": rng.randint(2, 9),
        "rtt": rng.randint(5, 25),
        }

def compute(ctx):
    trans_d_web = round(ctx["sizeweb"] / ctx["rate"], 2)
    trans_d_pa = round(ctx["sizepa"] / ctx["rate"], 2)
    trans_d_pb = round(ctx["sizepb"] / ctx["rate"], 2)
    ctx['sola'] = ctx["rtt"]
    ctx['solb'] = ctx['sola'] + ctx["rtt"] + trans_d_web
    ctx['solc'] = ctx['solb'] + ctx["rtt"] + trans_d_pa
    ctx['sold'] = ctx['solc'] + ctx["rtt"] + trans_d_pb
    ctx['sole'] = ctx['sold'] + ctx["rtt"]
    return ctx
    

def get_cmdstr(ctx):
    return TEMPLATE_CMD.format(
        sizeweb=ctx["sizeweb"],
        sizepa=ctx["sizepa"],
        sizepb=ctx["sizepb"],
        rate=ctx["rate"],
        rtt=ctx["rtt"],
        sola=ctx["sola"],
        solb=ctx["solb"],
        solc=ctx["solc"],
        sold=ctx["sold"],
        sole=ctx["sole"],
        )

def print_tex(rng):
    ctx = get_ctx(rng)
    ctx = compute(ctx)
    print(get_cmdstr(ctx))

def write_tex(rng):
    ctx = get_ctx(rng)
    ctx = compute(ctx)
    with open("HTTP_Transfer_commands.tex", "w") as commandfile:
        commandfile.write(get_cmdstr(ctx))

def generate(rng):
    write_tex(rng)
    files = ["HTTP_Transfer_commands.tex"]
    return files

if __name__ == "__main__":
    import random
    print_tex(random)
