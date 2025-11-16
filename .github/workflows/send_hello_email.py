import os
import smtplib
from email.message import EmailMessage

# Récupération des variables d'environnement
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")

if not (SMTP_USER and SMTP_PASSWORD and EMAIL_TO):
    raise ValueError("Les variables SMTP_USER, SMTP_PASSWORD et EMAIL_TO doivent être définies.")

# Création de l'e-mail
msg = EmailMessage()
msg["Subject"] = "Hello World depuis GitHub Actions"
msg["From"] = SMTP_USER
msg["To"] = EMAIL_TO
msg.set_content("Ceci est un message de test 'Hello World' envoyé depuis GitHub Actions.")

# Envoi via SMTP (exemple avec Gmail)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
    print(f"E-mail envoyé avec succès à {EMAIL_TO} !")
except Exception as e:
    print(f"Erreur lors de l'envoi de l'e-mail : {e}")
    raise
