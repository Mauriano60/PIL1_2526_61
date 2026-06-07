# CHABI AYEDOUN Yoéla
from flask import Blueprint, render_template, session, redirect, url_for
# On importe les deux outils nécessaires depuis ton database.py
from db.database import fetch_all, execute

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/notifications')
def notifications():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    try:
        # 1. Récupération de l'historique des notifications de l'utilisateur
        notifs = fetch_all("""
            SELECT * FROM notifications
            WHERE utilisateur_id = %s
            ORDER BY cree_le DESC
        """, (session['user_id'],))
        
        # 2. Passage automatique de toutes ses notifications au statut "lu"
        execute("""
            UPDATE notifications SET est_lu = 1
            WHERE utilisateur_id = %s
        """, (session['user_id'],))
        
        return render_template('notifications/index.html', notifications=notifs)
        
    except Exception as e:
        return f"Erreur lors du chargement des notifications: {str(e)}", 500