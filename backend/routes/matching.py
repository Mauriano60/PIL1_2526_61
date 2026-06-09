# CHABI AYEDOUN Yoéla
from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from services.matching_service import obtenir_suggestions_matching
from services.notification_service import creer_notification
from db.database import fetch_one, fetch_all, execute

matching_bp = Blueprint('matching', __name__)

# =====================================================================
# 1. PARCOURS AUTOMATIQUE & AFFICHAGE HISTORIQUE (Vue unifiée)
# =====================================================================
@matching_bp.route('/matching')
def matching():
    """
    Affiche la page de matching divisée en deux flux :
    - Le Top 4 des recommandations algorithmiques (Profils non encore contactés).
    - L'historique des interactions physiques réelles (En attente ou Acceptées).
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    utilisateur_id = session['user_id']
    role_actuel = request.args.get('role', 'mentee')
    if role_actuel not in ['mentor', 'mentee']:
        role_actuel = 'mentee'
        
    try:
        # --- A. RECOMMANDATIONS ALGORITHMIQUES ---
        toutes_suggestions = obtenir_suggestions_matching(utilisateur_id, role=role_actuel)
        toutes_suggestions.sort(key=lambda x: x['score_compatibilite'], reverse=True)
        
        # --- B. FILTRAGE SÉCURISÉ DES STATUS (Historique Catalogue) ---
        # On récupère les demandes actives de l'utilisateur (initiées ou reçues)
        # SÉCURITÉ : WHERE c.statut_correspondance != 2 permet de faire disparaître les matchs refusés
        matchs_physiques = fetch_all("""
            SELECT c.id, c.score_compatibilite, c.statut_correspondance, c.initiateur_id,
                   u.id AS partenaire_id, u.prenom, u.nom, u.email, f.nom as filiere, n.nom as niveau
            FROM correspondances c
            JOIN utilisateurs u ON (CASE 
                WHEN c.mentor_id = %s THEN c.mentee_id 
                ELSE c.mentor_id 
            END) = u.id
            JOIN filieres_etudes f ON u.id_filiere = f.id
            JOIN niveaux_etudes n ON u.id_niveau = n.id
            WHERE (c.mentor_id = %s OR c.mentee_id = %s) 
              AND c.statut_correspondance != 2
            ORDER BY c.id DESC
        """, (utilisateur_id, utilisateur_id, utilisateur_id))
        
        # Pour éviter qu'un profil apparaisse dans le Top 4 Recommandations alors qu'il a déjà 
        # fait l'objet d'une interaction physique (en attente ou accepté), on extrait les IDs connectés
        ids_interagis = {m['partenaire_id'] for m in matchs_physiques}
        
        # Filtrage : On ne garde dans le Top 4 que les profils purement "neufs" pour l'utilisateur
        suggestions_propres = [s for s in toutes_suggestions if s['id'] not in ids_interagis]
        suggestions_top_4 = suggestions_propres[:4]
        
        # Séparation des correspondances physiques pour le rendu Jinja
        matchs_en_attente = [m for m in matchs_physiques if m['statut_correspondance'] == 0]
        matchs_acceptes = [m for m in matchs_physiques if m['statut_correspondance'] == 1]
        
        return render_template(
            'matching/index.html', 
            mentors=suggestions_top_4, 
            role_actuel=role_actuel,
            matchs_en_attente=matchs_en_attente,
            matchs_acceptes=matchs_acceptes
        )
        
    except Exception as e:
        return f"Erreur lors du chargement des correspondances: {str(e)}", 500


# =====================================================================
# 2. PARCOURS CATALOGUE : CLIC SUR UNE OFFRE / DEMANDE
# =====================================================================
@matching_bp.route('/faire_match/<string:type_annonce>/<int:annonce_id>', methods=['POST'])
def faire_match(type_annonce, annonce_id):
    """
    Intercepte le clic sur le catalogue, calcule l'affinité, 
    crée la correspondance (Statut 0 = En attente), notifie le destinataire 
    et redirige instantanément vers l'onglet matching.
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    connecte_id = session['user_id']
    nom_expediteur = f"{session.get('prenom', 'Un étudiant')} {session.get('nom', '')}"
    
    try:
        if type_annonce == 'offre':
            role_matching = 'mentee'
            annonce = fetch_one("SELECT utilisateur_id FROM offre_mentorat WHERE id = %s AND statut_offre = 1", (annonce_id,))
            if not_annonce_valide(annonce, connecte_id):
                flash("Cette offre n'est plus disponible.", "warning")
                return redirect(url_for('offres.offres'))
                
            mentor_id = annonce['utilisateur_id']
            mentee_id = connecte_id
            destinataire_id = mentor_id
            message_notif = f"{nom_expediteur} a sollicité votre offre de mentorat ! Souhaitez-vous accepter le match ?"
            
        elif type_annonce == 'demande':
            role_matching = 'mentor'
            annonce = fetch_one("SELECT utilisateur_id FROM demande_mentorat WHERE id = %s AND statut_demande = 1", (annonce_id,))
            if not_annonce_valide(annonce, connecte_id):
                flash("Cette demande n'est plus disponible.", "warning")
                return redirect(url_for('demandes.demandes'))
                
            mentor_id = connecte_id
            mentee_id = annonce['utilisateur_id']
            destinataire_id = mentee_id
            message_notif = f"{nom_expediteur} propose de répondre à votre demande d'accompagnement ! Souhaitez-vous accepter ?"
            
        else:
            return "Action non autorisée", 400

        # Calcul automatique du score pour l'historiser
        score_final = 0.00
        suggestions = obtenir_suggestions_matching(connecte_id, role=role_matching)
        for sug in suggestions:
            if sug['id'] == destinataire_id:
                score_final = sug['score_compatibilite']
                break

        # Sauvegarde initiale : État 0 (En attente)
        correspondance_id = execute("""
            INSERT INTO correspondances (mentor_id, mentee_id, score_compatibilite, statut_correspondance, initiateur_id)
            VALUES (%s, %s, %s, 0, %s)
        """, (mentor_id, mentee_id, score_final, connecte_id))
        
        # Récupération de l'ID généré si nécessaire
        if not correspondance_id:
            recup = fetch_one("""
                SELECT id FROM correspondances 
                WHERE mentor_id = %s AND mentee_id = %s AND statut_correspondance = 0 AND initiateur_id = %s
                ORDER BY id DESC LIMIT 1
            """, (mentor_id, mentee_id, connecte_id))
            id_match = recup['id'] if recup else None
        else:
            id_match = correspondance_id

        if id_match:
            creer_notification(
                utilisateur_id=destinataire_id,
                message=message_notif,
                type_notification="match_demande",
                correspondance_id=id_match
            )
            
        flash("Votre demande de mise en relation a été enregistrée. Suivez son statut ici !", "success")
        return redirect(url_for('matching.matching'))
        
    except Exception as e:
        return f"Erreur lors de l'enregistrement de la mise en relation : {str(e)}", 500


