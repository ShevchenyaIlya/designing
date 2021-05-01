from flask import Blueprint
from flask_selfdoc import Autodoc

doc = Blueprint("documentation", __name__, url_prefix="/documentation")
auto = Autodoc()


@doc.route("/")
def documentation():
    return auto.html(title="RESTFull application documentation")
