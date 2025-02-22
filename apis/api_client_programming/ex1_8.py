"""
No.8 Convert Currency Rates

Objective: Fetch and calculate currency conversion rates.
Task: Use the requests library to access the ExchangeRate-API (https://api.exchangerate-api.com/v4/latest/USD) and convert USD to another specified currency.
Expected Output: The conversion rate and calculated conversion for a specified amount.
"""


import requests

def fetch_rates():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    print("response = " ,response)
    if response.status_code == 200:
        return response.json().get("rates", {})
    return {}

def convert(rates, target, amount):
    if target in rates:
        rate = rates[target]
        return rate, rate * amount
    return None, None

def main():
    rates = fetch_rates()
    target = input("Enter target currency code: ").upper().strip()
    amount = float(input("Enter amount in USD: "))
    rate, converted_amount = convert(rates, target, amount)
    if rate is not None:
        print(f"Conversion Rate: {rate}")
        print(f"Converted Amount: {converted_amount}")
    else:
        print("Invalid currency code.")

if __name__ == "__main__":
    main()