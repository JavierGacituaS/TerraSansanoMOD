from flask import Flask, render_template, send_file
import markdown
from pygments.formatters import HtmlFormatter
import os

app = Flask(__name__)

def getContent(file_name):
    file = open(f"docs/{file_name}")
    md_template_string = markdown.markdown(file.read(), extensions=["fenced_code", "tables", "codehilite", "mdx_math"])
    file.close()

    return md_template_string

@app.route("/descarga")
def descarga():
    return send_file(
        "mod/TerraSansanoMOD.tmod",
        attachment_filename='TerraSansano.tmod',
        as_attachment=True
    )

@app.route("/")
def home():
    all_files = os.listdir("docs")

    ordenar = []

    for file in all_files:
        ordenar.append([int(file[:-3]), file])

    ordenar.sort()
    ordenar.reverse()

    patches = []
    formatter = HtmlFormatter(style="native",full=True, cssclass="codehilite")

    for file in ordenar:
        print(file)
        patches.append(getContent(file[1]))

    return render_template(
        "pages/home.html",
        title="Mod Sansano - Inicio",
        styles=formatter.get_style_defs(),
        all_patches=patches
    )

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")