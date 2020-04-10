import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta

date1 = date(2020, 1, 22)
today = date.today()
cases_list = []
hit_countries = set()

while date1 < today:
    url_date1 = str(date1)
    url_date1 = url_date1[5]+url_date1[6]+"-"+url_date1[8]+url_date1[9]+"-"+url_date1[0]+url_date1[1]+url_date1[2]+url_date1[3]
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'+url_date1+'.csv'
    try:
        df = pd.read_csv(url)
    except:
        break
    try:
        hit_countries.update(df['Country/Region'].unique())
    except:
        hit_countries.update(df['Country_Region'].unique())
    cases_list.append(df)
    date1 = date1 + timedelta(days=1)
    last_date = url_date1

while True:
    print("Fetched all COVID-19 cases from 01-22-2020 to "+last_date)

    print(sorted(hit_countries))
    county_select = input("Type country (nothing typed = worldwide): ")

    sum_new = 0
    sum_active = 0
    last_confirmed = 0
    log_sum_new = []
    log_sum_active = []

    for i in cases_list:
        if(county_select == ""):
            subset = i
        else:
            try:
                subset = i.loc[i['Country/Region'] == county_select]
            except:
                subset = i.loc[i['Country_Region'] == county_select]
        confirmed = subset['Confirmed'].sum(skipna = True)
        deaths = subset['Deaths'].sum(skipna = True)
        recovered = subset['Recovered'].sum(skipna=True)
        sum_new = confirmed - last_confirmed
        sum_active = confirmed - deaths - recovered
        if(sum_new > 1 and sum_active > 1):
            log_sum_new.append(math.log(sum_new))
            log_sum_active.append(math.log(sum_active))
        last_confirmed = confirmed

    plt.plot(log_sum_active, log_sum_new)
    plt.xlabel('log of active infected')
    plt.ylabel('log of newly infected')
    plt.show()