from flask import Flask, Blueprint, redirect, url_for, render_template, request, session, flash, jsonify, send_file
from werkzeug.utils import secure_filename
from datetime import timedelta
import base64, io, os
from webapp.qr_id import *
from . import db
from .models import Commands
from .helpers import *


views = Blueprint("views", __name__)



@views.route("/", methods=["POST","GET"])
@views.route("/home", methods=["POST","GET"])
def home():
    if request.method == "POST":
        return redirect(url_for("views.lang"))
    else:
        return render_template("home.html")

@views.route("/lang", methods = ["POST", "GET"])
def lang():
    a = "Idioma · Hizkuntza · Language · Langage"
    if request.method == "POST":
        lang = request.form["lang"]
        session["lang"] = lang
        o =  QRandID(); o.generate_ID(); o.generate_QR(lang)
        id = o.get_ID()
        qr = o.get_QR_img()
        found_id = Commands.query.filter_by(print_sess=id).first()

        #Per veure que no hi ha alguna sessió prèvia amb el mateix ID
        while found_id is not None:
            o =  QRandID(); o.generate_ID(); o.generate_QR(lang)
            id = o.get_ID()
            qr = o.get_QR_img()
            found_id = Commands.query.filter_by(print_sess=id).first()

        with io.BytesIO() as buf:
            qr.save(buf, 'png')
            image_bytes = buf.getvalue()
        encoded_string = base64.b64encode(image_bytes).decode()
        session["encoded_string"] = encoded_string

        return redirect(url_for("views.qr_id"))
    else:
        if "lang" in session:
            return redirect(url_for("views.qr_id"))
        return render_template("lang.html",a = a)
    


@views.route("/qr_id", methods = ["POST", "GET"])
def qr_id():
    lang = session["lang"]
    encoded_string = session["encoded_string"]
    lang_icon = f"./static/images/{lang}.png"
    tr_texts = text(lang,1)
    tr_texts2 = text(lang,6)
    
    if request.method == "POST":
        id_user = request.form["id_user"]
        downloads = Commands.query.filter_by(print_sess=str(id_user)).all()
        if len(downloads) > 0:
            if not os.path.exists(os.path.join(os.environ["USERPROFILE"], f"Downloads\\{id_user}")):
                os.makedirs(os.path.join(os.environ["USERPROFILE"], f"Downloads\\{id_user}"))
            for file in downloads:
                data = file.data
                filename = file.filename
                with open(os.path.join(os.environ["USERPROFILE"], f"Downloads\\{id_user}\\{filename}"), 'wb') as file:
                    file.write(data)
        else:
            flash(message = tr_texts2[1], category ="Error")
        return redirect(url_for("views.qr_id"))
            
    else:  
        return render_template("qr_id.html", a = tr_texts[0], b = tr_texts[1], c = tr_texts[2], d = tr_texts[3], e = tr_texts[4], f = tr_texts[6], g = tr_texts[5], h = tr_texts[7], i = tr_texts2[0], qr = encoded_string, lang_icon=lang_icon)


@views.route("/mobile-upload", methods = ["POST", "GET"])
def mobile_upload():
    id = request.args.get('id')
    lang = request.args.get('lang')
    tr_texts = text(lang,2)
    tr_texts2 = text(lang,5)
    lang_icon = f"./static/images/{lang}.png"

    if request.method == "POST":
        # check if the post request has the file part
        if 'file' not in request.files:
            flash(tr_texts2[3],category='error')
            return redirect(url_for("views.mobile_upload",id=id,lang=lang))
        files = request.files.getlist("file")
        email = request.form['email']
        if allowed_mail(email):
            for file in files:
                if file.filename == '':
                    flash(tr_texts2[3],category='error')
                    return redirect(url_for("views.mobile_upload",id=id,lang=lang))
                
                if file and allowed_file(file.filename):
                    filename_sec = secure_filename(file.filename)
                    upload = Commands(print_sess=id,filename=filename_sec, data=file.read(),email=email)
                    db.session.add(upload)
                else:
                    flash(tr_texts2[6],category='error')
                    return redirect(url_for("views.mobile_upload",id=id,lang=lang))
            db.session.commit()
            send_mail(text=tr_texts2[0],id=id, recipient=str(email))
            return redirect(url_for("views.mobile_out",lang=lang))
        else:
            flash(tr_texts2[7],category='error')
            return redirect(url_for("views.mobile_upload",id=id,lang=lang))


    else: 
        return render_template("mobile.html", a= tr_texts[0], b=tr_texts[1], c=tr_texts[2], d=tr_texts[3], e=tr_texts[4], f=tr_texts[5], g=tr_texts[6],h = tr_texts2[1], i=tr_texts2[2],j=tr_texts2[3],k=tr_texts2[4], l=tr_texts2[5], m = tr_texts2[6],lang_icon=lang_icon)



@views.route("/mobile_out",methods = ["POST", "GET"])
def mobile_out():
    lang = request.args.get('lang')
    lang_icon = f"./static/images/{lang}.png"
    tr_texts = text(lang,3)
    tr_texts2 = text(lang,4)
    return render_template("mobile-out.html",a=tr_texts[0], b=tr_texts[1], c=tr_texts[2], d = tr_texts2[0], lang_icon=lang_icon)

@views.route("/view_data", methods = ["POST", "GET"])
def view():
    commands = Commands.query.all()
    return render_template('view_data.html', commands=commands)

    

@views.route("/logout",methods = ["POST", "GET"])
def logout():
    session.pop("lang",None)
    session.pop("encoded_string", None)
    users = Commands.query.all()
    for user in users:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for("views.home"))
