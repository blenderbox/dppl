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
    accepts two players arguments. The first is the winning player, the second
    is the losing player. Both should be Profile objects. This will not save
    the players.

    Args:
        player1: The winning user profile
        player2: The losing user profile

    Returns:
        A tuple of (player1, player2)
    """
    DRAW_PROBABILITY = 0  # It's impossible to draw 1 on 1
    approx = lambda f: round(f, 6)  # Round all floats to 6 decimals

    ts = TrueSkill(draw_probability=DRAW_PROBABILITY)
    t1 = (ts.Rating(mu=player1.mu, sigma=player1.sigma),)
    t2 = (ts.Rating(mu=player2.mu, sigma=player2.sigma),)
    r1, r2 = tuple(x[0] for x in ts.transform_ratings(rating_groups=(t1, t2)))

    player1.mu = approx(r1.mu)
    player1.sigma = approx(r1.sigma)
    player1.exposure = approx(r1.exposure)

    player2.mu = approx(r2.mu)
    player2.sigma = approx(r2.sigma)
    player2.exposure = approx(r2.exposure)

    player1.save()
    player2.save()

    return player1, player2
