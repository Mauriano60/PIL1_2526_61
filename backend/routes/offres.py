# CHABI AYEDOUN Yoéla
from flask import Blueprint, render_template, request, session, redirect, url_for
# Centralisation des accès BDD avec les outils de ton database.py
from db.database import fetch_all, execute

offres_bp = Blueprint('offres', __name__)

@offres_bp.route('/offres')
def offres():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    try:
        # Récupération de la liste des offres avec les jointures correspondantes
        offres_liste = fetch_all("""
            SELECT o.*, m.nom as matiere, u.prenom, u.nom as nom_user
            FROM offre_mentorat o
            JOIN matieres m ON m.id = o.matiere_id
            JOIN utilisateurs u ON u.id = o.utilisateur_id
            ORDER BY o.cree_le DESC
        """)
        return render_template('mentorat/offres.html', offres=offres_liste)
        
    except Exception as e:
        return f"Erreur lors du chargement des offres: {str(e)}", 500


@offres_bp.route('/offres/creer', methods=['GET', 'POST'])
def creer_offre():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    error = None
    
    # Chargement des matières disponibles pour le menu déroulant
    try:
        matieres = fetch_all("SELECT * FROM matieres")
    except Exception as e:
        matieres = []
        error = f"Erreur lors du chargement des matières: {str(e)}"

    if request.method == 'POST':
        # Utilisation de .get() pour sécuriser la récupération des champs de formulaire
        matiere_id = request.form.get('matiere_id')
        format_ = request.form.get('format')
        description = request.form.get('description', '').strip()
        
        # Validations des données entrantes
        if not matiere_id or not format_:
            error = "Matière et format sont requis"
        elif len(description) > 1000:
            error = "Description trop longue (max 1000 caractères)"
        else:
            try:
                # Insertion de la nouvelle offre de mentorat
                execute("""
                    INSERT INTO offre_mentorat (utilisateur_id, matiere_id, format, description)
                    VALUES (%s, %s, %s, %s)
                """, (session['user_id'], matiere_id, format_, description))
                
                return redirect(url_for('offres.offres'))
            except Exception as e:
                error = f"Erreur lors de la création de l'offre: {str(e)}"

    return render_template('mentorat/creer-offre.html', matieres=matieres, error=error)