"""
Exemples de Code Sécurisé - Corrections des Vulnérabilités
Ce fichier montre comment corriger les vulnérabilités détectées dans app.py
"""

from flask import Flask, request, render_template_string, escape
import sqlite3
import subprocess
import shlex

app = Flask(__name__)

# ============================================================================
# ✅ CORRECTION 1 : SQL Injection
# ============================================================================

# ❌ VERSION VULNÉRABLE (NE PAS UTILISER)
def login_vulnerable():
    """
    VULNÉRABILITÉ : SQL Injection via formatage de chaîne
    Un attaquant peut injecter : admin' OR '1'='1
    """
    user = request.args.get("user")
    query = "SELECT * FROM users WHERE username = '%s'" % user  # DANGEREUX !
    conn = sqlite3.connect("db.sqlite")
    conn.execute(query)
    return "Login OK"


# ✅ VERSION SÉCURISÉE (RECOMMANDÉ)
@app.route("/login")
def login_secure():
    """
    SÉCURISÉ : Utilisation de requêtes paramétrées
    Les paramètres sont échappés automatiquement par SQLite
    """
    user = request.args.get("user")
    
    # Méthode 1 : Placeholder avec ? (recommandé pour SQLite)
    query = "SELECT * FROM users WHERE username = ?"
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.execute(query, (user,))  # Tuple de paramètres
    
    # Méthode 2 : Placeholder nommé (plus lisible)
    # query = "SELECT * FROM users WHERE username = :username"
    # cursor = conn.execute(query, {"username": user})
    
    result = cursor.fetchone()
    
    if result:
        return f"Login OK for user ID {result[0]}"
    else:
        return "User not found"


# ✅ ALTERNATIVE : Utilisation d'un ORM (SQLAlchemy)
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)

@app.route("/login")
def login_orm():
    user = request.args.get("user")
    # SQLAlchemy échappe automatiquement les paramètres
    result = User.query.filter_by(username=user).first()
    if result:
        return f"Login OK for {result.username}"
    return "User not found"
"""


# ============================================================================
# ✅ CORRECTION 2 : Command Injection
# ============================================================================

# ❌ VERSION VULNÉRABLE (NE PAS UTILISER)
def ping_vulnerable():
    """
    VULNÉRABILITÉ : Command Injection
    Un attaquant peut injecter : 8.8.8.8; rm -rf /
    """
    ip = request.args.get("ip")
    import os
    os.system("ping " + ip)  # DANGEREUX !
    return "Ping sent"


# ✅ VERSION SÉCURISÉE - Méthode 1 : subprocess avec liste
@app.route("/ping")
def ping_secure_v1():
    """
    SÉCURISÉ : Utilisation de subprocess avec une liste d'arguments
    Les arguments sont passés séparément, pas via le shell
    """
    ip = request.args.get("ip")
    
    # Validation de l'IP (optionnel mais recommandé)
    import ipaddress
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        return "Invalid IP address", 400
    
    try:
        # subprocess.run avec une liste = pas d'interprétation shell
        result = subprocess.run(
            ["ping", "-c", "4", ip],  # Liste d'arguments
            capture_output=True,
            text=True,
            timeout=10,
            check=True
        )
        return f"<pre>{result.stdout}</pre>"
    except subprocess.CalledProcessError as e:
        return f"Ping failed: {e}", 500
    except subprocess.TimeoutExpired:
        return "Ping timeout", 500


# ✅ VERSION SÉCURISÉE - Méthode 2 : shlex.quote si shell=True nécessaire
def ping_secure_v2():
    """
    SÉCURISÉ : Si vous devez absolument utiliser shell=True,
    utilisez shlex.quote() pour échapper les arguments
    """
    ip = request.args.get("ip")
    
    # Échapper l'argument
    safe_ip = shlex.quote(ip)
    
    import os
    os.system(f"ping -c 4 {safe_ip}")
    return "Ping sent"


# ============================================================================
# ✅ CORRECTION 3 : XSS (Cross-Site Scripting)
# ============================================================================

# ❌ VERSION VULNÉRABLE (NE PAS UTILISER)
def hello_vulnerable():
    """
    VULNÉRABILITÉ : XSS via injection HTML
    Un attaquant peut injecter : <script>alert('XSS')</script>
    """
    name = request.args.get("name")
    return f"<h1>Hello {name}</h1>"  # DANGEREUX !


# ✅ VERSION SÉCURISÉE - Méthode 1 : markupsafe.escape()
@app.route("/hello")
def hello_secure_v1():
    """
    SÉCURISÉ : Échappement manuel avec markupsafe.escape()
    """
    from markupsafe import escape
    name = request.args.get("name", "Guest")
    
    # escape() convertit les caractères spéciaux HTML
    # < devient &lt;, > devient &gt;, etc.
    safe_name = escape(name)
    
    return f"<h1>Hello {safe_name}</h1>"


# ✅ VERSION SÉCURISÉE - Méthode 2 : Jinja2 templates (RECOMMANDÉ)
@app.route("/hello2")
def hello_secure_v2():
    """
    SÉCURISÉ : Utilisation de render_template() avec Jinja2
    Jinja2 échappe automatiquement toutes les variables par défaut
    """
    name = request.args.get("name", "Guest")
    
    # Template Jinja2 (peut être dans un fichier séparé)
    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hello</title>
    </head>
    <body>
        <h1>Hello {{ name }}</h1>
        <!-- {{ name }} est automatiquement échappé -->
    </body>
    </html>
    """
    
    return render_template_string(template, name=name)


