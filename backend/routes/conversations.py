from flask import Blueprint, render_template, request, session, redirect, url_for
from db.database import get_connection

conversations_bp = Blueprint('conversations', __name__)

@conversations_bp.route('/conversations')
def conversations():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.id, c.cree_le,
                u.prenom, u.nom
            FROM conversations c
            JOIN participants_conversation pc ON pc.conversation_id = c.id
            JOIN participants_conversation pc2 ON pc2.conversation_id = c.id
            JOIN utilisateurs u ON u.id = pc2.utilisateur_id
            WHERE pc.utilisateur_id = %s AND pc2.utilisateur_id != %s
        """, (session['user_id'], session['user_id']))
        convs = cursor.fetchall()
        conn.close()
        return render_template('conversations/index.html', conversations=convs)
    except Exception as e:
        return f"Erreur lors du chargement des conversations: {str(e)}", 500
    finally:
        if conn:
            conn.close()

@conversations_bp.route('/conversations/<int:conv_id>', methods=['GET', 'POST'])
def conversation(conv_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    error = None
    messages = []
    if request.method == 'POST':
        conn = None
        try:
            contenu = request.form['contenu']
            cursor.execute("""
                INSERT INTO messages (conversation_id, expediteur_id, contenu)
                VALUES (%s, %s, %s)
            """, (conv_id, session['user_id'], contenu))
            conn.commit()
            conn.close()
        except Exception as e:
            error = f"Erreur lors de l'envoi du message: {str(e)}"
        finally:
            if conn:
                conn.close()
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT m.*, u.prenom, u.nom
            FROM messages m
            JOIN utilisateurs u ON u.id = m.expediteur_id
            WHERE m.conversation_id = %s
            ORDER BY m.envoye_le ASC
        """, (conv_id,))
        messages = cursor.fetchall()
        conn.close()
    except Exception as e:
        error = f"Erreur lors du chargement des messages: {str(e)}"
    finally:
        if conn:
            conn.close()

    return render_template('conversations/index.html',
                           messages=messages,
                           conv_id=conv_id,
                           error=error)
