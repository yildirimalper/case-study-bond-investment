# bond_math.py
# |--- calculate_bond_price()
# |--- calculate_macaulay_duration()
# |--- calculate_modified_duration()
# |--- calculate_bond_convexity()
# |--- calculate_dv01()

# ==============================================================================================================
# 1. calculate_bond_price()
# ==============================================================================================================

def calculate_bond_price(face_value, years_to_maturity, ytm_bid, ytm_ask, coupon_rate=None, buying=True, periods_per_year=2):
    """
    Calculate the present value (price) of a bond based on its characteristics.

    Parameters:
    - face_value (float): The face value of the bond.
    - years_to_maturity (float): The number of years until the bond matures.
    - ytm_bid (float): The Yield to Maturity (YTM) for selling the bond.
    - ytm_ask (float): The Yield to Maturity (YTM) for buying the bond.
    - coupon_rate (float, optional): The annual coupon rate. Default is None for zero coupon bonds.
    - buying (bool, optional):  If True, calculate bond price for buying using YTM Ask; 
                                If False, calculate for selling using YTM Bid. Default is True.
    - periods_per_year (int, optional): Number of compounding periods per year. Default is 2 for semi-annual compounding.

    Returns:
    - float: The calculated present value (price) of the bond.
    """

    total_periods = int(years_to_maturity * periods_per_year)
    
    # Handle bonds with less than 1 year to maturity
    if years_to_maturity < 1:
        total_periods = int(years_to_maturity * periods_per_year) + 1
    
    # Determine which yield-to-maturity to use based on buying or selling
    ytm = ytm_ask if buying else ytm_bid
    
    # For coupon-bearing bonds
    if coupon_rate is not None and coupon_rate != 0:
        coupon_payment = (face_value * coupon_rate / 100) / periods_per_year  # Adjust for compounding frequency
        
        # Calculate the discount factors for each period
        discount_factors = [(1 + (ytm / (100 * periods_per_year)))**(-i) for i in range(1, total_periods + 1)]
        
        # Calculate the present value of coupon payments and face value
        bond_price = sum([coupon_payment * discount_factors[i-1] for i in range(1, total_periods + 1)])
        bond_price += face_value * discount_factors[-1]

    # For zero-coupon bonds
    else:
        bond_price = face_value / (1 + (ytm / (100 * periods_per_year)))**total_periods  # Adjust for compounding frequency

    return round(bond_price, 3)

# ==============================================================================================================
# 2. calculate_macaulay_duration()
# ==============================================================================================================

