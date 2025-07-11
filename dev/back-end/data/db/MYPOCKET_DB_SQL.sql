CREATE DATABASE MyPocketDb;
USE MyPocketDb;

CREATE TABLE test (
    id INT PRIMARY KEY AUTO_INCREMENT,
    firstname VARCHAR(20),
    lastname VARCHAR(20)
);

INSERT INTO test (firstname, lastname) VALUES
    ('amine', 'majid'),
    ('sounds', 'majid'),
    ('ilias', 'majid');



-- Table: Annonceur
CREATE TABLE Annonceur (
    AnnonceurId INT AUTO_INCREMENT PRIMARY KEY,
    CarteNationale VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Nom VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Prenom VARCHAR(255) NOT NULL,
    Profile_Image VARCHAR(255),
    Telephone VARCHAR(15) NOT NULL,
    Ville VARCHAR(255) NOT NULL,
    Status VARCHAR(255) NOT NULL,
    VerificationCode VARCHAR(6),
    VerificationCodeExpiration DATETIME,
    CONSTRAINT chk_PasswordComplexity_Annonceur CHECK (
        Password REGEXP '^(?=.*[0-9])(?=.*[!@#$%^&*])(?=.{8,})'
    ),
    CONSTRAINT check_status_Annonceur CHECK (Status IN ('active', 'disabled', 'toVerify','toVerifyByAdmin')),
    CONSTRAINT chk_EmailFormat_Annonceur CHECK (Email LIKE '%@%.%'),
    CONSTRAINT chk_PasswordLength_Annonceur CHECK (LENGTH(Password) >= 8),
    CONSTRAINT chk_TelephoneFormat_Annonceur CHECK (Telephone REGEXP '^[0-9]{10,15}$'),
    CONSTRAINT unq_CarteNationale_Annonceur UNIQUE (CarteNationale),
    CONSTRAINT unq_Email_Annonceur UNIQUE (Email),
    CONSTRAINT chk_VerificationCode_Annonceur CHECK (VerificationCode REGEXP '^[0-9]{6}$')
);

-- Table: Etudiant
CREATE TABLE Etudiant (
    EtudiantId INT AUTO_INCREMENT PRIMARY KEY,
    justificationDocument VARCHAR(255) NOT NULL,
    CarteNationale VARCHAR(255) NOT NULL,
    ConterInteret VARCHAR(255),
    Email VARCHAR(255) NOT NULL,
    EtablissementScolaire VARCHAR(255),
    Nom VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Prenom VARCHAR(255) NOT NULL,
    Profile_Image VARCHAR(255),
    Telephone VARCHAR(15) NOT NULL,
    Ville VARCHAR(255) NOT NULL,
    Status VARCHAR(255) NOT NULL,
    VerificationCode VARCHAR(6),
    VerificationCodeExpiration DATETIME,
    CONSTRAINT chk_PasswordComplexity_Etudiant CHECK (
        Password REGEXP '^(?=.*[0-9])(?=.*[!@#$%^&*])(?=.{8,})'
    ),
    CONSTRAINT check_status_Etudiant CHECK (Status IN ('active', 'disabled', 'toVerify','toVerifyByAdmin')),
    CONSTRAINT ConterInteret CHECK (ConterInteret IN ('productsOffers', 'housingOffers', 'jobOffers')),
    CONSTRAINT chk_EmailFormat CHECK (Email LIKE '%@%.%'),
    CONSTRAINT chk_PasswordLength CHECK (LENGTH(Password) >= 8),
    CONSTRAINT chk_TelephoneFormat CHECK (Telephone REGEXP '^[0-9]{10,15}$'),
    CONSTRAINT unq_CarteNationale UNIQUE (CarteNationale),
    CONSTRAINT unq_Email UNIQUE (Email),
    CONSTRAINT chk_VerificationCode_Etudiant CHECK (VerificationCode REGEXP '^[0-9]{6}$')
);

