from flask import Blueprint, render_template, request, session, redirect, url_for
from db.database import get_connection

offres_bp = Blueprint('offres', __name__)

@offres_bp.route('/offres')
def offres():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

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

@offres_bp.route('/offres/creer', methods=['GET', 'POST'])
def creer_offre():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        matiere_id = request.form['matiere_id']
        format_ = request.form['format']
        description = request.form['description']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO offre_mentorat (utilisateur_id, matiere_id, format, description)
            VALUES (%s, %s, %s, %s)
        """, (session['user_id'], matiere_id, format_, description))
        conn.commit()
        conn.close()
        return redirect(url_for('offres.offres'))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM matieres")
    matieres = cursor.fetchall()
    conn.close()

    return render_template('mentorat/creer-offre.html', matieres=matieres)