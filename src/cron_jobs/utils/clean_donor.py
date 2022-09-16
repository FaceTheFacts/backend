#Function to clean donors data
def clean_donor(data):
    clean_donors = []
    for donation in data:
        full_address = donation["donar"]
        if donation["amount"]:
            if "Übersetzung: " in donation["donar"][1]:
                #case 22
                if len(donation.donar) == 3:
                    donor = {
                    "donor_name" : donation["donar"][1][13:69],
                    "donor_address" : donation["donar"][1][70:],
                    "donor_zip" : donation["donar"][2][:4],
                    "donor_city" : "Kopenhagen",
                    "donor_foreign" : True,
                    }
            #case 19
                else:
                    donor = {
                    "donor_name" : donation["donar"][1][13:],
                    "donor_address" : donation["donar"][2],
                    "donor_zip" : donation["donar"][3][:4],
                    "donor_city" : "Kopenhagen",
                    "donor_foreign" : True,
                    }
            #case 27
            elif "Übersetzung:" in donation["donar"][2]:
                if len(donation.donar) == 6:
                    donor = {
                    "donor_name" : donation["donar"][3],
                    "donor_address" : donation["donar"][4],
                    "donor_zip" :  donation["donar"][5][3:7],
                    "donor_city" : "Kopenhagen",
                    "donor_foreign" : True,
                    }
                #case 26
                else:
                    donor = {
                    "donor_name" : donation["donar"][3][:47],
                    "donor_address" : donation["donar"][3][48:],
                    "donor_zip" :  donation["donar"][4][3:7],
                    "donor_city" : "Kopenhagen",
                    "donor_foreign" : True,
                    }
        clean_donors.append(donor)
    print(clean_donors)
        #return(clean_donors)