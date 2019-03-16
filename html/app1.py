#Dependencies
import os
import pickle

import flask

import pandas as pd
import numpy as np
import decimal

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template, json, request
from flask_sqlalchemy import SQLAlchemy
from json_encoder import MyJSONEncoder

app = Flask(__name__)
app.json_encoder = MyJSONEncoder

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/database.sqlite"
db = SQLAlchemy(app)

#Database Model
Base = automap_base()
Base.prepare(db.engine, reflect=True)
Base.classes.keys()

#Reference for each data tables in sqlite
health_conditions = Base.classes.filter

filename = 'finalized_model2.sav'
# Initialize model
def init_model():
    #use pickle to load model
    with open(filename, 'rb') as infile:
        model_loaded = pickle.load(infile)
    #return model
    return(model_loaded)

#initialize model instance
model = init_model()

#Home page
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/health_data")
def healthdata():

    sel = [
        health_conditions.SEQN,
        health_conditions.Gender,
        health_conditions.Age,
        health_conditions.Maritalstatus,
        health_conditions.Generic_Drug_Name,
        health_conditions.Condition,
        health_conditions.Redcelldistributionwidth,
        health_conditions.Redbloodcellcount,
        health_conditions.Hemoglobin,
        health_conditions.Hematocrit,
        health_conditions.Meancellvolume,
        health_conditions.Meancellhemoglobin,
        health_conditions.Plateletcount,
        health_conditions.Meanplateletvolume,
        health_conditions.Whitebloodcellcount,
        health_conditions.Basophilsnumber,
        health_conditions.Eosinophilsnumber,
        health_conditions.Monocytenumber,
        health_conditions.Lymphocytenumber,
        health_conditions.Basophilspercent,
        health_conditions.Eosinophilspercent,
        health_conditions.Segmentedneutrophilspercent,
        health_conditions.Monocytepercent,
        health_conditions.Lymphocytepercent,
        health_conditions.Segmentedneutrophilsnum,
        health_conditions.HepatitisAantibody,
        health_conditions.HepatitisBSurfaceAntibody,
        health_conditions.Cholesterol,
        health_conditions.Globulin
    ]

    results = db.session.query(*sel).all()

    hdata = []
    for result in results:
        hdata.append({
            "id":result[0],
            "gender":result[1],
            "age":result[2],
            "martial_status":result[3],
            "generic_drug_name":result[4],
            "condition":result[5],
            "red_cell_distribution_width":result[6],
            "red_blood_cell_count":result[7],
            "hemoglobin":result[8],
            "hematocrit":result[9],
            "mean_cell_volume":result[10],
            "mean_cell_hemoglobin":result[11],
            "platelet_count":result[12],
            "mean_platelet_volume":result[13],
            "white_blood_cell_count":result[14],
            "basophilis_number":result[15],
            "eosinophils_number":result[16],
            "monocyte_number":result[17],
            "lymphocyte_number":result[18],
            "basophils_percent":result[19],
            "eosinophils_percent":result[20],
            "segmented_netrophils_percent":result[21],
            "monocyte_percent":result[22],
            "lymphocyte_percent":result[23],
            "segmented_neutrophils_num":result[24],
            "hepatitis_A_antibody":result[25],
            "hepatitis_B_surface_antibody":result[26],
            "cholesterol":result[27],
            "globulin":result[28]
     })

    print(hdata)
    return jsonify(hdata)

@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data(request):
    jsdata = request.form['javascript_data']
    print(jsdata)
    return json.loads(jsdata)[0]



@app.route('/result', methods =['POST'])
def result():
    if request.method =='POST':
        result = request.form
        vals = []
        for x in request.form.listvalues():
            if x[0] == "Male" or x[0] == "False":
                val = 0
            elif x[0] == "Female" or x[0] == "True":
                val = 1
            else:
                val = float(x[0])
            vals.append(val)
        # vals.append(1)
        val_array = np.array([vals])
        prediction = model.predict(val_array)
        print(prediction)
        return jsonify(result)




if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)