import requests
from flask import Flask, render_template


api_key = "YOURAPIKEY"
URL = "https://the-one-api.dev/v2"
headers = {"Authorization": "Bearer YOURAPIKEY"}
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/books", methods=["GET", "POST"])
def books():
    response = requests.get(f"{URL}/book", headers=headers)
    data = response.json()["docs"]

    book_names = [n["name"] for n in data]
    book_id = [n["_id"] for n in data]

    chapters = requests.get(f"{URL}/chapter", headers=headers)
    chapter = chapters.json()["docs"]
    new_dict = {book_names[0]: [], book_names[1]: [], book_names[2]: []}
    for chap in chapter:
        if chap["book"] == book_id[0]:
            new_dict[book_names[0]].append(chap["chapterName"])
        elif chap["book"] == book_id[1]:
            new_dict[book_names[1]].append(chap["chapterName"])
        else:
            new_dict[book_names[2]].append(chap["chapterName"])
    for key, value in new_dict.items():
        res = str(value)
        res = res.replace("[", "")
        res = res.replace("]", "")
        res = res.replace("'", "")
        new_dict[key] = res

    return render_template("books.html", table=new_dict)


@app.route("/movies", methods=["GET", "POST"])
def movies():
    response = requests.get(f"{URL}/movie", headers=headers)
    data = response.json()["docs"]

    series = data[0:2]
    movies_list = data[2::]

    return render_template("movies.html", series=series, movies_list=movies_list)


if __name__ == "__main__":
    app.run(debug=True)
