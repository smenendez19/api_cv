# API Curriculum de Santiago Menendez

# Fuente de donde se baso: https://programando-python.github.io/posts/la-api-de-tu-curriculum-vitae/

# Imports

from flask import Flask, request, jsonify
import os
import json

# Start

app = Flask(__name__)

# Configs

app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_SORT_KEYS'] = False

# Paths

PATH_STATIC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
PATH_DATA = os.path.join(PATH_STATIC, "data")

# Endpoints

@app.route('/')
def index():
    info = {
        "mensaje" : "Bienvenido a la API del curriculum vitae de Santiago Menendez.",
        "acciones" : [
            {"GET /curriculum" : "Obtener el curriculum",
            "Argumentos" : {
                "lang" : "Idioma : ES o EN"
            }},
        ]
    }
    return jsonify(info)

@app.route('/curriculum', methods=['GET'])
def get_cv_info():
    language = request.args.get('lang')
    if not language:
        language = "ES"
    else:
        language = language.upper()
    if language == "ES":
        url_cv_pdf = request.host_url + "static/pdf/CV_ES.pdf"
        cv_data_path = os.path.join(PATH_DATA, "cv_data_es.json")
    elif language == "EN":
        url_cv_pdf = request.host_url + "static/pdf/CV_EN.pdf"
        cv_data_path = os.path.join(PATH_DATA, "cv_data_en.json")
    cv_data = json.load(open(cv_data_path))
    cv_data["url_cv_pdf"] = url_cv_pdf
    return jsonify(cv_data)

# Main

if __name__ == '__main__':
    app.run()

