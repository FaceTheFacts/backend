from fuzzywuzzy import fuzz, process

import src.db.models as models
from src.cron_jobs.utils.file import write_json
from src.cron_jobs.utils.fetch import fetch_last_id_from_model


def get_donor_org_id(donor, existing_donors):
    matching_donor = find_best_matching_donor(donor, existing_donors)

    if matching_donor:
        donor_id = matching_donor.id
        print("Found matching donor: " + matching_donor.donor_name)
    else:
        donor_id = create_new_donor(donor)
        print("Created new donor: " + donor["donor"][0])
    return donor_id


def find_best_matching_donor(donor, existing_donors, min_score=80):
    translated_donor_name = None
    for donor_info in donor["donor"]:
        if "Übersetzung:" in donor_info:
            translated_donor_name = donor_info.replace("Übersetzung: ", "").strip()
            break

    if translated_donor_name:
        search_name = translated_donor_name
    else:
        search_name = donor["donor"][0]

    best_match, best_match_score = process.extractOne(
        search_name,
        [existing_donor.donor_name for existing_donor in existing_donors],
    )

    if best_match_score >= min_score:
        for existing_donor in existing_donors:
            if existing_donor.donor_name == best_match:
                return existing_donor

    return None


def create_new_donor(donor):
    id = fetch_last_id_from_model(models.PartyDonationOrganization)
    new_donor = {}
    new_donor = clean_donor(donor)
    new_donor["id"] = id + 1
    write_json(f"new_donor_{id+1}.json", new_donor)


def clean_donor(donor):
    print(donor)
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
        if "Übersetzung: " in donor["donor"][1]:
            # case 22
            if len(donor["donor"]) == 3:
                clean_donor = {
                    "donor_name": donor["donor"][1][13:69],
                    "donor_address": donor["donor"][1][70:],
                    "donor_zip": donor["donor"][2][:4],
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
    if clean_donor:
        return clean_donor
    else:
        return None
