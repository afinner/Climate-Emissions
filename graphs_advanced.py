import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression
import queries
import csv
# import os
     
# Create Bar chart
def bar_chart(c):
    
    data = queries.bar_chart_data_dynamic(c)

    # Example data
    # sectors = ["Agriculture", "Buildings", "Fluorinated Gases", "Fossil Fuel Operations", "Forestry and Land Use", 
    #         "Manufacturing", "Mineral Extraction", "Power", "Transportation", "Waste"]
    # co2_emissions = [1500, 2000, 500, 3000, 1000, 2500, 700, 4000, 3500, 800]
    sectors = data[0]
    gas_emissions = data[1]

    # Create a bar chart
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=sectors,
        y=gas_emissions,
        name='CO2 Emissions',
        marker_color='blue'
    ))

    # Customize the layout
    fig.update_layout(
        title='CO2 Emissions by Sector',
        xaxis_title='Sector',
        yaxis_title='CO2 Emissions',
        template='plotly_dark',
        xaxis=dict(
            tickmode='linear'
        )
        # yaxis=dict(
        #     rangemode='tozero'
        # )
    )

    # Show the plot
    return fig


def pie_chart(gas, year):
    data1 = queries.pie_chart_data(gas, year)
    data = {
            'Countries': data1[0],
            'Emissions': data1[2]
            }
        # Create the pie chart
    fig = px.pie(data, names='Countries',
                    values='Emissions',
                    title='Emission Distribution by country') # Show the pie chart
    fig.update_layout(
    title={
        'text': 'Emission Distribution by Country',
        'x': 0.5,  # Center the title horizontally
        'y': 0.95,  # Move the title closer to the top
        'xanchor': 'center',
        'yanchor': 'top'
    })
    fig.update_layout(
        width=600,  # Set the width of the chart
        height=600  # Set the height of the chart
    )
    return fig
def animation():
    data1 = queries.stack_chart_data()
    years = data1[0]
    countries_data = data1[1]
    
    countries = list(countries_data.keys())
    countries1 = []
    years1 = []
    co2_emissions = []

    for year in years:
        for country in countries:
            countries1.append(country)
            years1.append(year)
            co2_emissions.append(countries_data[country][years.index(year)])

    data2 = {
        'Country': countries1,
        'Year': years1,
        'CO2 Emissions': co2_emissions
    }

    df = pd.DataFrame(data2)

    # Create an animated bar chart
    fig = px.bar(df, 
                x='Country', 
                y='CO2 Emissions', 
                color='Country', 
                animation_frame='Year', 
                range_y=[0, max(co2_emissions)], 
                title="CO2 Emissions Over Time by Country")
    
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 3000
    fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 3000    

    return fig
# def animation():
#     data1 = queries.stack_chart_data()
#     co2_emissions = []
#     years = data1[0]

#     countries = data1[1].keys()
#     countries1 = []
#     years1 = []
#     for c in range(len(years)):
#         for i in countries:
#             countries1.append(i) 
#     for j in years:
#         for c in range(len(countries)):
#             years1.append(j)
#     #for i in range(len(data1[1])):
#     for i in countries:
#         for j in range(len(years)):
#             co2_emissions.append((data1[1][i])[j])

#     data2 = {
#         'Country': countries1,
#         'Year': years1,
#         'CO2 Emissions': co2_emissions
#         }
#     #print(data1)
#     df = pd.DataFrame(data2)

#     # Create an animated bar chart
#     fig = px.bar(df, 
#                 x='Country', 
#                 y='CO2 Emissions', 
#                 color='Country', 
#                 animation_frame='Year', 
#                 range_y=[-100000000, 1200000000], 
#                 title="CO2 Emissions Over Time by Country")
    
#     fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 3000
#     fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 3000    

#     return fig
    # Show the figure
    #fig.show()
#animation()

