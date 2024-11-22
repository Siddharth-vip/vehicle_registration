from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)

# MongoDB setup
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['vehicle_registration']
    collection = db['vehicles']
    print("Connected to MongoDB successfully")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register_vehicle():
    try:
        data = request.json
        vin = data.get('vin')
        owner_name = data.get('owner_name')
        vehicle_model = data.get('vehicle_model')
        year = data.get('year')
        
        if collection.find_one({"vin": vin}):
            return jsonify({"error": "Vehicle with this VIN already exists."}), 400
        
        collection.insert_one({
            "vin": vin,
            "owner_name": owner_name,
            "vehicle_model": vehicle_model,
            "year": year
        })
        return jsonify({"message": "Vehicle registered successfully!"}), 201
    except Exception as e:
        print(f"Error registering vehicle: {e}")
        return jsonify({"error": "An error occurred during registration"}), 500

@app.route('/vehicle/<vin>', methods=['GET'])
def get_vehicle(vin):
    try:
        vehicle = collection.find_one({"vin": vin})
        if vehicle:
            return dumps(vehicle), 200
        return jsonify({"error": "Vehicle not found."}), 404
    except Exception as e:
        print(f"Error retrieving vehicle: {e}")
        return jsonify({"error": "An error occurred during retrieval"}), 500

@app.route('/vehicles', methods=['GET'])
def list_vehicles():
    try:
        vehicles = collection.find()
        return dumps(vehicles), 200
    except Exception as e:
        print(f"Error listing vehicles: {e}")
        return jsonify({"error": "An error occurred during listing"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
