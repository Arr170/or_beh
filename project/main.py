from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from .models import *
import os, pandas
from . import db
import logging
from logging.handlers import *


main = Blueprint('main', __name__)

# logger = logging.getLogger("")

# consoleHandler = logging.StreamHandler()
# logger.addHandler(consoleHandler)

# fileHandler= RotatingFileHandler(filename="app.log")
# logger.addHandler(fileHandler)


@main.route('/results_edit', methods=["PUT"])
@login_required
def results_edit():
    if request.method == 'PUT':
        None
    
@main.route('/rslt_remove/<id>', methods=["DELETE"])   
@login_required
def rslt_remove(id):
    try:
        record = Result.query.get(id)
        db.session.delete(record)
        db.session.commit()
        return "ok"
    except:
        print("nah, delete doesnt work")

@main.route('/rslt_change/<id>', methods=["PUT"])
@login_required
def rslt_change(id):
    try:
        data = request.get_json()
        record = Result.query.get(id)
        record.name = data.get('name')
        db.session.commit()
        return "ok"
    except Exception as e:
        print("nah, put doesnt work", e)
        return 500
    


@main.route('/external_rslts_upload', methods = ["POST"])
def ext_rslt_post():
    data = request.get_json()
    if(data["secret"] == os.environ["SECRET_POST"]):
        new_result=Result(name=data["name"], time = data["time"], track = data["track"], date = data["date"])
        db.session.add(new_result)
        db.session.commit()
        return_data={
            "id": new_result.id
        }
        return jsonify(return_data), 200
    else:
        return "missing or wrong secret key", 418

@main.route('/tracks', methods = ["GET"])
@login_required
def tracks():
    return render_template('track_mng.html')
    
@main.route('/tracks_data', methods=["GET", "POST"])
#@login_required
def tracks_data():
    if request.method == "GET":
        tracks = Track.query.all()
        print(tracks)  # List of Point objects
        data = [row.to_dict() for row in tracks]
        # for row in tracks:
        #     print(row.to_dict())
        #print(data)

        return jsonify(data)
    else:
        print("post tracks data")
        data = request.get_json()
        new_track = Track(name=data["name"])
        db.session.add(new_track)
        db.session.commit()

        for i in range(1, 256):
            point_key = "point" + str(i)
            print(point_key)
            if point_key in data:
                print(data[point_key])
                new_point = Point(number=data[point_key], track_id = new_track.id)
                db.session.add(new_point)
        db.session.commit()

        return jsonify({"message": "Track and points added successfully"})


@main.route('/tracks_delete/<id>', methods=["DELETE"])
@login_required
def tracks_delete(id):
    try:
        record = Track.query.get(id)
        for point in record.points:
            db.session.delete(point)
        print(record)
        db.session.delete(record)
        db.session.commit()
        return "ok"
    except Exception as e:
        #print("nah, delete doesnt work")
        return "error", 500

@main.route('/data', methods=['GET'])
def data():
    args_search = request.args
    # check is request contains args
    # if args are present, edit search to search by name
    query = Result.query.order_by(Result.time.asc())

    if args_search.__contains__("name"): # jestli je argument jmena, filtruje podle jmena
        name = args_search["name"]
        query = query.filter(Result.name.contains(f'{name}'))

    if args_search.__contains__("track"): # jeslti je argument trate, filtruje podle trate
        track = args_search["track"]
        query = query.filter(Result.track.contains(f'{track}'))   

    if args_search.__contains__("date"):
        date = args_search["date"]
        query = query.filter(Result.date.contains(f'{date}'))

    table = query.all()
         
    data = [row.to_dict() for row in table]
    #print(data)
    return jsonify(data)
 
    


    

@main.route('/', methods=['GET'])
def table():
    return render_template("rslt_table.html")   