#!/usr/bin/env python3
"""
Génération de rapports Semgrep - Version simplifiée
Génère uniquement JSON + Markdown
"""

import json
import os
from datetime import datetime


def load_results(json_file):
    """Charge les résultats JSON"""
    if not os.path.exists(json_file):
        return {"results": []}
    
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def severity_emoji(severity):
    """Emoji par sévérité"""
    return {'ERROR': '🔴', 'WARNING': '🟡', 'INFO': '🔵'}.get(severity.upper(), '⚪')


def generate_markdown(results, output='semgrep-report.md'):
    """Génère le rapport Markdown"""
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    errors = [r for r in results.get('results', []) if r.get('extra', {}).get('severity') == 'ERROR']
    warnings = [r for r in results.get('results', []) if r.get('extra', {}).get('severity') == 'WARNING']
    
    report = f"""# 🔒 Rapport de Sécurité SAST

**Date** : {timestamp}  
**Statut** : {'❌ ÉCHEC' if errors else '✅ SUCCÈS'}

---

## 📊 Résumé

| Sévérité | Nombre |
|----------|--------|
| 🔴 Erreurs | {len(errors)} |
| 🟡 Avertissements | {len(warnings)} |

"""

    if errors:
        report += """> ⚠️ **ACTION REQUISE** : Vulnérabilités critiques détectées.

"""

    report += "---\n\n## 🔍 Détails\n\n"
    
    if results.get('results'):
        for idx, finding in enumerate(results['results'], 1):
            sev = finding.get('extra', {}).get('severity', 'INFO')
            emoji = severity_emoji(sev)
            rule = finding.get('check_id', 'unknown').split('.')[-1]
            msg = finding.get('extra', {}).get('message', '').split('\n')[0]
            path = finding.get('path', 'unknown')
            line = finding.get('start', {}).get('line', '?')
            code = finding.get('extra', {}).get('lines', '').strip()
            
            report += f"""### {emoji} #{idx} - {rule}

**Sévérité** : {sev}  
**Fichier** : `{path}:{line}`  
**Message** : {msg}

```python
{code}
```

---

"""
    else:
        report += "✅ Aucune vulnérabilité détectée.\n\n"

    if errors:
        report += """## 💡 Prochaines Étapes

1. ⛔ **Bloquer le déploiement**
2. 🔧 **Corriger** (voir `app/app_secure.py`)
3. ✅ **Re-scanner** : `python run_demo.py`
4. 🚀 **Re-push**

"""

    report += """---

**Généré par** : Semgrep  
**Règles** : `semgrep-rules.yml`
"""

    with open(output, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ Rapport : {output}")


def main():
    results = load_results('semgrep-report.json')
    generate_markdown(results)
    
    errors = len([r for r in results.get('results', []) if r.get('extra', {}).get('severity') == 'ERROR'])
    
    print("\n" + "="*60)
    print("📊 RÉSUMÉ")
    print("="*60)
    print(f"🔴 Erreurs critiques : {errors}")
    
    if errors > 0:
        print("\n⚠️  Pipeline devrait échouer.")
    else:
        print("\n✅ Aucune vulnérabilité critique.")
    
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
