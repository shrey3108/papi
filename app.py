import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables from .env
load_dotenv()

# Get Supabase credentials from environment
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

@app.route('/locations', methods=['GET'])
def get_locations():
    try:
        response = supabase.table("crime_reports").select("latitude, longitude, crime_type").execute()

        data = [
            {
                "lat": row.get('latitude'),
                "lng": row.get('longitude'),
                "type": row.get('crime_type')
            }
            for row in response.data
            if row.get('latitude') and row.get('longitude') and row.get('crime_type')
        ]

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)

