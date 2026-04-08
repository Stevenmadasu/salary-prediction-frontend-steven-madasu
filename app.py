from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Existing ML API server URL (Module 12 deployment)
API_URL = "https://salary-predict-smadasu.azurewebsites.net/predict"


@app.route("/")
def index():
    """Render the salary prediction form"""
    return render_template("index.html", prediction=None)


@app.route("/predict", methods=["POST"])
def predict():
    """Collect form data, send to ML API, display result"""
    try:
        payload = {
            "age": int(request.form["age"]),
            "gender": int(request.form["gender"]),
            "country": int(request.form["country"]),
            "highest_deg": int(request.form["highest_deg"]),
            "coding_exp": int(request.form["coding_exp"]),
            "title": int(request.form["title"]),
            "company_size": int(request.form["company_size"]),
        }

        response = requests.post(API_URL, json=payload, timeout=30)
        data = response.json()

        if "predicted_salary" in data:
            prediction = f"${data['predicted_salary']:,.2f}"
        else:
            prediction = f"Error: {data.get('error', 'Unknown error')}"

    except Exception as e:
        prediction = f"Error: {str(e)}"

    return render_template("index.html", prediction=prediction)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
