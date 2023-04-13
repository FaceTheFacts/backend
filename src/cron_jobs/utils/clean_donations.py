# Function to clean donors data
import src.db.models as models
from src.cron_jobs.utils.fetch import fetch_last_id_from_model
from src.cron_jobs.utils.file import write_json
from fuzzywuzzy import fuzz, process


def clean_donations(donations, parties):
    clean_donations = []
    id = fetch_last_id_from_model(models.PartyDonation)

    for donation in donations:
        if not donation["amount"]:
            continue
        clean_donation = {
            "id": id,
            "party_id": get_party_id(donation["party"], parties),
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
    return clean_donations


def clean_amount(original_amount):
    # Get rid of "Euro" added to end of amount
    updated_amount = original_amount.split(" ")[0]

    # Convert from EU to JSON format imperial separators (e.g. 10.000,75 -> 10000.75)
    updated_amount = updated_amount.replace(".", "")
    updated_amount = updated_amount.replace(",", ".")

    # Convert to float, automatically removes trailing zeros
    updated_amount = float(updated_amount)

    return updated_amount


def get_party_id(donation_party, parties):
    # Map of common variations or abbreviations to standard party names
    party_name_mapping = {
        "Volt Deutsch-land": "Volt",
        "Bündnis 90 / Die Grünen": "Bündnis 90/Die Grünen",
        # Add more mappings as needed
    }

    # If the donation_party is in the mapping, use the mapped name
    if donation_party in party_name_mapping:
        donation_party = party_name_mapping[donation_party]

    best_match, best_match_score = process.extractOne(
        donation_party, [party.label for party in parties]
    )

    min_score = 80
    if best_match_score >= min_score:
        for party in parties:
            if party.label == best_match:
                return party.id
    else:
        print(f"Party not found: {donation_party}")

    return None


def reformat_date(original_date):
    split_date = original_date.split(".")
    new_date = split_date[2] + "-" + split_date[1] + "-" + split_date[0]

    return new_date
