# API Curriculum de Santiago Menendez

# Fuente de donde se baso: https://programando-python.github.io/posts/la-api-de-tu-curriculum-vitae/

# Modulos

from flask import Flask, request, jsonify, abort
from datetime import datetime
import os
import sys
import json

# Inicio de aplicacion y configuraciones

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_SORT_KEYS'] = False

# Rutas

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
    print(language)
    if language == "ES":
        url_cv = request.host_url + "static/pdf/cv_sm.pdf"
        cv_info = os.path.join(os.path.dirname(sys.argv[0]), "static", "data", "cv_sm.json")
    elif language == "EN":
        url_cv = request.host_url + "static/pdf/cv_sm_en.pdf"
        cv_info = os.path.join(os.path.dirname(sys.argv[0]), "static", "data", "cv_sm_en.json")
    cv = json.load(open(cv_info))
    cv["url_cv"] = url_cv
    return jsonify(cv)

# Main

if __name__ == '__main__':
    app.run()

