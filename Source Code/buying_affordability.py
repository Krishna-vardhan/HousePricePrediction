def check_buying_affordability(region, annual_income, home_price,
                                down_payment_percent=20,
                                interest_rate=0.06,
                                loan_term_years=30,
                                property_tax_rate=0.0125,
                                insurance_per_year=1500,
                                verbose=True):

    # Monthly income
    monthly_income = annual_income / 12

    # Down payment
    down_payment = home_price * (down_payment_percent / 100)

    # Loan amount
    loan_amount = home_price - down_payment

    # Monthly mortgage payment
    monthly_interest_rate = interest_rate / 12
    number_of_payments = loan_term_years * 12
    monthly_mortgage = loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments) / \
                       ((1 + monthly_interest_rate) ** number_of_payments - 1)

    # Property tax monthly
    monthly_property_tax = (home_price * property_tax_rate) / 12

    # Insurance monthly
    monthly_insurance = insurance_per_year / 12

    # Total monthly housing cost
    total_monthly_cost = monthly_mortgage + monthly_property_tax + monthly_insurance

    # Housing-to-Income ratio
    housing_to_income_ratio = total_monthly_cost / monthly_income

    # Affordability
    if housing_to_income_ratio <= 0.30:
        status = "Affordable"
    elif housing_to_income_ratio <= 0.40:
        status = "Stretching Budget"
    else:
        status = "Not Affordable"

        print(f"Region: {region}")
        print(f"Home Price: ${home_price:,.2f}")
        print(f"Down Payment: ${down_payment:,.2f} ({down_payment_percent}%)")
        print(f"Loan Amount: ${loan_amount:,.2f}")
        print(f"Monthly Mortgage Payment: ${monthly_mortgage:,.2f}")
        print(f"Monthly Property Tax: ${monthly_property_tax:,.2f}")
        print(f"Monthly Insurance: ${monthly_insurance:,.2f}")
        print(f"Total Monthly Housing Cost: ${total_monthly_cost:,.2f}")
        print(f"Monthly Income: ${monthly_income:,.2f}")
        print(f"Housing-to-Income Ratio: {housing_to_income_ratio:.2f} ({housing_to_income_ratio*100:.1f}%)")
        print(f"Affordability Status: {status}")

    return status,housing_to_income_ratio

# Example usage:
check_buying_affordability(region="Los Angeles", annual_income=100000, home_price=600000)
