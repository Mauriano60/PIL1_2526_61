from flask import Blueprint, render_template, request, session, redirect, url_for
from db.database import get_connection

offres_bp = Blueprint('offres', __name__)

@offres_bp.route('/offres')
def offres():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT o.*, m.nom as matiere, u.prenom, u.nom as nom_user
            FROM offre_mentorat o
            JOIN matieres m ON m.id = o.matiere_id
            JOIN utilisateurs u ON u.id = o.utilisateur_id
            ORDER BY o.cree_le DESC
        """)
        offres = cursor.fetchall()
        conn.close()
        return render_template('mentorat/offres.html', offres=offres)
    except Exception as e:
        return f"Erreur lors du chargement des offres: {str(e)}", 500
    finally:
        if conn:
            conn.close()

@offres_bp.route('/offres/creer', methods=['GET', 'POST'])
def creer_offre():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    error = None
    matieres = []
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM matieres")
        matieres = cursor.fetchall()
        conn.close()
    except Exception as e:
        error = f"Erreur lors du chargement des matières: {str(e)}"
    finally:
        if conn:
            conn.close()
    if request.method == 'POST':
        matiere_id = request.form['matiere_id']
        format_ = request.form['format']
        description = request.form['description']
        if not matiere_id or not format_:
            error = "Matière et format sont requis"
        elif len(description) > 1000:
            error = "Description trop longue (max 1000 caractères)"
        else:
            conn = None
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO offre_mentorat (utilisateur_id, matiere_id, format, description)
                    VALUES (%s, %s, %s, %s)
                """, (session['user_id'], matiere_id, format_, description))
                conn.commit()
                return redirect(url_for('offres.offres'))
            except Exception as e:
                    error = f"Erreur lors de la création de l'offre: {str(e)}"
            finally:
                    if conn:
                        conn.close()
    return render_template('mentorat/creer-offre.html', matieres=matieres, error=error)