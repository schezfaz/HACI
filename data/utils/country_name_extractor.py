import csv
import os
import json
import math
from statistics import mean

# Extract country abbreviation to full name data.
index_country_map = {}
with open("data/covid_data/index.csv", mode="r") as file:
    csvFile = csv.reader(file)

    for line in csvFile:
        if len(line[0]) == 2: index_country_map[line[0]] = line[5]

# Extract CoViD Severity Index data.
covid_severity_indexes = {}
for _, country in index_country_map.items(): covid_severity_indexes[country] = None

with open("static/graph_data/covid_severity.csv", mode="r") as file:
    # Format: index,location_key,covid_severity,cumulative_confirmed,cumulative_deceased,population
    csvFile = csv.reader(file)
    for line in csvFile: covid_severity_indexes[index_country_map[line[1]]] = line[2]

# Extract Vaccination Index data.
vaccination_indexes = {}
for _, country in index_country_map.items(): vaccination_indexes[country] = None

with open("static/graph_data/vaccination_index.csv", mode="r") as file:
    # Format: index,location_key,vaccination_index,cumulative_persons_vaccinated,cumulative_persons_fully_vaccinated,population
    csvFile = csv.reader(file)
    for line in csvFile: vaccination_indexes[index_country_map[line[1]]] = line[2]

# Extract differences between index.csv (Google data) and world_countries.csv (DVA choropleth data)
countries_index_csv = {}
with open("data/covid_data/index.csv", mode="r") as file:
    csvFile = csv.reader(file)

    for line in csvFile:
        if len(line[0]) == 2: countries_index_csv[line[5]] = 1

countries_dva = {}
f = open("static/graph_data/world_countries.json")
data = json.load(f)
for country in data["features"]: countries_dva[country["properties"]["name"]] = 1

for key, _ in countries_dva.items():
    # if key not in countries_index_csv: print(key)
    if key not in countries_index_csv: pass

# Extract Government Stringency Index data.
govt_stringency_indexes = {}
with open("data/covid_data/oxford-government-response.csv", mode="r") as file:
    # Format: date,location_key,school_closing,workplace_closing,cancel_public_events,restrictions_on_gatherings,public_transport_closing,stay_at_home_requirements,restrictions_on_internal_movement,international_travel_controls,income_support,debt_relief,fiscal_measures,international_support,public_information_campaigns,testing_policy,contact_tracing,emergency_investment_in_healthcare,investment_in_vaccines,facial_coverings,vaccination_policy,stringency_index
    csvFile = csv.reader(file)
    for line in csvFile:
        # if line[2]: indexes[index_country_map[line[1]]] = line[2]
        if line[1] in index_country_map:
            if index_country_map[line[1]] not in govt_stringency_indexes:
                try:
                    if float(line[-1]) != 0.0: govt_stringency_indexes[index_country_map[line[1]]] = [float(line[-1])]
                except: pass
            else:
                try:
                    if float(line[-1]) != 0.0: govt_stringency_indexes[index_country_map[line[1]]].append(float(line[-1]))
                except: pass
    
    temp_indexes = govt_stringency_indexes.copy()
    for country, stringency_indexes in temp_indexes.items():
        govt_stringency_indexes[country] = mean(stringency_indexes)

# Extract Cumulative Confirmed, Deceased, Recovered, Tested CoViD cases, globally and country wise.
# cumulative_records = {"confirmed": [], "deaths": [], "recoverd": [], "tested": []}
cumulative_records = {}
with open("data/covid_data/epidemiology.csv", mode="r") as file:
    # Format: date,location_key,new_confirmed,new_deceased,new_recovered,new_tested,cumulative_confirmed,cumulative_deceased,cumulative_recovered,cumulative_tested
    csvFile = csv.reader(file)
    for line in csvFile:
        if line[1] in index_country_map and (line[-1] or line[-2] or line[-3] or line[-4]):
            if line[0] not in cumulative_records: cumulative_records[line[0]] = [0, 0, 0, 0]
            # if line[-1]: cumulative_records[line[0]][-1] += int(line[-1])
            # if line[-2]: cumulative_records[line[0]][-2] += int(line[-2])
            # if line[-3]: cumulative_records[line[0]][-3] += int(line[-3])
            # if line[-4]: cumulative_records[line[0]][-4] += int(line[-4])
            if line[2]: cumulative_records[line[0]][0] += int(line[2])
            if line[3]: cumulative_records[line[0]][1] += int(line[3])
            if line[4]: cumulative_records[line[0]][2] += int(line[4])
            if line[5]: cumulative_records[line[0]][3] += int(line[5])

with open("static/graph_data/epidemiology_new.csv", "w", encoding="UTF8") as f:
    for key in sorted(cumulative_records.keys()):
        writer = csv.writer(f)
        writer.writerow([key] + cumulative_records[key])

hospitalization_data = {}
with open("data/covid_data/epidemiology.csv", mode="r") as file:
    # Format: date,location_key,
    #         new_hospitalized_patients,cumulative_hospitalized_patients,current_hospitalized_patients,
    #         new_intensive_care_patients,cumulative_intensive_care_patients,current_intensive_care_patients,
    #         new_ventilator_patients,cumulative_ventilator_patients,current_ventilator_patients
    csvFile = csv.reader(file)
    for line in csvFile:
        if line[1] in index_country_map:
            if line[0] not in hospitalization_data: hospitalization_data[line[0]] = [0, 0, 0]
            if line[2]: hospitalization_data[line[0]][2] += int(line[2])
            if line[6]: hospitalization_data[line[0]][0] += int(line[6])
            if line[7]: hospitalization_data[line[0]][1] += int(line[7])

with open("static/graph_data/hospitalizations.csv", "w", encoding="UTF8") as f:
    for key in sorted(hospitalization_data.keys()):
        writer = csv.writer(f)
        writer.writerow([key] + hospitalization_data[key])