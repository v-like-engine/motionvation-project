import random

def choose_challenge_plot():
    n = random.randint(0, 99)
    if n < 59:
        plot = [random.choice(VARIANTS[:7])]
    elif n < 80:
        plot = random.choice([VARIANTS[:2], VARIANTS[2:4], VARIANTS[4:6]])
    elif n < 95:
        plot = random.choice(VARIANTS[-2:])
    else:
        plot = VARIANTS[:7]
    return plot


def count_plot(plot):
    c, diff = 0, 0
    if len(plot) == 1:
        if plot[0] < 6:
            c = random.randint(1, 10)
            if c > 9:
                diff = 2
            elif c > 5:
                diff = 1
            else:
                diff = 0
        elif plot[0] < 7:
            c = random.randint(1, 3)
            if c > 2:
                diff = 2
            elif c > 1:
                diff = 1
            else:
                diff = 0
        elif plot[0] < 8:
            c = random.randint(1, 5)
            if c > 3:
                diff = 2
            elif c > 1:
                diff = 1
            else:
                diff = 0
        elif plot[0] == 8:
            c = random.randint(4, 40) * 5
            if c > 320:
                diff = 2
            elif c > 200:
                diff = 1
            else:
                diff = 0
    elif len(plot) == 2:
        c = random.randint(2, 25)
        if c > 20:
            diff = 2
        elif c > 12:
            diff = 1
        else:
            diff = 0
    else:
        c = random.randint(5, 60)
        if c > 50:
            diff = 2
        elif c > 25:
            diff = 1
        else:
            diff = 0
    return c, diff


required = 0
difficulty = 0
add_task = 1
add_note = 2
delete_task = 3
delete_note = 4
do_task = 5
do_challenge = 6
get_level = 7
get_xp = 8

VARIANTS = [add_task, add_note, delete_task, delete_note, do_task, do_challenge, get_level, get_xp]
