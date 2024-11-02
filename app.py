from flask import Flask, render_template, request, jsonify
import csv

app = Flask(__name__)

# Load pharmacy data from CSV file into a list of dictionaries
pharmacies = []
with open('on_call_pharmacies.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        pharmacies.append(row)

# Route to home page
@app.route('/')
def index():
    # Extract unique cities
    cities = sorted(set([pharmacy['City'] for pharmacy in pharmacies]))
    return render_template('index.html', cities=cities)

# Route to get districts based on selected city
@app.route('/get_districts', methods=['POST'])
def get_districts():
    selected_city = request.form['city']
    districts = sorted(set([pharmacy['District'] for pharmacy in pharmacies if pharmacy['City'] == selected_city]))
    return jsonify(districts)

# Route to get pharmacies based on city and district
@app.route('/filter_pharmacies', methods=['POST'])
def filter_pharmacies():
    city = request.form['city']
    district = request.form['district']
    filtered_pharmacies = [pharmacy for pharmacy in pharmacies if pharmacy['City'] == city and pharmacy['District'] == district]
    return jsonify(filtered_pharmacies)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
