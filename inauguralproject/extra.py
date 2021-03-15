import numpy as np
from types import SimpleNamespace
from scipy import optimize
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

# autoreload modules when code is run
%load_ext autoreload
%autoreload 2

par = SimpleNamespace()

par.phi = 0.3
par.epsilon = 0.5
par.r = 0.03
par.tau_g = 0.012
par.tau_p = 0.004
par.p_bar = 3
par.m = 0.5

#Q1


#Utility function
def u_func(h, c, par):
    return c**(1-par.phi)*h**par.phi

#Optimize function
def u_optimize(par):
    def objective(h, par):
        p_thilde = h * par.epsilon
        tax = par.r * h + par.tau_g * p_thilde + par.tau_p * max(p_thilde-par.p_bar, 0)
        c = par.m - tax
        return -u_func(h, c, par)


    res = optimize.minimize_scalar(value_of_choice, method ='brent', args=(par))

    h_star = res.x
    p_thilde = h_star * par.epsilon
    tax = par.r * par.h_star + par.tau_g * p_thilde + par.tau_p * max(p_thilde-par.p_bar, 0)
    c_star = m - tax
    u_star = u_func(h_star, c_star, par)
    return h_star, c_star, u_star

h, c, u = u_optimize(par=par)

# Q2