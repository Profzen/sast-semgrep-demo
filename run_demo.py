#!/usr/bin/env python3
"""
Script de test rapide - Scan + Génération rapports
"""

import subprocess
import sys
import os

def run_command(cmd, description):
    """Exécute une commande"""
    print(f"\n{'='*60}")
    print(f"🔍 {description}")
    print(f"{'='*60}\n")
    
    result = subprocess.run(cmd, shell=True, capture_output=False, text=True)
    return result.returncode

def main():
    print("""
╔═══════════════════════════════════════════════════════════╗
║        🔒 SAST Demo - Scan + Rapports                    ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Vérifier Semgrep
    print("✓ Vérification de Semgrep...")
    result = subprocess.run("semgrep --version", shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print("❌ Semgrep non installé ! Installez-le : pip install semgrep")
        sys.exit(1)
    
    print(f"✅ Semgrep version : {result.stdout.strip()}\n")
    
    # Scanner (affichage)
    run_command(
        "semgrep --config=semgrep-rules.yml app/",
        "Scan avec règles personnalisées"
    )
    
    # Générer JSON
    run_command(
        "semgrep --config=semgrep-rules.yml --json --output=semgrep-report.json app/",
        "Génération JSON"
    )
    
    # Générer Markdown
    run_command(
        "python generate_report.py",
        "Génération rapport Markdown"
    )
    
    # Résumé
    print(f"\n{'='*60}")
    print("📊 FICHIERS GÉNÉRÉS")
    print(f"{'='*60}")
    
    if os.path.exists("semgrep-report.json"):
        print("  ✅ semgrep-report.json")
    
    if os.path.exists("semgrep-report.md"):
        print("  ✅ semgrep-report.md")
    
    print(f"\n{'='*60}")
    print("🎉 TERMINÉ !")
    print(f"{'='*60}")
    print("\nConsultez semgrep-report.md pour les détails.")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
