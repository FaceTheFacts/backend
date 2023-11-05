# Function to clean donors data
import src.db.models as models
from src.cron_jobs.utils.fetch import fetch_last_id_from_model, load_entity_from_db
from fuzzywuzzy import process


def clean_donations(scraped_donations, parties, clean_donors):
    clean_donation_list = []
    last_id = fetch_last_id_from_model(models.PartyDonation)
    donations_from_db = load_entity_from_db(models.PartyDonation)
    exisisting_donations = [donation.__dict__ for donation in donations_from_db]

    for index, donation in enumerate(scraped_donations):
        if not donation["amount"]:
            continue
        cleaned_donor = clean_donors[index]

        # Check if the donation has a donor
        donor_org_id = cleaned_donor["id"] if cleaned_donor else None

        clean_donation = {
            "party_id": get_party_id(donation["party"], parties),
            "amount": clean_amount(donation["amount"]),
            "date": reformat_date(donation["date"]),
            "party_donation_organization_id": donor_org_id,
        }
        clean_donation_list.append(clean_donation)

    # Sort clean_donation list by date
    clean_donation_list = sorted(clean_donation_list, key=lambda k: k["date"])
    # Remove duplicates
    clean_donation_list = [
        donation
        for index, donation in enumerate(clean_donation_list)
        if not donation_exists(donation, exisisting_donations)
    ]
    # Add id to each donation
    for donation in clean_donation_list:
        last_id += 1
        donation["id"] = last_id

    return clean_donation_list


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
    if len(split_date) == 3 and not split_date[2]:
        year = "2022"
    else:
        year = split_date[2]
    new_date = year + "-" + split_date[1] + "-" + split_date[0]

    return new_date


def donation_exists(donation, existing_donations):
    for existing_donation in existing_donations:
        if (
            existing_donation["party_id"] == donation["party_id"]
            and str(existing_donation["date"]) == str(donation["date"])
            and existing_donation["party_donation_organization_id"]
            == donation["party_donation_organization_id"]
        ):
            return True
    return False
