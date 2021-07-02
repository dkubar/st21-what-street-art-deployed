from geopy.distance import geodesic
import pandas as pd
from flask import Flask, jsonify, request
import json

# Function to get street art close to a set of coordinates
def get_close_objects(lat, lng):
    input_coord = (lat, lng)
    df_final = pd.read_csv('data_final.csv')
    result = []
    for index, row in df_final.iterrows():
        location_coord = (row["location_lat"], row["location_lng"])
        distance = geodesic(location_coord, input_coord).km
        if distance <= 2:
            result.append({"id": index, "distance": distance})
    return result

# Function to load list of dictionaries of artworks ranked by similarity
def load_rankings():
    with open('liked_rankings.json') as rankings_file:
        similarity_dict = json.load(rankings_file)
        return similarity_dict

app = Flask(__name__)

# Route homepage
@app.route('/', methods=['GET'])
def home():
    return '''<h1>A prototype API for WSA 'You Might Also Like' and 'Near You' features.</h1><p></p>'''

# Route "near-you" function
@app.route('/near-you', methods = ['GET'])
def near_you():
    latitude = request.args['lat']
    longitude = request.args["lng"]
    response = jsonify(get_close_objects(latitude, longitude))
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# Route "you may also like" function
@app.route('/ymal', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."

    # Load list of dictionaries of artworks ranked by similarity.
    rankings = load_rankings()
    # Create an empty list for results
    results = []
    # Loop through the data and match 5 closest results that fit the requested ID.
    for i in range(5):
                similar_artwork = rankings[id][i]
                results.append(similar_artwork)
    response = jsonify(results)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    app.run(debug=True)
