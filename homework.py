import numpy as np
from scipy.stats import norm

# Set seed for reproducibility
np.random.seed(123)

# Set the number of simulations and people
n_simulations = 10000
n_people = 6

# Initialize a matrix to store the numbers for each person in each simulation
numbers_matrix = np.zeros((n_simulations, n_people))

# Simulate the game n_simulations times
for i in range(n_simulations):
    # Generate random numbers for each person and store them in the matrix
    numbers_matrix[i, :] = np.random.normal(size=n_people)
    
    # Calculate the product of numbers for each person
    for j in range(1, n_people):
        numbers_matrix[i, j] *= numbers_matrix[i, j - 1]

# Check if any number is larger than 0 in each simulation
game_results = np.any(numbers_matrix > 0, axis=1)

# Estimate the probability of winning
win_probability = game_results.mean()

# Construct a 99% confidence interval
ci_lower = win_probability - norm.ppf(0.995) * np.sqrt(win_probability * (1 - win_probability) / n_simulations)
ci_upper = win_probability + norm.ppf(0.995) * np.sqrt(win_probability * (1 - win_probability) / n_simulations)

# Print the results
print(f"Estimated probability of winning: {win_probability}")
print(f"99% Confidence Interval: {ci_lower} - {ci_upper}")
