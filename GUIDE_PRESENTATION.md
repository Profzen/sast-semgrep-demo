#  Guide de Présentation - Boucle de Rétroaction SAST

## ⏱ Plan (15 minutes)

### 1. Introduction (3 min)
**Problème** : Les vulnérabilités détectées tard coûtent cher  
**Solution** : SAST automatisé avec boucle de rétroaction

### 2. Concept (3 min)
```
Code → Push → Scan SAST → Vulnérabilités ?
                              ↓ Oui
                         ❌ Blocage
                              ↓
                      Correction → Retour au début
```

**Avantages** :
- Automatisation complète
- Détection avant production
- Feedback immédiat
- Traçabilité

### 3. Démonstration (7 min)

#### Étape 1 : Code vulnérable (1 min)
```python
# ❌ Command Injection - app/app.py ligne 20
ip = request.args.get("ip")
os.system("ping " + ip)  # DANGEREUX !
```

**Attaque** : `8.8.8.8; rm -rf /`

#### Étape 2 : Scan local (2 min)
```bash
# Scanner
semgrep --config=semgrep-rules.yml app/

# Générer rapports
python run_demo.py
```

**Résultat** : 2 erreurs critiques détectées

#### Étape 3 : Rapports (2 min)
Montrer `semgrep-report.md` :
- Résumé des vulnérabilités
- Code problématique
- Solutions recommandées

#### Étape 4 : Pipeline GitHub (1 min)
```bash
git push
```

**Résultat** : ❌ Pipeline échoue → Code bloqué

#### Étape 5 : Correction (1 min)
```python
# ✅ Version sécurisée - app/app_secure.py
import subprocess
subprocess.run(["ping", ip], check=True)
```

### 4. Conclusion (2 min)

**Impact** :
- Sécurité intégrée au développement
- Éducation continue des devs
- Économies (correction précoce)
- Conformité (traçabilité)

---

---

## Scénarios de Démo

### Scénario Simple (5 min)
1. Montrer `app/app.py`
2. Lancer `python run_demo.py`
3. Montrer `semgrep-report.md`
4. Expliquer le blocage du pipeline

### Scénario Complet 
1. Code vulnérable
2. Scan local + rapports
3. Push → pipeline échoue
4. Montrer corrections dans `app/app_secure.py`
5. Expliquer la boucle de rétroaction

---

##  Règles Configurées

| Type              | Sévérité | Action Pipeline |
|------             |----------|-----------------|
| SQL Injection     | ERROR    | ❌ Bloque       |
| Command Injection | ERROR    | ❌ Bloque       |
| XSS               | ERROR    | ❌ Bloque       |
| Debug Mode        | WARNING  | ⚠️ Alerte       |
| Secrets hardcodés | WARNING  | ⚠️ Alerte       |


### 2. Concept de Boucle de Rétroaction (5 minutes)

**Définition :**
Une boucle de rétroaction SAST permet de :
1. **Détecter** automatiquement les vulnérabilités dans le code
2. **Bloquer** le code non sécurisé avant le déploiement
3. **Notifier** les développeurs avec des rapports clairs
4. **Éduquer** l'équipe sur les bonnes pratiques
5. **Tracer** l'évolution de la sécurité du projet

**Le Cycle :**
```
Développeur écrit du code
         ↓
Commit + Push sur Git
         ↓
Pipeline CI/CD déclenché
         ↓
Analyse SAST (Semgrep)
         ↓
Vulnérabilités détectées ? ──Non──→ ✅ Déploiement
         ↓
        Oui
         ↓
❌ Pipeline échoue (blocage)
         ↓
Rapport généré + Notification
         ↓
Développeur corrige le code
         ↓
Retour au début du cycle
```

---

### 3. Démonstration Pratique (10 minutes)

#### Étape 1 : Présenter le code vulnérable

**Montrer le fichier [app/app.py](app/app.py) :**

```python
# ❌ VULNÉRABILITÉ 1 : SQL Injection
@app.route("/login")
def login():
    user = request.args.get("user")
    query = "SELECT * FROM users WHERE username = '%s'" % user
    conn.execute(query)  # DANGEREUX !
```

**Expliquation :**
- Un attaquant peut injecter : `admin' OR '1'='1`
- La requête devient : `SELECT * FROM users WHERE username = 'admin' OR '1'='1'`
- → Accès non autorisé !

```python
# ❌ VULNÉRABILITÉ 2 : Command Injection
@app.route("/ping")
def ping():
    ip = request.args.get("ip")
    os.system("ping " + ip)  # DANGEREUX !
```

**Expliquation :**
- Un attaquant peut injecter : `8.8.8.8; rm -rf /`
- → Exécution de commandes arbitraires !

```python
# ❌ VULNÉRABILITÉ 3 : XSS
@app.route("/hello")
def hello():
    name = request.args.get("name")
    return f"<h1>Hello {name}</h1>"  # DANGEREUX !
```

**Expliquation :**
- Un attaquant peut injecter : `<script>alert('XSS')</script>`
- → Exécution de JavaScript malveillant dans le navigateur !

---


## Slides Recommandés

1. **Slide 4** - Solution : Boucle de rétroaction SAST
2. **Slide 5** - Schéma du cycle complet
3. **Slide 6** - Démonstration (screen sharing)
4. **Slide 7** - Résultats et métriques



