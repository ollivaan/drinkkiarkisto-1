from application import app, db
from flask import render_template, request, url_for, redirect
from application.ingredients.models import Ingredient


@app.route("/ingredients", methods=["GET"])
def ingredients_index():
    return render_template("ingredients/list.html", ingredients=Ingredient.query.all())


@app.route("/ingredients/new/")
def ingredients_form():
    return render_template("ingredients/new.html")


@app.route("/ingredients/", methods=["POST"])
def ingredients_create():
    form = request.form
    i = Ingredient(form.get("name"), form.get("unit"))

    db.session().add(i)
    db.session().commit()

    return redirect(url_for("ingredients_index"))
