# CHABI AYEDOUN Yoéla
from flask import Blueprint, render_template, request, session, redirect, url_for
# On importe uniquement les outils d'abstraction de ton database.py
from db.database import fetch_all, execute

demandes_bp = Blueprint('demandes', __name__)

@demandes_bp.route('/demandes')
def demandes():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    try:
        # Récupération de toutes les demandes avec jointures (gérée proprement par fetch_all)
        demandes_liste = fetch_all("""
            SELECT d.*, m.nom as matiere, u.prenom, u.nom as nom_user
            FROM demande_mentorat d
            JOIN matieres m ON m.id = d.matiere_id
            JOIN utilisateurs u ON u.id = d.utilisateur_id
            ORDER BY d.cree_le DESC
        """)
        return render_template('mentorat/demandes.html', demandes=demandes_liste)
        
    except Exception as e:
        return f"Erreur lors du chargement des demandes: {str(e)}", 500


@demandes_bp.route('/demandes/creer', methods=['GET', 'POST'])
def creer_demande():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    error = None
    
    # Chargement initial des matières pour le formulaire
    try:
        matieres = fetch_all("SELECT * FROM matieres")
    except Exception as e:
        matieres = []
        error = f"Erreur lors du chargement des matières: {str(e)}"

    if request.method == 'POST':
        matiere_id = request.form.get('matiere_id')
        format_ = request.form.get('format')
        description = request.form.get('description', '').strip()
        
        # Validations de sécurité
        if not matiere_id or not format_:
            error = "Matière et format sont requis"
        elif len(description) > 1000:
            error = "Description trop longue (max 1000 caractères)"
        else:
            try:
                # CORRECTION CRITIQUE : Ajout de la clause VALUES pour l'insertion
                execute("""
                    INSERT INTO demande_mentorat (utilisateur_id, matiere_id, format, description)
                    VALUES (%s, %s, %s, %s)
                """, (session['user_id'], matiere_id, format_, description))
                
                return redirect(url_for('demandes.demandes'))
            except Exception as e:
                error = f"Erreur lors de la création de la demande: {str(e)}"

    return render_template('mentorat/creer-demande.html', matieres=matieres, error=error)