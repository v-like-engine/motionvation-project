def calculatexp(exp):
    lvl = 0
    i = 0
    mx = LVLS[0]
    cur = exp
    while exp > 0:
        i += 1
        d = find_det(i)
        exp -= LVLS[int(d)]
        if exp >= 0:
            mx = LVLS[int(d)]
            cur = exp
        else:
            mx = LVLS[int(find_det(i + 1))]
        lvl += 1
    if exp < 0:
        lvl -= 1
    return lvl, mx, cur


def find_det(i):
    si = str(i)
    if len(si) == 1:
        d = '0'
    elif len(si) == 2:
        d = si[-2]
    elif i >= list(LVLS.keys())[-1] * 10:
        d = '30'
    else:
        d = si[:-1]
    return d


def ranculate(exp):
    lvl = calculatexp(exp)[0]
    rank = 0
    for i in range(len(RANKS)):
        lvl -= 10 + 5 * i
        if lvl >= 0:
            rank += 1
        else:
            return RANKS[rank]
    return RANKS[-1]


RANKS = ['Novice', 'Private', 'Interested', 'Motivated', 'Motioned', 'Inspired', 'Experienced', 'Enlightened',
         'Master', 'Almightly']
LVLS = {0: 100, 1: 250, 2: 500, 3: 750, 4: 1000, 5: 1100, 6: 1200, 7: 1400, 8: 1600, 9: 1800,
        10: 2000, 11: 2050, 12: 2100, 13: 2150, 14: 2200, 15: 2250, 16: 2300, 17: 2350, 18: 2400,
        19: 2450, 20: 2500, 21: 2600, 22: 2700, 23: 2800, 24: 2900, 25: 3000, 26: 3300, 27: 3500,
        28: 3800, 29: 4000, 30: 5000}
