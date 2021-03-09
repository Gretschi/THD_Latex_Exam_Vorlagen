FILES = ["05_HTTP_Persistent_kein_Pipelining.tex"]

def get_base_context(rng):
    return {
        "sizeweb": rng.randint(2, 20),
        "sizepa": rng.randint(110, 490),
        "sizepb": rng.randint(110, 490),
        "rate": rng.randint(2, 9),
        "rtt": rng.randint(5, 25),
        }

def compute_solution(ctx):
    trans_d_web = round(ctx["sizeweb"] / ctx["rate"], 2)
    trans_d_pa = round(ctx["sizepa"] / ctx["rate"], 2)
    trans_d_pb = round(ctx["sizepb"] / ctx["rate"], 2)

    steps = [ctx["rtt"]] * 5
    steps[1] += trans_d_web
    steps[2] += trans_d_pa
    steps[3] += trans_d_pb

    ctx["steps"] = steps
    ctx["sums"] = [sum(steps[:i+1]) for i in range(len(steps))]
    return ctx
    

def get_context(rng):
    ctx = get_base_context(rng)
    ctx = compute_solution(ctx)
    return ctx
