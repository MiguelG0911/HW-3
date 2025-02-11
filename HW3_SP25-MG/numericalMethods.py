#region imports
import matrixOperations as mo  # this is the module from lecture 2 that has useful matrix manipulation functions
from math import sqrt, pi, exp, cos
#endregion

#region function definitions
#region probability calculations
"""
The following functions are designed to integrate the Gaussian/Normal Probability Density Function using the 
Simpson 1/3 rule.
Characteristics of the GNPDF (or GPDF) are:
1.  It is symmetric about the mean.
2.  The area beneath the GNPDF equals 1.0.
3.  Integrating between some left limit x to some right limit x represents the probability that the continuous random
    variable x lies between the limits.
4.  68% of the area is between +/-1*StDev of the mean, 95.5% between +/-2*StDev of the mean.
"""
def Probability(PDF, args, c, GT=True):
    """
    This is the function to calculate the probability that x is >c or <c depending
    on the GT boolean.
    Step 1:  unpack args into mu and stDev
    Step 2:  compute lhl and rhl for Simpson
    Step 3:  package new tuple args1=(mu, stDev, lhl, rhl) to be passed to Simpson
    Step 4:  call Simpson with GNPDF and args1
    Step 5:  return probability
    :param PDF: the probability density function to be integrated
    :param args: a tuple with (mean, standard deviation)
    :param c: value for which we ask the probability question
    :param GT: boolean deciding if we want probability x>c (True) or x<c (False)
    :return: probability value
    """
    mu, sig = args
    lhl = mu -5*sig
    rhl = c
    p = Simpson(PDF, (mu, sig, lhl,rhl))
    return 1-p if GT is True else p
def GPDF(args):
    """
    Here is where I will define the Gaussian probability density function.
    This requires knowing the population mean and standard deviation.
    To compute the GPDF at any value of x, I just need to compute as stated
    in the homework assignment.
    Step 1:  unpack the args tuple into variables called: x, mu, stDev
    Step 2:  compute GPDF value at x
    Step 3:  return value
    :param args: (x, mean, standard deviation)  tuple in that order
    :return: value of GPDF at the desired x
    """
    # Step 1: unpack args
    x, mu, sig = args
    # step 2: compute GPDF at x
    fx = (1 / (sig * sqrt(2 * pi))) * exp(-0.5 * ((x - mu) / sig) ** 2)
    # step 3: return value
    return fx
def Simpson(fn, args, N=100):
    """
    This executes the Simpson 1/3 rule for numerical integration (see page 832, Table 19.4).
    As I recall:
    1. divide the range from x=lhl to x=rhl into an even number of parts. Perhaps 20?
    2. compute fx at each x value between lhl and rhl
    3. sum the even and odd values of fx as prescribed
    4. return the area beneath the function fx
    :param fx: some function of x to integrate
    :param args: a tuple containing (mean, stDev, lhl, rhl)
    :return: the area beneath the function between lhl and rhl
    """
        if len(args) == 3:  # t-Distribution Case
        m, lower_limit, upper_limit = args
    elif len(args) == 4:  # Gaussian Case (Original)
        mu, sigma, lower_limit, upper_limit = args
    else:
        raise ValueError("Invalid number of arguments passed to Simpson function.")

    # Ensure even number of intervals
    if N % 2 == 1:
        N += 1

    h = (upper_limit - lower_limit) / N  # Step size
    x_values = [lower_limit + i * h for i in range(N + 1)]  # x values

    # Compute function values at x points
    if len(args) == 3:  # t-Distribution
        f_values = [fn((x, m)) for x in x_values]
    else:  # Gaussian
        f_values = [fn((x, mu, sigma)) for x in x_values]

    # Simpson's Rule Formula: Integral ≈ h/3 * [f(x0) + 4f(x1) + 2f(x2) + ... + f(xN)]
    integral = f_values[0] + f_values[-1]  # f(x0) + f(xN)
    integral += 4 * sum(f_values[i] for i in range(1, N, 2))  # Sum of f(x1), f(x3), ..., f(xN-1) (odd indices)
    integral += 2 * sum(f_values[i] for i in range(2, N - 1, 2))  # Sum of f(x2), f(x4), ..., f(xN-2) (even indices)

    return (h / 3) * integral

#endregion

#region other numerical methods
def Secant(fcn, x0, x1, maxiter=10, xtol=1e-5):
    """
    This funciton implements th Secant method to find the root of an equation.  You should write your equation in a form
    fcn = 0 such that when the correct value of x is selected, the fcn actually equals zero (or very close to it).
    :param fcn: the function for which we want to find the root
    :param x0: x value in neighborhood of root (or guess 1)
    :param x1: another x value in neighborhood of root (or guess x0+1)
    :param maxiter: exit if the number of iterations (new x values) equals this number
    :param xtol:  exit if the |xnewest - xprevious| < xtol
    :return: tuple with: (the final estimate of the root (most recent value of x), number of iterations)
    """
    x_diff = abs(xtol)+1
    iter=0
    f0=fcn(x0)
    f1=fcn(x1)
    while (iter<maxiter and abs(x_diff)>abs(xtol)):
        f1=fcn(x1)
        x_New = x1-f1*((x1-x0)/(f1-f0))
        f0=f1
        x_diff = x_New-x1
        x0=x1
        x1=x_New
        iter+=1
    return (x1,iter)
def GaussSeidel(Aaug, x, Niter = 15):
    """
    This should implement the Gauss-Seidel method (see page 860, Tabl 20.2) for solving a system of equations.
    :param Aaug: The augmented matrix from Ax=b -> [A|b]
    :param x:  An initial guess for the x vector. if A is nxn, x is nx1
    :param Niter:  Number of iterations to run the GS method
    :return: the solution vector x
    """
    # Step 1:  make the augmented matrix diagonal dominant
    # Step 2:  in a loop:
    # Step 2a:  solve first row for x[0] using old values for x[1], etc
    # Step 2b:  solve remaining rows for x[i] using new values above and old values below
    # Step 3:  return x after Niter
    Aaug = mo.MakeDiagDom(Aaug)
    n_Rows = len(Aaug)
    n_Cols = len(Aaug[0])-1

    for j in range(Niter):
        for i in range(n_Rows):
            rhs = Aaug[i][n_Cols]
            for k in range(n_Cols):
                rhs -= Aaug[i][k] * x[k] if not k==i else 0
            x[i] = rhs / Aaug[i][i]  # we can run into a problem if the diagonal has a zero
    return x
#endregion

def main():
    '''
    This is a function I created for testing the numerical methods locally.
    :return: None
    '''
    #region testing GPDF
    fx = GPDF((0,0,1))
    print("{:0.5f}".format(fx))  # Does this match the expected value?
    #edregion

    #region testing Simpson
    p=Simpson(GPDF,(0,1,-5,0)) # should return 0.5
    print("p={:0.5f}".format(p))  # Does this match the expected value?
    #endregion

    #region testing Probability
    p1 = Probability(GPDF, (0,1),0,True)
    print("p1={:0.5f}".format(p1))  # Does this match the expected value?
    #endregion
    p2 = 1-2*Probability(GPDF,(0,1),1)
    print("p2={:0.5f}".format(p2))  # Does this match the expected value?
    p3 = 1-2*Probability(GPDF,(0,1),2)
    print("p3={:0.5f}".format(p3))  # Does this match the expected value?
    p4 = 1-2*Probability(GPDF,(0,1),3)
    print("p4={:0.5f}".format(p4))  # Does this match the expected value?
#endregion

#region function calls
if __name__ == '__main__':
    main()
#endregion
