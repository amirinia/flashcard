from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import time
from flask import Flask, request, jsonify, render_template, request, redirect, flash
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_httpauth import HTTPBasicAuth # Authentication
from flask_marshmallow import Marshmallow
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import random

#initliazing our flask app, SQLAlchemy and Marshmallow
app = Flask(__name__)
auth = HTTPBasicAuth()# Authentication
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cardsdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Card(db.Model):
   id = db.Column(db.Integer, primary_key = True)
   category = db.Column(db.String(100))
   topic = db.Column(db.String(100))
   question = db.Column(db.String(100000))
   timestamp = db.Column(db.String(100), nullable=False,default = datetime.utcnow)
   #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   
   def __init__(self, category, topic, question):
       self.category = category
       self.topic = topic
       self.question = question

# user cards
class CardSchema(ma.Schema):
  class Meta:
    fields = ( 'category', 'topic', 'question')

# Init schema
card_schema = CardSchema()
cards_schema = CardSchema(many=True)


db.create_all()

@app.route("/cards/new", methods=["GET", "POST"])
def new_card():
    if request.method == "GET":
        all_satis = Card.query.all()
        cards = cards_schema.dump(all_satis)
        #all_topics = sorted(set([t.topic for t in u.posts.all()]))
        return render_template("new.html")
    else:
        category = request.form["category"]      
        topic = request.form["topic"]
        question = request.form["question"]
        if category == 'code':
            #using pygments to store code as html elements for highlighting.
            question = highlight(question, PythonLexer(), HtmlFormatter())

        card = Card(category, topic, question)
        db.session.add(card)
        db.session.commit()
        return redirect("/")
        #return card_schema.jsonify(card)

@app.route("/")
def index():
    
        all_satis = Card.query.all()
        cards = cards_schema.dump(all_satis)
        topics = set(list(t.topic for t in all_satis))
        random_card = random.choice(cards)
        total_cards = len(cards)
        all_topics_len = len(topics)
        all_topics = sorted(topics)
        #all_topics_len = 0
        #all_topics = 0
        #return jsonify(total_cards)
        return render_template("index.html", card=random_card, total_cards=total_cards, all_topics_len=all_topics_len, all_topics=all_topics)

# ---------------------------------------------------------------

# Show card's form with card info populated on form based on card id.
@app.route("/cards/<int:card_id>")
def get_card(card_id):
    card = Card.query.get(card_id)
    return render_template("show.html", card=card)

# Update card.
@app.route("/cards/<int:card_id>", methods=["POST"])
def edit(card_id):
    # TODO
        # Only show cards respective to user.
    card = Card.query.get(card_id)
    card.question = request.form["question"]
    card.topic = request.form["topic"]
    db.session.commit()
    return redirect("/")

@app.route("/cards/<int:card_id>/delete", methods=["POST"])
def delete_card(card_id):
    # TODO
        # Only show cards respective to user.
    Card.query.filter_by(id=card_id).delete()
    db.session.commit()
    return redirect("/")

# All cards
@app.route("/cards")
def show_cards():
    all_satis = Card.query.all()
    cards = cards_schema.dump(all_satis)
    return render_template("cards.html", cards=cards)

# ---------------------------------------------------------------
'''
Can refactor this.

Make a form that given a certain request.form (e.g) it would handle the
constraints.

Like if checkbox == category or topic do first querying, else do second.
'''
# Cards by category: General vs Code
@app.route("/cards/category/<string:card_category>")
def get_card_category(card_category):
    all_satis = Card.query.all()
    #cards = cards_schema.dump(all_satis)
    cards = [c for c in all_satis if c.category == card_category]
    return render_template("cards.html", cards=cards)

# Cards by Topic.
@app.route("/cards/topic/<string:card_topic>")
def get_card_topic(card_topic):
    all_satis = Card.query.all()
    #cards = cards_schema.dump(all_satis)
    cards = [c for c in all_satis if c.topic == card_topic]
    print(cards)
    return render_template("cards.html", cards=cards)


if __name__ == "__main__":
    app.run(debug=True)