def linear_regression(c):
 
    data1 = queries.projection_chart_data(c) #Returns: list of
    print(data1)
    data = {
        'Year': data1[0],
        'CO2 Emissions': data1[1][c]
    }
    df = pd.DataFrame(data)

    # Creating a linear regression model to project future emissions
    x = df[['Year']]
    y = df['CO2 Emissions']
    model = LinearRegression()
    model.fit(x, y)

    # Projecting future years (replace with your desired range)
    future_years = np.array([i for i in range(2015, 2040)]).reshape(-1, 1)
    projected_emissions = model.predict(future_years)

    # Combine historical and projected data
    projection_df = pd.DataFrame({
        'Year': future_years.flatten(),
        'CO2 Emissions': projected_emissions
    })
    combined_df = pd.concat([df, projection_df])

    # Plotting the data
    fig = go.Figure()

    # Historical data
    fig.add_trace(go.Scatter(x=df['Year'], y=df['CO2 Emissions'], mode='lines+markers', name='Historical CO2 Emissions'))

    # Projected data
    fig.add_trace(go.Scatter(x=projection_df['Year'], y=projection_df['CO2 Emissions'], mode='lines+markers', name='Projected CO2 Emissions', line=dict(dash='dash')))

    # Customize the layout
    fig.update_layout(
        title='CO2 Emissions Over Time with Projections',
        xaxis_title='Year',
        yaxis_title='CO2 Emissions',
        template='plotly'
    )

    fig.update_traces(hovertemplate="Year: %{x}<br>CO2: %{y:.0f}")

    # Show the figure
    # fig.show()
    return fig
#linear_regression('ireland')

def linear_regression_target(c, year):
    target = generate_targets(c)
    data1 = queries.projection_chart_data(c)  # Returns: list of data (adjust as needed)
    
    # Creating a DataFrame with the historical data
    data = {
        'Year': data1[0],
        'CO2 Emissions': data1[1][c]
    }
    df = pd.DataFrame(data)

    # Creating a linear regression model to project future emissions
    x = df[['Year']]
    y = df['CO2 Emissions']
    model = LinearRegression()
    model.fit(x, y)

    # Projecting future years
    future_years = np.array([i for i in range(2015, 2041)]).reshape(-1, 1)
    projected_emissions = model.predict(future_years)

    # Combine historical and projected data
    projection_df = pd.DataFrame({
        'Year': future_years.flatten(),
        'CO2 Emissions': projected_emissions
    })
    combined_df = pd.concat([df, projection_df])

    # Plotting the data
    fig = go.Figure()

    # Adding historical data
    fig.add_trace(go.Scatter(x=df['Year'], y=df['CO2 Emissions'], mode='lines+markers', name='Historical CO2 Emissions'))

    # Adding projected data
    fig.add_trace(go.Scatter(x=projection_df['Year'], y=projection_df['CO2 Emissions'], mode='lines+markers', name='Projected CO2 Emissions', line=dict(dash='dash')))

    # Adding Emission Cut Target line
    fig.add_trace(go.Scatter(x=[2023, year], y=[df['CO2 Emissions'].iloc[-1], target], mode='lines+markers', name='Emission Target', line=dict(color='green', dash='dot')))

    

    # Adding Climate Target line
    fig.add_trace(go.Scatter(x=[2015, 2040], y=[target, target], mode='lines+markers', name='Emission Target Line', line=dict(color='red', dash='dot')))

    # Adding emission target point
    fig.add_trace(go.Scatter(x=[year], y=[target], name="Target", marker=dict(color='red', size=5)))

    # Customize the layout
    # fig.update_layout(
    #     title='CO2 Emissions Over Time with Projections',
    #     xaxis_title='Year',
    #     yaxis_title='CO2 Emissions',
    #     template='plotly',
    #     shapes=[
    #         dict(
    #             type='line',
    #             y0=-250000000, y1=-250000000,
    #             x0=2015, x1=2040,
    #             line=dict(
    #                 color='Red',
    #                 width=4,
    #                 dash='dot',
    #             ),
    #         )
    #     ]
    # )
    fig.update_layout(
        title='CO2 Emissions Over Time with Projections',
        xaxis_title='Year',
        yaxis_title='CO2 Emissions',
        template='plotly'
    )

    fig.update_traces(hovertemplate="Year: %{x}<br>CO2: %{y:.0f}")

    return fig
def calculate_cut(c, target1):
    data1 = queries.projection_chart_data(c)
    year = data1[0][len(data1[0])-1]
    data_point = data1[1][c][len(data1[1][c])-1]
    target = generate_targets(c)
    #target = target*(10**6)
    years = target1 - year
    emissions = data_point - target
    cut = (emissions / years)
    return cut

