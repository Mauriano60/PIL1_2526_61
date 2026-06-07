from db.database import fetch_one, execute

def creer_notification(utilisateur_id, type_notif):
    """
    Insère une nouvelle notification pour un utilisateur donné.
    Le champ 'est_lu' sera à 0 par défaut grâce à la structure MySQL.
    """
    try:
        execute("""
            INSERT INTO notifications (utilisateur_id, type)
            VALUES (%s, %s)
        """, (utilisateur_id, type_notif))
        print(f"Notification '{type_notif}' créée avec succès pour l'utilisateur {utilisateur_id}")
    except Exception as e:
        print(f"Erreur lors de la création de la notification: {str(e)}")
