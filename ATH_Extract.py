from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import os
from win10toast import ToastNotifier

# get the name of the Python file
filename = os.path.basename(__file__)

# create a ToastNotifier instance
toaster = ToastNotifier()

# display a toast notification with the filename as the title
toaster.show_toast(f"{filename}", "Start", duration=2)



options = Options()
options.headless = True

driver = webdriver.Firefox(options=options)
# create a new instance of the Firefox driver

url = "https://stockbeep.com/52-week-high-stock-screener-sstime-desc"

# navigate to the page that contains the dynamically generated content
driver.get(url)

# wait for the JavaScript to finish executing
driver.implicitly_wait(10) # wait for up to 10 seconds

# Find the element by CSS selector
element = driver.find_element_by_css_selector("#DataTables_Table_0 > tbody:nth-child(2)")

# Get the inner HTML of the element
html = element.get_attribute("innerHTML")

# close the browser window
driver.quit()

# Parse the HTML code using BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Extract the data from the relevant tags
data = []
for tr in soup.find_all("tr"):
    row = []
    for td in tr.find_all("td"):
        row.append(td.text.strip())
    if row:
        data.append(row)

# Create a pandas dataframe from the extracted data
df = pd.DataFrame(data, columns=["Time", "Code", "Name", "Arrow", "Last", "High", "Change", "Change%", "Volume", "RV", "YTD%", "MC", "Comment"])

# drop all columns except for 'A' and 'B'
df = df.drop(columns=df.columns.difference(['Time', 'Code', 'Last', 'Change%', 'Volume', 'RV']))
df['Last'] = pd.to_numeric(df['Last'])
df['RV'] = pd.to_numeric(df['RV'])
df = df[(df['Last'] > 5) & (df['RV'] > 1)]

# Convert "Time" column to datetime object
df['Time'] = pd.to_datetime(df['Time'], format='%H:%M').dt.time

# select the 'Code' column and join the values with a space separator
codes = ' '.join(df['Code'].tolist())
#print(codes)

# copy the codes to the clipboard
import pyperclip
pyperclip.copy(codes)

# create a ToastNotifier instance
toaster = ToastNotifier()

# display a toast notification with the filename as the title
toaster.show_toast(f"{filename}", "End", duration=2)