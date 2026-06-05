import re

def valider_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return re.match(pattern, email) is not None

def valider_telephone(telephone):
    return telephone.isdigit() and len(telephone) >= 8

def valider_mot_de_passe(password):
    if len(password) < 8:
        return False, "Le mot de passe doit contenir au moins 8 caractères"
    if not any(c.isupper() for c in password):
        return False, "Le mot de passe doit contenir au moins une majuscule"
    if not any(c.isdigit() for c in password):
        return False, "Le mot de passe doit contenir au moins un chiffre"
    return True, None

def valider_inscription(form):
    erreurs = []

    if not form.get('prenom') or not form.get('nom'):
        erreurs.append("Prénom et nom obligatoires")

    if not valider_email(form.get('email', '')):
        erreurs.append("Email invalide")

    if not valider_telephone(form.get('telephone', '')):
        erreurs.append("Téléphone invalide")

    valide, msg = valider_mot_de_passe(form.get('password', ''))
    if not valide:
        erreurs.append(msg)

    if not form.get('id_filiere') or not form.get('id_niveau'):
        erreurs.append("Filière et niveau obligatoires")

    return erreurs