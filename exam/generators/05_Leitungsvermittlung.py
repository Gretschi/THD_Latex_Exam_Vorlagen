FILES = ["05_Rechnung_Leitungsvermittlung.tex"]

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

def get_context(rng):
    ctx = get_basic_ctx(rng)
    ctx = compute_solution(ctx)
    return ctx
