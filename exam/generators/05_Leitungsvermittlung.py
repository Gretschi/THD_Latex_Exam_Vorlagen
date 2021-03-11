FILES = ["05_Rechnung_Leitungsvermittlung.tex"]

def get_context(rng):
    return {
        "datarate": rng.randint(10, 100),
        "channels": rng.randint(10, 30),
        "switchingdelay": rng.randint(50, 1000),
        "data": rng.randint(10, 900),
        }
