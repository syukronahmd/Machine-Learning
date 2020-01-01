import pickle
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)
model = pickle.load(open('gempa.sav', 'rb'))

@app.route("/")
def home():
	return render_template("home.html")

@app.route("/visualization")
def visualization():
	return render_template("visualization.html")

@app.route("/classification", methods=["GET", "POST"])
def classification():
	if request.method == "POST":
		latitude = request.form.get('latitude') or 0
		longitude = request.form.get('longitude') or 0
		depth = request.form.get('depth') or 0
		magnitude = request.form.get('magnitude') or 0

		features = [[latitude, longitude, depth, magnitude]]
		df = pd.DataFrame(features, columns=['Latitude', 'Longitude', 'Depth', 'Magnitude'])
		binary_value = str([i for i in model.predict(df)][0])
		
		result = "Earthquake" if binary_value == "1" else "Not Earthquake"

		return render_template("classification.html", result=result)
	return render_template("classification.html")

if __name__ == "__main__":
	app.run()