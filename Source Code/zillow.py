def check_rent_affordability(region, annual_income, monthly_rent, verbose=True):
    monthly_income = annual_income / 12
    rent_to_income_ratio = monthly_rent / monthly_income
    if rent_to_income_ratio <= 0.30:
        status = "Affordable"
    elif rent_to_income_ratio <= 0.50:
        status = "Stretching Budget"
    else:
        status = "Not Affordable"
    return status
print(check_rent_affordability('Los Angeles', 50000, 1500))