from flask import Flask, request, jsonify

from ml.recommend import recommend

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route("/api/recommend", methods=["POST"])
def make_recommendation():
    data = request.json
    response = recommend(data["chosenArtists"])
    return jsonify({"recommendation": response})


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
