#%%
from julia import Main
# ForwardDiff is already included in the Docker image
# from julia import Pkg
# Pkg.add('ForwardDiff')
from julia import ForwardDiff

f = Main.eval('x -> x^2 - 5x + 6')
ForwardDiff.derivative(f, 2.5)

#%%
import matplotlib.pyplot as plt
import numpy as np

Main.eval('g(x) = x * exp(-x) / (x^2 + 1) * sin(pi * x)')
domain = np.arange(-2, 2, step=0.05)
image = Main.map(Main.g, domain)

a = -0.4
Main.eval('g1(x) = ForwardDiff.derivative(g, x)')
Main.eval('g2(x) = ForwardDiff.derivative(g1, x)')
Main.eval('g3(x) = ForwardDiff.derivative(g2, x)')

def taylor(x, a):
    return Main.g(a) + \
        Main.g1(a) * (x - a) + \
        Main.g2(a) * (x - a)**2 / 2 + \
        Main.g3(a) * (x - a)**3 / 6

plt.figure(figsize=(10,6))
plt.plot(domain, image)
plt.scatter([a], [Main.g(a)], color='red')
plt.plot(domain, taylor(domain, a), color='red')
plt.ylim(image.min() - 1, image.max() + 1)
plt.savefig('taylor.png')