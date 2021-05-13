#Import relevant packages
from scipy import optimize
import numpy as np
from types import SimpleNamespace
import matplotlib.pyplot as plt

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
        # Use monotonicity to find c as a function of h
        #par.V_2 = (1+par.r)(par.V_1 + par.Y_L1 - par.T_1 - C_1)
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

# Plot function
def two_figures(x_left, y_left, title_left, xlabel_left, ylabel_left, x_right, y_right, title_right, xlabel_right, ylabel_right, grid=True):
    """ 
    Plots two aligned figures. 
    
    Args: should be self explanatory...

    Returns: Two figures in 2D
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

#Testing model(good outline for later)


