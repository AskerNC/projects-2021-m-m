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

#Q2
def two_figures(x_left, y_left, title_left, xlabel_left, ylabel_left, x_right, y_right, title_right, xlabel_right, ylabel_right):
    """ 
    Plots two aligned figures. 
    
    Inputs: should be self explanatory...
    Output: Two figures in 2D
    """
    # a. initialise figure
    fig = plt.figure(figsize=(10,4))# figsize is in inches...

    # b. left plot
    ax_left = fig.add_subplot(1,2,1)
    ax_left.plot(x_left,y_left)

    ax_left.set_title(title_left)
    ax_left.set_xlabel(xlabel_left)
    ax_left.set_ylabel(ylabel_left)

    # c. right plot
    ax_right = fig.add_subplot(1,2,2)

    ax_right.plot(x_right, y_right)

    ax_right.set_title(title_right)
    ax_right.set_xlabel(xlabel_right)
    ax_right.set_ylabel(ylabel_right)
    fig.show()

# Creates an array for m and containers for the values of c* and h* 
N = 10000
m = np.linspace(0.4,1.5,num=N)
c_vals = np.empty(N)
h_vals = np.empty(N)

# Loops the optimiser over the m array.
for i,mi in enumerate(m):
    ch_star = u_optimize(phi, epsilon, r, tau_g, tau_p, p_bar, mi)

    c_vals[i] = ch_star[0]
    h_vals[i] = ch_star[1]

two_figures(m, c_vals, "Consumption", "$m$", "$c$", m, h_vals, "House Quality", "$m$", "$h$")

#Q3
seed = 1
size = 10000
low = -0.4
high = 0.35

def tax_burden(seed, size, low, high, phi=0.3, epsilon=0.5, r=0.03, tau_g=0.012, tau_p=0.004,p_bar=3):
    np.random.seed(seed)
    mi = np.random.lognormal(low,high,size)

    tax_burd = 0

    for i, mi in enumerate(mi):
        ch_star = u_optimize(phi, epsilon, r, tau_g, tau_p, p_bar, mi)
        tax_i = tau_g*ch_star[1] + tau_p*max(ch_star[1]-p_bar,0)
        tax_burd += tax_i/size
    return tax_burd

tax_burden(seed, size, low, high)
