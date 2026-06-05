from flask import Blueprint, render_template, session, redirect, url_for
from db.database import get_connection
from services.matching_service import calculer_correspondances

matching_bp = Blueprint('matching', __name__)

@matching_bp.route('/matching')
def matching():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    calculer_correspondances(session['user_id'])

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.score_compatibilite, u.id, u.prenom, u.nom, u.biographie,
               f.nom as filiere, n.nom as niveau
        FROM correspondances c
        JOIN utilisateurs u ON u.id = c.mentor_id
        JOIN filieres_etudes f ON f.id = u.id_filiere
        JOIN niveaux_etudes n ON n.id = u.id_niveau
        WHERE c.mentee_id = %s
        ORDER BY c.score_compatibilite DESC
    """, (session['user_id'],))
    mentors = cursor.fetchall()
    conn.close()

    return render_template('matching/index.html', mentors=mentors)