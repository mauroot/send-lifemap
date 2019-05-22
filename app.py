from flask import Flask, request, jsonify, render_template, send_file, Response
from connect_database import connect_mongo, get_lifemap
from twilio_helpers import send_template, send_messages
import pdfkit

app = Flask(__name__)


@app.route("/")
def hello_world():
    db = connect_mongo()
    family = db["family"]
    # exclude _id Mongo's ObjectID field for correct jsonification
    query = list(family.find({}, {"_id": 0}))
    return jsonify(query)


@app.route("/send-initial-message", methods=["POST"])
def send_inital_message():
    from_number = request.form["from"]
    return jsonify(send_template(from_number))


@app.route("/send-reminders", methods=["POST"])
def send_reminder():
    return jsonify(send_messages())


@app.route("/send-lifemap", methods=["GET", "POST"])
def send_lifemap():
    phone_number = "+595 000 000 000"
    lifemap = get_lifemap(phone_number)
    print(lifemap)
    return send_file(lifemap)


@app.route("/render-template", methods=["GET", "POST"])
def render_graphic():
    return render_template("grafic.html")

@app.route("/render-template/<string:number>", methods=["GET", "POST"])
def number_graphic(number):
    print(number)
    values = {}
    db = connect_mongo()
    lifemap = db.family.find_one({"phoneNumber":number})
    if lifemap:
        for v in range(1,4):
            key = float(v)
            values[key]=sum(value == key for value in lifemap.values())

    return render_template("chart_values.html", semaforo=values, lifemap=lifemap)

@app.route("/generate-pdf/<string:number>")
def pdfnetor(number):
    pdf = pdfkit.from_url(
        f"http://localhost:5000/render-template/{number}", 
        f"{number}.pdf", 
        options={"javascript-delay":2000})
    print(pdf,"!!!!!!!!!!!!")
    return send_file(f"{number}.pdf")
    #return jsonify(pdf)

if __name__ == "__main__":
    app.run(debug=True)
