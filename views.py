from flask import Blueprint, render_template, request
from movie import print_similar_movies, df2

views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("index.html")

@views.route("/los_los", methods= ['POST', 'GET'])
def losowanie():
    movie_att = print_similar_movies("")
    labels = df2
    if request.method == "POST":
        m_name = request.form["nm"]
        movie_att = print_similar_movies(m_name)
        return render_template("losowanie.html", mov_att=movie_att, mov_list=labels, name=m_name)
    else:
        return render_template("losowanie.html", mov_att=movie_att, mov_list=labels, name="")
@views.route("/info")
def info():
    return render_template("info.html")