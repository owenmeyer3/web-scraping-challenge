from bs4 import BeautifulSoup
from requests import get
from splinter import Browser
import pandas as pd
import re

def scrape():
    # Setup splinter------------------------------------
    executable_path = {'executable_path' : 'C:/chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless = False)

    ### Mars News---------------------------------------
    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
    newsURL = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    scrape_results = {}
    # Load page into browser
    browser.visit(newsURL)
    # Find tag for first news headline
    if browser.is_element_present_by_css('div[class="list_text"]', wait_time=5):
        firstSlide = browser.find_by_css('div[class="list_text"]')[0]
        # Find Title and paragraph of headline
        news_title = firstSlide.find_by_css('div[class="content_title"]').text
        news_p = firstSlide.find_by_css('div[class="article_teaser_body"]').text
        scrape_results.update({'news_title':news_title})
        scrape_results.update({'news_p':news_p})
    else:
        print('Page timed out:' + newsURL)
     ## JPL Mars Space Images - Featured Image
    # Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    featureURL = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    # Load page into browser
    browser.visit(featureURL)
    if browser.is_element_present_by_css('a[class="button fancybox"]', wait_time=5):
        # Find full image button tag for featured image
        full_image_button_tag = browser.find_by_css('a[class="button fancybox"]')[0]
        full_image_button_tag.click()
        if browser.is_element_present_by_css('div[class="addthis_toolbox addthis_default_style"]', wait_time=5):
            # Find more info button tag for featured image
            moreInfoButtonTag = browser.find_by_css('div[class="buttons"] a[class="button"]')[0]
            browser.visit(moreInfoButtonTag['href'])
            if browser.is_element_present_by_css('figure[class="lede"]', wait_time=5):
                # Find image url for featured image
                featured_image_tag = browser.find_by_css('img[class="main_image"]')[0]
                featured_image_url = featured_image_tag['src']
                scrape_results.update({'featured_image_url':featured_image_url})
    else:
        print('Page timed out:' + featureURL)
    print(featured_image_url)


    ## Mars Facts---------------------------------------
    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    marsFactsURL = 'https://space-facts.com/mars/'
    browser.visit(marsFactsURL)
    if browser.is_element_present_by_css('tr[class="row-1"]', wait_time=10):
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

        # Use Pandas to convert the data to a HTML table string. (with some table manipulation for aesthetics)
        
        htmlTable = marsFactsDF.to_html()
        htmlTable = htmlTable.replace("dataframe","table")
        htmlTable = htmlTable.replace('<tr style="text-align: right;">',"<tr>")
        htmlTable = htmlTable.replace('<th>unit</th>','<th scope="col">unit</th>')
        htmlTable = htmlTable.replace('<th>value</th>','<th scope="col">value</th>')
        htmlTable=re.sub("<th>[^>]*</th>","",htmlTable)
        htmlTable = htmlTable.replace('<th>','<th scope="row">')
        scrape_results.update({'mars_facts_html_table':htmlTable})
        
    else:
        print('Page timed out:' + marsFactsURL)

    ## Mars Hemispheres---------------------------------------
    # Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
    hemsURL = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemsURL)
    # You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    if browser.is_element_present_by_css('div[class="item"]', wait_time=5):
        # Find small image anchor tags
        smallImageAnchor = browser.find_by_css('div[class="item"] a')

        # Create list of links to full images
        smallImageLinks = []
        for a in smallImageAnchor:
            smallImageLinks.append(a['href'])
        smallImageLinks = list(set(smallImageLinks))

        hemispheresLinks = {}
        #loop through links to full images
        for smallLink in smallImageLinks:
            # browse to page with full image
            browser.visit(smallLink)
            # Find anchor tags in large image downloads container
            if browser.is_element_present_by_css('div[class="downloads"]', wait_time=5):
                fullImageAnchor = browser.find_by_css('div[class="downloads"] a')
                title = browser.find_by_css('h2[class="title"]').text
                title = title.split(" ")
                titleMod = []
                for word in title:
                    if word != "Hemisphere" and word != "Enhanced":
                        titleMod.append(word)
                titleMod = " ".join(titleMod)
                # Add all links in full image download container and append to array if extension is .jpg
                if fullImageAnchor['href'][-4:] == ".jpg":
                    hemispheresLinks.update({titleMod:fullImageAnchor['href']})
            else:
                print('Page timed out:' + smallLink)
        scrape_results.update({'mars_hem_img_urls':hemispheresLinks})
    else:
        print('Page timed out:' + hemsURL)
        


    if scrape_results:
        return scrape_results
    else:
        print('no results')
        return None
    

