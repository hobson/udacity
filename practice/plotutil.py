"""
Make a histogram of normally distributed random numbers and plot the
analytic PDF over it
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab


def plot_hist(x):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    num_bins = len(x) ** 0.5

    # bin the data
    n, bins, patches = ax.hist(x, num_bins, normed=1, facecolor='green', alpha=0.75)

    # compute bin centers
    # bincenters = 0.5*(bins[1:]+bins[:-1])
    # plot a normal curve
    #y = mlab.normpdf(bincenters, mu, sigma)
    #l = ax.plot(bincenters, y, 'r--', linewidth=1)

    ax.set_xlabel(' x')
    ax.set_ylabel(' y')
    #ax.set_title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
    #ax.set_xlim(40, 160)
    #ax.set_ylim(0, 0.03)
    ax.grid(True)
    plt.show()