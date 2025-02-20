import csv

countries = ["austria", "belgium", "bulgaria", "croatia", "cyprus", "czechia", "denmark", "estonia", "finland", "france", "germany", "greece", "hungary", "ireland", "italy", "latvia", "lithuania", "luxembourg", "malta", "netherlands", "poland", "portugal", "romania", "slovakia", "slovenia", "spain", "sweden"]
years = list(range(2015, 2024))
sectors = ["agriculture", "buildings", "fluorinated gases", "fossil fuel operations", "forestry and land use", "manufacturing", "mineral extraction", "power", "transportation", "waste"]

def load_countries_table():
    with open("populationsALL_GDP.csv", 'r') as fileR:
        reader = csv.reader(fileR)
        header = next(reader)  # Skip header row
        # header = reader[0]
        
        # Create a dictionary to store the data for each country
        data = {country: {} for country in countries}
        
        # Populate the dictionary with GDP and population data
        for row in reader:
            # if row != header
            country = row[0].lower()
            #subject = row[1].lower()
            if country in data:
                for year in years:
                    if year not in data[country]:
                        data[country][year] = []
                        data[country][year].append(row[header.index(str(year))])
                    elif year in data[country]:
                        data[country][year].append( row[header.index(str(year))])
    return data

def load_sector_table():
    with open("subsectors.csv", 'r') as fileR:
        reader = csv.reader(fileR)
        header = next(reader)  
        data = {sector: {} for sector in sectors}
        for row in reader:
            sector = row[0].lower()
            if sector in sectors:
                subsectors = []
                for subsector in row[1:]:
                    if subsector != "":
                        subsectors.append(subsector.replace(" ", "-").lower())
                data[sector] = subsectors
    return data
            

def load_emissions_table():
    data = []
    for c in range(len(countries)):
        with open(str(countries[c])+".csv", 'r') as fileR:
            reader = csv.reader(fileR)
            header = next(reader)
            for row in reader:   
                rdata = []
                rdata.append(countries[c])
                rdata.append(row[2]) # year
                rdata.append(row[1]) # subsector
                rdata.append(row[3]) # co2
                rdata.append(row[4]) # ch4
                rdata.append(row[5]) # n2o
                rdata.append(row[6]) # co2_100y
                rdata.append(row[7]) # co2_20y
                data.append(rdata)
    return data

def load_missing_subsectors():
    data = [("waste", "biological-treatment-of-solid-waste-and-biogenic"), ("agriculture", "enteric-fermentation-cattle-operation"), ("manufacturing", "food-beverage-tobacco"), ("forestry and land use", "forest-land-clearing"), ("forestry and land use", "forest-land-degradation"), ("forestry and land use", "forest-land-fires"), ("agriculture", "manure-management-cattle-operation"), ("forestry and land use", "net-forest-land"), ("forestry and land use", "net-shrubgrass"), ("forestry and land use", "net-wetland"), ("mineral extraction", "other-mining-quarrying"), ("waste", "removals"), ("forestry and land use", "shrubgrass-fires"), ("manufacturing", "textiles-leather-apparel"), ("forestry and land use", "wetland-fires")]
    return data

# data is dictionary { country:  year: [gdp, population] }
def write_country_data_csv(data):
    # Write the country, year, GDP, and population data to the country file
    with open("countries.csv", "w", newline='') as fileC:
        writer = csv.writer(fileC)
        writer.writerow(["Country", "Year", "GDP", "Population"])  # Write header row
        
        for country in countries:
            for year in years:
                #if "gross domestic product" in data[country][year] and "population" in data[country][year]:
                gdp = data[country][year][0]
                population = data[country][year][1]
                writer.writerow([country, year, gdp, population])

def write_emissions_data_csv(data):
    # Write the emissions data to csv
    with open("emissions.csv", "w", newline='') as fileC:
        writer = csv.writer(fileC)
        writer.writerow(["country", "year", "subsector", "co2", "ch4", "n2o", "co2_100y", "co2_20y"])  # Write header row
        for row in data:
            writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])

countryData = load_countries_table()
#write_country_data_csv(countryData)

emissionsData = load_emissions_table()
#write_emissions_data_csv(emissionsData)