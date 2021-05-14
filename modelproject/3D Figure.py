#Import relevant packages
from scipy import optimize
import numpy as np
from types import SimpleNamespace
import copy
import matplotlib.pyplot as plt


par = SimpleNamespace()

par.r = 0.02
par.V_1 = 5
par.Y_L1 = 2
par.Y_L2 = 2
par.T_1 = 0.5
par.T_2 = 0.5
par.phi = 0.3


# Utility function
def inter_utility(C_1, par):
    """
    Intertemporal consumer utility function in two periods

    Args:

        C_1 (float): consumption in period 1
        par: simplenamespace containing relevant parameters
            T_1 (float): lump-sum tax in period 1
            T_2 (float): lump-sum tax in period 2
            Y_L1 (float): labour income in period 1
            Y_L2 (float): labour income in period 2
            V_1 (float): initial endowment
            phi (float): degree of impatience
            r (float): rental rate

    Returns:
    
        (float): total utility
    """
    return np.log(C_1) + np.log((1+par.r)*(par.V_1 + par.Y_L1 - par.T_1 - C_1) + par.Y_L2 - par.T_2)/(1+par.phi)

# Utility optimise function
def u_optimise(par):
    """
    Optimises max_func 

     Args:

     C_1 (float): consumption in period 1
        par: simplenamespace containing relevant parameters
            T_1 (float): lump-sum tax in period 1
            T_2 (float): lump-sum tax in period 2
            Y_L1 (float): labour income in period 1
            Y_L2 (float): labour income in period 2
            V_1 (float): initial endowment
            phi (float): degree of impatience
            r (float): rental rate

    Returns:
    
        C_1star (float): optimal consumption in period 1
        C_2star (float): optimal consumption in period 2
        U_star (float): utility in optimum
    """
    def objective(C_1, par):
        return -inter_utility(C_1, par)
    
    #Creating bounds for optimization
    lower = 0
    upper = par.V_1 + par.Y_L1 - par.T_1 + (par.Y_L2 - par.T_2)/(1 + par.r)

    #Running the optimization function
    res = optimize.minimize_scalar(objective, method ='bounded', bounds = (lower,upper), args = (par))

    # Get optimal C_1, using monotonicity to find optimal C_2, then using u_func to find utility in optimum
    C_1star = res.x
    C_2star = (1+par.r)*(par.V_1 + par.Y_L1 - par.T_1 - C_1star) + par.Y_L2 - par.T_2
    U_star = np.log(C_1star) + (np.log(C_2star)/(1+par.phi))
    return C_1star, C_2star, U_star


#3D graph
N = 100
shape_tuple = (N,N)
r_values = np.empty(shape_tuple)
phi_values = np.empty(shape_tuple)
u_values = np.empty(shape_tuple)

for i in range(N):
        for j in range(N):
            par.r = i/100
            par.phi = j/100
            r_values[i,j] = par.r
            phi_values[i,j] = par.phi
            c1, c2, u = u_optimise(par)
            u_values[i,j] = u
    

from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
%matplotlib widget
fig = plt.figure(figsize=(10,7))
ax = plt.axes(projection='3d')
ax.plot_surface(phi_values,r_values, u_values, rstride=1, cstride=1,
                cmap='viridis', edgecolor='none');
ax.set_xlabel('$\phi$')
ax.set_ylabel('$r$')
ax.set_zlabel('$U$')
ax.set_title('Utility for values of $\phi$ and $r$');