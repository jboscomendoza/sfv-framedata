from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
import json
from markupsafe import escape


app = Flask(__name__)


with open("SFVFrameData.json") as json_file:
    FRAME_DATA = json.load(json_file)


CHAR_NAMES = FRAME_DATA.keys()


def extract_stats(char, fd=FRAME_DATA):
    stat_keys   = ["fastestNormal", "bestReversal", "fDash", "bDash"]
    stat_short  = ["fst", "rev", "dfw", "dbw"]
    stat_names  = [
            u"Normal más rápido", "Mejor reversal", 
            "Dash hacia adelante", u"Dash hacia atrás", 
    ]
    stat_values = [fd[char]["stats"][i] for i in stat_keys]
    stat_dict = {}
    for short, name, value in zip(stat_short, stat_names, stat_values):
        stat_dict[short] = {"nombre":name, "valor":value}
    return stat_dict


def extract_fd(char, fd=FRAME_DATA):
    fd_keys  = {
        "startup": "S", #"Inicio", 
        "active": "A", #"Activo", 
        "recovery": "R", #u"Recuperación", 
        "onHit": "oH", #"Al golpear", 
        "onBlock": "oB", #"Al ser bloqueado",
    }
    fd_dict = {}
    for key, value in FRAME_DATA[char]["moves"]["normal"].items():
        mov_dict = {}
        for eng, esp in fd_keys.items():
            try:
                mov_dict[esp] = value[eng]
            except:
                mov_dict[esp] = ""
        fd_dict[key] = mov_dict

    return fd_dict


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", char_names=CHAR_NAMES)


@app.route("/<string:char>/", methods=("GET", "POST"))
def character_page(char):
    stat_dict = extract_stats(char)
    fd_dict   = extract_fd(char)

    return render_template("character.html", char=char, 
    stat_dict=stat_dict, fd_dict=fd_dict)


if __name__ == "__main__":
    app.run()