-- Table: Admin
CREATE TABLE Admin (
    AdminId INT AUTO_INCREMENT PRIMARY KEY,
    CarteNationale VARCHAR(255) NOT NULL,
    Admin_Type VARCHAR(20) NOT NULL,
    CompteId INT NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Nom VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Prenom VARCHAR(255) NOT NULL,
    Profile_Image VARCHAR(255),
    Telephone VARCHAR(15) NOT NULL,
    Status VARCHAR(255) NOT NULL,
    VerificationCode VARCHAR(6),
    VerificationCodeExpiration DATETIME,
    CONSTRAINT chk_PasswordComplexity_Admin CHECK (
        Password REGEXP '^(?=.*[0-9])(?=.*[!@#$%^&*])(?=.{8,})'
    ),
    CONSTRAINT check_status_Admin CHECK (Status IN ('active', 'disabled', 'toVerify','toVerifyByAdmin')),
    CONSTRAINT check_Admin_Type_Admin CHECK (Admin_type IN ('admin', 'registerValidator')),
    CONSTRAINT chk_Admin_Type CHECK (Admin_Type IN (1, 2, 3)),
    CONSTRAINT chk_EmailFormat_Admin CHECK (Email LIKE '%@%.%'),
    CONSTRAINT chk_PasswordLength_Admin CHECK (LENGTH(Password) >= 8),
    CONSTRAINT chk_TelephoneFormat_Admin CHECK (Telephone REGEXP '^[0-9]{10,15}$'),
    CONSTRAINT unq_Email_Admin UNIQUE (Email),
    CONSTRAINT chk_VerificationCode_Admin CHECK (VerificationCode REGEXP '^[0-9]{6}$')
);

CREATE INDEX idx_email_annonceur ON Annonceur(Email);
CREATE INDEX idx_email_etudiant ON Etudiant(Email);
CREATE INDEX idx_email_admin ON Admin(Email);

-- Table: Produit
CREATE TABLE Produit (
    ProduitId INT AUTO_INCREMENT PRIMARY KEY,
    Categorie VARCHAR(255) NOT NULL,
    Description TEXT,
    Disponible INT NOT NULL,
    FK_AnnonceurId INT NOT NULL,
    Nom VARCHAR(255) NOT NULL UNIQUE ,
    Prix DOUBLE NOT NULL,
    Stock INT NOT NULL,
    CONSTRAINT chk_Disponible CHECK (Disponible IN (0, 1)),
    CONSTRAINT chk_Prix CHECK (Prix >= 0),
    CONSTRAINT chk_Stock CHECK (Stock >= 0),
    CONSTRAINT fk_Produit_Annonceur FOREIGN KEY (FK_AnnonceurId) REFERENCES Annonceur(AnnonceurId) ON DELETE CASCADE
);

-- Table: ProduitImages
CREATE TABLE ProduitImages (
    FK_ProduitId INT NOT NULL,
    ImageId INT NOT NULL,
    PRIMARY KEY (FK_ProduitId, ImageId),
    CONSTRAINT fk_ProduitImages_Produit FOREIGN KEY (FK_ProduitId) REFERENCES Produit(ProduitId) ON DELETE CASCADE
);


-- Table: Commande
CREATE TABLE Commande (
    CommandeId INT AUTO_INCREMENT PRIMARY KEY,
    DateCommande DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FK_EtudiantId INT NOT NULL,
    MontantTotal DOUBLE NOT NULL,
    CONSTRAINT chk_MontantTotal CHECK (MontantTotal >= 0),
    CONSTRAINT fk_Commande_Etudiant FOREIGN KEY (FK_EtudiantId) REFERENCES Etudiant(EtudiantId) ON DELETE CASCADE
);

-- Table: CommandeLine
CREATE TABLE CommandeLine (
    PK_CommandeId INT NOT NULL,
    PK_ProduitId INT NOT NULL,
    PrixUnitaire DOUBLE NOT NULL,
    Quantite INT NOT NULL,
    PRIMARY KEY (PK_CommandeId, PK_ProduitId),
    CONSTRAINT chk_PrixUnitaire CHECK (PrixUnitaire >= 0),
    CONSTRAINT chk_Quantite CHECK (Quantite > 0),
    CONSTRAINT fk_CommandeLine_Commande FOREIGN KEY (PK_CommandeId) REFERENCES Commande(CommandeId) ON DELETE CASCADE,
    CONSTRAINT fk_CommandeLine_Produit FOREIGN KEY (PK_ProduitId) REFERENCES Produit(ProduitId) ON DELETE CASCADE
);

-- Table: Paiement
CREATE TABLE Paiement (
    PaiementId INT AUTO_INCREMENT PRIMARY KEY,
    DatePaiement DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FK_CommandeId INT NOT NULL,
    MethodePaiement VARCHAR(255) NOT NULL,
    Montant DOUBLE NOT NULL,
    Statut VARCHAR(255) NOT NULL,
    CONSTRAINT chk_Montant CHECK (Montant >= 0),
    CONSTRAINT chk_Statut CHECK (Statut IN ('En attente', 'Payé', 'Échoué','Annuler')),
    CONSTRAINT fk_Paiement_Commande FOREIGN KEY (FK_CommandeId) REFERENCES Commande(CommandeId) ON DELETE CASCADE
);

