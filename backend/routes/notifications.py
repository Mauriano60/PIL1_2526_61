from flask import Blueprint, render_template, session, redirect, url_for
from db.database import get_connection

notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/notifications')
def notifications():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM notifications
        WHERE utilisateur_id = %s
        ORDER BY cree_le DESC
    """, (session['user_id'],))
    notifs = cursor.fetchall()

    cursor.execute("""
        UPDATE notifications SET est_lu = 1
        WHERE utilisateur_id = %s
    """, (session['user_id'],))
    conn.commit()
    conn.close()

    return render_template('notifications/index.html', notifications=notifs)