#!/usr/bin/env python

from cairosvg import svg2png

TEMPLATE_CMD = """
\\newcommand{{\\rekit}}{{{rekit}}}
\\newcommand{{\\sol}}{{{sol}}}
"""

def get_ctx(rng):
    return {
        "AA": rng.randint(15, 45),
        "AB": rng.randint(15, 45),
        "AC": rng.randint(15, 45),
        "AD": rng.randint(15, 45),
        "AE": rng.randint(15, 45),
        "AF": rng.randint(15, 45),
        "AG": rng.randint(15, 45),
        "AH": rng.randint(15, 45),
        "AI": rng.randint(15, 45),
        "AJ": rng.randint(15, 45),
        "AK": rng.randint(15, 45),
        "AL": rng.randint(15, 45),
        "AM": rng.randint(5, 15),
        "AN": rng.randint(5, 15),
        "AO": rng.randint(15, 45),
        "rekit": rng.choice(["rekursiv", "iterativ"]),
        }

def compute(ctx):
    if ctx['rekit'] == 'rekursiv':
        total = ctx["AM"] + ctx["AB"] + ctx["AC"] + ctx["AI"]
        solution = "{AM}ms + {AB}ms + {AC}ms + {AI}ms".format(**ctx)
        ctx['sol'] = solution + " = {}ms".format(total)
    else:
        total = ctx["AM"] + ctx["AB"] + ctx["AF"] + ctx["AJ"]
        solution = "{AM}ms + {AB}ms + {AF}ms + {AJ}ms".format(**ctx)
        ctx['sol'] = solution + " = {}ms".format(total)
    return ctx

def get_cmdstr(ctx):
    ctx = compute(ctx)
    return TEMPLATE_CMD.format(**ctx)

def get_DNS_contents(ctx):
    with open("tex_base/DNS_Hierarchie.svg", "r") as dnsfile:
        content = dnsfile.read()
        return content.format(**ctx)

def print_tex(rng):
    ctx = get_ctx(rng)
    print(get_cmdstr(ctx))

def write_tex(rng):
    ctx = get_ctx(rng)
    with open("DNS_commands.tex", "w") as commandfile:
        commandfile.write(get_cmdstr(ctx))
    dnscontents = get_DNS_contents(ctx).encode('utf-8')
    svg2png(bytestring=dnscontents, write_to="DNS_Hierarchie.png", dpi=150)

def generate(rng):
    write_tex(rng)
    files = ["DNS_commands.tex", "DNS_Hierarchie.png"]
    return files

if __name__ == "__main__":
    import random
    print_tex(random)
