from flask import Blueprint, render_template, session, redirect, url_for
from db.database import get_connection

references_bp = Blueprint('references', __name__)

@references_bp.route('/references')
def references():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM matieres ORDER BY nom")
        matieres = cursor.fetchall()
        cursor.execute("SELECT * FROM filieres_etudes ORDER BY nom")
        filieres = cursor.fetchall()
        cursor.execute("SELECT * FROM niveaux_etudes ORDER BY nom")
        niveaux = cursor.fetchall()
        conn.close()
        return render_template('references/index.html',
                           matieres=matieres,
                           filieres=filieres,
                           niveaux=niveaux)
    except Exception as e:
        return f"Erreur lors du chargement des références: {str(e)}", 500
    finally:
        if conn:
            conn.close()
