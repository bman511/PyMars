from flask import Flask, render_template
from scrape_mars import scrape
import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db


# Set route
@app.route('/scrape')

def run_scrape():

    # Drops collection if available to remove duplicates
    db.mars_info.drop()

    info_dict = scrape()

    # Creates a collection in the database and inserts two documents
    db.mars_info.insert_one(info_dict)

    message = '<h1>Database has been updated</h1>'
    
    return message


# Set route
@app.route('/')
def index():
    # Retrive the entire team collection from mongodb
    mars_dict = db.mars_info.find_one()
    #print(mars_dict)

    # Return the template with the teams list passed in
    return render_template('index.html', mars_data=mars_dict)


if __name__ == "__main__":
    app.run(debug=True)
