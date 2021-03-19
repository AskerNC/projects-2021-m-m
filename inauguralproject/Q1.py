import numpy as np
from scipy import optimize
from types import SimpleNamespace
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

# autoreload modules when code is run
#%load_ext autoreload
#%autoreload 2

#set seed
seed = 1
np.random.seed(seed)


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

N = 1000
m_vec = np.linspace(0.4, 1.5, N)
h_vec = np.zeros(N)
c_vec = np.zeros(N)
u_vec = np.zeros(N)

for i in range(N):
    h_vec[i], c_vec[i], u_vec[i] = u_optimize(phi, epsilon, r, tau_g, tau_p, p_bar, m_vec[i])


# create the figure
fig = plt.figure(figsize=(10,4))# figsize is in inches...


# left plot
ax_left = fig.add_subplot(1,2,1)

ax_left.plot(m_vec,h_vec)

ax_left.set_title('h* as function of m')
ax_left.set_xlabel('m')
ax_left.set_ylabel('h*')
ax_left.grid(True)

# c. right plot
ax_right = fig.add_subplot(1,2,2)

ax_right.plot(m_vec,c_vec)

ax_right.set_title('c* as function of m')
ax_right.set_xlabel('m')
ax_right.set_ylabel('c*')
ax_right.grid(True)

plt.show()


#Q3

np.random.seed(seed)
N = 10000
m_vec = np.random.lognormal(-0.4, 0.35, N)
h_vec = np.zeros(N)
c_vec = np.zeros(N)
u_vec = np.zeros(N)

for i in range(N):
    h_vec[i], c_vec[i], u_vec[i] = u_optimize(phi, epsilon, r, tau_g, tau_p, p_bar, m_vec[i])

def tax(h, tau_g, tau_p):
    T = 0
    for i, hi in enumerate(h):
        T += tau_g*hi + tau_p*max(hi-p_bar, 0)
    return T

T = tax(h_vec, tau_g, tau_p)
print(T)

tax_burden = T/N
print(tax_burden)