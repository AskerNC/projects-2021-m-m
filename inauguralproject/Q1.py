import numpy as np
from scipy import optimize
import numpy as np
from types import SimpleNamespace
from scipy import optimize
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

# autoreload modules when code is run
%load_ext autoreload
%autoreload 2


phi = 0.3
epsilon = 0.5
r = 0.03
tau_g = 0.012
tau_p = 0.004
p_bar = 3
m = 0.5

#Q1


#Utility function
def u_func(h, c, phi = 0.3):
    return c**(1-phi)*h**phi

#Optimize function
def u_optimize(phi, epsilon, r, tau_g, tau_p, p_bar, m):
    def objective(h, phi, epsilon, r, tau_g, tau_p, p_bar, m):
        p_thilde = h * epsilon
        tax = r * h + tau_g * p_thilde + tau_p * max(p_thilde-p_bar, 0)
        c = m - tax
        return -u_func(h, c, phi)


    sol = optimize.minimize_scalar(objective, method ='brent', args = (phi, epsilon, r, tau_g, tau_p, p_bar, m))

    h_star = sol.x
    p_thilde = h_star * epsilon
    tax = r * h_star + tau_g * p_thilde + tau_p * max(p_thilde-p_bar, 0)
    c_star = m - tax
    u_star = u_func(h_star, c_star, phi)
    return h_star, c_star, u_star

h, c, u = u_optimize(phi, epsilon, r, tau_g, tau_p, p_bar, m)

print(h, c, u)

# Q2