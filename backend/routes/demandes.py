from flask import Blueprint, render_template, request, session, redirect, url_for
from db.database import get_connection

demandes_bp = Blueprint('demandes', __name__)

@demandes_bp.route('/demandes')
def demandes():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT d.*, m.nom as matiere, u.prenom, u.nom as nom_user
        FROM demande_mentorat d
        JOIN matieres m ON m.id = d.matiere_id
        JOIN utilisateurs u ON u.id = d.utilisateur_id
        ORDER BY d.cree_le DESC
    """)
    demandes = cursor.fetchall()
    conn.close()

    return render_template('mentorat/demandes.html', demandes=demandes)

@demandes_bp.route('/demandes/creer', methods=['GET', 'POST'])
def creer_demande():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        matiere_id = request.form['matiere_id']
        format_ = request.form['format']
        description = request.form['description']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO demande_mentorat (utilisateur_id, matiere_id, format, description)
            VALUES (%s, %s, %s, %s)
        """, (session['user_id'], matiere_id, format_, description))
        conn.commit()
        conn.close()
        return redirect(url_for('demandes.demandes'))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM matieres")
    matieres = cursor.fetchall()
    conn.close()

    return render_template('mentorat/creer-demande.html', matieres=matieres)