# -*- coding: utf-8 -*-

from flask import (
    Flask,
    request,
    redirect,
)
from flask.helpers import send_from_directory
from renderer import CutycaptRenderer
from hashlib import sha1
import logging
import os
import argparse
import tempfile

renderer = CutycaptRenderer()
app = Flask(__name__, template_folder="", static_folder="web")

storage_path = tempfile.gettempdir()

logging.warning("TEMPDIR: " + storage_path)

generated_prefix = "genimages/"


@app.route('/', methods=['GET'])
@app.route('/<path:subpath>', methods=['GET'])
def run_get(subpath=None):
    if subpath is None:
        return app.send_static_file("index.html")

    if subpath.startswith(generated_prefix):
        filename = subpath[len(generated_prefix):]
        return send_from_directory(storage_path, filename)
    return app.send_static_file(subpath)


@app.route('/', methods=['POST'])
def run_post(subpath=None):
    # app.logger.warning(subpath)

    filename = sha1(str(request.form).encode('utf-8')).hexdigest() + ".png"
    filepath = os.path.join(storage_path, filename)

    if not os.path.exists(filepath):
        if "styles_str" in request.form:
            renderer.png_for_extra_styles(
                png_path=filepath,
                styles_str=request.form["styles"],
                template=request.form["template"]
            )
        elif "title" in request.form and "category" in request.form:
            # print("=========================")
            # a = str(request.form["title"])
            # print(a.encode())
            # print(request.get_json(force=True))
            # print(str(request.form["title"], 'ascii'))
            # print(repr(request.form["title"]))
            # print("=========================")
            renderer.png_for_title_and_category(
                png_path=filepath,
                title=request.form["title"],
                category=request.form["category"],
                template=request.form["template"]
            )
        else:
            raise ValueError

    return redirect("{path}?img_path=/genimages/{filename}".format(path="", filename=filename), code=302)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()

    parser.add_argument('--port', dest='port', type=int, action='store', default=5000)
    port = parser.parse_args().port
    app.run(host='0.0.0.0', port=port)
