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
    return np.log(C_1) + np.log((1+par.r)*(par.V_1 + par.Y_L1 - par.T_1 - C_1) + par.Y_L2 - par.T_2)/(1+par.phi)

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
        #par.V_2 = (1+par.r)(par.V_1 + par.Y_L1 - par.T_1 - C_1)
        return -max_func(C_1=C_1, par=par)
    
    #Creating bounds for optimization
    lower = 0
    upper = par.V_1 + par.Y_L1 - par.T_1 + (par.Y_L2 - par.T_2)/(1 + par.r)

    #Running the optimization function
    res = optimize.minimize_scalar(objective, method ='bounded', bounds = (lower,upper), args = (par))

    # Get optimal C_1, using monotonicity to find optimal C_2, then using u_func to find utility in optimum
    C_1star = res.x
    C_2star = (1+par.r)*(par.V_1 + par.Y_L1 - par.T_1 - C_1star)
    U_star = np.log(C_1star) + (np.log(C_2star)/(1+par.phi))
    return C_1star, C_2star, U_star


#Testing model(good outline for later)

par = SimpleNamespace()
par.r = 0.02
par.V_1 = 5
par.Y_L1 = 2
par.Y_L2 = 2
par.T_1 = 0.5
par.T_2 = 0.5
par.phi = 0.02

c1, c2, u = max_optimize(par)

print(c1, c2, u)