# CHABI AYEDOUN Yoéla
from flask import Blueprint, render_template, request, session, redirect, url_for
# On utilise les fonctions d'abstraction de ton groupe
from db.database import fetch_all, execute

conversations_bp = Blueprint('conversations', __name__)

@conversations_bp.route('/conversations')
def conversations():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    try:
        # Récupération de la liste des conversations de l'étudiant connecté
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
        
    error = None
    messages = []
    
    # 1. Traitement de l'envoi d'un nouveau message
    if request.method == 'POST':
        try:
            contenu = request.form['contenu'].strip()
            if contenu:  # Validation basique pour éviter les messages vides
                execute("""
                    INSERT INTO messages (conversation_id, expediteur_id, contenu)
                    VALUES (%s, %s, %s)
                """, (conv_id, session['user_id'], contenu))
                
                # Optionnel mais recommandé : Rediriger en GET pour éviter le renvoi du formulaire si on rafraîchit la page
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