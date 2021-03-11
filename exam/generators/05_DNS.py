#!/usr/bin/env python

FILES = ["05_DNS.tex", "DNS_Hierarchie.svg"]

def get_context(rng):
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
