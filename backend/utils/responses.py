from flask import redirect, url_for, session
from db.database import get_connection

def get_user_context():
    """Retourne les infos communes à toutes les pages (notifs non lues, user)"""
    if 'user_id' not in session:
        return {}
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM utilisateurs WHERE id = %s", (session['user_id'],))
        user = cursor.fetchone()
        cursor.execute("""
            SELECT COUNT(*) as nb FROM notifications
            WHERE utilisateur_id = %s AND est_lu = 0
        """, (session['user_id'],))
        notifs = cursor.fetchone()
        return {
            'user': user,
            'nb_notifs': notifs['nb'] if notifs else 0
        }
    except Exception as e:
        return {}
    finally:
        if conn:
            conn.close()

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated