import os
import shutil
#This script automatically sets the primary culture of all countries to the culture of their capital in the province files
#Written by ishky on the MU team
provinces_base_path = "history/provinces/"
countries_base_path = "history/countries/"

#
# Look up culture/religion for all provinces.  Some will end up being
# capital provinces.
#
province_id_to_culture = {}
province_id_to_religion = {}
for province_filename in os.listdir(provinces_base_path):
    province_id = province_filename.split(" ")[0]
    with open(provinces_base_path + province_filename) as province_file:
        for line in province_file:
            if line.startswith("culture"):
                culture = (line.split("=")[1]).strip()
                province_id_to_culture[province_id] = culture
            elif line.startswith("religion"):
                religion = (line.split("=")[1]).strip()
                province_id_to_religion[province_id] = religion

#
# For every country set primary culture and state religion to match
# how it is set for the capital province.
#
culture_placeholder = "CULTURE_PLACEHOLDER"
religion_placeholder = "RELIGION_PLACEHOLDER"
for country_filename in os.listdir(countries_base_path):
    capital_province_id = None
    lines = []
    with open(countries_base_path + country_filename) as country_file:
        for line in country_file:
            if line.startswith("primary_culture"):
                lines.append(culture_placeholder)
            elif line.startswith("religion"):
                lines.append(religion_placeholder)
            elif line.startswith("capital"):
                capital_province_id = (line.split("=")[1]).strip()
                lines.append(line)
            else:
                lines.append(line)

    if not capital_province_id:
        print("No capital found for " + country_filename)
        continue

    if capital_province_id in province_id_to_culture:
        primary_culture = province_id_to_culture[capital_province_id]
    else:
        print("No primary culture found for " + country_filename)
        continue

    if capital_province_id in province_id_to_religion:
        state_religion = province_id_to_religion[capital_province_id]
    else:
        print("No state religion found for " + country_filename)
        continue

    tmp_country_filename = country_filename + ".tmp"
    with open(countries_base_path + tmp_country_filename, "w") as tmp_country_file:
        for line in lines:
            if line == culture_placeholder:
                tmp_country_file.write("primary_culture = " + primary_culture + "\n")
            elif line == religion_placeholder:
                tmp_country_file.write("religion = " + state_religion + "\n")
            else:
                tmp_country_file.write(line)

    shutil.move(countries_base_path + tmp_country_filename,
                countries_base_path + country_filename)




