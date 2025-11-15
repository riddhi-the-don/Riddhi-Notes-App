from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import config

app = Flask(__name__)

client = MongoClient(config.MONGO_URI)
db = client.notesdb
notes_collection = db.notes


@app.route("/")
def index():
    notes = list(notes_collection.find().sort("_id", -1))
    return render_template("index.html", notes=notes)


@app.route("/add", methods=["POST"])
def add_note():
    title = request.form["title"]
    content = request.form["content"]

    notes_collection.insert_one({
        "title": title,
        "content": content
    })

    return redirect("/")


@app.route("/edit/<id>")
def edit(id):
    note = notes_collection.find_one({"_id": ObjectId(id)})
    return render_template("edit.html", note=note)


@app.route("/update/<id>", methods=["POST"])
def update(id):
    title = request.form["title"]
    content = request.form["content"]

    notes_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"title": title, "content": content}}
    )

    return redirect("/")


@app.route("/delete/<id>")
def delete(id):
    notes_collection.delete_one({"_id": ObjectId(id)})
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

