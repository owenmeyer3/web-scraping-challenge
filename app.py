from flask import Flask, render_template
import scrape_mars
import pymongo

app = Flask('__name__')

app.static_folder = 'static'

newsURL = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
featureURL = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
marsFactsURL = 'https://space-facts.com/mars/'

@app.route('/scrape')
def scrape_route():
    # scrape results to put in database
    scrape_results = scrape_mars.scrape()

    # connect to db
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    # create db
    marsDB = myclient["marsDB"]
    # create collection in db
    marsColl = marsDB["marsColl"]
    # Clear Collection
    marsColl.remove({})
    # Insert Data
    marsColl.insert_one(scrape_results)

    return '<div>Mars Data Added</div><a href="/">Go Back</a>'

@app.route('/')
def root_route():
    # connect to db
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    # create db
    marsDB = myclient["marsDB"]
    # create collection in db
    marsColl = marsDB["marsColl"]

    # find one result in the database (no filter, as we only uploading one dictionary)
    try:
        found_dict = marsColl.find_one({})
    except:
        print('no dictionary found')
        
    if not found_dict:
        found_dict = {
            'news_title':"",
            'news_p':"",
            'featured_image_url':"",
            'marsEqDia':"",
            'marsPolDia':"",
            'marsMass':"",
            'marsMoons':"",
            'marsOrbDist':"",
            'marsOrbPer':"",
            'marsSurfTemps':"",
            'marsFirstRecord':"",
            'marsRecBy':"",
            'mars_facts_html_table':"",
            'mars_hem_img_urls':{
                '1':"",
                '2':"",
                '3':'',
                '4':''
            }
        }
        
    return render_template('index.html',
    news_title = found_dict['news_title'],
    news_p = found_dict['news_p'],
    featured_image_url = found_dict['featured_image_url'],
    marsEqDia = found_dict['marsEqDia'],
    marsPolDia = found_dict['marsPolDia'],
    marsMass = found_dict['marsMass'],
    marsMoons = found_dict['marsMoons'],
    marsOrbDist = found_dict['marsOrbDist'],
    marsOrbPer = found_dict['marsOrbPer'],
    marsSurfTemps = found_dict['marsSurfTemps'],
    marsFirstRecord = found_dict['marsFirstRecord'],
    marsRecBy = found_dict['marsRecBy'],
    mars_facts_html_table = found_dict['mars_facts_html_table'],
    mars_hem_0_title = list(found_dict['mars_hem_img_urls'].keys())[0],
    mars_hem_1_title = list(found_dict['mars_hem_img_urls'].keys())[1],
    mars_hem_2_title = list(found_dict['mars_hem_img_urls'].keys())[2],
    mars_hem_3_title = list(found_dict['mars_hem_img_urls'].keys())[3],
    mars_hem_0_pic = found_dict['mars_hem_img_urls'][list(found_dict['mars_hem_img_urls'].keys())[0]],
    mars_hem_1_pic = found_dict['mars_hem_img_urls'][list(found_dict['mars_hem_img_urls'].keys())[1]],
    mars_hem_2_pic = found_dict['mars_hem_img_urls'][list(found_dict['mars_hem_img_urls'].keys())[2]],
    mars_hem_3_pic = found_dict['mars_hem_img_urls'][list(found_dict['mars_hem_img_urls'].keys())[3]]
    )

app.run(port = '5000', debug = True)