# ✅ VERSION SÉCURISÉE - Méthode 3 : Si vous voulez du HTML non échappé
def hello_secure_v3():
    """
    Si vous devez vraiment permettre du HTML (rare),
    utilisez Markup() et sanitisez avec bleach
    """
    from markupsafe import Markup
    import bleach
    
    name = request.args.get("name", "Guest")
    
    # Sanitizer avec bleach (permet seulement certaines balises)
    safe_html = bleach.clean(
        name,
        tags=['b', 'i', 'em', 'strong'],  # Balises autorisées
        strip=True
    )
    
    return f"<h1>Hello {Markup(safe_html)}</h1>"


# ============================================================================
# ✅ CORRECTION 4 : Mode Debug en Production
# ============================================================================

# ❌ VERSION VULNÉRABLE (NE PAS UTILISER)
def run_vulnerable():
    """
    VULNÉRABILITÉ : Mode debug activé
    Expose des informations sensibles et permet l'exécution de code
    """
    app.run(debug=True)  # DANGEREUX !


# ✅ VERSION SÉCURISÉE
if __name__ == "__main__":
    """
    SÉCURISÉ : Utiliser une variable d'environnement
    """
    import os
    
    # Récupérer depuis l'environnement (défaut = False)
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    
    # En production, FLASK_DEBUG ne doit PAS être défini ou = False
    app.run(debug=debug_mode)


# ============================================================================
# ✅ BONUS : Autres bonnes pratiques de sécurité
# ============================================================================

# 1. Secrets en variables d'environnement
import os

# ❌ MAUVAIS
SECRET_KEY = "my-secret-key-123"
API_KEY = "sk-1234567890abcdef"

# ✅ BON
SECRET_KEY = os.getenv("SECRET_KEY")
API_KEY = os.getenv("API_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be set in environment variables")


# 2. Validation des entrées
from marshmallow import Schema, fields, ValidationError

class UserSchema(Schema):
    username = fields.Str(required=True, validate=lambda x: len(x) <= 50)
    email = fields.Email(required=True)

@app.route("/register", methods=["POST"])
def register():
    schema = UserSchema()
    try:
        data = schema.load(request.json)
        # Données validées et sûres
        return {"message": "User registered"}, 201
    except ValidationError as err:
        return {"errors": err.messages}, 400


# 3. Rate Limiting
"""
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/api/sensitive")
@limiter.limit("10 per minute")
def sensitive_endpoint():
    return {"data": "sensitive"}
"""


# 4. HTTPS forcé en production
"""
from flask_talisman import Talisman

# Force HTTPS
Talisman(app, force_https=True)
"""


# 5. Headers de sécurité
@app.after_request
def set_security_headers(response):
    """Ajoute des headers de sécurité à toutes les réponses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response


# ============================================================================
# RÉSUMÉ DES RÈGLES D'OR
# ============================================================================
"""
1. SQL : Toujours utiliser des requêtes paramétrées ou un ORM
2. Commands : Toujours utiliser subprocess avec une liste, jamais shell=True
3. XSS : Toujours échapper les sorties HTML (Jinja2 le fait automatiquement)
4. Secrets : Jamais dans le code, toujours en variables d'environnement
5. Debug : Jamais en production
6. Validation : Toujours valider et sanitizer les entrées utilisateur
7. HTTPS : Toujours forcer HTTPS en production
8. Dependencies : Toujours maintenir les dépendances à jour
9. Logging : Logger les accès mais jamais les secrets
10. Tests : Toujours tester la sécurité avec des outils SAST/DAST
"""
