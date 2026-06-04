from flask import Blueprint

matching_bp = Blueprint(
    "matching",
    __name__,
    url_prefix="/api/matching"
)
