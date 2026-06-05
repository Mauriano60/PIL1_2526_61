from db.database import get_connection

def creer_notification(utilisateur_id, type_notif):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO notifications (utilisateur_id, type)
        VALUES (%s, %s)
    """, (utilisateur_id, type_notif))
    conn.commit()
    conn.close()

def marquer_toutes_lues(utilisateur_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE notifications SET est_lu = 1
        WHERE utilisateur_id = %s
    """, (utilisateur_id,))
    conn.commit()
    conn.close()

def compter_non_lues(utilisateur_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT COUNT(*) as nb FROM notifications
        WHERE utilisateur_id = %s AND est_lu = 0
    """, (utilisateur_id,))
    result = cursor.fetchone()
    conn.close()
    return result['nb'] if result else 0