
import os
from game import *
from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app

tickets = os.getenv("tickets").split(",")

# Initialize Flask App
app = Flask(__name__)
cred = credentials.Certificate("datomar-hackson-firebase-adminsdk-uq2cm-7cd46a5958.json")
fb_app = initialize_app(cred)

db = firestore.client()
players = db.collection('players')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        id = request.json['id']
        name = request.json['name']
        code = request.json['code']
        if id in tickets:
            compile(code,"","exec")
            players.document(id).set(request.json)
            return jsonify({"success": True}), 200
        else:
            return f"Invalid Ticket #: {id}" 
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/judge', methods=['POST'])
def judge():
    try:
        simulation = simulate(False)
        all = [doc.to_dict() for doc in players.stream()]
        for a in all:
            id = a["id"]
            disply_name = a["name"]
            code = a["code"]
            if id in tickets:
                simulation.add(id, disply_name, code) 
        result = simulation.simulate(50000) 
        return jsonify(result), 200
    except Exception as e:
        return f"An Error Occured: {e}"