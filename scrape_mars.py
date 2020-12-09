from bs4 import BeautifulSoup
from requests import get
from splinter import Browser
import pandas as pd

def scrape():
    # Setup splinter------------------------------------
    executable_path = {'executable_path' : 'C:/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless = False)

    ### Mars News---------------------------------------
    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
    newsURL = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Load page into browser
    browser.visit(newsURL)
    # Get Html code as BS object from browser
    newsObj = BeautifulSoup(browser.html, 'html.parser')
    # Find tag for first news headline
    if browser.is_element_present_by_tag('html', wait_time=10):
        firstSlide = newsObj.find('li', class_='slide')
        # Find Title and paragraph of headline
        news_title = firstSlide.find('h3').text
        news_p = firstSlide.find(class_='rollover_description_inner').text
        scrape_results = {'news_title':news_title, 'news_p':news_p}
    else:
        print('Page timed out:' + newsURL)
    ## JPL Mars Space Images - Featured Image-----------
    # Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    featureURL = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # Load page into browser
    browser.visit(featureURL)
    if browser.is_element_present_by_tag('html', wait_time=10):
        # Find article tag for featured image
        featured_image_tag = browser.find_by_css('div[class="carousel_items"] article')
        # Take style attribute, split string by quotes and take the url from index 1
        featured_image_url = featured_image_tag['style'].split('"')[1] 
        scrape_results.update({'featured_image_url':featured_image_url})
    else:
        print('Page timed out:' + featureURL)

    ## Mars Facts---------------------------------------
    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    marsFactsURL = 'https://space-facts.com/mars/'
    if browser.is_element_present_by_tag('html', wait_time=10):
        marsFactsDF = pd.read_html(marsFactsURL)[0]
        marsFactsDF = marsFactsDF.rename(columns = {0:'unit', 1:'value'})

        marsEqDia = marsFactsDF[marsFactsDF['unit'] == 'Equatorial Diameter:']['value'].values[0]
        marsPolDia = marsFactsDF[marsFactsDF['unit'] == 'Polar Diameter:']['value'].values[0]
        marsMass = marsFactsDF[marsFactsDF['unit'] == 'Mass:']['value'].values[0]
        marsMoons = marsFactsDF[marsFactsDF['unit'] == 'Moons:']['value'].values[0]
        marsOrbDist = marsFactsDF[marsFactsDF['unit'] == 'Orbit Distance:']['value'].values[0]
        marsOrbPer = marsFactsDF[marsFactsDF['unit'] == 'Orbit Period:']['value'].values[0]
        marsSurfTemps = marsFactsDF[marsFactsDF['unit'] == 'Surface Temperature:']['value'].values[0]
        marsFirstRecord = marsFactsDF[marsFactsDF['unit'] == 'First Record:']['value'].values[0]
        marsRecBy = marsFactsDF[marsFactsDF['unit'] == 'Recorded By:']['value'].values[0]
        scrape_results.update({
            'marsEqDia':marsEqDia,
            'marsPolDia':marsPolDia,
            'marsMass':marsMass,
            'marsMoons':marsMoons,
            'marsOrbDist':marsOrbDist,
            'marsOrbPer':marsOrbPer,
            'marsSurfTemps':marsSurfTemps,
            'marsFirstRecord':marsFirstRecord,
            'marsRecBy':marsRecBy
        })

        # Use Pandas to convert the data to a HTML table string.
        htmlTable = marsFactsDF.to_html()
        scrape_results.update({'mars_facts_html_table':htmlTable})
        ## Mars Hemispheres
    else:
        print('Page timed out:' + marsFactsURL)
        
    # Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
    if scrape_results:
        return scrape_results
    else:
        print('no results')
        return None

