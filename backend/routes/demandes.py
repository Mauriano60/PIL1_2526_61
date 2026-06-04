from flask import Blueprint

demandes_bp = Blueprint(
    "demandes",
    __name__,
    url_prefix="/api/demandes"
)
