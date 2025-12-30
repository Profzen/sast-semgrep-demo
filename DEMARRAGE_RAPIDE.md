#  Démarrage Rapide - SAST Semgrep

## Installation & Premier Scan

```bash
# 1. Installer Semgrep
pip install semgrep

# 2. Scanner et générer les rapports
python run_demo.py
```

**Résultat** : 2 fichiers générés → `semgrep-report.json` + `semgrep-report.md`

---

## Commandes Essentielles

### Scanner le code
```bash
# Scan complet avec vos règles
semgrep --config=semgrep-rules.yml app/

# Scan + génération rapports (JSON + MD)
python run_demo.py
```

### Générer seulement les rapports
```bash
# Génère semgrep-report.json + semgrep-report.md
python generate_report.py
```

### Push sur GitHub
```bash
git add .
git commit -m "test: pipeline SAST"
git push
```

**Le pipeline échouera** car le code contient 2 vulnérabilités ERROR !

---

## Fichiers Générés

Chaque scan crée **2 fichiers** :

| Fichier | Usage |
|---------|-------|
| `semgrep-report.json` | Format technique (automatisation) |
| `semgrep-report.md` | Rapport lisible (détails + solutions) |

---

## Vulnérabilités Détectées

Le code `app/app.py` contient :

- 🔴 **Command Injection** (ligne 20) - Bloque le pipeline
- 🟡 **Debug Mode** (ligne 30) - Avertissement

**Les erreurs 🔴 bloquent le pipeline GitHub Actions !**

---

##  Structure du Projet

```
sast-semgrep-demo/
├── app/
│   ├── app.py              # Code vulnérable (demo)
│   └── app_secure.py       # Exemples de corrections
├── .github/workflows/
│   └── sast-semgrep.yml    # Pipeline CI/CD
├── semgrep-rules.yml       # 10+ règles de sécurité
├── generate_report.py      # Génère les rapports
├── run_demo.py             # Tout-en-un
├── DEMARRAGE_RAPIDE.md     # Ce fichier
└── GUIDE_PRESENTATION.md   # Guide pour la présentation
```

---

## Pour la Présentation

Voir **[GUIDE_PRESENTATION.md](GUIDE_PRESENTATION.md)** pour le plan détaillé.

**Démo rapide ** :
1. Montrer `app/app.py` (code vulnérable)
2. Lancer `python run_demo.py`
3. Montrer `semgrep-report.md`
4. Push → pipeline échoue ❌
5. Montrer `app/app_secure.py` (corrections)

---

##  Commandes Rapides

```bash
# Problème d'encodage Windows
$env:PYTHONIOENCODING="utf-8"

# Vérifier version Semgrep
semgrep --version

# Scanner general
semgrep --config=auto 

# scanner pour python
semgrep --config=p/python --config=p/flask 

# scanner avec nos regles
semgrep --config=semgrep-rules.yml --no-git-ignore app/
```

---

** Ressources** : [Semgrep Docs](https://semgrep.dev/docs/) | [OWASP Top 10](https://owasp.org/Top10/)
