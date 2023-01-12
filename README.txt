The ‘HACI’ (Holistic Analysis of Covid-19 Impacts) Dashboard aims to highlight and quantify the disparities in how the pandemic affected the world by calculating a cumulative score of the impact of covid on each country, derived by analyzing and visualizing the global economic, social, environmental and health impacts of Covid-19. 

These impacts have been analysed and visualised across the following caterogies:
- Covid Severity
- Economy
- Government
- Mobility
- Symptoms
- Vaccination

The package contains the following components:
1. Data: The data folder contains the preprocessed data files leveraged by the HACI Dashboard
    a. covid_data: The main source of data is the Google COVID-19 Open Data Repository (https://health.google.com/covid-19/open-data/)
    b. generated_files: post-processed files used across the 6 verticals through which the analysis was conducted
    c. utils: python scripts to clean, process and manipulate data through regression and time-series analysis
2. Templates: Web templates used to render the various pages across the 6 tabs: Covid Severity, Economy, Government, Mobility, Symptoms and Vaccination
3. app.py: The server file, where data is fetched from the data repository, processed and served to the front-end via the api endpoints

Tech-Stack: Flask, JavaScript (D3.js)

Installation Instructions:

To install the application locally:
- Clone the git repository `git clone https://github.gatech.edu/asadhukha3/HACI.git`
- Use Python version 3.7 or higher
- Run `pip install -r requirements.txt` to install the required dependencies

Execution (Local Demo):
- Run the following command in the app's directory to run the webapp locally `python app.py`
- Go to http://127.0.0.1:5000/ to view the application

Demo Video:
https://youtu.be/ugORN3KjV-g
