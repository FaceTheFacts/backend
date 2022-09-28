# Function to clean donors data
from src.cron_jobs.utils.file import write_json


def clean_donor(data):
    clean_donors = []
    donor = {}
    donor2 = {}
    donor3 = {}
    donor4 = {}
    for donation in data:
        full_address = donation["donar"]
        # Ignore month (month entry has always amount = undefined)
        if donation["amount"]:
            if len(donation["donar"]) < 3:
                if len(donation["donar"][0]) > 10:
                    donor2 = {
                        "donor_name": donation["donar"][0][:78],
                        "donor_address": donation["donar"][0][80:],
                        "donor_zip": donation["donar"][1][:5],
                        "donor_city": donation["donar"][1][6:],
                        "donor_foreign": False,
                    }
                else:
                    donor2 = {
                        "donor_name": donation["donar"][0],
                        "donor_address": "",
                        "donor_zip": donation["donar"][1][:5],
                        "donor_city": donation["donar"][1][6:],
                        "donor_foreign": False,
                    }
                clean_donors.append(donor2)
            # continue

            if len(donation["donar"]) >= 3:
                # print(donation)
                if "Übersetzung: " in donation["donar"][1]:
                    # case 22
                    if len(donation["donar"]) == 3:
                        donor = {
                            "donor_name": donation["donar"][1][13:69],
                            "donor_address": donation["donar"][1][70:],
                            "donor_zip": donation["donar"][2][:4],
                            "donor_city": "Kopenhagen",
                            "donor_foreign": True,
                        }
                    # case 19
                    else:
                        donor = {
                            "donor_name": donation["donar"][1][13:],
                            "donor_address": donation["donar"][2],
                            "donor_zip": donation["donar"][3][:4],
                            "donor_city": "Kopenhagen",
                            "donor_foreign": True,
                        }
                    clean_donors.append(donor)
                # case 27
                elif "Übersetzung:" in donation["donar"][2]:
                    if len(donation["donar"]) == 6:
                        donor = {
                            "donor_name": donation["donar"][3],
                            "donor_address": donation["donar"][4],
                            "donor_zip": donation["donar"][5][3:7],
                            "donor_city": "Kopenhagen",
                            "donor_foreign": True,
                        }
                    # case 26
                    else:
                        donor = {
                            "donor_name": donation["donar"][3][:46],
                            "donor_address": donation["donar"][3][47:],
                            "donor_zip": donation["donar"][4][3:7],
                            "donor_city": "Kopenhagen",
                            "donor_foreign": True,
                        }
                    clean_donors.append(donor)

            if len(donation["donar"]) == 3:
                # print(donation)
                if "Übersetzung: " not in donation["donar"][1]:
                    # Edge case: Netherlands. Hardcoded ZipCode due to trailing space
                    if "NL " in donation["donar"][2]:
                        donor3 = {
                            "donor_name": donation["donar"][0],
                            "donor_address": donation["donar"][1],
                            # "donor_zip": donation["donar"][2][6:9],
                            "donor_zip": "6422",
                            "donor_city": donation["donar"][2][:7],
                            "donor_foreign": True,
                        }
                    # Edge Case: Switzerland
                    elif "CH-7500" in donation["donar"][2]:
                        donor3 = {
                            "donor_name": donation["donar"][0],
                            "donor_address": donation["donar"][1],
                            "donor_zip": donation["donar"][2][:7],
                            "donor_city": donation["donar"][2][8:],
                            "donor_foreign": True,
                        }
                    # Edge Case: Switzerland
                    elif "CH-8834" in donation["donar"][2]:
                        donor3 = {
                            "donor_name": donation["donar"][0],
                            "donor_address": donation["donar"][1],
                            "donor_zip": donation["donar"][2][:7],
                            "donor_city": donation["donar"][2][8:],
                            "donor_foreign": True,
                        }
                    # Edge Case: Thailand
                    elif "Thailand" in donation["donar"][2]:
                        donor3 = {
                            "donor_name": donation["donar"][0],
                            "donor_address": donation["donar"][1],
                            "donor_zip": donation["donar"][2][8:13],
                            "donor_city": donation["donar"][2][:7],
                            "donor_foreign": True,
                        }
                    # Edge case: missing one digit in ZipCode in 2 cases. City name with w/ trailing spaces
                    elif "Deutsche Vermögensberatung" in donation["donar"][0]:
                        donor3 = {
                            "donor_name": donation["donar"][0],
                            "donor_address": donation["donar"][1],
                            "donor_zip": "60329",
                            "donor_city": "Frankfurt am Main",
                            "donor_foreign": True,
                        }
                    else:
                        donor3 = {
                            "donor_name": donation["donar"][0],
                            "donor_address": donation["donar"][1],
                            "donor_zip": donation["donar"][2][:5],
                            "donor_city": donation["donar"][2][6:],
                            "donor_foreign": False,
                        }
                    clean_donors.append(donor3)

            if len(donation["donar"]) == 4:
                # print(donation)
                if "Übersetzung: " not in donation["donar"][1]:
                    donor4 = {
                        "donor_name": donation["donar"][0],
                        "donor_address": donation["donar"][2],
                        "donor_zip": donation["donar"][3][:5],
                        "donor_city": donation["donar"][3][6:],
                        "donor_foreign": False,
                    }
                clean_donors.append(donor4)

    # print(clean_donors)
    print(len(clean_donors))
    write_json("clean_donors.json", clean_donors)
    # return(clean_donors)
