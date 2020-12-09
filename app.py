from flask import Flask, render_template
import scrape_mars
import pymongo

app = Flask('__name__')
a = '''
@app.route('/scrape')
def scrape_route():
    scrape_results = scrape_mars.scrape()

    return render_template('index.html',
        news_title = scrape_results['news_title'],
        news_p = scrape_results['news_p'],
        featured_image_url = scrape_results['featured_image_url'],
        marsEqDia = scrape_results['marsEqDia'],
        marsPolDia = scrape_results['marsPolDia'],
        marsMass = scrape_results['marsMass'],
        marsMoons = scrape_results['marsMoons'],
        marsOrbDist = scrape_results['marsOrbDist'],
        marsOrbPer = scrape_results['marsOrbPer'],
        marsSurfTemps = scrape_results['marsSurfTemps'],
        marsFirstRecord = scrape_results['marsFirstRecord'],
        marsRecBy = scrape_results['marsRecBy'],
        mars_facts_html_table = scrape_results['mars_facts_html_table'],
        )
'''

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

    # Insert Data
    marsColl.insert_one(scrape_results)

    return "Mars data added to mongo database"

@app.route('/')
def root_route():
    # connect to db
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    # create db
    marsDB = myclient["marsDB"]
    # create collection in db
    marsColl = marsDB["marsColl"]

    # find one result in the database (no filter, as we only uploading one dictionary)
    found_dict = marsColl.find_one({})

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
    )

app.run(port = '5000', debug = True)