# =====================================================================
# 3. TRAITEMENT DE LA DÉCISION (Boutons Accepter / Refuser)
# =====================================================================
@matching_bp.route('/traiter_match/<string:action>/<int:correspondance_id>', methods=['POST'])
def traiter_match(action, correspondance_id):
    """
    Route synchrone de décision : Modifie le statut en BDD (1=Accepté, 2=Refusé).
    Si l'action est 'refuser', le statut devient 2, ce qui provoquera 
    le retrait immédiat de l'affichage lors du rechargement automatique.
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    connecte_id = session['user_id']
    
    try:
        # Détermination de l'état : 1 si accepté, 2 si refusé
        nouveau_statut = 1 if action == 'accepter' else 2
        
        # Sécurité : On s'assure que l'utilisateur qui clique n'est pas l'initiateur de l'action
        execute("""
            UPDATE correspondances 
            SET statut_correspondance = %s 
            WHERE id = %s AND (mentor_id = %s OR mentee_id = %s) AND initiateur_id != %s
        """, (nouveau_statut, correspondance_id, connecte_id, connecte_id, connecte_id))
        
        if action == 'accepter':
            flash("Félicitations ! Le match est validé. Retrouvez vos coordonnées mutuelles.", "success")
        else:
            flash("La demande a été refusée. Le profil a été retiré de votre espace.", "info")
            
        return redirect(url_for('matching.matching'))
        
    except Exception as e:
        return f"Erreur lors du traitement du match : {str(e)}", 500


def not_annonce_valide(annonce, connecte_id):
    return not annonce or annonce['utilisateur_id'] == connecte_id