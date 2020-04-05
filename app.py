from flask import Flask, jsonify, request
from markupsafe import escape
import json, mysql.connector, sys


app = Flask(__name__)


@app.route("/")
def index():
    return "bikes API 1.0"


@app.route("/bike/specs/<model_name>", methods=["GET"])
def bikes(model_name):
    try:
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bikes"
    )
    except Exception as e:
        return jsonify(e)

    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT table_name FROM index_table WHERE model_name like '%{escape(model_name)}%'")
    table = mycursor.fetchall()
    try:
        table_name = table[0][0]
    except Exception as e:
        print(e)
        return jsonify(None)
    sql = f"SELECT * FROM {table_name} WHERE model_name like '%{escape(model_name)}%'"
    mycursor.execute(sql)
    spec_res = mycursor.fetchall()
    result = spec_res[0]
    column_names = mycursor.description
    spec_dict = {}
    i = 0
    for t in column_names:
        key = t[0].replace("_", " ").title()
        spec_dict[key] = result[i]
        i += 1
    return jsonify(spec_dict)


if __name__ == "__main__":
    app.run(debug=True)
