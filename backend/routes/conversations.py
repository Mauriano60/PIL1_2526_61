# CHABI AYEDOUN Yoéla
from flask import Blueprint, render_template, request, session, redirect, url_for
from db.database import fetch_all, fetch_one, execute

conversations_bp = Blueprint('conversations', __name__)


@conversations_bp.route('/conversations')
def conversations():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    try:
        convs = fetch_all("""
            SELECT c.id, c.cree_le,
                   u.prenom, u.nom
            FROM conversations c
            JOIN participants_conversation pc ON pc.conversation_id = c.id
            JOIN participants_conversation pc2 ON pc2.conversation_id = c.id
            JOIN utilisateurs u ON u.id = pc2.utilisateur_id
            WHERE pc.utilisateur_id = %s AND pc2.utilisateur_id != %s
        """, (session['user_id'], session['user_id']))

        return render_template('conversations/index.html', conversations=convs)

    except Exception as e:
        return f"Erreur lors du chargement des conversations: {str(e)}", 500


@conversations_bp.route('/conversations/<int:conv_id>', methods=['GET', 'POST'])
def conversation(conv_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    # Vérification que l'utilisateur est bien participant
    try:
        participant = fetch_one("""
            SELECT 1 AS existe FROM participants_conversation
            WHERE conversation_id = %s AND utilisateur_id = %s
        """, (conv_id, session['user_id']))

        if not participant:
            return render_template('errors/403.html'), 403

    except Exception as e:
        return f"Erreur de vérification d'accès: {str(e)}", 500

    error = None
    messages = []

    # 1. Traitement de l'envoi d'un nouveau message
    if request.method == 'POST':
        try:
            contenu = request.form['contenu'].strip()
            if contenu:
                execute("""
                    INSERT INTO messages (conversation_id, expediteur_id, contenu)
                    VALUES (%s, %s, %s)
                """, (conv_id, session['user_id'], contenu))
                return redirect(url_for('conversations.conversation', conv_id=conv_id))
        except Exception as e:
            error = f"Erreur lors de l'envoi du message: {str(e)}"

    # 2. Chargement de l'historique des messages
    try:
        messages = fetch_all("""
            SELECT m.*, u.prenom, u.nom
            FROM messages m
            JOIN utilisateurs u ON u.id = m.expediteur_id
            WHERE m.conversation_id = %s
            ORDER BY m.envoye_le ASC
        """, (conv_id,))
    except Exception as e:
        error = f"Erreur lors du chargement des messages: {str(e)}"

    return render_template('conversations/index.html',
                           messages=messages,
                           conv_id=conv_id,
                           error=error)