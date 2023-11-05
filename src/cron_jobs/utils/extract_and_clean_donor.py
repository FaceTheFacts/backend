from src.cron_jobs.utils.partydonations import clean_donations
from src.cron_jobs.utils.fetch import load_entity_from_db
import src.db.models as models
from src.cron_jobs.utils.partydonation_organisation import (
    clean_donor,
    create_new_donor,
    get_donor_org_id,
)
from src.cron_jobs.utils.file import read_json


def clean_donation_and_organisations(scraped_donations_path: str):
    scraped_donations = read_json(scraped_donations_path)
    scraped_donations = scraped_donations[::-1]
    existing_donation_organization = load_entity_from_db(
        models.PartyDonationOrganization
    )
    donation_organization = [org.__dict__ for org in existing_donation_organization]
    clean_donors = []

    for donation in scraped_donations:
        if donation["donor"]:
            try:
                cleaned_donor = clean_donor(donation)
                donor_id = get_donor_org_id(cleaned_donor, donation_organization)
                if not donor_id:
                    donor_id = create_new_donor(donation)
                    donation_organization.append(
                        {
                            "id": donor_id,
                            "donor_name": clean_donor(donation)["donor_name"],
                        }
                    )
                if cleaned_donor["donor_city"] == "København":
                    cleaned_donor["donor_city"] = "Kopenhagen"
                cleaned_donor["id"] = donor_id
                clean_donors.append(cleaned_donor)
            except Exception as e:
                print(f"Error processing donor: {donation['donor']}. Error: {e}")
        else:
            # Add None or a placeholder for donations without donors
            clean_donors.append(None)

    # Load party information
    parties = load_entity_from_db(models.Party)

    # Process the donations with cleaned donor information
    cleaned_donations = clean_donations(scraped_donations, parties, clean_donors)

    return cleaned_donations
