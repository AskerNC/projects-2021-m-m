from scipy import optimize
import numpy as np
from types import SimpleNamespace
# Utility function
def max_func(C_1, par):
    """
    Intertemporal consumer utility function in two periods

    Args:

       
    Returns:
    
        (float): Optimal consumption in period 1
    """
    return np.log(C_1) + np.log((1+par.r)(par.V_1 + par.Y_L1 - par.T1 - C_1) + par.Y_L2 - par.T_2)/(1+par.phi)

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
    def objective(C_1, par):
        # Use monotonicity to find c as a function of h
        par.V_2 = (1+par.r)(par.V_1 + par.Y_L1 - par.T1 - C_1)
        return -max_func(C_1, par)
    
    res = optimize.minimize_scalar(objective, method ='brent', args = (par))

    # Get optimal c_1, using monotonicity to find optimal c, then using u_func to find utility in optimum
    C_1star = res.x
    C_2star = (1+par.r)(par.V_1 + par.Y_L1 - par.T1 - C_1star)
    U_star = np.log(C_1star) + (np.log(C_2star)/(1+par.phi))
    return C_1star, C_2star, U_star

