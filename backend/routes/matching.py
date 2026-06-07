# CHABI AYEDOUN Yoéla
from flask import Blueprint, render_template, session, redirect, url_for
# On utilise uniquement fetch_all depuis ton database.py
from db.database import fetch_all 
from services.matching_service import calculer_correspondances

matching_bp = Blueprint('matching', __name__)

@matching_bp.route('/matching')
def matching():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    try:
        # Exécute l'algorithme de matching pour l'étudiant connecté
        calculer_correspondances(session['user_id'])
        
        # Récupération des correspondances triées par score (gérée proprement par fetch_all)
        mentors = fetch_all("""
            SELECT c.score_compatibilite, u.id, u.prenom, u.nom, u.biographie,
                   f.nom as filiere, n.nom as niveau
            FROM correspondances c
            JOIN utilisateurs u ON u.id = c.mentor_id
            JOIN filieres_etudes f ON f.id = u.id_filiere
            JOIN niveaux_etudes n ON n.id = u.id_niveau
            WHERE c.mentee_id = %s
            ORDER BY c.score_compatibilite DESC
        """, (session['user_id'],))
        
        return render_template('matching/index.html', mentors=mentors)
        
    except Exception as e:
        return f"Erreur lors du chargement des correspondances: {str(e)}", 500