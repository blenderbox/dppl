from trueskill import TrueSkill


''' ELO Rankings are lame, let's use TrueSkill!
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
'''


def rank(player1, player2):
    """ This function will calculate the TrueSkill ranking of each player. It
    accepts two player arguments. A player is a dictionary containing the
    player's 'mu', and 'sigma'. Player1 is the winner, and Player2 is the
    loser.
    """
    DRAW_PROBABILITY = 0  # It's impossible to draw 1 on 1
    ts = TrueSkill(draw_probability=DRAW_PROBABILITY)
    team1 = (ts.Rating(**player1),)
    team2 = (ts.Rating(**player2),)
    r1, r2 = tuple(x[0] for x in ts.transform_ratings(
        rating_groups=(team1, team2)))
    return ({
        'mu': r1.mu,
        'sigma': r1.sigma,
        'exposure': r1.exposure,
        },
        {
        'mu': r2.mu,
        'sigma': r2.sigma,
        'exposure': r2.exposure,
        })
