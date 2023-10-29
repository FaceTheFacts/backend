from src.cron_jobs.utils.partydonations import clean_donations
from src.cron_jobs.utils.fetch import load_entity_from_db
import src.db.models as models
from src.cron_jobs.utils.partydonation_organisation import (
    clean_donor,
    create_new_donor,
    get_donor_org_id,
)
from src.cron_jobs.utils.file import read_json

scraped_donations = read_json("src/cron_jobs/data/partydonation.json")
scraped_donations = scraped_donations[::-1]
donation_organization = load_entity_from_db(models.PartyDonationOrganization)
existing_donations = load_entity_from_db(models.PartyDonation)
donation_organization = [org.__dict__ for org in donation_organization]
clean_donors = []
for donation in scraped_donations:
    if donation["donor"] != []:
        try:
            cleaned_donor = clean_donor(donation)
            donor_id = get_donor_org_id(donation, donation_organization)
            if not donor_id:
                donor_id = create_new_donor(donation)
                donation_organization.append(
                    {"id": donor_id, "donor_name": clean_donor(donation)["donor_name"]}
                )
            cleaned_donor["id"] = donor_id
            clean_donors.append(cleaned_donor)
        except:
            print(donation["donor"])

parties = load_entity_from_db(models.Party)
cleaned_donations = clean_donations(scraped_donations, parties, donation_organization)
