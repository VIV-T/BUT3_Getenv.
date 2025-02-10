import psycopg2

# Initialisation de la connexion
conn = psycopg2.connect(database = "SAE - Analyse et conception outil decisionnel",
                        user = "postgres",
                        host= 'localhost',
                        password = "postgres",
                        port = 5432)


# Creation d'un curseur pour executer des requêtes
cur = conn.cursor()

# Execution d'une requête - SELECT
cur.execute("SELECT * FROM main;")

# Les changements deviennent persistants - très important !
conn.commit()

# recuperation du resultat de la requête
rows = cur.fetchall()

# affichage
print(rows)

# Fermeture du curseur et de la connexion
cur.close()
conn.close()