from __future__ import division


def calculate_elo(winner, loser, draw=False):
    """ This function will calculate the new ELO rankings of each player's
    score which is fed in. In the case that the match is a draw, set draw to
    True.

    int(winner)
    int(loser)
    bool(draw)
    returns {'winner': int(), 'loser': int()}
    """
    K = 20
    prob = lambda x, y: 1 / (10 ** ((x - y) / 400) + 1)
    prob_win = prob(loser, winner)
    prob_los = prob(winner, loser)
    scor_win = 0.5 if draw else 1
    scor_los = 0.5 if draw else 0
    return {
            'winner': int(winner + (K * (scor_win - prob_win))),
            'loser': int(loser + (K * (scor_los - prob_los))),
            }
