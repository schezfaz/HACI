import pandas as pd
filenames = [
    "by-age.csv",
    "by-sex.csv",
    "demographics.csv",
    "economy.csv",
    "epidemiology.csv",
    "facility-boundary-us-all.csv",
    "geography.csv",
    "Global_vaccination_search_insights.csv",
    "google-search-trends.csv",
    "health.csv",
    "hospitalizations.csv",
    "lawatlas-emergency-declarations.csv",
    "mobility.csv",
    "oxford-government-response.csv",
    "vaccinations.csv",
    "weather.csv",
    "worldbank.csv"
]
for f in filenames:
    print (f)
    df = pd.read_csv("../raw/" + f)
    df["location_key"].fillna("UNK", inplace = True)
    df["country"]=df.location_key.apply(lambda x: x.split("_")[0])
    # if "location_key" in df: df["country"]=df.location_key.apply(lambda x: x.split("_")[0])
    # else: df["country"] = "UNK"
    print ("Number of unique countries",df.country.nunique())
    cols = df.columns
    for col in cols:
        if col not in ["location_key","date","country"]:
            print (col)
            df2 = df[col].isnull().groupby([df["country"]]).sum().astype(int).reset_index(name="count")
            df3 = df[col].groupby([df["country"]]).size().astype(int).reset_index(name="size")
            df4 = df2.merge(df3,how="inner",on="country")
            df4["null_proportion"] = df4["count"]*100/df4["size"]
            # print ("Countries with all nulls: ",df4[df4["null_proportion"]==100].shape[0])
            # print (df4[df4["null_proportion"]==100].shape[0])
            # print (df4[["country","null_proportion","size"]].sort_values(by=["null_proportion"],ascending=False))
            # print ("\n\n")