# TAGINE VOLANT — Maroc & Monde

Site statique gratuit de revue de presse, alimenté automatiquement par des flux RSS publics.

## Mise en ligne (GitHub Pages)
1. Créer un dépôt GitHub **public**, par exemple `taginevolant`.
2. Importer **tout le contenu** de ce dossier, y compris `.github/workflows/update.yml`.
3. Dans **Settings → Pages**, choisir **Deploy from a branch**, branche `main`, dossier `/ (root)`.
4. Ouvrir **Actions → Actualiser la revue de presse → Run workflow** pour la première édition.
5. L'adresse sera `https://nabiltaoufik-cpu.github.io/taginevolant/`.
6. Dans **Settings → Actions → General**, autoriser les workflows à écrire dans le dépôt si nécessaire (`Read and write permissions`).

## Automatisation
Trois exécutions quotidiennes programmées (06h15, 11h15 et 16h15 UTC). GitHub Actions peut avoir du retard et les exécutions programmées peuvent être désactivées sur des dépôts inactifs. Les flux peuvent changer, tomber en panne ou limiter les accès. Aucun résultat n'est inventé : si la collecte est vide, la dernière édition reste en place.

## Important
- Aucun service d'IA payant ni serveur applicatif.
- Les titres et extraits sont fournis par les éditeurs via RSS ; ne pas les présenter comme des articles rédigés ou vérifiés indépendamment.
- Les sources RSS doivent être contrôlées avant exploitation publique et adaptées à leurs conditions de réutilisation. La liste de flux dans `scripts/update.py` est une configuration de départ ; leur disponibilité n'a pas été vérifiée en direct.
- Le site n'envoie **pas** la newsletter : ajoutez son URL dans votre système de NL existant.
- Un dépôt public signifie que les fichiers de données et le code sont publics.

## Domaine personnalisé (facultatif)
Après achat et contrôle du domaine `taginevolant.news`, configurer les DNS chez le registraire puis renseigner `taginevolant.news` dans Settings → Pages → Custom domain. Ne pas activer le domaine personnalisé avant de le posséder.
