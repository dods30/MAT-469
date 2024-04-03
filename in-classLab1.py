import numpy as np


## (c) Create an nxd matrix to record the numbers of d people for n games
n = 3 # number of games
d = 5 # number of people
game_numbers = np.full((n, d), np.nan) # create empty matrix to store the numbers

## (d) Assign the leftmost person with a random number on [0,1].
game_numbers[:, 0] = np.random.uniform(0, 1, size=n)

## (e) Assign numbers to the rest of people in n games.
for i in range(1, d): # loop through columns 1 to d-1 (Python is 0-indexed)
    game_numbers[:, i] = (game_numbers[:, i-1] + np.random.uniform(0, 1, size=n)) / 2

## (f) Record the winning (1) or losing (0) of each row (game).
game_results = np.apply_along_axis(lambda x: np.any(x > 0.6), 1, game_numbers)
game_results = game_results.astype(int)

## (g) Count the number of times that we win.
number_wins = np.sum(game_results)

## (h) Compute the estimated probability.
n = 10000 # increase the number of games for accurate estimate
game_numbers = np.full((n, d), np.nan)
game_numbers[:, 0] = np.random.uniform(0, 1, size=n)
for i in range(1, d):
    game_numbers[:, i] = (game_numbers[:, i-1] + np.random.uniform(0, 1, size=n)) / 2

game_results = np.apply_along_axis(lambda x: np.any(x > 0.6), 1, game_numbers)
game_results = game_results.astype(int)
est_prob = np.sum(game_results) / n

## (i) Compute the confidence interval.
CI_low = est_prob - 2.58 * np.sqrt(est_prob * (1 - est_prob) / n)
CI_high = est_prob + 2.58 * np.sqrt(est_prob * (1 - est_prob) / n)

print(f"We are 99% confident that the probability of winning the game falls between {CI_low} and {CI_high}")
print(f"The estimated probability of winning the game is {est_prob}.")
