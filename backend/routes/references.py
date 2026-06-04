from flask import Blueprint

references_bp = Blueprint(
    "references",
    __name__,
    url_prefix="/api"
)