-- Table: Favorites
CREATE TABLE Favorites (
    FavoriId INT AUTO_INCREMENT PRIMARY KEY,
    DateAjout DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FK_AdminId INT,
    FK_AnnonceurId INT,
    FK_EtudiantId INT,
    
    ProduitId INT,
    LogementId INT,
    OffreEmploiId INT,
    Type VARCHAR(255) NOT NULL,
    
    -- Foreign Key Constraints
    CONSTRAINT fk_Favorites_Admin FOREIGN KEY (FK_AdminId) REFERENCES Admin(AdminId) ON DELETE CASCADE,
    CONSTRAINT fk_Favorites_Annonceur FOREIGN KEY (FK_AnnonceurId) REFERENCES Annonceur(AnnonceurId) ON DELETE CASCADE,
    CONSTRAINT fk_Favorites_Etudiant FOREIGN KEY (FK_EtudiantId) REFERENCES Etudiant(EtudiantId) ON DELETE CASCADE,
    CONSTRAINT fk_Favorites_Produit FOREIGN KEY (ProduitId) REFERENCES Produit(ProduitId) ON DELETE CASCADE,
    CONSTRAINT fk_Favorites_Logement FOREIGN KEY (LogementId) REFERENCES Logement(LogementId) ON DELETE CASCADE,
    CONSTRAINT fk_Favorites_OffreEmploi FOREIGN KEY (OffreEmploiId) REFERENCES OffreEmploi(OffreEmploiId) ON DELETE CASCADE,
    CONSTRAINT uniqueOffer UNIQUE (FK_AdminId,FK_AnnonceurId,FK_EtudiantId,ProduitId,LogementId,OffreEmploiId),
    
    -- Check Constraint for Type
    CONSTRAINT chk_Type CHECK (Type IN ('Produit', 'Logement', 'OffreEmploi')),
    
    -- Ensure only one of ProduitId, LogementId, or OffreEmploiId is set based on Type
    CONSTRAINT chk_Favorites_TypeMatch CHECK (
        (Type = 'Produit' AND ProduitId IS NOT NULL AND LogementId IS NULL AND OffreEmploiId IS NULL) OR
        (Type = 'Logement' AND LogementId IS NOT NULL AND ProduitId IS NULL AND OffreEmploiId IS NULL) OR
        (Type = 'OffreEmploi' AND OffreEmploiId IS NOT NULL AND ProduitId IS NULL AND LogementId IS NULL)
    )
);





-- Table: Panier
CREATE TABLE Panier (
    PanierId INT AUTO_INCREMENT PRIMARY KEY,
    FK_EtudiantId INT NOT NULL,
    CONSTRAINT fk_Panier_Etudiant FOREIGN KEY (FK_EtudiantId) REFERENCES Etudiant(EtudiantId) ON DELETE CASCADE
);

-- Table: PanierItem
CREATE TABLE PanierItem (
    PK_PanierId INT NOT NULL,
    PK_ProduitId INT NOT NULL,
    Quantite INT NOT NULL,
    PRIMARY KEY (PK_PanierId, PK_ProduitId),
    CONSTRAINT chk_Quantite_PanierItem CHECK (Quantite > 0),
    CONSTRAINT fk_PanierItem_Panier FOREIGN KEY (PK_PanierId) REFERENCES Panier(PanierId) ON DELETE CASCADE,
    CONSTRAINT fk_PanierItem_Produit FOREIGN KEY (PK_ProduitId) REFERENCES Produit(ProduitId) ON DELETE CASCADE
);

-- Table: Logement
CREATE TABLE Logement (
    LogementId INT AUTO_INCREMENT PRIMARY KEY,
    Description TEXT,
    Localisation VARCHAR(255) NOT NULL,
    Prix INT NOT NULL,
    Status VARCHAR(255) NOT NULL,
    Titre VARCHAR(255) NOT NULL,
	FK_AnnonceurId INT NOT NULL,
     XPosition DECIMAL(10, 6) NOT NULL DEFAULT 0.000000,
     YPosition DECIMAL(10, 6) NOT NULL DEFAULT 0.000000,
	CONSTRAINT fk_Logement_Annonceur FOREIGN KEY (FK_AnnonceurId) REFERENCES Annonceur(AnnonceurId) ON DELETE CASCADE,
    CONSTRAINT chk_Prix_Logement CHECK (Prix >= 0),
    CONSTRAINT chk_Status_Logement CHECK (Status IN ('Disponible', 'Réservé', 'Indisponible'))

);


