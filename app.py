from flask import Flask, jsonify, request
from markupsafe import escape
import json, mysql.connector, sys
from configparser import ConfigParser


app = Flask(__name__)

# Get the database credentials from the config file
config = ConfigParser()
config.read("config.ini")
DB_HOST = config.get("DATABASE", "host")
DB_USER = config.get("DATABASE", "user")
DB_PASS = config.get("DATABASE", "password")
DB_DTBS = config.get("DATABASE", "database")


@app.route("/")
def index():
    return "bikes API 1.0"


@app.route("/bike/specs_by_name/<model_name>", methods=["GET"])
def specs_by_name(model_name):
    try:
        mydb = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_DTBS
    )
    except Exception as e:
        print(e)
        return jsonify(None)

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
    keys_for_deletion = []
    for k, v in spec_dict.items():
        if v is None:
            keys_for_deletion.append(k)
    for key in keys_for_deletion:
        del spec_dict[key]
    
    return jsonify(spec_dict)


@app.route("/bike/all_bike_brands", methods=["GET"])
def all_bike_brands():
    try:
        mydb = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_DTBS
    )
    except Exception as e:
        print(e)
        return jsonify(None)
    mycursor = mydb.cursor()
    sql = f"SELECT brand_names, brand_logos FROM  brands_table"
    mycursor.execute(sql)
    brand_res = mycursor.fetchall()
    lst = []
    for item in brand_res:
        tmp = item[0].title().replace("_", " ")
        lst.append([tmp, item[1]])
    return jsonify(lst)


@app.route("/bike/all_bike_types", methods=["GET"])
def all_bike_types():
    try:
        mydb = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_DTBS
    )
    except Exception as e:
        print(e)
        return jsonify(None)
    mycursor = mydb.cursor()
    sql = "SELECT type_names FROM types_table"
    mycursor.execute(sql)
    type_res = mycursor.fetchall()
    type_list = []
    for typ in type_res:
        type_list.append(typ[0].title().replace("_", " "))
    
    return jsonify(type_list)


@app.route("/bike/specs_by_brand/<brand_name>", methods=["GET"])
def specs_by_brand(brand_name):
    try:
        mydb = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_DTBS
    )
    except Exception as e:
        print(e)
        return jsonify(None)
    mycursor = mydb.cursor()
    sql = f"SELECT * FROM {brand_name}"
    mycursor.execute(sql)
    spec_res = mycursor.fetchall()
    column_names = mycursor.description
    column_names_list = []
    spec_list_of_dics = []
    for name in column_names:
        column_names_list.append(name[0])
    for items in spec_res:
        tmp = []
        for item in items:
            tmp.append(item)
        tmpdct = {}
        i=0
        for name in column_names_list:
            tmpdct[name] = tmp[i]
            i += 1
        keys_for_deletion = []
        for k, v in tmpdct.items():
            if v is None:
                keys_for_deletion.append(k)
        for key in keys_for_deletion:
            del tmpdct[key]
        spec_list_of_dics.append(tmpdct)
    
    return jsonify(spec_list_of_dics)


@app.route("/bike/specs_by_type/<bike_type>", methods=["GET"])
def specs_by_type(bike_type):
    try:
        mydb = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_DTBS
    )
    except Exception as e:
        print(e)
        return jsonify(None)
    mycursor = mydb.cursor()
    sql = f"SELECT * FROM {bike_type}"
    mycursor.execute(sql)
    type_res = mycursor.fetchall()
    column_names = mycursor.description
    column_names_list = []
    spec_list_of_dics = []
    for name in column_names:
        column_names_list.append(name[0])
    for items in type_res:
        tmp = []
        for item in items:
            tmp.append(item)
        tmpdct = {}
        i=0
        for name in column_names_list:
            tmpdct[name] = tmp[i]
            i += 1
        keys_for_deletion = []
        for k, v in tmpdct.items():
            if v is None:
                keys_for_deletion.append(k)
        for key in keys_for_deletion:
            del tmpdct[key]
        spec_list_of_dics.append(tmpdct)
    return jsonify(spec_list_of_dics)


if __name__ == "__main__":
    app.run(debug=True)
