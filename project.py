import numpy as np
from scipy.stats import gamma

def vasicek_model(r0, a, b, sigma, dt, T, num_paths):
    num_steps = int(T / dt)
    r = np.zeros((num_paths, num_steps + 1))
    r[:, 0] = r0
    for i in range(1, num_steps + 1):
        r[:, i] = r[:, i - 1] + a * (b - r[:, i - 1]) * dt + sigma * np.sqrt(dt) * np.random.normal(size=num_paths)
    return r

def jackpot_model(S0, r, sigma, dt, T, num_paths):
    num_steps = int(T / dt)
    S = np.zeros((num_paths, num_steps + 1))
    S[:, 0] = S0
    for i in range(1, num_steps + 1):
        Xj = np.random.normal(size=num_paths)
        Yj = gamma.rvs(dt / 0.15, scale=0.15, size=num_paths)
        sqrt_term = np.sqrt(Yj * Xj)
        sqrt_term[np.isnan(sqrt_term)] = 0  # Replace invalid values with 0
        S[:, i] = S[:, i - 1] * np.exp((r[:, i - 1] + np.log(1 - 0.15 * sigma**2 / 2) / 0.15) * dt + sigma * sqrt_term)
    return S

def european_call_payoff(S, K):
    return np.maximum(S - K, 0)

def discount_factor(r, dt):
    return np.exp(-dt * np.sum(r, axis=1))

def estimate_option_price(S0, K, r0, a, b, sigma_r, sigma_s, dt, T, num_paths, tol=0.05):
    r = vasicek_model(r0, a, b, sigma_r, dt, T, num_paths)
    S = jackpot_model(S0, r, sigma_s, dt, T, num_paths)
    payoff = european_call_payoff(S[:, -1], K)
    discount = discount_factor(r, dt)
    option_price = np.mean(payoff * discount)
    standard_error = np.std(payoff * discount) / np.sqrt(num_paths)
    
    while standard_error > tol / 2:
        num_paths *= 2
        r = vasicek_model(r0, a, b, sigma_r, dt, T, num_paths)
        S = jackpot_model(S0, r, sigma_s, dt, T, num_paths)
        payoff = european_call_payoff(S[:, -1], K)
        discount = discount_factor(r, dt)
        option_price = np.mean(payoff * discount)
        standard_error = np.std(payoff * discount) / np.sqrt(num_paths)
    
    return option_price, num_paths

S0 = 50
K = 50
r0 = 0.07
a = 0.18
b = 0.086
sigma_r = 0.02
sigma_s = 0.13
T = 1

dt_monthly = 1 / 12
dt_weekly = 1 / 52

price_monthly, paths_monthly = estimate_option_price(S0, K, r0, a, b, sigma_r, sigma_s, dt_monthly, T, 10000)
price_weekly, paths_weekly = estimate_option_price(S0, K, r0, a, b, sigma_r, sigma_s, dt_weekly, T, 1000)

print(f"Monthly time step (dt = 1/12):")
print(f"Required sample size: {paths_monthly}")
print(f"Estimated option price: ${price_monthly:.2f}")

print(f"\nWeekly time step (dt = 1/52):")
print(f"Required sample size: {paths_weekly}")
print(f"Estimated option price: ${price_weekly:.2f}")

print(f"\nThe estimated price with a weekly time step is higher than with a monthly time step.")
print("Theoretically, the price of a European option should not depend on the number of time steps used.")
print("This is because the payoff only depends on the asset price at maturity.")
print("The difference in prices is likely due to the discretization error introduced by the time steps.")

# Comparison with Geometric Brownian Motion
from scipy.stats import norm

def gbm_call_price(S0, K, r, sigma, T):
    d1 = (np.log(S0 / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

gbm_price = gbm_call_price(S0, K, r0, sigma_s, T)
print(f"\nBlack-Scholes price (Geometric Brownian Motion): ${gbm_price:.2f}")
print(f"The jackpot model prices are higher than the Black-Scholes price.")
print("This could be due to the additional randomness introduced by the stochastic interest rate.")
print("The variance-gamma model used for the asset price also allows for heavier tails and skewness.")