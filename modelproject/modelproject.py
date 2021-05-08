from scipy import optimize
import numpy as np
from types import SimpleNamespace
# Utility function
def max_func(c_1, par):
    """
    Intertemporal consumer utility function in two periods

    Args:

       
    Returns:
    
        (float): Optimal consumption in period 1
    """
    return np.log(c_1) + np.log((1+par.r)(par.V_1 + par.Y_L1 - par.T1- par.C_1) + par.Y_L2 - par.T_2)/(1+par.phi)

# Optimize function
def max_optimize(par):
    """
    Optimises max_func 

     Args:

        

    Local variables:

        p_thilde (float): public housing assement price
        tax (float): interest rates and tax paid as a function of housing quality
        c (float): other consumption
    Returns:
    
        h_star (float): optimal housing quality
        c_star (float): optimal consumption
        u_star (float): utility in optimum
    """
    def objective(c_1, par):
        # Use monotonicity to find c as a function of h
        par.V_2 = (1+par.r)(par.V_1 + par.Y_L1 - par.T1- par.C_1)
        return -max_func(c_1, par)
    
    res = optimize.minimize_scalar(objective, method ='brent', args = (par))

    # Get optimal c_1, using monotonicity to find optimal c, then using u_func to find utility in optimum
    c_1star = res.x
    c_2star = (1+par.r)(par.V_1 + par.Y_L1 - par.T1- c_1star)
    u_star = np.log(c_1star) + (np.log(c_2star)/(1+par.phi))
    return c_1star, u_star