def calculate_sector(c):
    data= queries.bar_chart_data_dynamic(c)
    sectors = data[0]
    gas_emissions = data[1]
    max_index = 0
    for i in range(1, len(gas_emissions)):
        if gas_emissions[i] > gas_emissions[max_index]:
            max_index = i
    return sectors[max_index]    

def generate_targets(country):
    with open("climate_targets.csv", 'r') as fileR:
        reader = csv.reader(fileR)
        header = next(reader)
        data = {}
        for row in reader:
            data[row[0].lower()] = ((1-(float(row[1])/100))*(float(row[2])))*(10**6)
    return data[country]

# def create_table(year, gas):
#     data = queries.create_table_data(year, gas)
#     countries =data[0]
#     population = data[1]
#     emissions = data[2]
#     indices = list(range(len(emissions)))

#     # Sort the indices based on the emissions values in descending order
#     for i in range(len(indices)):
#         for j in range(i + 1, len(indices)):
#             if emissions[indices[i]] < emissions[indices[j]]:
#                 indices[i], indices[j] = indices[j], indices[i]

#     # Create sorted lists based on the sorted indices
#     sorted_countries = [countries[i] for i in indices]
#     sorted_population = [population[i] for i in indices]
#     sorted_emissions = [emissions[i] for i in indices]
#     actual_population = []
#     for i in range(len(sorted_emissions)):
#         j = (sorted_emissions[i]/(sorted_population[i]*(10**6)))
#         j = round(j, 3)
#         actual_population.append(j)

#     return (sorted_countries, actual_population, sorted_emissions)



def sort_by_emissions(item):
    return item[2]

def sort_by_capita(item):
    return item[1]

def sort_by_countries(item):
    return item[0]

def create_table(gas, year, sort_key="emissions"):
    data = queries.create_table_data(gas, year)
    countries = data[0]
    population = data[1]
    emissions = data[2]

    # Debugging: Print the input lists
    print(f"Countries: {countries}")
    print(f"Population: {population}")
    print(f"Emissions: {emissions}")

    actual_population = [(emission / (pop * 10**6)) for emission, pop in zip(emissions, population)]
    actual_population = [round(val, 3) for val in actual_population]

    # Create a combined list
    combined_list = list(zip(countries, actual_population, emissions))
    
    # Debugging: Print the combined list
    print(f"Combined List: {combined_list}")
    
    # Check if the combined_list is not empty before sorting
    if not combined_list:
        return [], [], []

    # Sort based on the sort_key
    if sort_key == "emissions":
        combined_list.sort(key=sort_by_emissions, reverse=True)
    elif sort_key == "capita":
        combined_list.sort(key=sort_by_capita, reverse=True)
    elif sort_key == "countries":
        combined_list.sort(key=sort_by_countries)

    sorted_countries, sorted_actual_population, sorted_emissions = zip(*combined_list)
    
    return sorted_countries, sorted_actual_population, sorted_emissions




# Example usage
#linear_regression_target('spain')  # Adjust the parameter based on your data structure


# Add hover functionality to display Year and Growth Rate values
# fig.update_traces(hovertemplate="Year: %{x}<br>Growth Rate: %{y:.2f}%")
# Save the interactive line chart as an HTML file in the templates folder
# fig.write_html("templates/"+filename)  # Save as HTML

def generate_bar(c):
    filename = 'bar_chart.html'
    fig = bar_chart(c)    
    fig.write_html("templates/"+filename) 
    return filename

def generate_graph(c):
    filename = 'emissions.html'
    fig = linear_regression(c)
    fig.write_html("templates/"+filename) 
    return filename

def generate_projections(c, year):
    filename = 'emissions_projected.html'
    fig = linear_regression_target(c, year) #[0]
    fig.write_html("templates/"+filename) 
    return filename

def generate_animation():
    filename = 'animation.html'
    fig = animation()
    fig.write_html("templates/"+filename) 
    return filename

def generate_pie_chart(gas, year):
    filename = 'pie_chart.html'
    fig = pie_chart(gas, year)
    fig.write_html("templates/"+filename) 
    return filename
# generate_bar(1, 99)
# generate_graph()
#generate_animation()
#generate_pie_chart('co2', '2019')
#generate_projections('spain')
#generate_bar("ireland")