from flask import Blueprint, render_template, request, session, redirect, url_for
from db.database import get_connection
import bcrypt

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings/profil', methods=['GET', 'POST'])
def profil():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    error = None
    success = None
    user = None
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        if request.method == 'POST':
            prenom = request.form['prenom']
            nom = request.form['nom']
            biographie = request.form['biographie']
            telephone = request.form['telephone']
            cursor.execute("""
                UPDATE utilisateurs SET prenom=%s, nom=%s, biographie=%s, telephone=%s
                WHERE id=%s
            """, (prenom, nom, biographie, telephone, session['user_id']))
            conn.commit()
        cursor.execute("SELECT * FROM utilisateurs WHERE id=%s", (session['user_id'],))
        user = cursor.fetchone()
        conn.close()
    except Exception as e:
        error = f"Erreur lors de la mise à jour du profil: {str(e)}"
    finally:
        if conn:
            conn.close()
    return render_template('settings/profil.html', user=user, error=error)

@settings_bp.route('/settings/securite', methods=['GET', 'POST'])
def securite():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    error = None
    success = None
    conn = None
    if request.method == 'POST':
        try:
            ancien = request.form['ancien_mdp']
            nouveau = request.form['nouveau_mdp']
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT mot_de_passe FROM utilisateurs WHERE id=%s", (session['user_id'],))
            user = cursor.fetchone()
            if bcrypt.checkpw(ancien.encode('utf-8'), user['mot_de_passe'].encode('utf-8')):
                hashed = bcrypt.hashpw(nouveau.encode('utf-8'), bcrypt.gensalt())
                cursor.execute("UPDATE utilisateurs SET mot_de_passe=%s WHERE id=%s",
                            (hashed.decode('utf-8'), session['user_id']))
                conn.commit()
                success = "Mot de passe mis à jour"
            else:
                error = "Ancien mot de passe incorrect"
            conn.close()
        except Exception as e:
            error = f"Erreur lors de la mise à jour du mot de passe: {str(e)}"
        finally:
            if conn:
                conn.close()
    return render_template('settings/securite.html', error=error, success=success)

@settings_bp.route('/settings/confidentialite', methods=['GET', 'POST'])
def confidentialite():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    error = None
    success = None
    params = None
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        if request.method == 'POST':
            visibilite = request.form['visibilite_profil']
            email_notif = 1 if 'email_notification' in request.form else 0
            push_notif = 1 if 'push_notification' in request.form else 0
            match_alerts = 1 if 'new_match_alerts' in request.form else 0
            weekly = 1 if 'weekly_summary' in request.form else 0
            cursor.execute("""
                UPDATE parametres SET visibilite_profil=%s, email_notification=%s,
                push_notification=%s, new_match_alerts=%s, weekly_summary=%s
                WHERE utilisateur_id=%s
            """, (visibilite, email_notif, push_notif, match_alerts, weekly, session['user_id']))
            conn.commit()
            success = "Paramètres mis à jour"
        cursor.execute("SELECT * FROM parametres WHERE utilisateur_id=%s", (session['user_id'],))
        params = cursor.fetchone()
        conn.close()
    except Exception as e:
        error = f"Erreur lors de la mise à jour des paramètres: {str(e)}"
    finally:
        if conn:
            conn.close()
    return render_template('settings/confidentialite.html', params=params, error=error)

@settings_bp.route('/settings/supprimer-compte', methods=['GET', 'POST'])
def supprimer_compte():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    error = None
    conn = None
    if request.method == 'POST':
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE utilisateurs SET est_actif=0 WHERE id=%s", (session['user_id'],))
            conn.commit()
            conn.close()
            session.clear()
            return redirect(url_for('auth.login'))
        except Exception as e:
            error = f"Erreur lors de la suppression du compte: {str(e)}"
        finally:
            if conn:
                conn.close()

    return render_template('settings/supprimer-compte.html' , error=error)