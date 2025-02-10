#region imports
from scipy.stats import t
#endregion

#region function definitions
def compute_t_distribution_probability(df, z):
    """
    Computes the probability using the t-distribution.
    :param df: Degrees of freedom
    :param z: t-score
    :return: Probability P(T < z)
    """
    return t.cdf(z, df)

def main():
    """
    This program calculates probabilities from the t-distribution and compares with Table A9.
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


        response = input("Enter t-score (z1 value): ").strip()
        try:
            z1 = float(response)
        except ValueError:
            print("Invalid input! Please enter a numeric value.")
            continue

        response = input("Enter t-score (z2 value): ").strip()
        try:
            z2 = float(response)
        except ValueError:
            print("Invalid input! Please enter a numeric value.")
            continue

        response = input("Enter t-score (z3 value): ").strip()
        try:
            z3 = float(response)
        except ValueError:
            print("Invalid input! Please enter a numeric value.")
            continue

        probability = compute_t_distribution_probability(df, z1)
        print(f"P(T < {z1}) for {df} degrees of freedom = {probability:.5f}")

        probability = compute_t_distribution_probability(df, z2)
        print(f"P(T < {z2}) for {df} degrees of freedom = {probability:.5f}")

        probability = compute_t_distribution_probability(df, z3)
        print(f"P(T < {z3}) for {df} degrees of freedom = {probability:.5f}")

        response = input("Go again? (Y/N): ").strip().lower()
        Again = response in yesOptions

#endregion

if __name__ == "__main__":
    main()
