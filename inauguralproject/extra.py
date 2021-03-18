import numpy as np
from types import SimpleNamespace
from scipy import optimize


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