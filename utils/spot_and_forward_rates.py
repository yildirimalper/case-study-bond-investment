# spot_and_forward_rates.py
# |--- calculate_spot_rate()
# |--- create_spot_rate_curve()
# |--- calculate_forward_rate()
# |--- create_forward_rate_curve()

# ==============================================================================================================
# 1. calculate_spot_rate()
# ==============================================================================================================
def calculate_spot_rate(ytm, coupon_rate, time_to_maturity, face_value):
    """
    Calculate the spot rate for a given bond.

    Parameters:
    - ytm (float): Yield to Maturity.
    - coupon_rate (float): Annual coupon rate.
    - time_to_maturity (int): Time to maturity in years.
    - face_value (float): Face value of the bond.

    Returns:
    - float: Calculated spot rate.
    """
    C = face_value * (coupon_rate / 100)  # Annual coupon payment
    T = time_to_maturity

    # Solve for spot rate using the formula
    spot_rate = ((C / (1 - (1 / (1 + ytm) ** T))) + (face_value / (1 + ytm) ** T)) ** (1 / T) - 1

    return spot_rate

# ==============================================================================================================
# 2. create_spot_rate_curve()
# ==============================================================================================================
def create_spot_rate_curve(ytms, coupon_rates, maturities, face_value):
    """
    Create a spot rate curve based on a list of bonds with varying maturities.

    Parameters:
    - ytms (list): List of Yield to Maturity values.
    - coupon_rates (list): List of annual coupon rates.
    - maturities (list): List of time to maturities in years.
    - face_value (float): Face value of the bonds.

    Returns:
    - list: Spot rates corresponding to each maturity.
    """
    spot_rates= [calculate_spot_rate(ytm, coupon_rate, maturity, face_value)
                for ytm, coupon_rate, maturity in zip(ytms, coupon_rates, maturities)]
    return spot_rates

# ==============================================================================================================
# 3. calculate_forward_rate()
# ==============================================================================================================
def calculate_forward_rate(spot_rate_i, spot_rate_j, time_i, time_j):
    """
    Calculate the forward rate from time i to time j.

    Parameters:
    - spot_rate_i (float): Spot rate for time i.
    - spot_rate_j (float): Spot rate for time j.
    - time_i (int): Time i in years.
    - time_j (int): Time j in years.

    Returns:
    - float: Calculated forward rate.
    """
    forward_rate = ((1 + spot_rate_j) ** time_j) / ((1 + spot_rate_i) ** time_i) - 1
    return forward_rate

# ==============================================================================================================
# 4. create_forward_rate_curve()
# ==============================================================================================================
def create_forward_rate_curve(spot_rates, maturities):
    """
    Create a forward rate curve based on a list of spot rates and maturities.

    Parameters:
    - spot_rates (list): List of spot rates.
    - maturities (list): List of time intervals in years.

    Returns:
    - list: Forward rates corresponding to each time interval.
    """
    forward_rates = [calculate_forward_rate(spot_rates[i], spot_rates[j], maturities[i], maturities[j])
                    for i in range(len(spot_rates)) for j in range(i + 1, len(spot_rates))]
    return forward_rates
