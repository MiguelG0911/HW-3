# region imports
from numericalMethods import GPDF, Probability, Secant


# endregion

# region function definitions
def FindCForProbability(target_P, mean, stDev, OneSided, GT):
    """
    Uses the Secant method to find the value of c that results in the given probability.
    :param target_P: The desired probability
    :param mean: Mean of the normal distribution
    :param stDev: Standard deviation
    :param OneSided: Boolean indicating one-sided or two-sided integration
    :param GT: Boolean indicating whether to compute P(x>c) or P(x<c)
    :return: Value of c that matches the target probability
    """

    def prob_diff(c):
        computed_P = Probability(GPDF, (mean, stDev), c, GT=GT)
        if not OneSided:
            computed_P = 1 - 2 * computed_P
        return computed_P - target_P

    c_guess1 = mean
    c_guess2 = mean + stDev
    c_solution, _ = Secant(prob_diff, c_guess1, c_guess2)
    return c_solution


def main():
    """
    Builds on hw2a.py to allow solving for either P given c or c given P using the Secant method.
    """
    Again = True
    mean = 0
    stDev = 1.0
    c = 0.5
    target_P = 0.5
    OneSided = True
    GT = False
    yesOptions = ["y", "yes", "true"]

    while Again:
        mode = input(
            "Are you specifying c and solving for P (enter 'P') or specifying P and solving for c (enter 'C')? ").strip().lower()

        response = input(f"Population mean? ({mean:0.3f})").strip().lower()
        mean = float(response) if response else mean

        response = input(f"Standard deviation? ({stDev:0.3f})").strip().lower()
        stDev = float(response) if response else stDev

        if mode == "p":
            response = input(f"c value? ({c:0.3f})").strip().lower()
            c = float(response) if response else c

            response = input(f"Probability greater than c? ({GT})").strip().lower()
            GT = response in yesOptions

            response = input(f"One-sided probability? ({OneSided})").strip().lower()
            OneSided = response in yesOptions

            prob = Probability(GPDF, (mean, stDev), c, GT=GT)
            if not OneSided:
                prob = 1 - 2 * prob
                print(f"P({mean - (c - mean)} < x < {mean + (c - mean)} | {mean:0.2f}, {stDev:0.2f}) = {prob:0.3f}")
            else:
                print(f"P(x {'>' if GT else '<'} {c:0.2f} | {mean:0.2f}, {stDev:0.2f}) = {prob:0.3f}")

        elif mode == "c":
            response = input(f"Target probability? ({target_P:0.3f})").strip().lower()
            target_P = float(response) if response else target_P

            response = input(f"Probability greater than c? ({GT})").strip().lower()
            GT = response in yesOptions

            response = input(f"One-sided probability? ({OneSided})").strip().lower()
            OneSided = response in yesOptions

            c_solution = FindCForProbability(target_P, mean, stDev, OneSided, GT)
            print(f"Value of c that gives probability {target_P:0.3f} is: {c_solution:0.3f}")

        response = input("Go again? (Y/N)").strip().lower()
        Again = response in yesOptions


# endregion

if __name__ == "__main__":
    main()