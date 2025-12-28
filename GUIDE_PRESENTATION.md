# 🎤 Guide de Présentation - Boucle de Rétroaction SAST

## ⏱️ Plan (15 minutes)

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

## 📊 Slides Recommandés

1. Titre
2. Problématique (coût des failles)
3. Solution (boucle SAST)
4. Schéma du cycle
5. **Démo live** ← L'essentiel
6. Résultats & métriques
7. Conclusion & Questions

---

## 🎯 Scénarios de Démo

### Scénario Simple (5 min)
1. Montrer `app/app.py`
2. Lancer `python run_demo.py`
3. Montrer `semgrep-report.md`
4. Expliquer le blocage du pipeline

### Scénario Complet (10 min)
1. Code vulnérable
2. Scan local + rapports
3. Push → pipeline échoue
4. Montrer corrections dans `app/app_secure.py`
5. Expliquer la boucle de rétroaction

---

## 🛡️ Règles Configurées

| Type | Sévérité | Action Pipeline |
|------|----------|-----------------|
| SQL Injection | ERROR | ❌ Bloque |
| Command Injection | ERROR | ❌ Bloque |
| XSS | ERROR | ❌ Bloque |
| Debug Mode | WARNING | ⚠️ Alerte |
| Secrets hardcodés | WARNING | ⚠️ Alerte |

---

## 💡 Points Clés à Mentionner

1. **10+ règles** de sécurité personnalisées
2. **Blocage automatique** si erreur critique
3. **Rapports clairs** (JSON + Markdown)
4. **Messages pédagogiques** avec solutions
5. **Zéro configuration** après setup

---

## ❓ Questions Fréquentes

**"Ça ralentit pas le dev ?"**  
→ Non ! C'est plus rapide de corriger à la source qu'en production.

**"Taux de faux positifs ?"**  
→ Très faible avec Semgrep. Les règles sont affinables.

**"Coût ?"**  
→ Semgrep est open-source et gratuit.

---

## ✅ Checklist Avant Présentation

- [ ] Tester `python run_demo.py`
- [ ] Vérifier que le pipeline échoue sur GitHub
- [ ] Préparer le terminal avec les commandes
- [ ] Avoir `app/app.py` et `app/app_secure.py` ouverts
- [ ] Chronométrer la démo

---

**Conseil** : Privilégiez la démo live au PowerPoint ! Les gens retiennent mieux ce qu'ils voient en action.

## 📋 Structure de la Présentation (15-20 minutes)

### 1. Introduction (3 minutes)

**Contexte :**
- Les vulnérabilités de sécurité coûtent cher (données, réputation, conformité)
- Plus une vulnérabilité est détectée tard, plus elle coûte cher à corriger
- SAST = Static Application Security Testing = Analyse statique du code

**Problématique :**
- Comment détecter les failles de sécurité **avant** la mise en production ?
- Comment créer une **boucle de rétroaction** pour améliorer continuellement la sécurité ?

---

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

**Avantages :**
- ✅ **Automatisation** - Pas d'intervention manuelle
- ✅ **Prévention** - Détection avant la production
- ✅ **Éducation** - Messages pédagogiques
- ✅ **Traçabilité** - Historique complet
- ✅ **Culture de sécurité** - Sensibilisation continue

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

**Expliquer :**
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

**Expliquer :**
- Un attaquant peut injecter : `8.8.8.8; rm -rf /`
- → Exécution de commandes arbitraires !

```python
# ❌ VULNÉRABILITÉ 3 : XSS
@app.route("/hello")
def hello():
    name = request.args.get("name")
    return f"<h1>Hello {name}</h1>"  # DANGEREUX !
```

**Expliquer :**
- Un attaquant peut injecter : `<script>alert('XSS')</script>`
- → Exécution de JavaScript malveillant dans le navigateur !

---

#### Étape 2 : Exécuter l'analyse locale

**Dans le terminal :**

```bash
# Scanner avec les règles personnalisées
semgrep --config=semgrep-rules.yml .
```

**Résultat attendu :**
```
❯❯❱ command-injection-os-system
    Injection de commande OS détectée avec os.system().
    
    20┆ os.system("ping " + ip)

❯❯❱ sql-injection-string-formatting
    SQL Injection détectée via formatage de chaîne (%).
    
    11┆ query = "SELECT * FROM users WHERE username = '%s'" % user

✅ Findings: 2 (2 blocking)
```

**Montrer le fichier [semgrep-rules.yml](semgrep-rules.yml) :**
- 10+ règles de sécurité
- Détection de SQL Injection, Command Injection, XSS, etc.
- Messages pédagogiques avec solutions

---

#### Étape 3 : Générer le rapport

**Dans le terminal :**

```bash
# Générer les fichiers JSON
semgrep --config=semgrep-rules.yml --json --output=semgrep-report.json .

# Générer le rapport Markdown
python generate_report.py
```

**Montrer les fichiers générés :**

1. **[security-report.md](security-report.md)** :
   - Résumé exécutif avec compteurs
   - Détails des vulnérabilités avec CWE/OWASP
   - Code vulnérable
   - Recommandations de correction

2. **[SECURITY_HISTORY.md](SECURITY_HISTORY.md)** :
   - Historique incrémental de toutes les analyses
   - Traçabilité de l'évolution de la sécurité

---

