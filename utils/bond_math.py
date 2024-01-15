# bond_math.py
# |--- calculate_bond_price()
# |--- calculate_macaulay_duration()
# |--- calculate_modified_duration()
# |--- calculate_bond_convexity()
# |--- calculate_dv01()

# ==============================================================================================================
# 1. calculate_bond_price()
# ==============================================================================================================

def calculate_bond_price(face_value, years_to_maturity, ytm_bid, ytm_ask, coupon_rate=None, buying=True):
    """
    Calculate the present value of a bond based on its characteristics.

    Parameters:
    - face_value (float): The face value of the bond.
    - years_to_maturity (int): The number of years until the bond matures.
    - ytm_bid (float): The Yield to Maturity (YTM) for buying the bond.
    - ytm_ask (float): The Yield to Maturity (YTM) for selling the bond.
    - coupon_rate (float, optional): The annual coupon rate. Default is None for zero coupon bonds.
    - buying (bool, optional):  If True, calculate bond price for buying using YTM Ask; 
                                If False, calculate for selling using YTM Bid. Default is True.

    Returns:
    - float: The calculated present value (price) of the bond.
    """

    total_periods = years_to_maturity
    
    # determine which yield-to-maturity to use based on buying or selling
    ytm = ytm_ask if buying else ytm_bid
    
    # for coupon-bearing bonds
    if coupon_rate is not None and coupon_rate != 0:
        
        coupon_payment = face_value * (coupon_rate / 100)                                 # convert coupon rate to decimal
        discount_factor = [(1 + (ytm / 100))**(-i) for i in range(1, total_periods + 1)]  # convert YTM to decimal

        bond_price = sum([coupon_payment / (1 + (ytm / 100))**i for i in range(1, total_periods + 1)])
        bond_price += face_value / (1 + (ytm / 100))**total_periods

    # for zero-coupon bond
    else:
        bond_price = face_value / (1 + (ytm / 100))**total_periods

    return round(bond_price, 3)

# ==============================================================================================================
# 2. calculate_macaulay_duration()
# ==============================================================================================================
def calculate_macaulay_duration(face_value, years_to_maturity, ytm_bid, ytm_ask, coupon_rate=None, buying=True):
    """
    Calculate the Macaulay duration of a bond based on its characteristics.

    Parameters:
    - face_value (float): The face value of the bond.
    - years_to_maturity (int): The number of years until the bond matures.
    - ytm_bid (float): The Yield to Maturity (YTM) for buying the bond.
    - ytm_ask (float): The Yield to Maturity (YTM) for selling the bond.
    - coupon_rate (float, optional): The annual coupon rate. Default is None for zero coupon bonds.
    - buying (bool, optional):  If True, calculate bond duration for buying using YTM Ask; 
                                if False, calculate for selling using YTM Bid. Default is True.

    Returns:
    - float: The calculated Macaulay duration of the bond.
    """

    total_periods = years_to_maturity
    
    # Determine which YTM to use based on buying or selling
    ytm = ytm_ask if buying else ytm_bid
    
    if coupon_rate is not None and coupon_rate != 0:
        # Coupon-bearing bond
        coupon_payment = face_value * (coupon_rate / 100)  # Convert coupon rate to decimal
        discount_factor = [(1 + (ytm / 100))**(-i) for i in range(1, total_periods + 1)]  # Convert YTM to decimal

        present_value = sum([coupon_payment / (1 + (ytm / 100))**i for i in range(1, total_periods + 1)])
        present_value += face_value / (1 + (ytm / 100))**total_periods

        macaulay_duration = sum([i * coupon_payment / (1 + (ytm / 100))**i for i in range(1, total_periods + 1)])
        macaulay_duration += total_periods * face_value / (1 + (ytm / 100))**total_periods
        macaulay_duration /= present_value

    else:
        # Zero coupon bond
        macaulay_duration = years_to_maturity / ((1 + (ytm / 100))**total_periods)

    return round(macaulay_duration, 2)

# ==============================================================================================================
# 3. calculate_bond_convexity()
# ==============================================================================================================

