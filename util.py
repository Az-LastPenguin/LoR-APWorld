import random, math

def box_muller(random: random.Random):
    theta = 2 * math.pi * random.random()
    R = math.sqrt(-2 * math.log(random.random()))
    x = R * math.cos(theta)
    y = R * math.sin(theta)

    return x, y

def box_muller_constraint(random: random.Random, f: int, t: int):
    while True:
        diff = t - f
        mean = (t + f) / 2
        x, y = box_muller(random)
        x = .42 * diff / 2 * x + mean
        y = .42 * diff / 2 * y + mean
        if f <= x and x <= t:
            return x
        if f <= y and y <= t:
            return y