#### Étape 4 : Pipeline GitHub Actions

**Montrer le workflow [.github/workflows/sast-semgrep.yml](.github/workflows/sast-semgrep.yml) :**

```yaml
- name: Run Semgrep avec règles personnalisées
  run: semgrep --config=semgrep-rules.yml --json --output=semgrep-report.json .
  
- name: Vérifier les vulnérabilités critiques
  run: |
    ERROR_COUNT=$(jq '[.results[] | select(.extra.severity == "ERROR")] | length' semgrep-report.json)
    if [ "$ERROR_COUNT" -gt 0 ]; then
      echo "❌ $ERROR_COUNT vulnérabilité(s) critique(s) détectée(s) !"
      exit 1  # ← BLOQUE LE PIPELINE
    fi
```

**Expliquer :**
- Le pipeline s'exécute automatiquement à chaque push
- Si des vulnérabilités ERROR sont détectées → le pipeline échoue
- Les rapports sont générés et uploadés comme artefacts
- Le code ne peut pas être déployé tant qu'il n'est pas sécurisé

---

#### Étape 5 : Démontrer le blocage

**Push sur GitHub :**

```bash
git add .
git commit -m "Demo: code with vulnerabilities"
git push
```

**Aller sur GitHub → Actions :**
- Le pipeline s'exécute
- ❌ Il échoue avec le message : "2 vulnérabilité(s) critique(s) détectée(s) !"
- Les développeurs reçoivent une notification
- Les rapports sont disponibles dans les artefacts

---

#### Étape 6 : Corriger et re-tester

**Corriger la SQL Injection dans [app/app.py](app/app.py) :**

```python
# ✅ VERSION SÉCURISÉE
@app.route("/login")
def login():
    user = request.args.get("user")
    query = "SELECT * FROM users WHERE username = ?"
    conn.execute(query, (user,))  # Requête paramétrée
```

**Re-scanner :**

```bash
semgrep --config=semgrep-rules.yml .
```

**Résultat :**
- La vulnérabilité SQL Injection n'apparaît plus
- Mais les autres persistent encore

**Expliquer :**
- Le développeur corrige itérativement
- La boucle de rétroaction se poursuit
- Chaque correction est tracée dans l'historique

---

### 4. Bénéfices et Impact (2 minutes)

**Pour l'équipe :**
- 🎓 **Formation continue** - Les développeurs apprennent en codant
- ⚡ **Feedback immédiat** - Détection en quelques secondes
- 🛡️ **Confiance** - Le code en production est sécurisé

**Pour l'entreprise :**
- 💰 **Économies** - Correction précoce = moins cher
- 📊 **Traçabilité** - Historique de sécurité pour les audits
- 🏆 **Réputation** - Moins de failles en production

**Métriques possibles :**
- Nombre de vulnérabilités détectées par sprint
- Temps de correction moyen
- Évolution du nombre de vulnérabilités dans le temps
- Taux de blocage du pipeline

---

### 5. Conclusion (2 minutes)

**Points clés :**
1. Le SAST est un **outil essentiel** dans le DevSecOps moderne
2. La **boucle de rétroaction** transforme la sécurité en processus continu
3. L'**automatisation** supprime la charge manuelle
4. L'**éducation** des développeurs est la clé du succès

**Recommandations :**
- Commencer petit (quelques règles critiques)
- Étendre progressivement
- Impliquer l'équipe dans la création des règles
- Mesurer et communiquer les progrès

**Questions à anticiper :**
- **"Ça ne ralentit pas le développement ?"** → Non, au contraire ! C'est plus rapide de corriger à la source qu'en production.
- **"Combien de faux positifs ?"** → Semgrep a un taux de faux positifs très faible. Les règles peuvent être affinées.
- **"Quel coût ?"** → Semgrep est open-source et gratuit. Le ROI est très élevé.

---

## 📊 Slides Recommandés

1. **Slide 1** - Titre + Votre nom
2. **Slide 2** - Contexte : Pourquoi la sécurité est critique ?
3. **Slide 3** - Problématique : Détecter tôt vs détecter tard
4. **Slide 4** - Solution : Boucle de rétroaction SAST
5. **Slide 5** - Schéma du cycle complet
6. **Slide 6** - Démonstration (screen sharing)
7. **Slide 7** - Résultats et métriques
8. **Slide 8** - Bénéfices
9. **Slide 9** - Conclusion + Questions

---

## 🎯 Checklist Pré-Présentation

- [ ] Vérifier que Semgrep est installé
- [ ] Tester `semgrep --config=semgrep-rules.yml .` en local
- [ ] Générer un rapport pour avoir des exemples visuels
- [ ] Préparer le repository GitHub accessible
- [ ] Avoir le terminal prêt avec les commandes
- [ ] Tester le workflow GitHub Actions
- [ ] Préparer des exemples de corrections
- [ ] Chronométrer la démonstration (max 10 min)

---

## 💡 Conseils de Présentation

1. **Commencer par l'impact** - Montrer des cas réels de failles célèbres
2. **Démontrer visuellement** - Les gens retiennent mieux ce qu'ils voient
3. **Garder un rythme dynamique** - Alterner théorie et pratique
4. **Anticiper les questions** - Préparer des réponses concises
5. **Finir sur une note positive** - Insister sur les bénéfices

**Bonne présentation ! 🚀**
