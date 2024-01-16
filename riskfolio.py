import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import riskfolio as rp
import warnings
warnings.filterwarnings("ignore")

start = "2019-01-01"
end = "2022-01-01"

assets = ["BTC-USD", "ETH-USD", "LTC-USD"]

data = yf.download(assets, start=start, end=end)

returns = data["Adj Close"].pct_change().dropna()

# Variables
method_mu  = "hist"    # Method to estimate expected returns
method_cov = "hist"    # Method to estimate covariance matrix
hist = True            # Use historical scenarios for risk measures that depend on scenarios
model      = "Classic" # Could bassice Cl or BL
rm         = "MV"      # Risk measure used, this time will be variance
obj        = "Sharpe"  # Objective function, could be MinRisk, MaxRet, Utility, Sharpe, etc
rf         = 0         # Risk free rate
#l          = 0.5       # Risk aversion factor, only useful when obj is "Utility"

# initialize the portfolio object
port = rp.Portfolio(returns=returns)
port.assets_stats(method_mu=method_mu, method_cov=method_cov)
w = port.optimization(model=model, rm=rm, obj=obj, rf=rf, hist=hist)

# Plotting
ax = rp.plot_pie(w=w, title="Portfolio Weights", others=0.05, nrow=25, cmap="tab20")
plt.show()

frontier = port.efficient_frontier(model=model, rm=rm, rf=rf, hist=hist, n_points=100) # or "points"
ax = rp.plot_frontier(w_frontier=frontier, model=model, rm=rm, rf=rf, hist=hist, nrow=25, cmap="tab20")

# just print the efficient frontier to see the distributions of weights
frontier

ax = rp.plot_frontier_area(w_frontier=frontier, cmap="tab20")
plt.show()

ax = rp.jupyter_report(returns, w, rm=rm)
plt.show()