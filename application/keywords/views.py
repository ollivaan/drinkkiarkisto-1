from application import app, db, login_required
from flask import render_template, request, url_for, redirect
from flask_login import current_user

from application.keywords.models import Keyword
from application.keywords.forms import NewKeywordForm


@app.route("/keywords", methods=["GET"])
def keywords_index():
    keywords = Keyword.query.filter(Keyword.accepted == '1').order_by(Keyword.name).all()
    return render_template("keywords/list.html", keywords=keywords)


@app.route("/keywords/new/")
@login_required(role="ANY")
def keywords_form():
    return render_template("keywords/new.html", form=NewKeywordForm())


@app.route("/keywords/", methods=["POST"])
@login_required(role="ANY")
def keywords_create():
    form = NewKeywordForm(request.form)

    if not form.validate():
        return render_template("keywords/new.html", form=form)

    name = str(form.name.data).capitalize()
    k = Keyword(name)

    if current_user is not None:
        k.account_id = current_user.id
        if current_user.role.name == "USER+" or current_user.role.name == "ADMIN":
            k.accepted = True

    db.session().add(k)
    db.session().commit()

    return redirect(url_for("keywords_index"))


@app.route("/keywords/edit/<keyword_id>/", methods=["GET"])
@login_required(role=3)
def keywords_edit(keyword_id):
    k = Keyword.query.get(keyword_id)

    form = NewKeywordForm()
    form.name.data = k.name
    return render_template("keywords/edit.html", form=form, keyword=k)


@app.route("/keywords/edit/<keyword_id>/", methods=["POST"])
@login_required(role=3)
def keywords_save_edit(keyword_id):
    form = NewKeywordForm(request.form)
    k = Keyword.query.get(keyword_id)

    if not form.validate():
        return render_template("keywords/edit.html", form=form, keyword=k)

    k.name = form.name.data

    db.session().commit()

    return redirect(url_for("keywords_index"))


@app.route("/keywords/delete/<keyword_id>/", methods=["GET"])
@login_required(role=3)
def keywords_delete(keyword_id):
    keyword = Keyword.query.get(keyword_id)

    if keyword is None:
        return redirect(url_for("keywords_index"))

    db.session.delete(keyword)
    db.session().commit()

    return redirect(url_for("keywords_index"))


@app.route("/keywords/publish/<keyword_id>", methods=["GET"])
@login_required(role=3)
def publish_keyword(keyword_id):
    k = Keyword.query.get(keyword_id)

    if not k:
        return redirect(url_for("admin_index"))

    k.accepted = True
    db.session().commit()

    return redirect(url_for("admin_index"))


@app.route("/keywords/reject/<keyword_id>", methods=["GET"])
@login_required(role=3)
def reject_keyword(keyword_id):
    k = Keyword.query.get(keyword_id)

    if not k:
        return redirect(url_for("admin_index"))

    db.session.delete(k)
    db.session().commit()

    return redirect(url_for("admin_index"))
