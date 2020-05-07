import random


def choose_challenge_plot():
    chance = random.randint(0, 99)
    if chance < 59:
        plot = [random.choice(CHALLENGE_TASK_VARIANTS[:7])]
    elif chance < 80:
        plot = random.choice([CHALLENGE_TASK_VARIANTS[:2], CHALLENGE_TASK_VARIANTS[2:4], CHALLENGE_TASK_VARIANTS[4:6]])
    elif chance < 95:
        plot = [CHALLENGE_TASK_VARIANTS[-2]]
    elif chance <= 99:
        plot = CHALLENGE_TASK_VARIANTS[:6]
    else:
        plot = [CHALLENGE_TASK_VARIANTS[-1]]
    return plot


def count_plot(plot):
    count_of_points_required, diff, points_for_hard_diff, points_for_medium_diff = 0, 0, 0, 0
    if not isinstance(plot, list):
        plot = [plot]
    if len(plot) == 1:
        if plot[0] < do_challenge:
            count_of_points_required = random.randint(1, 10)
            if plot[0] not in [2, 3, 4]:
                points_for_hard_diff, points_for_medium_diff = 9, 6
            else:
                points_for_hard_diff, points_for_medium_diff = 10, 8
        elif plot[0] < get_xp:
            count_of_points_required = random.randint(1, 3)
            points_for_hard_diff, points_for_medium_diff = 2, 1
        elif plot[0] == get_xp:
            count_of_points_required = random.randint(4, 40) * 5
            points_for_hard_diff, points_for_medium_diff = 320, 200
        elif plot[0] == get_level:
            count_of_points_required = random.randint(1, 5)
            points_for_hard_diff, points_for_medium_diff = 3, 1
    elif len(plot) == 2:
        if delete_task not in plot:
            count_of_points_required = random.randint(2, 25)
            points_for_hard_diff, points_for_medium_diff = 17, 12
        else:
            count_of_points_required = random.randint(2, 18)
            points_for_hard_diff, points_for_medium_diff = 17, 10
    else:
        count_of_points_required = random.randint(5, 60)
        points_for_hard_diff, points_for_medium_diff = 50, 25
    return count_of_points_required, calculate_difficulty(count_of_points_required,
                                                          points_for_hard_diff, points_for_medium_diff)


def calculate_difficulty(count_of_points_required, points_for_hard_diff, points_for_medium_diff):
    if count_of_points_required > points_for_hard_diff:
        diff = 2
    elif count_of_points_required > points_for_medium_diff:
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
        if add_task in plot:
            text = 'Add tasks or notes: '
        elif delete_task in plot:
            text = 'Delete tasks or notes: '
        elif do_task in plot:
            text = 'Do tasks or challenges: '
        else:
            text = 'Do some kind of action: '
    else:
        text = TITLES_OF_CHALLENGES[plot[0] - 1]
    text += str(required)
    return {'plot': plot, 'required': required, 'difficulty': difficulty, 'text': text}


add_task = 1
add_note = 2
delete_task = 3
delete_note = 4
do_task = 5
do_challenge = 6
get_xp = 7
get_level = 8

CHALLENGE_TASK_VARIANTS = [add_task, add_note, delete_task, delete_note, do_task, do_challenge, get_xp, get_level]
TITLES_OF_CHALLENGES = ['Add tasks: ', 'Add notes: ', 'Delete tasks: ', 'Delete notes: ', 'Do tasks: ',
                        'Win challenges: ', 'Get experience: ', 'Get levels: ']
