def calculatexp(exp):
    lvl = 0
    i = 0
    while exp > 0:
        i += 1
        si = str(i)
        if len(si) == 1:
            d = '0'
        elif len(si) == 2:
            d = si[-2]
        elif i >= list(LVLS.keys())[-1] * 10:
            d = '30'
        else:
            d = si[:-1]
        exp -= LVLS[int(d)]
        lvl += 1
    if exp < 0:
        lvl -= 1
    return lvl


def ranculate(exp):
    lvl = calculatexp(exp)
    rank = 0
    for i in range(len(RANKS)):
        lvl -= 10 + 5 * i
        if lvl >= 0:
            rank += 1
        else:
            return RANKS[rank]
    return RANKS[-1]


RANKS = ['Novice', 'Private', 'Interested', 'Motivated', 'Inspired', 'Experienced', 'Enlightened',
         'Master', 'Almightly']
LVLS = {0: 100, 1: 250, 2: 500, 3: 800, 4: 1200, 5: 1500, 6: 1600, 7: 1700, 8: 1800, 9: 1900,
        10: 2000, 11: 2050, 12: 2100, 13: 2150, 14: 2200, 15: 2250, 16: 2300, 17: 2350, 18: 2400,
        19: 2450, 20: 2500, 21: 2600, 22: 2700, 23: 2800, 24: 2900, 25: 3000, 26: 3200, 27: 3330,
        28: 3500, 29: 4000, 30: 5000}

print(ranculate(277999))
print(ranculate(278000))
print(ranculate(389599))
print(ranculate(389600))