def calculate_macaulay_duration(face_value, years_to_maturity, ytm_bid, ytm_ask, coupon_rate=None, buying=True, periods_per_year=2):
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
    - periods_per_year (int, optional): Number of compounding periods per year. Default is 2 for semi-annual compounding.

    Returns:
    - float: The calculated Macaulay duration of the bond.
    """

    # Determine which YTM to use based on buying or selling
    ytm = ytm_ask if buying else ytm_bid

    if coupon_rate is not None and coupon_rate != 0:
        # Coupon-bearing bond
        total_periods = int(years_to_maturity * periods_per_year)
        coupon_payment = face_value * (coupon_rate / 100) / periods_per_year  # Adjust for compounding frequency
        discount_factor = (1 + (ytm / (100 * periods_per_year)))

        numerator = sum([(i * coupon_payment) / (discount_factor**i) for i in range(1, total_periods + 1)])
        numerator += total_periods * face_value / (discount_factor**total_periods)

        present_value = sum([coupon_payment / (discount_factor**i) for i in range(1, total_periods + 1)])
        present_value += face_value / (discount_factor**total_periods)

        macaulay_duration = numerator / present_value / periods_per_year

    else:
        # Zero coupon bond
        total_periods = int(years_to_maturity * periods_per_year)
        macaulay_duration = years_to_maturity / ((1 + (ytm / (100 * periods_per_year)))**total_periods)  # Adjust for compounding frequency

    return round(macaulay_duration, 3)

# ==============================================================================================================
# 3. calculate_modified_duration()
# ==============================================================================================================

def calculate_modified_duration(face_value, years_to_maturity, ytm_bid, ytm_ask, coupon_rate=None, buying=True, periods_per_year=2):
    """
    Calculate the modified duration of a bond based on its characteristics.

    Parameters:
    - face_value (float): The face value of the bond.
    - years_to_maturity (float): The number of years until the bond matures.
    - ytm_bid (float): The Yield to Maturity (YTM) for buying the bond.
    - ytm_ask (float): The Yield to Maturity (YTM) for selling the bond.
    - coupon_rate (float, optional): The annual coupon rate. Default is None for zero coupon bonds.
    - buying (bool, optional):  If True, calculate bond modified duration for buying using YTM Ask; 
                                If False, calculate for selling using YTM Bid. Default is True.
    - periods_per_year (int, optional): Number of compounding periods per year. Default is 2 for semi-annual compounding.

    Returns:
    - float: The calculated modified duration of the bond.
    """

    # Calculate Macaulay Duration first
    macaulay_duration = calculate_macaulay_duration(face_value, years_to_maturity, ytm_bid, ytm_ask, coupon_rate, buying, periods_per_year)

    # Determine which YTM to use based on buying or selling
    ytm = ytm_ask if buying else ytm_bid

    # Calculate Modified Duration
    modified_duration = macaulay_duration / (1 + (ytm / (100 * periods_per_year)))

    return round(modified_duration, 3)

# ==============================================================================================================
# 4. calculate_bond_convexity()
# ==============================================================================================================

def calculate_bond_convexity(face_value, years_to_maturity, ytm_bid, ytm_ask, coupon_rate=None, buying=True, periods_per_year=2):
    """
    Calculate the convexity of a bond based on its characteristics.

    Parameters:
    - face_value (float): The face value of the bond.
    - years_to_maturity (float): The number of years until the bond matures.
    - ytm_bid (float): The Yield to Maturity (YTM) for buying the bond.
    - ytm_ask (float): The Yield to Maturity (YTM) for selling the bond.
    - coupon_rate (float, optional): The annual coupon rate. Default is None for zero coupon bonds.
    - buying (bool, optional):  If True, calculate bond convexity for buying using YTM Ask; 
                                If False, calculate for selling using YTM Bid. Default is True.
    - periods_per_year (int, optional): Number of compounding periods per year. Default is 2 for semi-annual compounding.

    Returns:
    - float: The calculated convexity of the bond.
    """

    total_periods = int(years_to_maturity * periods_per_year)
    
    # Handle bonds with less than 1 year to maturity
    if years_to_maturity < 1:
        total_periods = int(years_to_maturity * periods_per_year) + 1
    
    # Determine which YTM to use based on buying or selling
    ytm = ytm_ask if buying else ytm_bid
    
    if coupon_rate is not None and coupon_rate != 0:
        # Coupon-bearing bond
        coupon_payment = (face_value * coupon_rate / 100) / periods_per_year  # Adjust for compounding frequency

        convexity = sum([(coupon_payment * (i * (i + 1))) / (1 + (ytm / (100 * periods_per_year)))**i for i in range(1, total_periods + 1)])
        convexity += (total_periods * (total_periods + 1) * face_value) / (1 + (ytm / (100 * periods_per_year)))**total_periods
        convexity /= (1 + (ytm / (100 * periods_per_year)))**2
        convexity /= face_value
    else:
        # Zero coupon bond
        convexity = (total_periods * (total_periods + 1)) / ((1 + (ytm / (100 * periods_per_year)))**total_periods)

    return round(convexity, 2)

# ==============================================================================================================
# 5. calculate_dv01()
# ==============================================================================================================

def calculate_dv01(face_value, coupon_rate, years_to_maturity, ytm, basis_point_change=1, periods_per_year=2):
    """
    Calculate the DV01 (dollar value of 01) for a bond.

    Parameters:
    - face_value (float): The face value of the bond.
    - coupon_rate (float): The annual coupon rate.
    - years_to_maturity (float): The number of years until the bond matures.
    - ytm (float): The Yield to Maturity (YTM) for the bond.
    - basis_point_change (int, optional): The change in yield in basis points. Default is 1.
    - periods_per_year (int, optional): Number of compounding periods per year. Default is 2 for semi-annual compounding.

    Returns:
    - float: The calculated DV01 for the bond.
    """

    # Calculate the initial bond price
    initial_price = calculate_bond_price(face_value, years_to_maturity, ytm, ytm, coupon_rate=coupon_rate)

    # Calculate the bond price after a 1 basis point increase in yield
    new_ytm = ytm + (basis_point_change / 100)
    new_price = calculate_bond_price(face_value, years_to_maturity, ytm, new_ytm, coupon_rate=coupon_rate, periods_per_year=periods_per_year)

    # Calculate the change in bond price
    price_change = new_price - initial_price

    # Calculate DV01
    dv01 = price_change / basis_point_change

    return dv01