from turtle import distance
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

# NASA Exoplanet URL
START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"

# Webdriver
browser = webdriver.Chrome("/Users/mayanktyagi/Desktop/Whitehat/Projects/Project_127/chromedriver_mac64/chromedriver")
browser.get(START_URL)

time.sleep(10)

scraped_data = []

# Define Exoplanet Data Scrapping Method
def scrape():

    bright_star_table =  soup.find("table", attrs={"class", "wikitable"})
    table_body = bright_star_table.find('tbody')
    table_rows = table_body.find_all("tr")

    for row in table_rows:
        table_cols = row.find_all('td')
        print(table_cols)
        
        # BeautifulSoup Object     
        soup = BeautifulSoup(browser.page_source, "html.parser")
        temp_list = []

        # Loop to find element using XPATH  
        for col_data in table_cols:

            print(col_data.text)
           
            data = col_data.text.strip()
            print(data)

            temp_list.append(data)
            
        scraped_data.append(temp_list)

stars_data = []
new_stars_data = []

for i in range(0,len(scraped_data)):

    Star_names = scraped_data[i][1]
    Distance = scraped_data[i][3]
    Mass = scraped_data[i][5]
    Radius = scraped_data[i][6]
    Lum = scraped_data[i][7]

    required_data = [Star_names, Distance, Mass, Radius, Lum]
    stars_data.append(required_data)

    # Find all elements on the page and click to move to the next page
    browser.find_element(by=By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

# Calling Method    
scrape()

# Define Header
headers = ['Star_Name', 'Distance', 'Mass', 'Radius', 'Luminosity']

# Define pandas DataFrame   
star_df_1 = pd.DataFrame(stars_data, columns=headers)

new_star_df_1 = pd.DataFrame(new_stars_data, columns=headers)

# Convert to CSV
star_df_1.to_csv('scraped_data.csv',index=True, index_label="id")

new_star_df_1.to_csv('scraped_data.csv',index=True, index_label="id")

def scrape_more_data(hyperlink):
    print(hyperlink)
    
    ## ADD CODE HERE ##
    try:
        page=requests.get(hyperlink)
        soup = BeautifulSoup(page.content,"html.parser")
        temp_list = []
        for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tags.find_all("div",attrs={"class":"value"})[0].contents[0])
                except:
                    temp_list.append("")
        stars_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

star_df_1.drop(columns=['discovery_date', 'mass', 'detection_method'],inplace=True)
star_df_1.head()
headers = ["name","light_years_from_earth","planet_mass","stellar_magnitude","discovery_date","hyperlink","planet_type","discovery_date","mass","planet_radius","orbital_period","eccentricity","detection_method"]
final_star_df = pd.DataFrame(columns=headers)
final_star_df = pd.merge(star_df_1,new_star_df_1)
final_star_df.head()
final_star_df.to_csv('final_scraped_data.csv')
archive_star_df = pd.read_csv('/content/PRO-NASA-Exoplanet-Scraped-Data/PSCompPars.csv')
archive_star_df.head()
merge_star_df = pd.merge(final_star_df,archive_star_df,on="id")
merge_star_df.columns()
merge_star_df.to_csv('merge_star.csv')
mass = merge_star_df.mass() * 0.000954588
radius = merge_star_df.radius() * 0.102763