def calculate_modified_duration(face_value, years_to_maturity, ytm_bid, ytm_ask, coupon_rate=None, buying=True):
    """
    Calculate the modified duration of a bond based on its characteristics.

    Parameters:
    - face_value (float): The face value of the bond.
    - years_to_maturity (int): The number of years until the bond matures.
    - ytm_bid (float): The Yield to Maturity (YTM) for buying the bond.
    - ytm_ask (float): The Yield to Maturity (YTM) for selling the bond.
    - coupon_rate (float, optional): The annual coupon rate. Default is None for zero coupon bonds.
    - buying (bool, optional):  If True, calculate bond modified duration for buying using YTM Ask; 
                                if False, calculate for selling using YTM Bid. Default is True.

    Returns:
    - float: The calculated modified duration of the bond.
    """

    # Calculate Macaulay Duration first
    macaulay_duration = calculate_macaulay_duration(face_value, years_to_maturity, ytm_bid, ytm_ask, coupon_rate, buying)

    # Determine which YTM to use based on buying or selling
    ytm = ytm_ask if buying else ytm_bid

    # Calculate Modified Duration
    modified_duration = macaulay_duration / (1 + (ytm / 100))

    return round(modified_duration, 2)

# ==============================================================================================================
# 4. calculate_bond_convexity()
# ==============================================================================================================

def calculate_bond_convexity(face_value, years_to_maturity, ytm_bid, ytm_ask, coupon_rate=None, buying=True):
    """
    Calculate the convexity of a bond based on its characteristics.

    Parameters:
    - face_value (float): The face value of the bond.
    - years_to_maturity (int): The number of years until the bond matures.
    - ytm_bid (float): The Yield to Maturity (YTM) for buying the bond.
    - ytm_ask (float): The Yield to Maturity (YTM) for selling the bond.
    - coupon_rate (float, optional): The annual coupon rate. Default is None for zero coupon bonds.
    - buying (bool, optional):  If True, calculate bond convexity for buying using YTM Ask; 
                                if False, calculate for selling using YTM Bid. Default is True.

    Returns:
    - float: The calculated convexity of the bond.
    """

    total_periods = years_to_maturity
    
    # Determine which YTM to use based on buying or selling
    ytm = ytm_ask if buying else ytm_bid
    
    if coupon_rate is not None and coupon_rate != 0:
        # Coupon-bearing bond
        coupon_payment = face_value * (coupon_rate / 100)  # Convert coupon rate to decimal

        convexity = sum([(coupon_payment / (1 + (ytm / 100))**i) * (i * (i + 1)) for i in range(1, total_periods + 1)])
        convexity += total_periods * (total_periods + 1) * face_value / (1 + (ytm / 100))**total_periods
        convexity /= (1 + (ytm / 100))**2
        convexity /= face_value
    else:
        # Zero coupon bond
        convexity = total_periods * (total_periods + 1) / ((1 + (ytm / 100))**total_periods)

    return round(convexity, 2)

# ==============================================================================================================
# 5. calculate_dv01()
# ==============================================================================================================

def calculate_dv01(face_value, coupon_rate, years_to_maturity, ytm, basis_point_change=1):
    """
    Calculate the DV01 (dollar value of 01) for a bond.

    Parameters:
    - face_value (float): The face value of the bond.
    - coupon_rate (float): The annual coupon rate.
    - years_to_maturity (int): The number of years until the bond matures.
    - ytm (float): The Yield to Maturity (YTM) for the bond.
    - basis_point_change (int, optional): The change in yield in basis points. Default is 1.

    Returns:
    - float: The calculated DV01 for the bond.
    """

    # Calculate the initial bond price
    initial_price = calculate_bond_price(face_value, coupon_rate, years_to_maturity, ytm)

    # Calculate the bond price after a 1 basis point increase in yield
    new_ytm = ytm + (basis_point_change / 100)
    new_price = calculate_bond_price(face_value, coupon_rate, years_to_maturity, new_ytm)

    # Calculate the change in bond price
    price_change = new_price - initial_price

    # Calculate DV01
    dv01 = price_change / basis_point_change

    return dv01
