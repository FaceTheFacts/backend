def convert_income_level(income_level: str):
    income_dict = {
        "1": "1.000 € bis 3.500 €",
        "2": "3.500 € bis 7.000 €",
        "3": "7.000 € bis 15.000 €",
        "4": "15.000 € bis 30.000 €",
        "5": "30.000 € bis 50.000 €",
        "6": "50.000 € bis 75.000 €",
        "7": "75.000 € bis 100.000 €",
        "8": "100.000 € bis 150.000 €",
        "9": "150.000 € bis 250.000 €",
        "10": "ab 250.000 €",
    }
    return income_dict.get(income_level, None)
