from fuzzywuzzy import process

import src.db.models as models
from src.cron_jobs.utils.insert_and_update import insert_and_update
from src.cron_jobs.utils.fetch import fetch_last_id_from_model


def get_donor_org_id(donor, existing_donors):
    matching_donor = find_best_matching_donor(donor, existing_donors)

    if matching_donor:
        print("Found matching donor:", matching_donor["donor_name"])
        return matching_donor["id"]

    print("Created new donor:", donor["donor"][0])
    return None


def find_best_matching_donor(donor, existing_donors, min_score=80):
    search_name = get_search_name(donor)
    for existing_donor in existing_donors:
        print(existing_donor["donor_name"])

    best_match, best_match_score = process.extractOne(
        search_name,
        [existing_donor["donor_name"] for existing_donor in existing_donors],
    )

    if best_match_score >= min_score:
        return next(
            (
                existing_donor
                for existing_donor in existing_donors
                if existing_donor["donor_name"] == best_match
            ),
            None,
        )
    return None


def get_search_name(donor):
    for donor_info in donor["donor"]:
        if "Übersetzung:" in donor_info:
            return donor_info.replace("Übersetzung: ", "").strip()
    return donor["donor"][0]


def create_new_donor(donor):
    last_id = fetch_last_id_from_model(models.PartyDonationOrganization)
    new_id = last_id + 1

    new_donor = clean_donor(donor)
    new_donor["id"] = new_id

    insert_and_update(models.PartyDonationOrganization, [new_donor])
    print("Inserted new donor into db:", new_donor["donor_name"])

    return new_id


def clean_donor(donor):
    clean_donor = {}
    if len(donor["donor"]) < 3:
        if len(donor["donor"][0]) > 10:
            clean_donor = {
                "donor_name": donor["donor"][0][:78],
                "donor_address": donor["donor"][0][80:],
                "donor_zip": donor["donor"][1][:5],
                "donor_city": donor["donor"][1][6:],
                "donor_foreign": False,
            }
        else:
            clean_donor = {
                "donor_name": donor["donor"][0],
                "donor_address": "",
                "donor_zip": donor["donor"][1][:5],
                "donor_city": donor["donor"][1][6:],
                "donor_foreign": False,
            }
        return clean_donor

    if len(donor["donor"]) >= 3:
        if "Übersetzung:" in donor["donor"][1]:
            # case 22
            if len(donor["donor"]) == 3:
                clean_donor = {
                    "donor_name": donor["donor"][1][13:69],
                    "donor_address": donor["donor"][1][70:],
                    "donor_zip": donor["donor"][2][:4],
                    "donor_city": "Kopenhagen",
                    "donor_foreign": True,
                }
            elif len(donor["donor"]) == 5:
                clean_donor = {
                    "donor_name": donor["donor"][2],
                    "donor_address": donor["donor"][3],
                    "donor_zip": donor["donor"][4].split()[0],
                    "donor_city": "Kopenhagen",
                    "donor_foreign": True,
                }
            # case 19
            else:
                clean_donor = {
                    "donor_name": donor["donor"][1][13:],
                    "donor_address": donor["donor"][2],
                    "donor_zip": donor["donor"][3][:4],
                    "donor_city": "Kopenhagen",
                    "donor_foreign": True,
                }
            return clean_donor
        # case 27
        elif "Übersetzung:" in donor["donor"][2]:
            if len(donor["donor"]) == 6:
                clean_donor = {
                    "donor_name": donor["donor"][3],
                    "donor_address": donor["donor"][4],
                    "donor_zip": donor["donor"][5][3:7],
                    "donor_city": "Kopenhagen",
                    "donor_foreign": True,
                }
            # case 26
            else:
                clean_donor = {
                    "donor_name": donor["donor"][3][:46],
                    "donor_address": donor["donor"][3][47:],
                    "donor_zip": donor["donor"][4][3:7],
                    "donor_city": "Kopenhagen",
                    "donor_foreign": True,
                }
            return clean_donor

    if len(donor["donor"]) == 3:
        if "Übersetzung: " not in donor["donor"][1]:
            # Edge case: Netherlands. Hardcoded ZipCode due to trailing space
            if "NL " in donor["donor"][2]:
                clean_donor = {
                    "donor_name": donor["donor"][0],
                    "donor_address": donor["donor"][1],
                    "donor_zip": "6422",
                    "donor_city": donor["donor"][2][:7],
                    "donor_foreign": True,
                }
            # Edge Case: Switzerland
            elif "CH-7500" in donor["donor"][2]:
                clean_donor = {
                    "donor_name": donor["donor"][0],
                    "donor_address": donor["donor"][1],
                    "donor_zip": donor["donor"][2][:7],
                    "donor_city": donor["donor"][2][8:],
                    "donor_foreign": True,
                }
            # Edge Case: Switzerland
            elif "CH-8834" in donor["donor"][2]:
                clean_donor = {
                    "donor_name": donor["donor"][0],
                    "donor_address": donor["donor"][1],
                    "donor_zip": donor["donor"][2][:7],
                    "donor_city": donor["donor"][2][8:],
                    "donor_foreign": True,
                }
            # Edge Case: Thailand
            elif "Thailand" in donor["donor"][2]:
                clean_donor = {
                    "donor_name": donor["donor"][0],
                    "donor_address": donor["donor"][1],
                    "donor_zip": donor["donor"][2][8:13],
                    "donor_city": donor["donor"][2][:7],
                    "donor_foreign": True,
                }
            # Edge case: missing one digit in ZipCode in 2 cases. City name with w/ trailing spaces
            elif "Deutsche Vermögensberatung" in donor["donor"][0]:
                clean_donor = {
                    "donor_name": donor["donor"][0],
                    "donor_address": donor["donor"][1],
                    "donor_zip": "60329",
                    "donor_city": "Frankfurt am Main",
                    "donor_foreign": True,
                }
            else:
                clean_donor = {
                    "donor_name": donor["donor"][0],
                    "donor_address": donor["donor"][1],
                    "donor_zip": donor["donor"][2][:5],
                    "donor_city": donor["donor"][2][6:],
                    "donor_foreign": False,
                }
            return clean_donor

    if len(donor["donor"]) == 4:
        if "Übersetzung: " not in donor["donor"][1]:
            clean_donor = {
                "donor_name": donor["donor"][0],
                "donor_address": donor["donor"][2],
                "donor_zip": donor["donor"][3][:5],
                "donor_city": donor["donor"][3][6:],
                "donor_foreign": False,
            }
            return clean_donor
    if len(donor["donor"]) == 5:
        if "Übersetzung:" in donor["donor"][1]:
            clean_donor = {
                "donor_name": donor["donor"][2],
                "donor_address": donor["donor"][3],
                "donor_zip": donor["donor"][4].split()[0],
                "donor_city": " ".join(donor["donor"][4].split()[1:]),
                "donor_foreign": True,
            }
        return clean_donor
    if clean_donor:
        return clean_donor
    else:
        raise ValueError(f"Failed to clean donor: {donor}")
