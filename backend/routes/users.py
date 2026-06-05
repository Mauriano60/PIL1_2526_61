from flask import Blueprint, render_template, session, redirect, url_for
from db.database import get_connection
from utils.responses import login_required, get_user_context

users_bp = Blueprint('users', __name__)

@users_bp.route('/dashboard')
@login_required
def dashboard():
    conn = None
    try:
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
            ORDER BY c.score_compatibilite DESC LIMIT 5
        """, (session['user_id'],))
        correspondances = cursor.fetchall()

        cursor.execute("""
            SELECT o.*, m.nom as matiere
            FROM offre_mentorat o
            JOIN matieres m ON m.id = o.matiere_id
            WHERE o.utilisateur_id = %s
            ORDER BY o.cree_le DESC
        """, (session['user_id'],))
        mes_offres = cursor.fetchall()

        cursor.execute("""
            SELECT d.*, m.nom as matiere
            FROM demande_mentorat d
            JOIN matieres m ON m.id = d.matiere_id
            WHERE d.utilisateur_id = %s
            ORDER BY d.cree_le DESC
        """, (session['user_id'],))
        mes_demandes = cursor.fetchall()
        conn.close()

        context = get_user_context()
        context.update({
            'correspondances': correspondances,
            'mes_offres': mes_offres,
            'mes_demandes': mes_demandes
        })
        return render_template('dashboard/index.html', **context)
    except Exception as e:
        return f"Erreur lors du chargement du dashboard: {str(e)}", 500
    finally:
        if conn:
            conn.close()
@users_bp.route('/profil/<int:user_id>')
@login_required
def profil(user_id):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT u.*, f.nom as filiere, n.nom as niveau
            FROM utilisateurs u
            JOIN filieres_etudes f ON f.id = u.id_filiere
            JOIN niveaux_etudes n ON n.id = u.id_niveau
            WHERE u.id = %s AND u.est_actif = 1
        """, (user_id,))
        profil_user = cursor.fetchone()
        if not profil_user:
            return "Utilisateur introuvable", 404
        cursor.execute("""
            SELECT m.nom FROM competences_utilisateur cu
            JOIN matieres m ON m.id = cu.matiere_id
            WHERE cu.utilisateur_id = %s
        """, (user_id,))
        competences = cursor.fetchall()

        cursor.execute("""
            SELECT m.nom FROM difficultes_utilisateur du
            JOIN matieres m ON m.id = du.matiere_id
            WHERE du.utilisateur_id = %s
        """, (user_id,))
        difficultes = cursor.fetchall()

        cursor.execute("""
            SELECT o.*, m.nom as matiere
            FROM offre_mentorat o
            JOIN matieres m ON m.id = o.matiere_id
            WHERE o.utilisateur_id = %s
        """, (user_id,))
        offres = cursor.fetchall()
        conn.close()

        context = get_user_context()
        context.update({
            'profil_user': profil_user,
            'competences': competences,
            'difficultes': difficultes,
            'offres': offres
        })
        return render_template('profil/public.html', **context)
    except Exception as e:
        return f"Erreur lors du chargement du profil: {str(e)}", 500
    finally:
        if conn:
            conn.close()