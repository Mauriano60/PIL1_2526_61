from flask import Blueprint, render_template, request, redirect, url_for, session
from db.database import fetch_all, fetch_one, execute
from utils.validators import valider_competences_et_lacunes

settings_bp = Blueprint('settings', __name__)

# =====================================================================
# 1. NOUVELLE ROUTE : MODIFICATION DES COMPÉTENCES ET LACUNES
# =====================================================================
@settings_bp.route('/settings/profil', methods=['GET', 'POST'])
def modifier_profil_matieres():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    user_id = session['user_id']
    error = None
    success = None
    
    try:
        if request.method == 'POST':
            # Récupération des listes d'IDs envoyées par le formulaire
            competences = request.form.getlist('competences')
            lacunes = request.form.getlist('lacunes')
            
            # SÉCURITÉ : Validation des contraintes métiers (Max 4 et Pas de doublons)
            est_valide, message_erreur = valider_competences_et_lacunes(competences, lacunes)
            if not est_valide:
                error = message_erreur
            else:
                # 1. Nettoyage des anciens choix en base de données
                execute("DELETE FROM competences_utilisateur WHERE utilisateur_id = %s", (user_id,))
                execute("DELETE FROM difficultes_utilisateur WHERE utilisateur_id = %s", (user_id,))
                
                # 2. Insertion des nouvelles compétences
                for comp_id in competences:
                    execute("""
                        INSERT INTO competences_utilisateur (utilisateur_id, matiere_id) 
                        VALUES (%s, %s)
                    """, (user_id, comp_id))
                    
                # 3. Insertion des nouvelles lacunes
                for lacune_id in lacunes:
                    execute("""
                        INSERT INTO difficultes_utilisateur (utilisateur_id, matiere_id) 
                        VALUES (%s, %s)
                    """, (user_id, lacune_id))
                    
                success = "Vos compétences et lacunes ont été mises à jour avec succès."

        # A. Charger toutes les matières disponibles dans l'application
        toutes_matieres = fetch_all("SELECT * FROM matieres ORDER BY nom ASC")
        
        # B. Récupérer uniquement les IDs des compétences actuelles de l'utilisateur
        res_comp = fetch_all("SELECT matiere_id FROM competences_utilisateur WHERE utilisateur_id = %s", (user_id,))
        ids_competences_actuelles = [rc['matiere_id'] for rc in res_comp]
        
        # C. Récupérer uniquement les IDs des lacunes actuelles de l'utilisateur
        res_lac = fetch_all("SELECT matiere_id FROM difficultes_utilisateur WHERE utilisateur_id = %s", (user_id,))
        ids_lacunes_actuelles = [rl['matiere_id'] for rl in res_lac]

    except Exception as e:
        toutes_matieres = []
        ids_competences_actuelles = []
        ids_lacunes_actuelles = []
        error = f"Erreur lors du traitement des données : {str(e)}"
        
    return render_template(
        'settings/profil_matieres.html',
        matieres=toutes_matieres,
        mes_competences=ids_competences_actuelles,
        mes_lacunes=ids_lacunes_actuelles,
        error=error,
        success=success
    )


# =====================================================================
# 2. VOS ROUTES EXISTANTES (CONSERVÉES À 100% SANS ALTERATION)
# =====================================================================
@settings_bp.route('/settings/preferences', methods=['GET', 'POST'])
def preferences():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    error = None
    success = None
    
    try:
        if request.method == 'POST':
            email_notif = 1 if 'email_notification' in request.form else 0
            push_notif  = 1 if 'push_notification' in request.form else 0
            match_notif = 1 if 'new_match_alerts' in request.form else 0
            weekly_notif = 1 if 'weekly_summary' in request.form else 0
            
            execute("""
                UPDATE parametres 
                SET email_notification = %s, 
                    push_notification = %s, 
                    new_match_alerts = %s, 
                    weekly_summary = %s
                WHERE utilisateur_id = %s
            """, (email_notif, push_notif, match_notif, weekly_notif, session['user_id']))
            
            success = "Préférences de notification mises à jour"
            
        params = fetch_one("SELECT * FROM parametres WHERE utilisateur_id = %s", (session['user_id'],))
        
    except Exception as e:
        params = None
        error = f"Erreur lors du cachement des préférences: {str(e)}"
        
    return render_template('settings/preferences.html', params=params, error=error, success=success)


@settings_bp.route('/settings/confidentialite', methods=['GET', 'POST'])
def confidentialite():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    error = None
    success = None
    
    try:
        if request.method == 'POST':
            visibilite = request.form['visibilite_profil']
            email_notif = 1 if 'email_notification' in request.form else 0
            push_notif = 1 if 'push_notification' in request.form else 0
            match_alerts = 1 if 'new_match_alerts' in request.form else 0
            weekly = 1 if 'weekly_summary' in request.form else 0
            
            execute("""
                UPDATE parametres SET visibilite_profil=%s, email_notification=%s,
                                      push_notification=%s, new_match_alerts=%s, weekly_summary=%s
                WHERE utilisateur_id=%s
            """, (visibilite, email_notif, push_notif, match_alerts, weekly, session['user_id']))
            
            success = "Paramètres de confidentialité mis à jour"
            
        params = fetch_one("SELECT * FROM parametres WHERE utilisateur_id=%s", (session['user_id'],))
        
    except Exception as e:
        params = None
        error = f"Erreur lors de la mise à jour des paramètres: {str(e)}"
        
    return render_template('settings/confidentialite.html', params=params, error=error, success=success)


@settings_bp.route('/settings/supprimer-compte', methods=['GET', 'POST'])
def supprimer_compte():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    error = None
    
    if request.method == 'POST':
        try:
            execute("UPDATE utilisateurs SET est_actif=0 WHERE id=%s", (session['user_id'],))
            session.clear()
            return redirect(url_for('auth.login'))
        except Exception as e:
            error = f"Erreur lors du traitement : {str(e)}"

    return render_template('settings/supprimer-compte.html', error=error)