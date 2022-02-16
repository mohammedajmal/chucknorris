"""Code for a Chucknorris API to Create, Read, Update, Delete Joke"""
import os
from flask import jsonify, request, Flask
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("db_root_password")
app.config["MYSQL_DATABASE_DB"] = os.getenv("db_name")
app.config["MYSQL_DATABASE_HOST"] = os.getenv("MYSQL_SERVICE_HOST")
app.config["MYSQL_DATABASE_PORT"] = int(os.getenv("MYSQL_SERVICE_PORT"))
mysql.init_app(app)


@app.route("/")
def index():
    """Function to test the functionality of the API"""
    return "Hello, world!"


@app.route("/create", methods=["POST"])
def add_joke():
    """Function to create a joke to the MySQL database"""
    json = request.json
    joke = json["joke"]
    if joke and request.method == "POST":
        sql = "INSERT INTO ChuckNorrisJokes(joke) " \
              "VALUES(%s)"
        data = (joke)
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            cursor.close()
            conn.close()
            resp = jsonify("Joke created successfully!")
            resp.status_code = 200
            return resp
        except Exception as exception:
            return jsonify(str(exception))
    else:
        return jsonify("Please provide Joke")


@app.route("/jokes", methods=["GET"])
def jokes():
    """Function to retrieve all Jokes from the MySQL database"""
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ChuckNorrisJokes")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))


@app.route("/joke/<int:joke_id>", methods=["GET"])
def user(joke_id):
    """Function to get information of a specific Joke in the MSQL database"""
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ChuckNorrisJokes WHERE joke_id=%s", joke_id)
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))


@app.route("/delete/<int:joke_id>")
def delete_joke(joke_id):
    """Function to delete a Joke from the MySQL database"""
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ChuckNorrisJokes WHERE joke_id=%s", joke_id)
        conn.commit()
        cursor.close()
        conn.close()
        resp = jsonify("Joke deleted successfully!")
        resp.status_code = 200
        return resp
    except Exception as exception:
        return jsonify(str(exception))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)