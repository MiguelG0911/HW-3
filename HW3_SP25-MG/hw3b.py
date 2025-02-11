#region imports
from math import gamma, pi
from numericalMethods import Simpson
#endregion

#region function definitions
def t_pdf(args):
    """
    Computes the probability density function (PDF) of the t-distribution.
    :param args: Tuple (x, df) where x is the t-score and df is the degrees of freedom
    :return: Probability density at x
    """
    x, df = args  # Unpack arguments
    numerator = gamma((df + 1) / 2)
    denominator = gamma(df / 2) * (df * pi) ** 0.5
    scaling_factor = (1 + (x ** 2) / df) ** (-(df + 1) / 2)
    return (numerator / denominator) * scaling_factor

def t_cdf(z, df):
    """
    Computes the cumulative probability P(T < z) using Simpson’s 1/3 Rule for numerical integration.
    Since the t-distribution is symmetric, we integrate from 0 to z and adjust accordingly.
    :param z: Upper limit of integration (t-score)
    :param df: Degrees of freedom
    :return: Cumulative probability P(T < z)
    """
    if z < 0:
        return 1 - t_cdf(-z, df)  # Use symmetry for negative z-values

    # Integrate the PDF from 0 to z using Simpson’s Rule
    prob = Simpson(t_pdf, (df, 0, z), N=1000)  # Pass extra argument structure
    return 0.5 + prob  # Add 0.5 since we integrated from 0 (symmetric property)

def main():
    """
    Computes probabilities from the t-distribution.
    The user inputs degrees of freedom (df) and a z-value.
    """
    Again = True
    yesOptions = ["y", "yes", "true"]

    while Again:
        response = input("Enter degrees of freedom (m=7, 11, or 15): ").strip()
        try:
            df = int(response)
            if df not in [7, 11, 15]:
                print("Invalid choice! Please enter 7, 11, or 15.")
                continue
        except ValueError:
            print("Invalid input! Please enter an integer.")
            continue

        response = input("Enter t-score (z value): ").strip()
        try:
            z1 = float(response)
        except ValueError:
            print("Invalid input! Please enter a numeric value.")
            continue

        response = input("Enter t-score (z value): ").strip()
        try:
            z2 = float(response)
        except ValueError:
            print("Invalid input! Please enter a numeric value.")
            continue

        response = input("Enter t-score (z value): ").strip()
        try:
            z3 = float(response)
        except ValueError:
            print("Invalid input! Please enter a numeric value.")
            continue

        probability = t_cdf(z1, df)
        print(f"P(T < {z1}) for {df} degrees of freedom = {probability:.5f}")

        probability = t_cdf(z2, df)
        print(f"P(T < {z2}) for {df} degrees of freedom = {probability:.5f}")

        probability = t_cdf(z3, df)
        print(f"P(T < {z3}) for {df} degrees of freedom = {probability:.5f}")


        response = input("Go again? (Y/N): ").strip().lower()
        Again = response in yesOptions

#endregion

if __name__ == "__main__":
    main()

