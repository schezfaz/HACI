from statistics import mean
from flask import Flask, jsonify, render_template, request
import csv
import pandas as pd
import numpy as np
import os
import statsmodels.tsa.stattools as ts
from statsmodels.tsa.stattools import acf, pacf
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import scipy.stats as ss
import json

app = Flask(__name__)

# API ENDPOINTS

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/economy.html")
def economy():
    return render_template("economy.html")

@app.route("/government.html")
def government():
    return render_template("government.html")

@app.route("/mobility.html")
def mobility():
    return render_template("mobility.html")

@app.route("/symptoms.html")
def symptoms():
    return render_template("symptoms.html")

@app.route("/vaccination.html")
def vaccination():
    return render_template("vaccination.html")

# @app.route('/vaccination_new')
# def process_country():
#     response = request.get_json()
#     country = response['country']
#     pre = response['pre']
#     df1 = pd.read_csv("data/generated_files/vac_country.csv")
#     df2 = pd.read_csv("data/generated_files/ep_country.csv")
#     df_vac_country = df1[df1["country_name"]==country]
#     df_vac_country = df_vac_country.groupby(['date','location_key'])['new_persons_vaccinated','new_persons_fully_vaccinated','population'].sum().reset_index()
#     df_vac_country['vaccination_index'] = (df_vac_country['new_persons_vaccinated']+2*df_vac_country['new_persons_fully_vaccinated'])/df_vac_country['population']
#     df_vac_country.sort_values(by='date',inplace=True,ignore_index=True)
#     df_ep_country = df2[df2["country_name"]==country]
#     df_ep_country = df_ep_country.groupby(['date','location_key'])['new_confirmed','new_deceased','population'].sum().reset_index()
#     df_ep_country['covid_severity'] = (df_ep_country['new_confirmed']+10*df_ep_country['new_deceased'])/df_ep_country['population']
#     df_ep_country.sort_values(by='date',inplace=True,ignore_index=True)
    
    
#     if pre=='True':
#         df_final = df_ep_country[(df_ep_country['date']<df_vac_country.date[0])]
#     else:
#         df_final = df_ep_country[(df_ep_country['date']>=df_vac_country.date[0])]
#     x = np.arange(df_final.shape[0])
#     fit = np.polyfit(x, df_final['covid_severity'], deg=1)
#     fit_function = np.poly1d(fit)
#     line = fit_function(x)

#     final = []
#     for i in range(len(line)):
#         final.append([df_final.date.values[i],df_final.covid_severity.values[i],line[i]])
#     minval = min(df_final.covid_severity.values)
#     if min(line)<minval:
#         minval=min(line)
#     return jsonify({'resp':final,'min':minval})

@app.route("/about.html")
def about():
    return render_template("about.html")

# UTIL FUNCTIONS

