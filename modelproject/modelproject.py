from scipy import optimize
import numpy as np

# Utility function
def u_func(h, c, par):
    """
    Cobb-Douglas utility function for consumption and housing quality

    Args:

        h (float): housing quality and equal to housing price
        c (float): other consumption
        par: simplenamespace containing relevant parameters
            phi (float): C-D weights
            epsilon (float): public housing assement factor
            r (float): mortgage interest
            tau_g (float): base housing tax
            tau_p (float): progressive housing tax 
            p_bar (float): cutoff price
            m (float): cash-on-hand
    Returns:
    
        (float): utility
    """
    return c**(1-par.phi)*h**par.phi

# Optimize function
def u_optimize(par):
    """
    Optimises u_func with respect to housing quality and finds housing quality and consumption at the optimum

     Args:

        h (float): housing quality and equal to housing price
        par: simplenamespace containing relevant parameters
            phi (float): C-D weights
            epsilon (float): public housing assement factor
            r (float): mortgage interest
            tau_g (float): base housing tax
            tau_p (float): progressive housing tax 
            p_bar (float): cutoff price
            m (float): cash-on-hand

    Local variables:

        p_thilde (float): public housing assement price
        tax (float): interest rates and tax paid as a function of housing quality
        c (float): other consumption
    Returns:
    
        h_star (float): optimal housing quality
        c_star (float): optimal consumption
        u_star (float): utility in optimum
    """
    def objective(h, par):
        # Use monotonicity to find c as a function of h
        p_thilde = h * par.epsilon
        tax = par.r * h + par.tau_g * p_thilde + par.tau_p * max(p_thilde-par.p_bar, 0)
        c = par.m - tax
        return -u_func(h, c, par)
    
    res = optimize.minimize_scalar(objective, method ='brent', args = (par))

    # Get optimal h, using monotonicity to find optimal c, then using u_func to find utility in optimum
    h_star = res.x
    p_thilde = h_star * par.epsilon
    tax = par.r * h_star + par.tau_g * p_thilde + par.tau_p * max(p_thilde-par.p_bar, 0)
    c_star = par.m - tax
    u_star = u_func(h_star, c_star, par)
    return h_star, c_star, u_star