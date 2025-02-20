from flask import Flask
from flask_mysqldb import MySQL
import load_tables

countries = ["austria", "belgium", "bulgaria", "croatia", "cyprus", "czechia", "denmark", "estonia", "finland", "france", "germany", "greece", "hungary", "ireland", "italy", "latvia", "lithuania", "luxembourg", "malta", "netherlands", "poland", "portugal", "romania", "slovakia", "slovenia", "spain", "sweden"]
years = list(range(2015, 2024))
sectors = ["agriculture", "buildings", "fluorinated gases", "fossil fuel operations", "forestry and land use", "manufacturing", "mineral extraction", "power", "transportation", "waste"]
gas = ["co2", "ch4", "n2o", "co2e_100yr", "co2e_20yr"]
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'project7'
 
mysql = MySQL(app)
# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="root",
#   charset="utf8mb3",
#   database="project9"
# )

# mycursor = mydb.cursor()
#mysql = MySQL(app)
 
#Creating a connection cursor
with app.app_context():
    cursor = mysql.connection.cursor()
    # mycursor.execute("CREATE DATABASE project11")
    # mydb.commit()
    # mycursor.execute("SHOW DATABASES")
    # for x in mycursor:
    #   print(x)
    # mycursor.execute("CREATE TABLE countries (country VARCHAR(255), year INT, gdp FLOAT(10,5), population FLOAT(10,5))")
    # mycursor.execute("CREATE TABLE sectors (sector VARCHAR(255), subsector VARCHAR(255))")
    # mycursor.execute("CREATE TABLE emissions (country VARCHAR(255), year VARCHAR(255), subsector VARCHAR(255), gas VARCHAR(255), emission INT)")
    # mydb.commit()
    cursor.execute(" CREATE TABLE countries ( country VARCHAR(255), year INT, gdp FLOAT(10,5), population FLOAT(10,5), PRIMARY KEY (country, year) ) ") 
    cursor.execute(" CREATE TABLE sectors ( sector VARCHAR(255), subsector VARCHAR(255), PRIMARY KEY (subsector) ) ") 
    cursor.execute(" CREATE TABLE emissions ( country VARCHAR(255), year INT, subsector VARCHAR(255), gas VARCHAR(255), emission INT, PRIMARY KEY (country, year, subsector, gas), FOREIGN KEY (country, year) REFERENCES countries(country, year), FOREIGN KEY (subsector) REFERENCES sectors(subsector) ) ") 
    #mycursor.execute(" CREATE TABLE emissions ( country VARCHAR(255), year INT, subsector VARCHAR(255), gas VARCHAR(255), emission INT, PRIMARY KEY (country, year, subsector, gas), FOREIGN KEY (country, year) REFERENCES countries(country, year) ) ") 
    mysql.connection.commit()

    def insert_countries():
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO countries (country, year, gdp, population) VALUES (%s, %s, %s, %s)"
        dataCountries = load_tables.load_countries_table()
        for i in (countries):
            for j in years:
                a = dataCountries[i][j]
                val = (i, j, a[0], a[1])
                cursor.execute(sql, val)
                mysql.connection.commit()

    def insert_sectors():
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO sectors (sector, subsector) VALUES (%s, %s)"
        dataSectors = load_tables.load_sector_table()
        for i in sectors:
            for j in dataSectors[i]:
                val = (i, j)
                cursor.execute(sql, val)
                mysql.connection.commit()

    def insert_missing_sectors():
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO sectors (sector, subsector) VALUES (%s, %s)"
        dataMissing = load_tables.load_missing_subsectors()
        for data in dataMissing:
            val = (data[0], data[1])
            cursor.execute(sql, val)
            mysql.connection.commit()

    

    def insert_emissions():
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO emissions (country, year, subsector, gas, emission) VALUES (%s, %s, %s, %s, %s)"
        dataEmissions = load_tables.load_emissions_table()
        for i in range(len(dataEmissions)):
            a = dataEmissions[i]
            for j in range(len(gas)):   
                val = (a[0], a[1], a[2], gas[j], a[j+3])
                cursor.execute(sql, val)
                mysql.connection.commit()

    def delete_problem_data():
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM emissions WHERE subsector = 'removals'")
        sql = "DELETE FROM sectors (sector, subsector) VALUES (%s, %s)"
        val = ("waste", "removals")
        cursor.execute(sql, val)
        mysql.connection.commit()
        #-- Step 1: Identify the subsectors associated with the specific sector
        cursor.execute("SELECT subsector FROM sectors WHERE sector = 'forestry and land use'")
        #data = cursor.fetchall()

        #-- Step 2: Delete all rows from other tables that reference these subsectors
        cursor.execute("DELETE FROM emissions WHERE subsector IN (SELECT subsector FROM sectors WHERE sector = 'forestry and land use')")

        #-- Step 3: Delete the subsectors from the sectors table
        cursor.execute("DELETE FROM sectors WHERE sector = 'forestry and land use'")

    insert_countries()
    insert_sectors()
    insert_missing_sectors()
    insert_emissions()
    #delete_problem_data()
#cursor.close()