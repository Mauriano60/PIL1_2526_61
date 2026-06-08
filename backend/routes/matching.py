# CHABI AYEDOUN Yoéla
from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from services.matching_service import obtenir_suggestions_matching
from services.notification_service import creer_notification
from db.database import fetch_one, execute

matching_bp = Blueprint('matching', __name__)

# =====================================================================
# PARCOURS AUTOMATIQUE : LE MATCHING GLOBAL (Top 4 Recommandations)
# =====================================================================
@matching_bp.route('/matching')
def matching():
    """
    Affiche la page des suggestions de matching global basées sur le profil.
    Prend en compte le cas de figure (rôle) demandé via l'URL (?role=mentor ou ?role=mentee).
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    utilisateur_id = session['user_id']
    
    # Récupération du rôle choisi dans l'interface (par défaut 'mentee')
    role_actuel = request.args.get('role', 'mentee')
    if role_actuel not in ['mentor', 'mentee']:
        role_actuel = 'mentee'
        
    try:
        # Calcul des correspondances globales selon le rôle (Cas de figure)
        toutes_suggestions = obtenir_suggestions_matching(utilisateur_id, role=role_actuel)
        
        # Tri des profils par score de compatibilité décroissant
        toutes_suggestions.sort(key=lambda x: x['score_compatibilite'], reverse=True)
        
        # Limitation stricte aux 4 meilleurs profils pour l'affichage
        suggestions_top_4 = toutes_suggestions[:4]
        
        return render_template(
            'matching/index.html', 
            mentors=suggestions_top_4, 
            role_actuel=role_actuel
        )
        
    except Exception as e:
        return f"Erreur lors du chargement des correspondances: {str(e)}", 500


# =====================================================================
# PARCOURS CATALOGUE : L'ACTION PHYSIQUE DE MISE EN RELATION (Clic)
# =====================================================================
@matching_bp.route('/faire_match/<string:type_annonce>/<int:annonce_id>', methods=['POST'])
def faire_match(type_annonce, annonce_id):
    """
    Route d'action unifiée : Intercepte le clic sur une offre ou une demande,
    calcule le score réel basé sur le profil, fige l'annonce concernée en BDD (En attente : 0)
    et déclenche la notification interactive en temps réel.
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    connecte_id = session['user_id']
    nom_expediteur = f"{session.get('prenom', 'Un étudiant')} {session.get('nom', '')}"
    
    try:
        # 1. Traitement et définition des rôles selon la nature de l'élément cliqué
        if type_annonce == 'offre':
            # Clic sur une Offre -> L'auteur de l'offre est MENTOR, le connecté est MENTEE
            # Pour calculer le score, on se place sous le rôle de 'mentee'
            role_matching = 'mentee'
            annonce = fetch_one("SELECT utilisateur_id FROM offre_mentorat WHERE id = %s AND statut_offre = 1", (annonce_id,))
            if not_annonce_valide(annonce, connecte_id):
                flash("Cette offre n'est plus disponible.", "warning")
                return redirect(url_for('offres.offres'))
                
            mentor_id = annonce['utilisateur_id']
            mentee_id = connecte_id
            destinataire_id = mentor_id  # Le créateur de l'offre reçoit la notification
            message_notif = f"{nom_expediteur} a sollicité votre offre de mentorat ! Souhaitez-vous accepter le match ?"
            
        elif type_annonce == 'demande':
            # Clic sur une Demande -> L'auteur de la demande est MENTEE, le connecté est MENTOR
            # Pour calculer le score, on se place sous le rôle de 'mentor'
            role_matching = 'mentor'
            annonce = fetch_one("SELECT utilisateur_id FROM demande_mentorat WHERE id = %s AND statut_demande = 1", (annonce_id,))
            if not_annonce_valide(annonce, connecte_id):
                flash("Cette demande n'est plus disponible.", "warning")
                return redirect(url_for('demandes.demandes'))
                
            mentor_id = connecte_id
            mentee_id = annonce['utilisateur_id']
            destinataire_id = mentee_id  # Le créateur de la demande reçoit la notification
            message_notif = f"{nom_expediteur} propose de répondre à votre demande d'accompagnement ! Souhaitez-vous accepter ?"
            
        else:
            return "Action non autorisée", 400

        # 2. Sécurisation du Score : Calcul direct en arrière-plan via l'algorithme stabilisé
        score_final = 0.00
        suggestions = obtenir_suggestions_matching(connecte_id, role=role_matching)
        
        for sug in suggestions:
            if sug['id'] == destinataire_id:
                score_final = sug['score_compatibilite']
                break

        # 3. Sauvegarde de la correspondance en BDD (Statut 0 = En attente)
        correspondance_id = execute("""
            INSERT INTO correspondances (mentor_id, mentee_id, score_compatibilite, statut_correspondance, initiateur_id)
            VALUES (%s, %s, %s, 0, %s)
        """, (mentor_id, mentee_id, score_final, connecte_id))
        
        # Récupération de sécurité de l'ID généré si le wrapper n'historise pas cursor.lastrowid
        if not correspondance_id:
            recup = fetch_one("""
                SELECT id FROM correspondances 
                WHERE mentor_id = %s AND mentee_id = %s AND statut_correspondance = 0 AND initiateur_id = %s
                ORDER BY id DESC LIMIT 1
            """, (mentor_id, mentee_id, connecte_id))
            id_match = recup['id'] if recup else None
        else:
            id_match = correspondance_id

        # 4. Envoi de la notification interactive via le service WebSocket
        if id_match:
            creer_notification(
                utilisateur_id=destinataire_id,
                message=message_notif,
                type_notification="match_demande",  # Ce type magique active les boutons Accepter/Refuser
                correspondance_id=id_match
            )
            
        flash("Votre demande de mise en relation a été transmise en temps réel !", "success")
        
        # Redirection intelligente selon la provenance du flux
        if type_annonce == 'offre':
            return redirect(url_for('offres.offres'))
        else:
            return redirect(url_for('demandes.demandes'))
        
    except Exception as e:
        return f"Erreur lors de l'enregistrement de la mise en relation : {str(e)}", 500


def not_annonce_valide(annonce, connecte_id):
    """
    Fonction de sécurité : Vérifie si l'annonce existe et 
    empêche un étudiant de matcher avec sa propre publication.
    """
    return not annonce or annonce['utilisateur_id'] == connecte_id