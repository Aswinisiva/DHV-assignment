# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 17:40:35 2024

@author: Aswini
"""

import matplotlib.pyplot as plt #Importing matplotlib for Data Visualisation
import seaborn as sns #Import the seaborn for statistical data visualization
import pandas as pd #Importing pandas for analysis

def filter_and_process_data(df, indicator_name, countries):
    
    """
    Filter and process data from a DataFrame based on a specified indicator 
    and list of countries.
    Parameters:
    - df (pd.DataFrame): The input DataFrame containing the data.
    - indicator_name (str): The indicator name to filter the data.
    - countries (list): List of country names to filter the data.

    """
    # Filter the dataframe based on indicator name and countries
    data = df[(df["Series Name"] == indicator_name) & (df["Country Name"].
                                                       isin(countries))]
    
    # Rename columns for specific years
    data_re =data.rename(columns={'1995 [YR1995]': '1995', '1996 [YR1996]':
                    '1996','1997 [YR1997]':'1997', '1998 [YR1998]': '1998', 
                    '1999 [YR1999]' :'1999', '2000 [YR2000]':'2000',
                    '2001 [YR2001]':'2001', '2002 [YR2002]': '2002',
                    '2003 [YR2003]': '2003', '2004 [YR2004]': '2004', 
                    '2005 [YR2005]' :'2005', '2006 [YR2006]':'2006', 
                    '2007 [YR2007]':'2007', '2008 [YR2008]':'2008', 
                    '2009 [YR2009]':'2009', '2010 [YR2010]':'2010',
                    '2011 [YR2011]':'2011','2012 [YR2012]':'2012',
                    '2013 [YR2013]': '2013','2014 [YR2014]': '2014'})

    # Drop unnecessary columns
    cln_data = data_re.drop(['Country Code', 'Series Name', 'Series Code'],
                            axis=1).reset_index(drop=True)

    # Transpose the dataframe
    data_t = cln_data.transpose()
    data_t.columns = data_t.iloc[0]
    data_t = data_t.iloc[1:]

    # Set index to numeric and add a 'Years' column
    data_t.index = pd.to_numeric(data_t.index)
    data_t['Years'] = data_t.index
    data_t.reset_index(drop=True, inplace=True)

    return cln_data, data_t


# Create a 2x2 subplot
fig, axes = plt.subplots(2, 2, figsize=(12, 7),facecolor='lightyellow')

# Plot 1: Bar plot
def bar_plot(df, x_value, y_values, head_title, x_label, y_label, ax):
    """
    Generate a bar plot for selected years from a DataFrame.
    - x_value and y_value: lists column name for the x-axis and y-axis values.
    - head_title: The title of the plot.
    - x_label and y_label : Label for the x-axis and Label for the y-axis.
    - ax The subplot to which the plot is assigned.
    """
       
    sns.set_style('whitegrid')
    
    # Filter the DataFrame for specific years
    df_filtered = df[df['Years'].isin([1995,2000, 2007, 2014])]
    
    # Generate the bar plot
    df_filtered.plot(x=x_value, y=y_values, kind='bar', title=head_title,
                     width=0.70, xlabel=x_label, ylabel=y_label, ax=ax)
    
    # Adjust legend position
    ax.legend(loc='best', bbox_to_anchor=(1, 0.8))
    
def pie_plot(df, year, ax=None, autopct='%1.0f%%', fontsize=11):
    
    """
    Generate a pie chart for electricity production from nuclear sources for a 
    specific year.
    - df (pd.DataFrame): Input DataFrame containing electricity production data.
    - year (int): The specific year for which the pie chart is generated.
    - ax (matplotlib.axes._subplots.AxesSubplot): Target subplot. 
    - autopct (str): Format string for autopct parameter in pie chart. 
    """
    
    # 'explode' defines the degree of separation for each wedge in the pie chart.
    explode = (0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.0)
    
    # 'labels' contains the country names associated with each wedge in pie chart.
    labels = ['Netherlands','Mexico','China','Pakistan','Germany','Spain',
                                                              'Argentina']
    
    # Create a pie plot using the filtered DataFrame
    pie = df[str(year)].plot.pie(autopct=autopct,labels=labels, explode=explode,
                startangle=180, wedgeprops={"edgecolor": "black", "linewidth": 
                1.5, "antialiased": True},
                title=f'Electricity production from nuclear source {year}',ax=ax)
    
    # Remove y-label
    pie.set_ylabel('')
    
def line_plot(line_plot_data, title, x_label, y_label, legend_labels, ax):
    
    """Create a line plot from the provided DataFrame.
    Parameters:
        
    - line_plot_data: The input DataFrame containing data for the  line plot.
    - title (str): The title of the line plot.
    - x_label (str): The label for the x-axis.
    - y_label (str): The label for the y-axis.
    - legend_labels (list): A list of labels for the legend."""
    
    line_plot_data.plot(x='Years', y=legend_labels,
                        kind='line', marker='*', markersize=5, ax=ax)
    
    # Set labels and title
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.legend(loc='best', bbox_to_anchor=(1, 0.8))

# Plot 4: Line plot
def horizontal_plot(data_t, countries, year, ax):
    """Create a line plot from the provided DataFrame.
    Parameters:
    - data_t : Transposed DataFrame containing urban population data.
    - countries: List of countries to include in the plot.
    - year: The specific year for which the urban population data is visualized.
    - ax : Target subplot for the bar plot."""
    
    # Extract subset data for the specified year and countries.
    subset_data = data_t[data_t['Years'] == year][countries]
    
    # Melt the data for better visualization in a horizontal bar plot.
    melted_data = subset_data.melt(value_vars=countries, var_name='Country', 
                                               value_name='Production Rate')

    # Create a horizontal bar plot using seaborn
    ax = sns.barplot(data=melted_data, x='Production Rate', y='Country',
                                                     palette='Set1', width=0.7)

    # Set labels and title
    ax.set_xlabel(f'% of total population - {year}')
    ax.set_ylabel('Countries')
    ax.set_title(f'Urban population - {year}')

    # Add actual values inside the bars with black color
    for i, value in enumerate(melted_data['Production Rate']):
        ax.text(value / 2, i, f'{value}%', ha='center', va='center', 
                                                    fontsize=10, color='black')


# Reading the CSV file.
df = pd.read_csv("Electricity.csv")

# List of countries to be analyzed and visualized in the data.
countries = ['Netherlands','Mexico','China','Pakistan','Germany','Spain',
                                                                 'Argentina']

# Extract and process data for indicators across specified countries.
hydr, hydr_t = filter_and_process_data(df, 'Electricity production from hydroelectric sources (% of total)', countries)
nucl, nucl_t = filter_and_process_data(df, 'Electricity production from nuclear sources (% of total)', countries)
gas, gas_t = filter_and_process_data(df, 'Electricity production from natural gas sources (% of total)', countries)
urban, urban_t = filter_and_process_data(df, 'Urban population (% of total population)', countries)

# Visualising the barplot.
bar_plot(hydr_t, 'Years', ['Netherlands','Mexico','China','Pakistan','Germany',
                                                           'Spain','Argentina'],
         'Electricity production from hydroelectric sources', 'Years',
                                        '% of total production', ax=axes[0, 0])

# Visualising the pieplot.
pie_plot(nucl, 2014, ax=axes[0, 1])

# Visualising the lineplot.
line_plot(gas_t, 'Electricity production from natural gas sources', 'Years',
          '% of production', ['Netherlands','Mexico','China','Pakistan', 
                                 'Germany','Spain','Argentina'], ax=axes[1, 0])

# Visualising the horizontal barplot.
horizontal_plot(urban_t, countries, year=2014, ax=axes[1, 1])

# Create 2x2 grid of subplots with specified figure size.
fig.suptitle("Urban Population Growth and Electricity Production",fontsize=16,
             fontweight='bold',color='black',ha='center',va='top',x=0.5,y=1.02,
                 bbox=dict(boxstyle='round', facecolor='lightpink', alpha=0.8))

# Add report text for all subplots at the end
report= (
    """The visual exploration of electricity production and urban population growth across selected countries reveals nuanced patterns and interconnections. 
    Germany appears to dominate in hydroelectric production, maintaining a consistent share over the years. Spain and China also exhibit significant contributions,
    with fluctuations in Mexico and Argentina. The pie chart depicts the distribution of electricity production from nuclear sources in 2014 across the same countries. 
    Spain and Germany emerge as a significant contributor making up a notable share alongside other nation. The line plot displays the trend in electricity production 
    from natural gas sources, the visualization indicates fluctuations in the contributions of each country, with China and Argentina showing distinct patterns. 
    The horizontal bar plot visualizes the urban population for the year 2014 where Argentina stands out with a substantial urban population. The diverse energy 
    production sources and the rapid urbanization in Argentina highlight its dynamic role in the energy landscape and demographic trends."""
    
)

Name = 'ASWINI SIVAKUMAR'
student_id = '22027143'


# Adjust layout and save the figure
fig.text(0.5, -0.09, report, ha='center', va='center', fontsize=12, 
                                     bbox=dict(facecolor='yellow', alpha=0.20))
fig.text(0.5, -0.21, 'Name: {}'.format(Name), ha='center', va='center', 
                                                    fontsize=12, color='black')
fig.text(0.5, -0.24, 'Student id: {}'.format(student_id), ha='center', 
                                     va='center', fontsize=12, color='black')

# Adjust layout for better spacing between subplots.
plt.tight_layout()

#Display the plot
plt.show()


