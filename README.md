# Overview
This project performs web scraping of Nasa Mars pages, stores data in a noSQL database and writes data to a Flask webpage. The project uses Jupyter Notebooks, BeautifulSoup, Flask, pandas, requests and splinter to complete all tasks. MongoDB is used as the noSQL database.

## Step 1 - Scraping

### NASA Mars News

* Scrapes the NASA Mars News Site (https://mars.nasa.gov/news/) and collects the latest news title and paragraph text. 

### JPL Mars Space Images - Featured Image

* Visits the url for JPL Featured Space Image (https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).

* Navigates the site and finds the image url for the current featured Mars image.

### Mars Facts

* Visits the Mars facts webpage (https://space-facts.com/mars/) and scrapes the table containing facts about the planet including diameter, mass, etc.

* Converts the data to a HTML table string.

![](webCapture1.png)

### Mars Hemispheres

* Visits the USGS Astrogeology site (https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtains high resolution images for each of Mars' hemispheres.

* Saves both the image url string for the full resolution hemisphere image, and the hemisphere title containing the hemisphere name.

* Appends the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.

![](webCapture2.png)
- - -

## Step 2 - MongoDB and Flask Application

* Duplicates the Jupyter notebook functionality in `scrape_mars.py` with a function called `scrape` that will execute all scraping code from above and return one python dictionary containing all of the scraped data.

* Creates a route called `/scrape` that will import `scrape_mars.py` script and call the `scrape` function.

  * Stores the return value in Mongo as a Python dictionary.

* Creates a root route `/` that will query the Mongo database and pass the Mars data into an HTML template to display the data.

* Creates a template HTML file called `index.html` that will take the Mars data dictionary and display all of the data in the appropriate HTML elements.
