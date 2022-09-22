# Function to clean donors data
from src.cron_jobs.utils.file import write_json
import src.cron_jobs.data.parties as parties

def clean_donations(donations):
    clean_donations = []
    id = 1

    for donation in donations:
        clean_donation = {
            "id": id,
            "party_id": get_party_id(donation["id"]),
            "amount": clean_amount(donation["amount"]),
            "date": donation["date"], #has to be converted to date during population
        }
            
        clean_donations.append(clean_donation)
        id += 1

    write_json("clean_donors.json", clean_donations)
    # return(clean_donors)

def clean_amount(original_amount):
    #50.001 Euro - "Euro" added to end of amount
    updated_amount = original_amount.split(" ")[0]

    #69.081,24 - Swap decimal and comma separators, remove now-redundant comma
    updated_amount = updated_amount.replace(".", ",")
    updated_amount = updated_amount.replace(",", "")

    #10000.00 - Convert to float, automatically removes trailing zeros
    updated_amount = float(updated_amount)
   
    return updated_amount

def get_party_id(donation, parties):
    found = False

    for party in parties:
        if donation["party"] == party["name"]:
            party_id = party["id"]
            found = True
            break

    if not found:
        print("Party not found: " + donation["party"])
        party_id = None

    return party_id
    