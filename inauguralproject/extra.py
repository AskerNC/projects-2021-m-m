import numpy as np
from types import SimpleNamespace
from scipy import optimize
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

# autoreload modules when code is run
#%load_ext autoreload
#%autoreload 2

#set seed
seed = 1


#Creates parameters as a namespace

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
def u_func(h, c, parameters):
    return c**(1-parameters.phi)*h**parameters.phi

#Optimize function
def u_optimize(parameters):
    def objective(h, parameters):
        p_thilde = h * parameters.epsilon
        tax = parameters.r * h + parameters.tau_g * p_thilde + parameters.tau_p * max(p_thilde-parameters.p_bar, 0)
        c = parameters.m - tax
        return -u_func(h, c, parameters)
    
    res = optimize.minimize_scalar(objective, method ='brent', args = (parameters))

    h_star = res.x
    p_thilde = h_star * parameters.epsilon
    tax = parameters.r * h_star + parameters.tau_g * p_thilde + parameters.tau_p * max(p_thilde-parameters.p_bar, 0)
    c_star = parameters.m - tax
    u_star = u_func(h_star, c_star, parameters)
    return h_star, c_star, u_star

h, c, u = u_optimize(par)

print(h, c, u)

# Q2


def two_figures(x_left, y_left, title_left, xlabel_left, ylabel_left, x_right, y_right, title_right, xlabel_right, ylabel_right, grid=True):
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
    ax_left.grid(grid)

    # c. right plot
    ax_right = fig.add_subplot(1,2,2)

    ax_right.plot(x_right, y_right)

    ax_right.set_title(title_right)
    ax_right.set_xlabel(xlabel_right)
    ax_right.set_ylabel(ylabel_right)
    ax_right.grid(grid)
    return fig

#Creaters array of m's and container for h*, c* and u*
N = 1000
m_vec = np.linspace(0.4, 1.5, N)
h_vec = np.zeros(N)
c_vec = np.zeros(N)
u_vec = np.zeros(N)

for i in range(N):
    par.m = m_vec[i]
    h_vec[i], c_vec[i], u_vec[i] = u_optimize(par)

#Creates graph
Q2 = two_figures(m_vec, c_vec, "Consumption", "$m$", "$c$", m_vec, h_vec, "House Quality", "$m$", "$h$")
#Shows graph
Q2.show()