-- Table: LogementReservation
CREATE TABLE LogementReservation (
    LogementReservationId INT AUTO_INCREMENT PRIMARY KEY,
    FK_EtudiantId INT NOT NULL,
    FK_LogementId INT NOT NULL,
    Status VARCHAR(255) NOT NULL,
    Nombre_Jours INT NOT NULL,
    Start_Date DATE NOT NULL,
    End_Date DATE NOT NULL,
    CONSTRAINT chk_Status CHECK (Status IN ('en_attente', 'annuler', 'reserve')),
    CONSTRAINT chk_Nombre_Jours CHECK (Nombre_Jours > 0),
    CONSTRAINT chk_Start_End_Date CHECK (Start_Date < End_Date),
    CONSTRAINT fk_LogementReservation_Etudiant FOREIGN KEY (FK_EtudiantId) REFERENCES Etudiant(EtudiantId) ON DELETE CASCADE,
    CONSTRAINT fk_LogementReservation_Logement FOREIGN KEY (FK_LogementId) REFERENCES Logement(LogementId) ON DELETE CASCADE
);

-- Table: LogementImages
CREATE TABLE LogementImages (
    FK_LogementId INT NOT NULL,
    ImageId INT NOT NULL,
    PRIMARY KEY (FK_LogementId, ImageId),
    CONSTRAINT fk_LogementImages_Logement FOREIGN KEY (FK_LogementId) REFERENCES Logement(LogementId) ON DELETE CASCADE
);

-- Table: OffreEmploi
CREATE TABLE OffreEmploi (
    OffreEmploiId INT AUTO_INCREMENT PRIMARY KEY,
    Description TEXT,
    Entreprise VARCHAR(255) NOT NULL,
    Salaire INT NOT NULL,
    Titre VARCHAR(255) NOT NULL,
    	FK_AnnonceurId INT NOT NULL,
	CONSTRAINT fk_OffreEmploi_Annonceur FOREIGN KEY (FK_AnnonceurId) REFERENCES Annonceur(AnnonceurId) ON DELETE CASCADE,
    CONSTRAINT chk_Salaire CHECK (Salaire >= 0)
);



-- Table: ValidationArchive
CREATE TABLE ValidationArchive (
    ArchiveId INT AUTO_INCREMENT PRIMARY KEY,
    DateValidation DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FK_AdminId INT NOT NULL,
    FK_CompteId INT NOT NULL,
    CONSTRAINT fk_ValidationArchive_Admin FOREIGN KEY (FK_AdminId) REFERENCES Admin(AdminId) ON DELETE CASCADE,
    CONSTRAINT fk_ValidationArchive_Etudiant FOREIGN KEY (FK_CompteId) REFERENCES Etudiant(EtudiantId) ON DELETE CASCADE
);

-- Table: Conversation
CREATE TABLE Conversation (
    ConversationId INT AUTO_INCREMENT PRIMARY KEY,
    FK_AdminId INT,
    FK_AnnonceurId INT,
    FK_EtudiantId INT,
    CONSTRAINT fk_Conversation_Admin FOREIGN KEY (FK_AdminId) REFERENCES Admin(AdminId) ON DELETE CASCADE,
    CONSTRAINT fk_Conversation_Annonceur FOREIGN KEY (FK_AnnonceurId) REFERENCES Annonceur(AnnonceurId) ON DELETE CASCADE,
    CONSTRAINT fk_Conversation_Etudiant FOREIGN KEY (FK_EtudiantId) REFERENCES Etudiant(EtudiantId) ON DELETE CASCADE
);

-- Table: Message
CREATE TABLE Message (
    MessageId INT AUTO_INCREMENT PRIMARY KEY,
    Contenu TEXT NOT NULL,
    FK_ConversationId INT NOT NULL,
    Time TIME NOT NULL,
    CONSTRAINT fk_Message_Conversation FOREIGN KEY (FK_ConversationId) REFERENCES Conversation(ConversationId) ON DELETE CASCADE
);



