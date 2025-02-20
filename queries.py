import pymysql.cursors

#from app import emissions    

# from flask_mysqldb import MySQL
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'root'
# app.config['MYSQL_DB'] = 'project7'
# mysql = MySQL(app)
# with app.app_context():

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             database='project7',
                             cursorclass=pymysql.cursors.DictCursor)
# Static Graphs
def bar_chart_data():
    cursor = connection.cursor()
    cursor.execute("SELECT e.country, s.sector, SUM(e.emission) as co2 FROM emissions e, sectors s WHERE e.subsector = s.subsector AND country = 'ireland' AND gas = 'co2e_100yr' GROUP BY s.sector")
    data = cursor.fetchall()
    data1 = []
    for i in data:
        row = []
        row.append(i['country'])
        row.append(i['sector'])
        row.append(int(i['co2']))
        #print(row)
        data1.append(row)
    cursor.close()
    return data1

def bar_chart_data_dynamic(c):
    cursor = connection.cursor()
    cursor.execute("SELECT e.country, s.sector, SUM(e.emission) as co2 FROM emissions e, sectors s WHERE e.subsector = s.subsector AND country = %s AND gas = 'co2e_100yr' GROUP BY s.sector", (c, ))
    data = cursor.fetchall()
    sector = []
    emissions = []
    for i in data:
        sector.append(i['sector'])
        emissions.append(int(i['co2']))
    cursor.close()
    return (sector, emissions)
    #mysql.connection.commit()
def stack_chart_data():
    cursor = connection.cursor()
    cursor.execute("SELECT country, year, SUM(emission)as co2 FROM emissions WHERE gas = 'co2e_100yr' GROUP BY country, year")
    data = cursor.fetchall()
    years = []
    emission_by_country = {}
    for row in data:
        country = row['country']
        year = row['year']
        emission = int(row['co2'])
        if year not in years:
            years.append(year)
        if country not in emission_by_country:
            emission_by_country[country] = []
        emission_by_country[country].append(emission)
        
        #print(i)
    #print(emission_by_country)
    cursor.close()
    return (years, emission_by_country)
    #mysql.connection.commit()
def line_chart_data():
    cursor = connection.cursor()
    cursor.execute("SELECT e.country, c.gdp, SUM(e.emission) as co2 FROM emissions e, countries c WHERE e.country = c.country AND e.year = 2023 AND c.year = 2023 AND e.gas = 'co2e_100yr' GROUP BY e.country")
    data = cursor.fetchall()
    countries = []
    gdp = []
    co2 = []
    for row in data:
        #print(i)
        country = row['country']
        gdp_val = row['gdp']
        co2_val = row['co2']
        countries.append(country)
        gdp.append(gdp_val)
        co2.append(co2_val)

    cursor.close()
    return (countries, gdp, co2)
    #mysql.connection.commit()
def pie_chart_data(gas, year):
   
    cursor = connection.cursor()
    cursor.execute("SELECT e.country, c.gdp, SUM(e.emission) as %s FROM emissions e, countries c WHERE e.country = c.country AND e.year = %s AND c.year = %s AND e.gas = %s GROUP BY e.country", (gas, year, year, gas,))
    
    data = cursor.fetchall()
    countries = []
    gdp = []
    gas1 = []
    for row in data:
        #print(i)
        country = row['country']
        gdp_val = row['gdp']
        gas1_val = row[gas]
        countries.append(country)
        gdp.append(gdp_val)
        gas1.append(gas1_val)

    cursor.close()
    return (countries, gdp, gas1)
# Dynamic Graphs
def projection_chart_data(c):
    cursor = connection.cursor()
    cursor.execute("SELECT country, year, SUM(emission)as co2 FROM emissions WHERE gas = 'co2e_100yr' AND country = %s GROUP BY country, year", (c,))
    data = cursor.fetchall()
    years = []
    emission_by_country = {}
    for row in data:
        country = row['country']
        year = row['year']
        emission = int(row['co2'])
        if year not in years:
            years.append(year)
        if country not in emission_by_country:
            emission_by_country[country] = []
        emission_by_country[country].append(emission)
    cursor.close()
    return (years, emission_by_country)    
#print(projection_chart_data('ireland'))

def create_table_data(year, gas):
    cursor = connection.cursor()
    cursor.execute("SELECT country, year, SUM(emission) as %s FROM emissions WHERE gas = %s AND year = %s  GROUP BY country, year", (gas, gas, year))
    cursor.execute("SELECT e.country, c.population, SUM(e.emission) as %s FROM emissions e, countries c WHERE e.country = c.country AND e.year = %s AND c.year = %s AND e.gas = %s GROUP BY e.country", (gas, year, year, gas))
    data = cursor.fetchall()
    #print(data)
    country = []
    emission = []
    population = []
    for row in data:
        country.append(row['country'])
        population.append(row['population'])
        emission.append(int(row[gas]))
    return (country, population, emission)

#create_table_data(2020, 'co2e_100yr')

def close_connection():
    connection.close()