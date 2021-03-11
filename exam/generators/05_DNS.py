#!/usr/bin/env python

FILES = ["05_DNS.tex", "DNS_Hierarchie.svg"]

def get_base_ctx(rng):
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

def compute_solution(ctx):
    if ctx['rekit'] == 'rekursiv':
        total = ctx["AM"] + ctx["AB"] + ctx["AC"] + ctx["AI"]
        solution = "{AM}ms + {AB}ms + {AC}ms + {AI}ms".format(**ctx)
        ctx['sol'] = solution + " = {}ms".format(total)
    else:
        total = ctx["AM"] + ctx["AB"] + ctx["AF"] + ctx["AJ"]
        solution = "{AM}ms + {AB}ms + {AF}ms + {AJ}ms".format(**ctx)
        ctx['sol'] = solution + " = {}ms".format(total)
    return ctx

def get_context(rng):
    ctx = get_base_ctx(rng)
    ctx = compute_solution(ctx)
    return ctx
