import csv

from src.cron_jobs.utils.file import write_json

def create_zip_code_file() -> None:
    ### Open CSV file, which got downloaded from the website of the federal returning officer (deutsch: Bundeswahlleiter).
    ### The file to download is called "Wahlkreise und zugeordnete Gemeinden" https://www.bundeswahlleiter.de/bundestagswahlen/2021/wahlkreiseinteilung/downloads.html
    ### These zip codes are specific to the general election in Germany and might change for the next election.
    with open("src/cron_jobs/data/zip-codes.csv", newline="") as csvfile:
        zip_codes_file = csv.reader(csvfile, delimiter=";")
        line_count = 0
        zip_code_list = []
        # Structure of csv file found in this example in line 7
        csv_columns = 7
        for row in zip_codes_file:
            if line_count < csv_columns:
                line_count += 1
            elif line_count == csv_columns:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                #For connecting the data in the csv file to the consituency data in cons.json we need the following information:
                # 1) Wahlkreis-Nr (constituency number)
                # 2) Wahlkreis-Bez (constituency name)
                # 3) Gemeindename (municipality)
                # 4) PLZ-GemVerwaltung (zip code)

                #print(f'\t{row[0]} | {row[1]} | {row[11]} | {row[15]}')
                if zip_code_list == []:
                    zip_code = {"constituency_number": row[0],
                                        "constituency_name": row[1],
                                        "zip_codes": [row[15]]}
                    zip_code_list.append(zip_code)
                else:
                    for zip_code_item in zip_code_list:
                        constituency_numbers = []
                        constituency_numbers.append(zip_code_item["constituency_number"])
                        if zip_code_item["constituency_number"] == row[0]:
                            if row[15] not in zip_code_item["zip_codes"] and row[15] != "00000":
                                zip_code_item["zip_codes"].append(row[15])
                    if row[0] not in constituency_numbers:
                        zip_code = {"constituency_number": row[0],
                                    "constituency_name": row[1],
                                    "zip_codes": [row[15]]}
                        zip_code_list.append(zip_code)
    write_json("src/cron_jobs/data/zipcodes.json", zip_code_list)    