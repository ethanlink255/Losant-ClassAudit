from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, escape
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required, login_manager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_socketio import SocketIO, send, emit

from rest import app, db, User, Students_out, Students, Classes, Log, Dashboard
from forms import LoginForm, RegistrationForm

import requests
import json

def index_dashboards():
    dashboards = Dashboard.query.all()
    data = []

    for _dashboard in dashboards:
        data.append({"caption" : _dashboard.description, "href" : url_for('dashboard', id = _dashboard.dashboard_id, _external=True) })

    return data



@app.route('/')
@login_required
def index():
    
    return render_template("dashboard.html", dashboards = index_dashboards(), page_title = "Home", dashboard_id = "5da88e1562cf9d0006d740f2")

@app.route('/dashboard')
def dashboard():
    if "id" in request.args:
        return render_template("dashboard.html", dashboard_id = escape(request.args.get("id")))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index', _external=True))
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login', _external=True))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index', _external=True))
    
    return render_template('login.html', title="Sign In", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index', _external=True))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login', _external=True))
    return render_template('register.html', title="Register", form = form)


@app.route('/api')
def api():
    if request.args:
        if "func" in request.args:
            func = request.args.get('func')

            if func == "out":
                student_id = Students.query.filter_by(uuid=request.args.get('uuid')).first().id
                if student_id is None:
                    return "Student not found", 300
                out = Students_out.query.filter_by(student_id=student_id).first()
                if out is None:
                   
                    out = Students_out(student_id, 1, "Restroom")
                    out_log = Log(student_id, 1, "out", "Restroom")
                    out.save_to_db()
                    out_log.save_to_db()
                else:
                    out.remove_from_db()
                    in_log = Log(student_id, 1, "in", "Restroom")
                    in_log.save_to_db()
                trigger = requests.get("https://triggers.losant.com/webhooks/dNYJmaHMAydFYL_fE4MkI0fbZWsE0Z3DH5EcoHhFaA1$")
                return jsonify({"result" : "success"})


                
            if (func == "classlist"):
                if("studentid" in request.args):
                    classes = Classes.query.filter(Classes.student.any(id=request.args.get('studentid'))).all()
                    json_data = {}

                    i = 0
                    for _class in classes:
                        json_data[i] = {
                            "id" : _class.id,
                            "name" : _class.name,
                            "teacher" : _class.teacher,
                            "period" : _class.period
                        }
                        i = i + 1
                    return jsonify(json_data)
                else:
                    classes = Classes.query.all()
                    json_data = {}
                    i = 0 
                    for _class in classes:
                        json_data[i] = {
                            "id" : _class.id,
                            "name" : _class.name,
                            "teacher" : _class.teacher,
                            "period" : _class.period
                        }
                        i = i + 1
                    return jsonify(json_data)
            if (func == "studentlist"):
                if("classid" in request.args):
                    students = Students.query.filter(Students.classes.any(id=request.args.get("classid"))).all()
                    json_data = {}
                    i = 0
                    for _student in students:
                        json_data[i] = {
                            "id" : _student.id,
                            "first_name" : _student.first_name,
                            "last_name" : _student.last_name,
                            "uuid" : _student.uuid
                        }
                        i = i + 1
                    return jsonify(json_data)
                else:
                    students = Students.query.all()
                    json_data = {}
                    i = 0
                    for _student in students:
                        json_data[i] = {
                            "id" : _student.id,
                            "first_name" : _student.first_name,
                            "last_name" : _student.last_name,
                            "uuid" : _student.uuid
                        }
                        i = i + 1
                    return jsonify(json_data)
            if (func == "outlist"):
                out_list = None
                if("classid" in request.args):
                    out_list = Students_out.query(class_id=request.args.get("classid")).all()
                else:
                    out_list = Students_out.query.all()
                json_data = {}
                i = 0
                for _student in out_list:
                    json_data[i] = {
                        "id" : _student.id,
                        "student_id" : _student.student_id,
                        "class_id" : _student.class_id,
                        "destination" : _student.destination
                    }
                    i = i + 1
                return jsonify(json_data)

            if func == "studentadd":
                if ("id" in request.args) and ("firstname" in request.args) and ("lastname" in request.args) and ("uuid" in request.args):
                    NewStudent = Students(request.args.get("id"), request.args.get("firstname"), request.args.get("lastname"), request.args.get("uuid"))
                    NewStudent.save_to_db()
                    return jsonify({"result":"success"})
            
            if func == "classadd":
                if ("id" in request.args) and ("name" in request.args) and ("teacher" in request.args) and ("period" in request.args):
                    NewClass = Classes(request.args.get("id"), request.args.get("name"), request.args.get("teacher"), request.args.get("period"))
                    NewClass.save_to_db()
                    return jsonify({"result":"success"})


   # else:
   #     return "Malformed API Call", 300


