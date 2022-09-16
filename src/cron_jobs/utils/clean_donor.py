# Function to clean donors data
from src.cron_jobs.utils.file import write_json


def clean_donor(data):
    clean_donors = []
    donor = {}
    donar2 = {}
    for donation in data:
        full_address = donation["donar"]
        # Ignore month (month entry has always amount = undefined)
        if donation["amount"]:
            if len(donation["donar"]) < 3:
                clean_donors.append(donation)
            continue
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
    print(clean_donors)
    print(len(clean_donors))
    write_json("clean_donors.json", clean_donors)
    # return(clean_donors)
