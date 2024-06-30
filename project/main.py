from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from .models import Result
import os, pandas
from . import db


main = Blueprint('main', __name__)

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
        return "OK", 200
    else:
        return "missing or wrong secret key", 418



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