# CHABI AYEDOUN Yoéla
from flask import Blueprint, render_template, request, session, redirect, url_for
# Centralisation des outils d'accès BDD depuis ton database.py
from db.database import fetch_one, execute
import bcrypt

settings_bp = Blueprint('settings', __name__)
# CHABI AYEDOUN Yoéla
from flask import Blueprint, render_template, request, session, redirect, url_for
from db.database import fetch_one, execute

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings/profil', methods=['GET', 'POST'])
def profil():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    error = None
    success = None
    
    try:
        if request.method == 'POST':
            prenom = request.form['prenom'].strip()
            nom = request.form['nom'].strip()
            biographie = request.form['biographie'].strip()
            telephone = request.form['telephone'].strip()
            # 🟢 AJOUT : Récupération de l'URL de l'avatar
            avatar_url = request.form['avatar_url'].strip()
            
            # 🛡️ ZONE SÉCURITÉ : Validation de base de l'URL
            if avatar_url and not (avatar_url.startswith('http://') or avatar_url.startswith('https://')):
                error = "L'URL de l'avatar doit commencer par http:// ou https://"
            else:
                # Si le champ est vide, on peut mettre une valeur par défaut ou None
                if not avatar_url:
                    avatar_url = None
                
                # 🟢 MISE A JOUR : Ajout de avatar_url dans la requête SQL
                execute("""
                    UPDATE utilisateurs 
                    SET prenom=%s, nom=%s, biographie=%s, telephone=%s, avatar_url=%s
                    WHERE id=%s
                """, (prenom, nom, biographie, telephone, avatar_url, session['user_id']))
                
                success = "Profil mis à jour avec succès"
            
        # Récupération des données fraîches (contenant le nouvel avatar_url)
        user = fetch_one("SELECT * FROM utilisateurs WHERE id=%s", (session['user_id'],))
        
    except Exception as e:
        user = None
        error = f"Erreur lors de la mise à jour du profil: {str(e)}"
        
    return render_template('settings/profil.html', user=user, error=error, success=success)

@settings_bp.route('/settings/securite', methods=['GET', 'POST'])
def securite():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    error = None
    success = None
    
    if request.method == 'POST':
        try:
            ancien = request.form['ancien_mdp']
            nouveau = request.form['nouveau_mdp']
            
            # Récupération du hash actuel en BDD
            user = fetch_one("SELECT mot_de_passe FROM utilisateurs WHERE id=%s", (session['user_id'],))
            
            if user and bcrypt.checkpw(ancien.encode('utf-8'), user['mot_de_passe'].encode('utf-8')):
                # Hachage sécurisé du nouveau mot de passe (Règle d'or Crypto 🛡️)
                hashed = bcrypt.hashpw(nouveau.encode('utf-8'), bcrypt.gensalt())
                
                execute("UPDATE utilisateurs SET mot_de_passe=%s WHERE id=%s",
                        (hashed.decode('utf-8'), session['user_id']))
                success = "Mot de passe mis à jour avec succès"
            else:
                error = "Ancien mot de passe incorrect"
        except Exception as e:
            error = f"Erreur lors de la mise à jour du mot de passe: {str(e)}"
            
    return render_template('settings/securite.html', error=error, success=success)


@settings_bp.route('/settings/confidentialite', methods=['GET', 'POST'])
def confidentialite():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    error = None
    success = None
    
    try:
        if request.method == 'POST':
            visibilite = request.form['visibilite_profil']
            # Gestion propre des checkboxes (1 si cochée, 0 si absente du formulaire)
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
            
        # Récupération des paramètres actuels de l'utilisateur
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
            # Soft delete (Bonne pratique : on désactive le compte au lieu de purger brutalement la ligne)
            execute("UPDATE utilisateurs SET est_actif=0 WHERE id=%s", (session['user_id'],))
            session.clear()
            return redirect(url_for('auth.login'))
        except Exception as e:
            error = f"Erreur lors de la suppression du compte: {str(e)}"

    return render_template('settings/supprimer-compte.html', error=error)