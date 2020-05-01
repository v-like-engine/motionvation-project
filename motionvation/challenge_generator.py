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
    c, diff, step2, step1 = 0, 0, 0, 0
    if len(plot) == 1:
        if plot[0] < 6:
            c = random.randint(1, 10)
            if plot[0] not in [2, 3, 4]:
                step2, step1 = 9, 6
            else:
                step2, step1 = 10, 8
        elif plot[0] < 7:
            c = random.randint(1, 3)
            step2, step1 = 2, 1
        elif plot[0] < 8:
            c = random.randint(1, 5)
            step2, step1 = 3, 1
        elif plot[0] == 8:
            c = random.randint(4, 40) * 5
            step2, step1 = 320, 200
    elif len(plot) == 2:
        if 3 not in plot:
            c = random.randint(2, 25)
            step2, step1 = 20, 12
        else:
            c = random.randint(2, 16)
            step2, step1 = 15, 9
    else:
        c = random.randint(5, 60)
        step2, step1 = 50, 25
    return c, calculate_difficulty(c, step2, step1)


def calculate_difficulty(c, step2, step1):
    if c > step2:
        diff = 2
    elif c > step1:
        diff = 1
    else:
        diff = 0
    return diff


def generate_challenge():
    plot = choose_challenge_plot()
    required, difficulty = count_plot(plot)
    if len(plot) > 2:
        text = 'Do actions on site: '
    elif len(plot) == 2:
        if 1 in plot:
            text = 'Add tasks or notes: '
        elif 3 in plot:
            text = 'Delete tasks or notes: '
        elif 5 in plot:
            text = 'Do tasks or challenges: '
        else:
            text = 'Do some kind of action: '
    else:
        text = TEXTS[plot[0] - 1]
    text += str(required)
    return {'plot': plot, 'required': required, 'difficulty': difficulty, 'text': text}


add_task = 1
add_note = 2
delete_task = 3
delete_note = 4
do_task = 5
do_challenge = 6
get_level = 7
get_xp = 8

VARIANTS = [add_task, add_note, delete_task, delete_note, do_task, do_challenge, get_level, get_xp]
TEXTS = ['Add tasks: ', 'Add notes: ', 'Delete tasks: ', 'Delete notes: ', 'Do tasks: ',
         'Win challenges: ', 'Get levels: ', 'Get experience: ']
