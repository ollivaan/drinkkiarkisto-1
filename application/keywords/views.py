from application import app, db
from flask import render_template, request, url_for, redirect
from flask_login import login_required

from application.keywords.models import Keyword
from application.keywords.forms import NewKeywordForm


@app.route("/keywords", methods=["GET"])
def keywords_index():
    return render_template("keywords/list.html", keywords=Keyword.query.all())


@app.route("/keywords/new/")
@login_required
def keywords_form():
    return render_template("keywords/new.html", form=NewKeywordForm())


@app.route("/keywords/", methods=["POST"])
@login_required
def keywords_create():
    form = NewKeywordForm(request.form)

    if not form.validate():
        return render_template("keywords/new.html", form=form)

    k = Keyword(form.name.data)

    db.session().add(k)
    db.session().commit()

    return redirect(url_for("keywords_index"))

@app.route("/keywords/edit/<keyword_id>/", methods=["GET"])
@login_required
def keywords_edit(keyword_id):
    k = Keyword.query.get(keyword_id)

    form = NewKeywordForm()
    form.name.data = k.name
    return render_template("keywords/edit.html", form=form, keyword=k)

@app.route("/keywords/edit/<keyword_id>/", methods=["POST"])
@login_required
def keywords_save_edit(keyword_id):
    form = NewKeywordForm(request.form)
    k = Keyword.query.get(keyword_id)

    if not form.validate():
        return render_template("keywords/edit.html", form=form, keyword=k)

    k.name = form.name.data

    db.session().commit()

    return redirect(url_for("keywords_index"))

@app.route("/keywords/delete/<keyword_id>/", methods=["GET"])
@login_required
def keywords_delete(keyword_id):
    keyword = Keyword.query.get(keyword_id)

    if keyword is None:
        return redirect(url_for("keywords_index"))
    
    db.session.delete(keyword)
    db.session().commit()

    return redirect(url_for("keywords_index"))