INSERT INTO Annonceur (
     CarteNationale, Email, Nom, Password, Prenom, Profile_Image, Telephone, Ville, Status
)
VALUES (
    'ayoub.annonceur@gmail.com_CarteNationale.pdf', -- CarteNationale
    'ayoub.annonceur@gmail.com', -- Email
    'Ayoub', -- Nom
    '$2b$12$I0Mb6B1fCS/GgucWLQjAeeFutMS94eC7BCc2TZdAx7WjUgji/aXp6', -- Password (hashed)
    'Annonceur', -- Prenom
    'ayoub.annonceur@gmail.com_Profile_Image.webp', -- Profile_Image (NULL if no image)
    '1122334455', -- Telephone
    'Casablanca', -- Ville
    'active' -- status
);

INSERT INTO Etudiant (
    AttestationScolarite, justificationDocument, CarteNationale, ConterInteret, Email, EtablissementScolaire, Nom, Password, Prenom, Profile_Image, Telephone, Ville, Status
)
VALUES (
    'ayoub.etudiant@gmail.com_AttestationScolarite.pdf', -- AttestationScolarite
    'ayoub.etudiant@gmail.com_justificationDocument.pdf', -- justificationDocument
    'CN654321', -- CarteNationale
    'productsOffers', -- ConterInteret
    'ayoub.etudiant@gmail.com', -- Email
    'University of Casablanca', -- EtablissementScolaire
    'Ayoub', -- Nom
    '$2b$12$I0Mb6B1fCS/GgucWLQjAeeFutMS94eC7BCc2TZdAx7WjUgji/aXp6', -- Password (hashed) majid12@
    'Etudiant', -- Prenom
     'ayoub.etudiant@gmail.com_Profile_Image.webp', -- Profile_Image (NULL if no image)
    '5566778899', -- Telephone
    'Casablanca', -- Ville
    'active' -- status
);

-- Insert Admin (type: admin)
INSERT INTO Admin (
    CarteNationale, Admin_Type, Email, Nom, Password, Prenom, Profile_Image, Telephone, Status
)
VALUES (
    'ayoub.admin@.gmail.com_carteNationale.pdf', -- CarteNationale
    'admin', -- Admin_Type
    'ayoub.admin@gmail.com', -- Email
    'Ayoub', -- Nom
    '$2b$12$I0Mb6B1fCS/GgucWLQjAeeFutMS94eC7BCc2TZdAx7WjUgji/aXp6', -- Password (hashed)
    'admin', -- Prenom
   'ayoub.admin@gmail.com_Profile_Image.webp', -- Profile_Image (NULL if no image)
    '0987654321', -- Telephone
    'active' -- status
);

-- Insert Admin (type: registerValidator)
INSERT INTO Admin (
    CarteNationale, Admin_Type, Email, Nom, Password, Prenom, Profile_Image, Telephone, Status
)
VALUES (
      
    'ayoub.registerValidator@.gmail.com_carteNationale.pdf', -- CarteNationale
    'registerValidator', -- Admin_Type
    'ayoub.registerValidator@gmail.com', -- Email
    'Ayoub', -- Nom
    '$2b$12$I0Mb6B1fCS/GgucWLQjAeeFutMS94eC7BCc2TZdAx7WjUgji/aXp6', -- Password (hashed)
    'RegisterValidator', -- Prenom
   'ayoub.registerValidator@gmail.com_Profile_Image.webp', -- Profile_Image (NULL if no image)
    '0987654321', -- Telephone
    'active' -- status
);



INSERT INTO LogementReservation (
    FK_EtudiantId, 
    FK_LogementId, 
    Status, 
    Nombre_Jours, 
    Start_Date, 
    End_Date
) VALUES (
    1, -- FK_EtudiantId (EtudiantId = 1)
    101, -- FK_LogementId (LogementId = 101)
    'en_attente', -- Status
    7, -- Nombre_Jours (7 days)
    '2023-03-15', -- Start_Date
    '2023-03-22' -- End_Date
);

INSERT INTO LogementReservation (
    FK_EtudiantId, 
    FK_LogementId, 
    Status, 
    Nombre_Jours, 
    Start_Date, 
    End_Date
) VALUES (
    2, -- FK_EtudiantId (EtudiantId = 2)
    102, -- FK_LogementId (LogementId = 102)
    'reserve', -- Status
    14, -- Nombre_Jours (14 days)
    '2023-04-01', -- Start_Date
    '2023-04-15' -- End_Date
);