import numpy as np
import copy
from types import SimpleNamespace
from scipy import optimize
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

# autoreload modules when code is run
#%load_ext autoreload
#%autoreload 2


#Creates parameters as a namespace

par = SimpleNamespace()

par.phi = 0.3
par.epsilon = 0.5
par.r = 0.03
par.tau_g = 0.012
par.tau_p = 0.004
par.p_bar = 3
par.m = 0.5
par.seed = 1

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
    
    res = optimize.minimize_scalar(objective, method ='brent', args = (par))

    h_star = res.x
    p_thilde = h_star * par.epsilon
    tax = par.r * h_star + par.tau_g * p_thilde + par.tau_p * max(p_thilde-par.p_bar, 0)
    c_star = par.m - tax
    u_star = u_func(h_star, c_star, par)
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


#Q3

def tax_total(par):
    np.random.seed(par.seed)
    T = 0
    for i in range(par.pop):
        par.m = np.random.lognormal(par.mu, par.sigma)
        h_cit, c_cit, u_cit = u_optimize(par)
        T += par.tau_g*(h_cit*par.epsilon) + par.tau_p*max((par.epsilon*h_cit)-par.p_bar, 0)
    return T


#Defining population size, mean and standard deviation
par.pop = 10000
par.mu = -0.4
par.sigma = 0.35

T = tax_total(par)
print(T)

tax_burden = T/par.pop
print(tax_burden)

#BONUS


#Resetting seed
np.random.seed(par.seed)

m_pop = np.random.lognormal(par.mu, par.sigma, par.pop)
h_pop = np.zeros(par.pop)
c_pop = np.zeros(par.pop)
u_pop = np.zeros(par.pop)

for i in range(par.pop):
    par.m = m_pop[i]
    h_pop[i], c_pop[i], u_pop[i] = u_optimize(par)


#Creates and plots figure

bonus = plt.figure(dpi=100)
ax_left = bonus.add_subplot(1,1,1)
ax_left.hist(m_pop,bins=100,density=True,alpha=0.5,label='cash-on-hand')

ax_right = bonus.add_subplot(1,1,1)
ax_right.hist(h_pop,bins=100,density=True,alpha=0.5,label='housing')
#ax.legend(loc='upper left');
# note: the ; stops output from being printed
bonus.show()

#Both have right leaning normal distrubutions, not suprising given m's log-normal distribution.
#Nothing odd about m's distrubution
#The distrubution of h is odd since it has a large concentration around 6
#This is due to the cutoff-tax




#Q4

par2 = copy.copy(par)

par2.epsilon = 0.8
par2.tau_g = 0.01
par2.tau_p = 0.009
par2.p_bar = 8

T_reform = tax_total(par2)
print(T_reform)

tax_burden_reform = T_reform/par2.pop
print(tax_burden_reform)




#Q5 - find new lower tau_g


def base_tax_pct(par):
    def obj(tau_g, par):
        par.tau_g = tau_g
        return tax_total(par) - par.T_goal
    sol = optimize.root(obj, 0.01, args=(par))
    tau = sol.x
    return tau

par2.T_goal = T

tau_g = base_tax_pct(par2)
print(tau_g)

par2.tau_g = tau_g

print(tax_total(par2))