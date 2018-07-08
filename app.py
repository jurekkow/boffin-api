from flask import Flask, request, jsonify
from flask_cors import CORS

import build_data
import timetable
import ml.recommend


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app)

@app.route("/api/recommend", methods=["POST"])
def make_recommendation():
    data = request.json
    response = ml.recommend.recommend(data["chosenArtists"])
    return jsonify({"recommendation": response})


@app.route("/api/timetable", methods=["GET"])
def get_timetable():
    current_timetable = timetable.get_current_timetable()
    return jsonify(current_timetable)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
