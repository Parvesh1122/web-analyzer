from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

load_dotenv()  

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

@app.route("/")
def home():
    return render_template("index.html", show_result=False)

@app.route("/analyze", methods=["POST"])
def analyze():

    user_url = request.form.get("url")

    if not user_url:
        return "Please enter a valid URL"

    if not user_url.startswith("http"):
        user_url = "https://" + user_url

    api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={user_url}&strategy=desktop&category=performance&category=accessibility&category=best-practices&category=seo&key={API_KEY}"    
    res = requests.get(api_url, timeout=10)
    data = res.json()

    if "lighthouseResult" not in data:
        return render_template("index.html", show_result=False, error="Failed to fetch data. Try again.")
    lighthouse = data["lighthouseResult"]["categories"]

    performance = lighthouse.get("performance", {}).get("score", 0) * 100
    seo = lighthouse.get("seo", {}).get("score", 0) * 100
    accessibility = lighthouse.get("accessibility", {}).get("score", 0) * 100
    best_practices = lighthouse.get("best-practices", {}).get("score", 0) * 100

    overall = int((performance + seo + accessibility + best_practices) / 4)

    print(lighthouse)

    return render_template(
        "index.html",
        performance=performance,
        seo=seo,
        accessibility=accessibility,
        best_practices=best_practices,
        overall=overall,
        show_result=True
    )

@app.route("/upload", methods=["POST"])
def upload():
    return "Coming soon"


     

