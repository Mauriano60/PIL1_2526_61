CREATE DATABASE IF NOT EXISTS ifri_mentorlink CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ifri_mentorlink;

DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS participants_conversation;
DROP TABLE IF EXISTS conversations;
DROP TABLE IF EXISTS competences_utilisateur;
DROP TABLE IF EXISTS difficultes_utilisateur;
DROP TABLE IF EXISTS review;
DROP TABLE IF EXISTS correspondances;
DROP TABLE IF EXISTS offre_mentorat;
DROP TABLE IF EXISTS demande_mentorat;
DROP TABLE IF EXISTS notifications;
DROP TABLE IF EXISTS disponibilites;
DROP TABLE IF EXISTS utilisateurs;
DROP TABLE IF EXISTS matieres;
DROP TABLE IF EXISTS filieres_etudes;
DROP TABLE IF EXISTS niveaux_etudes;

CREATE TABLE matieres (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) UNIQUE NOT NULL
) ENGINE=InnoDB;

CREATE TABLE conversations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cree_le TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE filieres_etudes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) UNIQUE NOT NULL
) ENGINE=InnoDB;

CREATE TABLE niveaux_etudes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) UNIQUE NOT NULL
) ENGINE=InnoDB;

CREATE TABLE utilisateurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    telephone VARCHAR(20) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    avatar_url TEXT,
    biographie TEXT,
    email_verifie TINYINT(1) DEFAULT 0,
    cree_le TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_filiere INT NOT NULL,
    id_niveau INT NOT NULL,
    FOREIGN KEY (id_filiere) REFERENCES filieres_etudes(id) ON DELETE CASCADE,
    FOREIGN KEY (id_niveau) REFERENCES niveaux_etudes(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE competences_utilisateur (
    utilisateur_id INT NOT NULL,
    matiere_id INT NOT NULL,
    PRIMARY KEY(utilisateur_id, matiere_id),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE,
    FOREIGN KEY (matiere_id) REFERENCES matieres(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE difficultes_utilisateur (
    utilisateur_id INT NOT NULL,
    matiere_id INT NOT NULL,
    PRIMARY KEY(utilisateur_id, matiere_id),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE,
    FOREIGN KEY (matiere_id) REFERENCES matieres(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE disponibilites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur_id INT NOT NULL,
    jour_semaine VARCHAR(20) NOT NULL,
    heure_debut TIME NOT NULL,
    heure_fin TIME NOT NULL,
    CHECK (heure_debut < heure_fin),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE offre_mentorat (
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur_id INT NOT NULL,
    matiere_id INT NOT NULL,
    format VARCHAR(20) NOT NULL,
    description TEXT,
    cree_le TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (format IN ('en_ligne', 'presentiel', 'les_deux')),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE,
    FOREIGN KEY (matiere_id) REFERENCES matieres(id)
) ENGINE=InnoDB;

CREATE TABLE demande_mentorat (
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur_id INT NOT NULL,
    matiere_id INT NOT NULL,
    format VARCHAR(20) NOT NULL,
    description TEXT,
    cree_le TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (format IN ('en_ligne', 'presentiel', 'les_deux')),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE,
    FOREIGN KEY (matiere_id) REFERENCES matieres(id)
) ENGINE=InnoDB;

CREATE TABLE correspondances (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mentor_id INT NOT NULL,
    mentee_id INT NOT NULL,
    score_compatibilite DECIMAL(5,2) NOT NULL,
    cree_le TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (mentor_id) REFERENCES utilisateurs(id) ON DELETE CASCADE,
    FOREIGN KEY (mentee_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE participants_conversation (
    conversation_id INT NOT NULL,
    utilisateur_id INT NOT NULL,
    PRIMARY KEY (conversation_id, utilisateur_id),
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conversation_id INT NOT NULL,
    expediteur_id INT NOT NULL,
    contenu TEXT NOT NULL,
    envoye_le TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    FOREIGN KEY (expediteur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    utilisateur_id INT NOT NULL,
    type VARCHAR(50) NOT NULL,
    est_lu TINYINT(1) DEFAULT 0,
    cree_le TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
) ENGINE=InnoDB;

 CREATE TABLE review (
    id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    reviewer_id INT NOT NULL,
    reviewed_user_id INT NOT NULL,
    rating SMALLINT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    cree_le TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (match_id) REFERENCES correspondances(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewer_id) REFERENCES utilisateurs(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewed_user_id) REFERENCES utilisateurs(id) ON DELETE CASCADE
) ENGINE=InnoDB;

INSERT INTO matieres (nom) VALUES
('Algorithmique'), ('Base de donnees'), ('Programmation web'), ('Reseaux'),
('Genie logiciel'), ('Mathematiques'), ('Systeme Linux'), ('Anglais technique');

INSERT INTO filieres_etudes (nom) VALUES
('Genie logiciel'), ('Informatique'), ('Mathematiques'), ('Systeme Linux');

INSERT INTO niveaux_etudes (nom) VALUES
('Licence 1'), ('Licence 2'), ('Licence 3'), ('Master 1'), ('Master 2');

INSERT INTO utilisateurs (email, telephone, mot_de_passe, prenom, nom, id_filiere, id_niveau, biographie, email_verifie)
VALUES
('mentor@ifri.test', '97000001', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2uheWG/igi.', 'Aminata', 'Mensah', 1, 3, 'Je peux aider en web, bases de donnees et methodologie de projet.', 1),
('mentee@ifri.test', '97000002', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2uheWG/igi.', 'Koffi', 'Dossou', 2, 1, 'Je cherche un accompagnement regulier pour progresser en programmation.', 1);

INSERT INTO competences_utilisateur VALUES (1, 2), (1, 3), (1, 5), (2, 7);
INSERT INTO difficultes_utilisateur VALUES (2, 2), (2, 3), (1, 6);

INSERT INTO disponibilites (utilisateur_id, jour_semaine, heure_debut, heure_fin)
VALUES (1, 'Samedi', '09:00:00', '12:00:00'), (2, 'Samedi', '10:00:00', '13:00:00');

INSERT INTO offre_mentorat (utilisateur_id, matiere_id, format, description)
VALUES
(1, 3, 'les_deux', 'Sessions pratiques pour comprendre HTML, CSS, PHP et les bases MVC.');
INSERT INTO demande_mentorat (utilisateur_id, matiere_id, format, description)
VALUES
(2, 2, 'en_ligne', 'Besoin d aide pour SQL, jointures et conception de schema.');
INSERT INTO correspondances (mentor_id, mentee_id, score_compatibilite) VALUES (1, 2, 85.00);
INSERT INTO conversations () VALUES ();
INSERT INTO participants_conversation (conversation_id, utilisateur_id) VALUES (1, 1), (1, 2);
INSERT INTO messages (conversation_id, expediteur_id, contenu) VALUES (1, 1, 'Bonjour Koffi, ravi de te rencontrer! Je suis Aminata, ton mentor pour la programmation web. N hesite pas a me poser toutes tes questions.'), (1, 2, 'Bonjour Aminata, merci de m accompagner! J ai deja quelques questions sur les bases de donnees, notamment les jointures. Pourrais tu m expliquer comment elles fonctionnent?');
INSERT INTO notifications (utilisateur_id, type) VALUES (1, 'nouvelle_conversation'), (2, 'nouvelle_conversation');
INSERT INTO review (match_id, reviewer_id, reviewed_user_id, rating, comment) VALUES (1, 2, 1, 5, 'Aminata est une mentor exceptionnelle! Elle a su expliquer les concepts de manière claire et m a donné des exercices pratiques qui m ont beaucoup aidé. Je recommande vivement!');