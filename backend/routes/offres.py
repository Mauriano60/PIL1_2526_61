# CHABI AYEDOUN Yoéla
from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from db.database import fetch_all, execute
from services.matching_service import obtenir_suggestions_matching

offres_bp = Blueprint('offres', __name__)

# =====================================================================
# CAS DE FIGURE 1 : LE CATALOGUE DES OFFRES DISPONIBLES (Consultation)
# =====================================================================
@offres_bp.route('/offres')
def offres():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    connecte_id = session['user_id']
        
    try:
        # Sécurité & Filtrage : 
        # - Uniquement les offres actives (o.statut_offre = 1). Les inactives (0) disparaissent de la liste.
        # - Exclusion des offres créées par l'utilisateur connecté (o.utilisateur_id != %s).
        # - LEFT JOIN pour récupérer l'état d'un éventuel match initié ou reçu.
        offres_liste = fetch_all("""
            SELECT o.*, m.nom as matiere, u.prenom, u.nom as nom_user,
                   f.nom as filiere, n.nom as niveau,
                   c.statut_correspondance, c.initiateur_id, c.score_compatibilite as score_enregistre
            FROM offre_mentorat o
            JOIN matieres m ON m.id = o.matiere_id
            JOIN utilisateurs u ON u.id = o.utilisateur_id
            JOIN filieres_etudes f ON f.id = u.id_filiere
            JOIN niveaux_etudes n ON n.id = u.id_niveau
            LEFT JOIN correspondances c ON (
                (c.mentor_id = o.utilisateur_id AND c.mentee_id = %s)
                OR (c.mentor_id = %s AND c.mentee_id = o.utilisateur_id)
            )
            WHERE o.statut_offre = 1 
              AND o.utilisateur_id != %s
            ORDER BY o.cree_le DESC
        """, (connecte_id, connecte_id, connecte_id))
        
        # Injection dynamique du score calculé par l'algorithme basé sur le profil
        for offre in offres_liste:
            if offre['statut_correspondance'] is not None:
                # Si l'utilisateur a déjà cliqué, on affiche fixement le score sauvegardé en BDD
                offre['score_affiche'] = offre['score_enregistre']
            else:
                # Sinon, calcul et affichage du score de compatibilité en temps réel avant l'action
                scores_profil = obtenir_suggestions_matching(connecte_id)
                offre['score_affiche'] = 0.00
                for sug in scores_profil:
                    if sug['id'] == offre['utilisateur_id']:
                        offre['score_affiche'] = sug['score_compatibilite']
                        break

        return render_template('mentorat/offres.html', offres=offres_liste)
        
    except Exception as e:
        return f"Erreur lors du chargement des offres: {str(e)}", 500


# =====================================================================
# CAS DE FIGURE 2 : LA PUBLICATION + MATCHING INSTANTANÉ (Même fenêtre)
# =====================================================================
@offres_bp.route('/offres/creer', methods=['GET', 'POST'])
def creer_offre():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    connecte_id = session['user_id']
    error = None
    matchs_trouves = None  # Passe à une liste de profils après le POST (déclenche le masquage du formulaire)
    
    # Chargement des matières disponibles pour le menu déroulant
    try:
        matieres = fetch_all("SELECT * FROM matieres")
    except Exception as e:
        matieres = []
        error = f"Erreur lors du chargement des matières: {str(e)}"

    if request.method == 'POST':
        # Récupération sécurisée des champs du formulaire
        matiere_id = request.form.get('matiere_id')
        format_ = request.form.get('format')
        description = request.form.get('description', '').strip()
        
        # Validation des données entrantes
        if not matiere_id or not format_:
            error = "Matière et format sont requis"
        elif len(description) > 1000:
            error = "Description trop longue (max 1000 caractères)"
        else:
            try:
                # 1. Insertion de la nouvelle offre de mentorat marquée comme ACTIVE (1)
                execute("""
                    INSERT INTO offre_mentorat (utilisateur_id, matiere_id, format, description, statut_offre)
                    VALUES (%s, %s, %s, %s, 1)
                """, (connecte_id, matiere_id, format_, description))
                
                flash("Votre offre de mentorat a été publiée avec succès !", "success")
                
                # 2. Exécution immédiate de l'algorithme de matching basé sur le profil
                toutes_suggestions = obtenir_suggestions_matching(connecte_id)
                
                # Tri décroissant selon le score de pertinence
                toutes_suggestions.sort(key=lambda x: x['score_compatibilite'], reverse=True)
                
                # On capture le top 5 des mentees compatibles. 
                # Le fait de remplir cette variable fera disparaître le formulaire côté HTML.
                matchs_trouves = toutes_suggestions[:5]
                
            except Exception as e:
                error = f"Erreur lors de la création de l'offre et du matching instantané: {str(e)}"

    return render_template(
        'mentorat/creer-offre.html', 
        matieres=matieres, 
        error=error, 
        matchs=matchs_trouves
    )