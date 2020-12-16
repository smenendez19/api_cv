# API Curriculum de Santiago Menendez

# Fuente de donde se baso: https://programando-python.github.io/posts/la-api-de-tu-curriculum-vitae/

# Modulos

from flask import Flask, request, jsonify, abort
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# Funciones

def send_mail_gmail(from_mail, password, to_mail, subject, message):
    # SMTP Gmail
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_mail, password)
        msg = MIMEMultipart()
        msg['From'] = from_mail
        msg['To'] = to_mail
        msg['Subject'] = subject
        msg.attach(MIMEText(str(message, encoding="utf-8-sig"), 'plain'))
        # Envio del mail
        server.sendmail(msg['From'], to_mail, msg.as_string())
    except BaseException as err:
        abort(400, description=f"Error en el envio del mensaje al mail, detalle del error: {err}")

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
            "GET /curriculum",
            "POST /mensajes"
        ]
    }
    return jsonify(info)

@app.route('/curriculum', methods=['GET'])
def cv():
    #url_photo = request.host_url + "static/foto.png"
    url_cv = request.host_url + "static/cv_sm.pdf"
    cv = {
        "nombre" : "Santiago",
        "apellido" : "Menendez",
        "residencia" : "Argentina",
        "experiencia" : [{
            "posición" : "Data Engineer",
            "empresa" : "Ergo Renova",
            "desde" : "Enero de 2019",
            "hasta" : "Actualidad",
            "descripcion" : """Ingrese a Ergo Renova como Trainee en enero de 2019. Actualmente me desempeño como Data Engineer para los proyectos de Movistar y GIRE."""
        }],
        "educación" : {
            "nivel" : "Universitario",
            "titulo" : "Ingenieria Informatica",
            "institucion" : "Universidad Nacional de La Matanza",
            "facultad" : "Desde 2016 hasta la actualidad, estoy terminando el 3er año de la carrera"
        },
        "tecnologias" : {
            "lenguajes_programacion" : ["Python", "Bash", "Java SE", "C", "C++", "Javascript"],
            "cloud" : ["AWS", "GCP"],
            "bases_de_datos" : ["MySQL", "PostresSQL", "Hadoop/Hive", "Teradata", "Oracle SQL/PL SQL", "MongoDB"],
            "web" : ["HTML", "CSS"],
            "office" : ["Word", "Excel", "PowerPoint"],
            "otros" : ["Git", "PowerBI"]
        },
        "intereses" : ["Python", "APIs", "Big Data", "Machine Learning", "Linux", "GitHub", "Desarrollo Web", "Desarrollo Backend"],
        "redes" : {
            "github" : "https://github.com/santimenendez19",
            "linkedin" : "https://www.linkedin.com/in/menendezsantiago",
            "portfolio" : "En desarrollo"
        },
        "cv_pdf" : url_cv
    }
    return jsonify(cv)

@app.route('/mensajes', methods=['POST'])
def contacto():
    msg = request.get_data()
    sys_date = datetime.now().strftime("%Y-%m-%d")
    if not msg:
        abort(400, description="Debe enviar su mensaje en el body del POST, por ejemplo: curl -X POST -d 'mensaje' url.")
    #print("MENSAJE DE CONTACTO: " + str(msg))
    # Guardado del mensaje como archivo
    with open(f"messages/{sys_date}_message.txt", "wt", encoding="utf-8-sig") as f:
        f.write(str(msg, encoding="utf-8-sig"))
    # Parametros .env
    from_mail = os.environ.get("FROM_MAIL")
    to_mail = os.environ.get("TO_MAIL")
    password = os.environ.get("PASSWORD")
    # Envio del mensaje por mail
    send_mail_gmail(from_mail, password, to_mail, "Mensaje API CV", msg)
    return "Gracias por su mensaje."

# Main

if __name__ == '__main__':
    app.run()

