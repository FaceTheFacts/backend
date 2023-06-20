# Function to clean donors data
from src.cron_jobs.utils.file import write_json


def clean_donations(donations, parties):
    clean_donations = []
    # TODO: implement get_last_id here for future inserts
    id = 1

    for donation in donations:
        clean_donation = {
            "id": id,
            "party_id": get_party_id(
                donation["party"], parties
            ),  ##TODO: implement DB version
            "amount": clean_amount(
                donation["amount"]
            ),  ##JSON imperial float (e.g. 15000.25)
            "donar": donation["donar"],  # TODO: fix this typo in the scraper
            "date": reformat_date(donation["date"]),  # YYY-MM-DD
            # TODO: add function for donor org ID
            # "donor_organization_id": donation["donor_organization_id"]
        }

        clean_donations.append(clean_donation)
        id += 1

    write_json("clean_donations.json", clean_donations)
    # return(clean_donations)


def clean_amount(original_amount):
    # Get rid of "Euro" added to end of amount
    updated_amount = original_amount.split(" ")[0]

    # Convert from EU to JSON format imperial separators (e.g. 10.000,75 -> 10000.75)
    updated_amount = updated_amount.replace(".", "")
    updated_amount = updated_amount.replace(",", ".")

    # Convert to float, automatically removes trailing zeros
    updated_amount = float(updated_amount)

    return updated_amount


# TODO: implement DB version, this is currently set up locally
def get_party_id(donation_party, parties):
    found = False

    for party in parties:
        if donation_party == party["name"]:
            party_id = party["id"]
            found = True
            break

    # TODO: figure out better way to handle imperfect party names (Bündnis90/DieGrünen is a problem)
    if not found:
        print("Party not found: " + donation_party)
        party_id = None

    return party_id


def reformat_date(original_date):
    split_date = original_date.split(".")
    new_date = split_date[2] + "-" + split_date[1] + "-" + split_date[0]

    return new_date
