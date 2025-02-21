# LC-Project-Climate-Emissions
# Analyzing Climate Emissions of Different Countries in the EU

## Overview
This project aims to analyze climate emissions data of various countries in the European Union (EU). The project involves downloading CSV files from the internet, cleaning the data, storing it in a MySQL database, and creating a Flask application with a user-interface website. The website provides information on the project, dynamic graphical representations of the data, and custom recommendations for each country regarding their progress in meeting emission targets.

## Features
- **Data Download and Cleaning**: Automated downloading and cleaning of climate emissions data from various sources.
- **MySQL Database Storage**: Storing the cleaned data in a MySQL database for efficient querying and analysis.
- **Flask Application**: Developing a Flask web application to serve the user interface.
- **User Interface**: A website that provides:
  - Information about the project.
  - Dynamic graphical representations of the data.
  - Custom recommendations for each country on their emission targets, required cuts per year, and the highest greenhouse gas emission sectors.

## Technologies Used
- **Python**: For data processing and backend development.
- **Pandas**: For data cleaning and manipulation.
- **MySQL**: For database storage.
- **Flask**: For developing the web application.
- **HTML/CSS/JavaScript**: For the user interface.
- **Matplotlib/Plotly**: For dynamic graphical representations.

## File Structure
eu-climate-emissions/   
│  
├── templates/                  # HTML templates for Flask  
│
├── static/  
│   ├── css/                     # CSS files   
│   └── js/                      # JavaScript files  
│  
├── data.csv                     # csv file for each countries data  
│  
├── app.py                       # Flask application  
├── config.py                    # Configuration file for database credentials  
├── load_tables.py               # Script for downloading and cleaning data   
├── load_database.py             # Script for sending data to database  
├── queries.py                   # Script for querying database  
├── graphs_advanced.py           # Script for generating dynamic graphs  
<!--- ├── requirements.txt             # List of required Python packages --->
└── README.md                    # Project README file  

## Getting Started
### Prerequisites
- Python 3.x
- MySQL
- Flask
- Pandas
- Matplotlib/Plotly

<!--- ### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/eu-climate-emissions.git --->
