# CHABI AYEDOUN Yoéla
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from db.database import fetch_all, execute
from services.matching_service import obtenir_suggestions_matching

demandes_bp = Blueprint('demandes', __name__)

# =====================================================================
# CAS DE FIGURE 1 : LE CATALOGUE DES DEMANDES DISPONIBLES (Consultation)
# =====================================================================
@demandes_bp.route('/demandes')
def demandes():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    connecte_id = session['user_id']
        
    try:
        # Sécurité & Filtrage : 
        # - Uniquement les demandes actives (d.statut_demande = 1). Les inactives (0) disparaissent.
        # - Exclusion des demandes créées par le connecté (d.utilisateur_id != %s).
        # - LEFT JOIN pour lier dynamiquement le statut de la correspondance si elle existe.
        demandes_liste = fetch_all("""
            SELECT d.*, m.nom as matiere, u.prenom, u.nom as nom_user,
                   f.nom as filiere, n.nom as niveau,
                   c.statut_correspondance, c.initiateur_id, c.score_compatibilite as score_enregistre
            FROM demande_mentorat d
            JOIN matieres m ON m.id = d.matiere_id
            JOIN utilisateurs u ON u.id = d.utilisateur_id
            JOIN filieres_etudes f ON f.id = u.id_filiere
            JOIN niveaux_etudes n ON n.id = u.id_niveau
            LEFT JOIN correspondances c ON (
                (c.mentor_id = %s AND c.mentee_id = d.utilisateur_id)
                OR (c.mentor_id = d.utilisateur_id AND c.mentee_id = %s)
            )
            WHERE d.statut_demande = 1 
              AND d.utilisateur_id != %s
            ORDER BY d.cree_le DESC
        """, (connecte_id, connecte_id, connecte_id))
        
        # Injection du score de compatibilité calculé via le profil
        for demande in demandes_liste:
            if demande['statut_correspondance'] is not None:
                # Si le match existe (en attente ou accepté), on utilise le score stocké
                demande['score_affiche'] = demande['score_enregistre']
            else:
                # Sinon, calcul du score en temps réel par rapport au profil de l'auteur de la demande
                scores_profil = obtenir_suggestions_matching(demande['utilisateur_id'])
                demande['score_affiche'] = 0.00
                for sug in scores_profil:
                    if sug['id'] == connecte_id:  # Si le connecté correspond au mentor potentiel
                        demande['score_affiche'] = sug['score_compatibilite']
                        break

        return render_template('mentorat/demandes.html', demandes=demandes_liste)
        
    except Exception as e:
        return f"Erreur lors du chargement des demandes: {str(e)}", 500


# =====================================================================
# CAS DE FIGURE 2 : LA PUBLICATION + MATCHING INSTANTANÉ (Même fenêtre)
# =====================================================================
@demandes_bp.route('/demandes/creer', methods=['GET', 'POST'])
def creer_demande():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    connecte_id = session['user_id']
    error = None
    matchs_trouves = None  # Devient une liste de profils après la soumission réussie
    
    # Chargement initial des matières pour le menu déroulant
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
                # 1. Insertion de la nouvelle demande marquée comme ACTIVE (1)
                execute("""
                    INSERT INTO demande_mentorat (utilisateur_id, matiere_id, format, description, statut_demande)
                    VALUES (%s, %s, %s, %s, 1)
                """, (connecte_id, matiere_id, format_, description))
                
                flash("Votre demande d'aide a été partagée avec succès !", "success")
                
                # 2. Exécution et capture immédiate des mentors suggérés par l'algorithme
                toutes_suggestions = obtenir_suggestions_matching(connecte_id)
                
                # Tri par score de compatibilité décroissant
                toutes_suggestions.sort(key=lambda x: x['score_compatibilite'], reverse=True)
                
                # Top 5 des mentors potentiels. Sa simple présence masquera le formulaire dans ton HTML.
                matchs_trouves = toutes_suggestions[:5]
                
            except Exception as e:
                error = f"Erreur lors de la création de la demande et du matching instantané: {str(e)}"

    return render_template(
        'mentorat/creer-demande.html', 
        matieres=matieres, 
        error=error, 
        matchs=matchs_trouves
    )