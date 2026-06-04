from flask import Blueprint

offres_bp = Blueprint(
    "offres",
    __name__,
    url_prefix="/api/offres"
)
