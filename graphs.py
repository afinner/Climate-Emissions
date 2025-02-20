from calendar import c
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mticker
#from app import emissions
import queries
from decimal import Decimal

def generate_chart_bar():
    data = queries.bar_chart_data()
    sectors =[]
    emissions = []
    for row in data:
        sectors.append(row[1])
        emissions.append(row[2])
    # sectors = ["Ag", "Waste", "Power", "Mining"]
    # emissions = [500, 100, 700, 300]
    plt.figure(figsize=(20, 12))
    plt.bar(sectors, emissions)
    plt.title("Total Irish CO2 emissions by sector")
    plt.xlabel("Sectors")
    plt.ylabel("Emissions level")
    plt.savefig("static/emissions_by_sector_chart.png")
    #plt.show()
    
#generate_chart_bar()

def generate_chart_line():
    data = queries.line_chart_data()
    country = data[0]
    gdp = data[1]
    co2 = data[2]
    plt.figure(figsize=(20, 12))
    plt.plot(country, co2, marker="o", color="orange")
    plt.plot(country, gdp, marker="o", color="red")
    plt.title("CO2 emissions and gdp of countries in 2023")
    plt.xlabel("Countries")
    plt.ylabel("CO2: orange - gdp: red")
    plt.savefig("static/co2_and_gdp_chart.png") 
    #plt.show()
#generate_chart_line()


def generate_pie_charts():
    data = queries.line_chart_data()
    country = data[0]
    gdp = data[1]
    co2 = data[2]
    
    # Get the indexes of the top 10 CO2 emissions
    top_10_indexes = sorted(range(len(co2)), key=lambda i: co2[i], reverse=True)[:10]
    
    # Create new lists for country and GDP based on the top 10 CO2 indexes
    top_10_countries = [country[i] for i in top_10_indexes]
    top_10_gdp = [gdp[i] for i in top_10_indexes]
    top_10_co2 = [co2[i] for i in top_10_indexes]

    fig, ax = plt.subplots(1, 2, figsize=(14, 7))

    # First pie chart for CO2 emissions
    ax[0].pie(top_10_co2, labels=top_10_countries, autopct='%1.1f%%')
    ax[0].set_title("Top 10 CO2 Emissions of Countries in 2023")

    # Second pie chart for GDP
    ax[1].pie(top_10_gdp, labels=top_10_countries, autopct='%1.1f%%')
    ax[1].set_title("GDP of Top 10 CO2 Emitting Countries in 2023")

    plt.tight_layout()
    plt.savefig("static/co2_gdp_comparison.png")
    #plt.show()

# Call the function to generate the pie charts
generate_pie_charts()


def generate_stack_chart():
    data = queries.stack_chart_data()
    years = data[0] 
    emissions_by_country = data[1]
    keys = sorted(emissions_by_country, key=emissions_by_country.get, reverse=True)[:10]
    d = {}
    for k in keys:
        d[k]=emissions_by_country[k]
    emissions_by_country = d
    plt.figure(figsize=(12, 2))
    fig, ax = plt.subplots()
    ax.stackplot(years, emissions_by_country.values(),
                labels=emissions_by_country.keys(), alpha=0.8)
    ax.legend(loc= 'lower left', frameon=False, reverse=True)
    ax.set_title('Emissions')
    ax.set_xlabel('Year')
    ax.set_ylabel('CO2 emsissions (millions)')
    # add tick at every 200 thousand emissions
    #ax.yaxis.set_minor_locator(mticker.MultipleLocator(.2))
    plt.savefig("static/emissions_by_country_chart.png")
    #plt.show()
generate_stack_chart()

def generate_fill_in_graph():
    t = np.arange(0.0, 2, 0.01)
    s = np.sin(2*np.pi*t)

    fig, ax = plt.subplots()

    ax.plot(t, s, color='black')
    ax.axhline(0, color='black')

    ax.fill_between(t, 1, where=s > 0, facecolor='green', alpha=.5)
    ax.fill_between(t, -1, where=s < 0, facecolor='red', alpha=.5)
    plt.savefig("static/emissions_by_sector_cool_chart.png")
    #plt.show()
#generate_fill_in_graph()