@app.context_processor
def utility_processor():    
    def get_abb_to_country_name_map():
        # Extract country abbreviation to full name data.
        index_country_map = {}
        with open("data/covid_data/index.csv", mode="r", encoding="utf-8") as file:
            csvFile = csv.reader(file)

            for line in csvFile:
                if len(line[0]) == 2: index_country_map[line[0]] = line[5]
        
        return index_country_map

    def get_correlation_matrix(page_name):
         corr_feat = []
         if page_name == "wb_corr_matrix":
            with open("data/generated_files/wb_corr_matrix.csv", mode="r") as file:
                csvFile = csv.reader(file)
                for line in csvFile:
                    corr_feat.append(line)

         elif page_name== "Dashboard":
            with open("data/generated_files/all_correlation_matrix.csv", mode="r") as file:
                csvFile = csv.reader(file)
                for line in csvFile:
                    corr_feat.append(line)
         return corr_feat


    def get_time_series_plot(page_name):
        if page_name=='vaccination':
            df = pd.read_csv("data/generated_files/severity_vaccination_cross_correlation.csv")
            s1 = df.vaccination_index.values
        elif page_name=='mobility':
            df=pd.read_csv("data/generated_files/severity_mobility_cross_correlation.csv")
            s1 = df.mob_total.values
        elif page_name=='govt':
            df=pd.read_csv("data/generated_files/govtresponse_severity_cross_correlation.csv")
            s1 = df.stringency_index.values
        x = []
        y = []
        s2 = df.covid_severity.values
        plt.ioff()
        for i in range(1,len(s1)):
            x.append(s1[i]-s1[i-1])
            y.append(s2[i]-s2[i-1])
        lag,c,line,b = plt.xcorr(y, x, normed=True, usevlines=True, maxlags=365)
        ci = [2/(len(x)-abs(lag[i]))**0.5 for i in range(len(lag))]
        neg_ci = [-i for i in ci]
        final = []
        for i in range(len(lag)):
            final.append([lag[i],c[i],ci[i],neg_ci[i]])
        return final


    def get_govt_bar_plots(page_name):
        df = pd.read_csv('data/generated_files/government_response_bar_plot.csv')
        return df.values.tolist()


    def get_world_index_data(index_name):
        # Extract country abbreviation to full name data.
        index_country_map = {}
        with open("data/covid_data/index.csv", mode="r", encoding="utf-8") as file:
            csvFile = csv.reader(file)

            for line in csvFile:
                if len(line[0]) == 2: index_country_map[line[0]] = line[5]

        indexes = {}

        # Extract CoViD Severity Index data.
        if index_name == "CoViD Severity":
            with open("static/graph_data/covid_severity.csv", mode="r") as file:
                # Format: index,location_key,covid_severity,cumulative_confirmed,cumulative_deceased,population
                csvFile = csv.reader(file)
                for line in csvFile:
                    if line[2]: indexes[index_country_map[line[1]]] = line[2]

        # Extract Vaccination Index data.
        elif index_name == "Vaccination Status":
            with open("static/graph_data/vaccination_index.csv", mode="r") as file:
                # Format: index,location_key,vaccination_index,cumulative_persons_vaccinated,cumulative_persons_fully_vaccinated,population
                csvFile = csv.reader(file)
                for line in csvFile:
                    if line[2]: indexes[index_country_map[line[1]]] = line[2]
        
        # Extract Government Stringency Index data.
        elif index_name == "Government Stringency":
            with open("data/covid_data/oxford-government-response.csv", mode="r") as file:
                # Format: date,location_key,school_closing,workplace_closing,cancel_public_events,restrictions_on_gatherings,public_transport_closing,stay_at_home_requirements,restrictions_on_internal_movement,international_travel_controls,income_support,debt_relief,fiscal_measures,international_support,public_information_campaigns,testing_policy,contact_tracing,emergency_investment_in_healthcare,investment_in_vaccines,facial_coverings,vaccination_policy,stringency_index
                csvFile = csv.reader(file)
                for line in csvFile:
                    # if line[2]: indexes[index_country_map[line[1]]] = line[2]
                    if line[1] in index_country_map:
                        if index_country_map[line[1]] not in indexes:
                            try:
                                if float(line[-1]) != 0.0: indexes[index_country_map[line[1]]] = [float(line[-1])]
                            except: pass
                        else:
                            try:
                                if float(line[-1]) != 0.0: indexes[index_country_map[line[1]]].append(float(line[-1]))
                            except: pass
                
                temp_indexes = indexes.copy()
                for country, stringency_indexes in temp_indexes.items():
                    indexes[country] = mean(stringency_indexes)
        
        # Extract World GDP data.
        elif index_name == "Gdp":
            with open("data/generated_files/economy_gdp.csv", mode="r") as file:
                # Format: date,location_key,school_closing,workplace_closing,cancel_public_events,restrictions_on_gatherings,public_transport_closing,stay_at_home_requirements,restrictions_on_internal_movement,international_travel_controls,income_support,debt_relief,fiscal_measures,international_support,public_information_campaigns,testing_policy,contact_tracing,emergency_investment_in_healthcare,investment_in_vaccines,facial_coverings,vaccination_policy,stringency_index
                csvFile = csv.reader(file)
                for line in csvFile:
                    if line[0]=="location_key":
                        continue
                    indexes[index_country_map[line[0]]] = line[1]
        
        elif index_name == "gdp_per_capita":
            with open("data/generated_files/economy_gdp.csv", mode="r") as file:
                # Format: date,location_key,school_closing,workplace_closing,cancel_public_events,restrictions_on_gatherings,public_transport_closing,stay_at_home_requirements,restrictions_on_internal_movement,international_travel_controls,income_support,debt_relief,fiscal_measures,international_support,public_information_campaigns,testing_policy,contact_tracing,emergency_investment_in_healthcare,investment_in_vaccines,facial_coverings,vaccination_policy,stringency_index
                csvFile = csv.reader(file)
                for line in csvFile:
                    if line[0]=="location_key":
                        continue
                    indexes[index_country_map[line[0]]] = line[2]

        return indexes

    def get_other_eco_data():
        indexes = {}
        index_country_map = {}
        with open("data/covid_data/index.csv", mode="r", encoding="utf-8") as file:
            csvFile = csv.reader(file)

            for line in csvFile:
                if len(line[0]) == 2: index_country_map[line[0]] = line[5]

        with open("data/generated_files/economy_gdp.csv", mode="r") as file:
            csvFile = csv.reader(file)
            for line in csvFile:
                if line[0]=="location_key":
                    continue
                indexes[index_country_map[line[0]]] = line[2:]
        return indexes

    def get_top_countries(count, order):
        # Extract country abbreviation to full name data.
        index_country_map = {}
        with open("data/covid_data/index.csv", mode="r", encoding="utf-8") as file:
            csvFile = csv.reader(file)

            for line in csvFile:
                if len(line[0]) == 2: index_country_map[line[0]] = line[5]

        indexes = []

        # Extract CoViD Severity Index data.
        with open("static/graph_data/covid_severity.csv", mode="r") as file:
            # Format: index,location_key,covid_severity,cumulative_confirmed,cumulative_deceased,population
            csvFile = csv.reader(file)
            for line in csvFile:
                if line[2]: indexes.append([line[0], line[1], float(line[2]), float(line[3]), float(line[4]), float(line[5])])
        
        data = []
        if order == "worst":
            # indexes = sorted(indexes, key=lambda x: x[2])
            indexes = sorted(indexes, key=lambda x: x[4] / (x[3] + 1))
            indexes = np.array(indexes)
            indexes = indexes[:, 1:]
            indexes = list([list(indexes[i]) for i in range(len(indexes))])
            indexes = indexes[::-1][:count]

            for index in indexes:
                data.append([index_country_map[index[0]], float(index[1]), float(index[2]), float(index[3]), float(index[4])])
        
        elif order == "worst_population":
            # indexes = sorted(indexes, key=lambda x: x[2])
            indexes = sorted(indexes, key=lambda x: x[3] / (x[5] + 1))
            indexes = np.array(indexes)
            indexes = indexes[:, 1:]
            indexes = list([list(indexes[i]) for i in range(len(indexes))])

            for index in indexes:
                if float(index[2]) != 0: data.append([index_country_map[index[0]], float(index[1]), float(index[2]), float(index[3]), float(index[4])])
            
            data = data[::-1][:count]
        
        elif order == "best_cases":
            # indexes = sorted(indexes, key=lambda x: x[2])
            indexes = sorted(indexes, key=lambda x: x[4] / (x[3] + 1))
            indexes = np.array(indexes)
            indexes = indexes[:, 1:]
            indexes = list([list(indexes[i]) for i in range(len(indexes))])
            # indexes = indexes[:count]

            for index in indexes:
                if float(index[3]) > 0: data.append([index_country_map[index[0]], float(index[1]), float(index[2]), float(index[3]), float(index[4])])
            
            data = data[:count]

        else:
            # indexes = sorted(indexes, key=lambda x: x[2])
            indexes = sorted(indexes, key=lambda x: x[3] / (x[5] + 1))
            indexes = np.array(indexes)
            indexes = indexes[:, 1:]
            indexes = list([list(indexes[i]) for i in range(len(indexes))])

            for index in indexes:
                if float(index[2]) != 0: data.append([index_country_map[index[0]], float(index[1]), float(index[2]), float(index[3]), float(index[4])])
            
            data = data[:count]

        return data

    
    def get_correlation_data(page_name):
        feat_imp = []

        # Extract World bank correlation data
        if page_name == "Dashboard":
            with open("data/generated_files/feature_importance_wrt_covid_severity", mode="r") as file:
                csvFile = csv.reader(file)
                for line in csvFile:
                    if line[1]=="indicator_code":
                        continue
                    feat_imp.append(line[1:])
        elif page_name == "Economy":
            with open("data/generated_files/world_Bank_feature_importance_wrt_covid_severity.csv", mode="r") as file:
                csvFile = csv.reader(file)
                for line in csvFile:
                    if line[1]=="indicator_code":
                        continue
                    feat_imp.append(line[1:])
        return feat_imp
   
    def get_world_epidemiology_data():
        world_epidemiology_data = []

        with open("static/graph_data/epidemiology_new.csv", mode="r") as file:
            csvFile = csv.reader(file)
            for line in csvFile: world_epidemiology_data.append([line[0], int(line[1]), int(line[2]), int(line[3]), int(line[4])])
        
        return world_epidemiology_data

    def get_mobility_data_feat_pie():
        feat_imp = []
        with open("data/generated_files/mobility_pie_plot.csv", mode="r") as file:
                csvFile = csv.reader(file)
                for line in csvFile:
                    if line[1]=="feature":
                        continue
                    feat_imp.append(line[1:])
        return feat_imp
    

    def get_mobility_data():
        mobility_monthly_data = []
        with open("data/generated_files/mobility_monthly.csv", mode="r") as file:
            csvFile = csv.reader(file)
            for line in csvFile:
                mobility_monthly_data.append(line)
        # print(mobility_monthly_data)
        return mobility_monthly_data





        # mobility_country_data = {}
        # # {'country': ['date1': [data, data, data, data], 'date2': [data, data, data, data]]}
        # with open("data/generated_files/mobility_cummulative.csv", mode="r") as file:
        #     csvFile = csv.reader(file)
        #     for line in file:
        #         line = line.split(',')
        #         country = line[2]
        #         if(country!='location_key' and country not in mobility_country_data.keys()):
        #             mobility_country_data[country] = []

        #     # {'AE': {'date1': {'mob': 0}}
        # with open("data/generated_files/mobility_cummulative.csv", mode="r") as file:
        #     count = 0
        #     for line in file:
        #         count+=1
        #         row = line.split(',')
        #         date = row[1]  
        #         mobility_country = row[2]  
        #         mobility_retail_and_recreation = row[3]
        #         mobility_grocery_and_pharmacy = row[4]
        #         mobility_parks = row[5]
        #         mobility_transit_stations = row[6]
        #         mobility_workplaces = row[7]
        #         mobility_residential = row[8]
        #         mobility_all= row[9]
               
        #         mobility_date_data = {}
        #         mobility_data = {}
        #         mobility_data['country'] = mobility_country
        #         mobility_data['mobility_retail_and_recreation'] = mobility_retail_and_recreation
        #         mobility_data['mobility_grocery_and_pharmacy'] = mobility_grocery_and_pharmacy
        #         mobility_data['mobility_parks'] = mobility_parks
        #         mobility_data['mobility_transit_stations'] = mobility_transit_stations
        #         mobility_data['mobility_workplaces'] = mobility_workplaces
        #         mobility_data['mobility_residential'] = mobility_residential
        #         mobility_data['mobility_all'] = mobility_all
        #         mobility_date_data[date] = mobility_data

        #         # mobility_date_data.pop('date')
        #         removed_key = mobility_date_data.pop("date", None)
        #         # print(mobility_date_data)

        #         if count == 5:
        #             break

        #         for key in mobility_date_data.keys():
        #             # print('key: ', key)
        #             extracted_country = mobility_date_data[key]['country']
        #             for country in mobility_country_data.keys():
        #                 if extracted_country == country:
        #                     date_data = {'date': key, 'country:': extracted_country ,'data': mobility_date_data[key]}
        #                     mobility_country_data[country].append(date_data)
                
        #     print('data: ' , mobility_country_data)
        #     return mobility_country_data

                
    def get_mobility_pie_data():
        mobility_pie_data = []
        with open("data/generated_files/mean_mobility.csv", mode="r") as file:
                csvFile = csv.reader(file)
                for line in csvFile:
                    mobility_pie_data.append(line)
        # print(mobility_pie_data)
        return mobility_pie_data
  
    def get_health_data():
        abb_name_map = get_abb_to_country_name_map()

        country_data_map = {}
        with open("data/covid_data/health.csv", mode="r") as file:
            csvFile = csv.reader(file)
            for line in csvFile:
                if line[0] in abb_name_map:
                    # Format: location_key,life_expectancy,smoking_prevalence,diabetes_prevalence,
                    # infant_mortality_rate,adult_male_mortality_rate,adult_female_mortality_rate,
                    # pollution_mortality_rate,comorbidity_mortality_rate,hospital_beds_per_1000,
                    # nurses_per_1000,physicians_per_1000,health_expenditure_usd,out_of_pocket_health_expenditure_usd
                    if abb_name_map[line[0]] not in country_data_map: country_data_map[abb_name_map[line[0]]] = {}

                    if line[1]: country_data_map[abb_name_map[line[0]]]["life_expectancy"] = float(line[1])
                    if line[2]: country_data_map[abb_name_map[line[0]]]["smoking_prevalence"] = float(line[2])
                    if line[3]: country_data_map[abb_name_map[line[0]]]["diabetes_prevalence"] = float(line[3])
                    if line[4]: country_data_map[abb_name_map[line[0]]]["infant_mortality_rate"] = float(line[4])
                    if line[5]: country_data_map[abb_name_map[line[0]]]["adult_male_mortality_rate"] = float(line[5])
                    if line[6]: country_data_map[abb_name_map[line[0]]]["adult_female_mortality_rate"] = float(line[6])
                    if line[7]: country_data_map[abb_name_map[line[0]]]["pollution_mortality_rate"] = float(line[7])
                    if line[8]: country_data_map[abb_name_map[line[0]]]["comorbidity_mortality_rate"] = float(line[8])
                    if line[9]: country_data_map[abb_name_map[line[0]]]["hospital_beds_per_1000"] = float(line[9])
                    if line[10]: country_data_map[abb_name_map[line[0]]]["nurses_per_1000"] = float(line[10])
                    if line[11]: country_data_map[abb_name_map[line[0]]]["physicians_per_1000"] = float(line[11])
                    if line[12]: country_data_map[abb_name_map[line[0]]]["health_expenditure_usd"] = float(line[12])
                    if line[13]: country_data_map[abb_name_map[line[0]]]["out_of_pocket_health_expenditure_usd"] = float(line[13])
        
        return country_data_map
    
    def get_hospitalization_data():
        hospitalization_data = []

        with open("static/graph_data/hospitalizations.csv", mode="r") as file:
            csvFile = csv.reader(file)
            # for line in csvFile: hospitalization_data.append([line[0], int(line[1]), int(line[2]), int(line[3])])
            # for line in csvFile: hospitalization_data.append({"date": line[0], "Hospitalizations": int(line[1]), "ICUs": int(line[2]), "Ventilators": int(line[3])})
            for line in csvFile:
                hospitalization_data.append([
                    {"date": line[0], "category": "Hospitalizations", "value": (int(line[1]) / 100) + 1, "color": "#98abc5"},
                    {"date": line[0], "category": "ICUs", "value": int(line[2]) + 1, "color": "#6b486b"},
                    {"date": line[0], "category": "Ventilators", "value": int(line[3]) + 1, "color": "#ff8c00"}
                ])

        return hospitalization_data


    def get_vaccine_country_list():
        df = pd.read_csv("data/generated_files/vac_country.csv")
        temp = ['Select Country']+df.country_name.unique().tolist()
        return temp
        
    def get_search_trends():
        df = pd.read_csv("static/graph_data/search-trends-strains.csv",sep=',', encoding='utf-8')
        wc_dict = df.to_dict(orient='records')
        wc_list = []
    
        for strain in wc_dict:
            elements = [[x, y] for x, y in strain.items()]
            wc_list.append(elements)
        
        return wc_list

    def get_top_search_trends():
        df = pd.read_csv("static/graph_data/search-trends-top.csv",sep=',', encoding='utf-8')
        top20 = df.to_dict(orient='records')
        symptom_list = list(df.columns)

        return [top20, symptom_list]

    def get_epidemiology_strains():
        df = pd.read_csv("static/graph_data/epidemiology-strains.csv",sep=',', encoding='utf-8')
        strain_dict = df.to_dict(orient='records')
        bar_labels = list(df.columns)
        strains = list(df['strain'])

        return [strain_dict,bar_labels,strains]


    return dict(
        get_vaccine_country_list    = get_vaccine_country_list,
        get_world_index_data        = get_world_index_data,
        get_correlation_data        = get_correlation_data,
        get_correlation_matrix      = get_correlation_matrix,
        get_world_epidemiology_data = get_world_epidemiology_data,
        get_top_countries           = get_top_countries,
        get_mobility_data           = get_mobility_data,
        get_mobility_pie_data       = get_mobility_pie_data,
        get_mobility_data_feat_pie  = get_mobility_data_feat_pie,
        get_time_series_plot        = get_time_series_plot,
        get_health_data             = get_health_data,
        get_govt_bar_plots          = get_govt_bar_plots,
        get_other_eco_data          = get_other_eco_data,
        get_search_trends           = get_search_trends,
        get_hospitalization_data    = get_hospitalization_data,
        get_top_search_trends       = get_top_search_trends,
        get_epidemiology_strains    = get_epidemiology_strains)

if __name__ == "__main__":
    app.run()