# Maquette – page d'accueil ITS Travaux Spéciaux

Maquette de démonstration réalisée par Collet Marketing pour montrer qu'un site
peut être à la fois très rapide (Lighthouse 100/100/100/100 en mobile et en
bureau) et parfaitement lisible par les moteurs de réponse IA (ChatGPT, Gemini,
Perplexity, Claude).

Site de référence : https://www.its-entreprise.com/

## Contenu du dépôt

| Chemin | Rôle |
| --- | --- |
| `index.html` | Page d'accueil : HTML sémantique, CSS critique en ligne, JSON-LD (Organization, 3 × GeneralContractor, Service, FAQPage) |
| `assets/img/` | Images AVIF + WebP en plusieurs largeurs (`srcset`), logo provisoire |
| `assets/js/menu.js` | Seul script du site (menu mobile), chargé en `defer` |
| `assets/fonts/` | Police Inter (woff2, sous-ensemble latin) conservée en option, non utilisée par défaut |
| `llms.txt` | Résumé de l'entreprise pour les IA (expertises, zones, pages clés) |
| `robots.txt` | Autorise GPTBot, ClaudeBot, PerplexityBot, Google-Extended… et déclare le sitemap |
| `sitemap.xml` | Plan du site |
| `pathologies/`, `ouvrages/`, `expertises/`, `contact/`, `recrutement/`, `mentions-legales/` | Pages secondaires « squelette » générées, marquées [À COMPLÉTER] |
| `rapports/` | Rapports Lighthouse (mobile, bureau) de la maquette |
| `tools/` | Scripts de génération (images, pages, changement d'URL de base) |
| `.github/workflows/pages.yml` | Déploiement GitHub Pages par Actions (lancement manuel, si la source Pages est « GitHub Actions ») |

## Éléments à compléter avant mise en ligne

- **Photos de chantier** : l'environnement de génération n'avait pas accès à
  its-entreprise.com. Les visuels actuels sont des images de substitution
  marquées « Photo de chantier à remplacer ». Déposer les vraies photos dans
  `photos-src/` sous les noms attendus (`hero-chantier`, `parc-des-princes`,
  `parking-lorilleux`, `centre-commercial`, `equipe-chantier`, en .jpg/.png),
  ou renseigner leurs URL dans `tools/fetch-photos.sh`, puis lancer
  `python3 tools/build-images.py`.
- **Logo** : `assets/img/logo-its.webp`, `logo-512.png` et `favicon.png` sont
  issus d'un fichier de 300 px de large ; à remplacer par le logo officiel en
  SVG ou en haute définition.
- **Logos clients** (`assets/img/clients/`, bandeau « Ils nous ont fait
  confiance ») : découpés à partir de captures d'écran du site actuel, donc en
  basse définition. À remplacer par les fichiers sources, en gardant les mêmes
  noms. Le carrousel du site actuel compte 12 clients ; 11 ont pu être relevés
  (E.Leclerc, Primark, AXA, RIVP, BNP Paribas Real Estate, Les Sables d'Olonne,
  SIAH, SIAV, Icade, Unibail-Rodamco-Westfield, Airbus).
- **Blocs [À COMPLÉTER]** : contexte et date des réalisations, téléphone de
  l'agence de La Mézière, contenu des pages secondaires.
- **Police** : la maquette utilise la pile de polices système (LCP mobile
  simulé 0,9 s). Inter est fournie dans `assets/fonts/` ; l'activer ajoute
  environ 0,3 s au LCP simulé.

## Déploiement

Maquette en ligne : https://fabiencollet64.github.io/ITS/ (GitHub Pages,
source « Deploy from a branch », branche `claude/inspiring-newton-tw2j3r`,
dossier racine). Chaque push sur cette branche met le site à jour.

## Changer l'URL de base

Les URL absolues pointent vers l'hébergement de démonstration. Pour les faire
pointer vers le domaine définitif :

```bash
python3 tools/set-base-url.py https://www.its-entreprise.com/
```

Note : `llms.txt` et `robots.txt` doivent être servis à la racine du domaine
pour être pris en compte par Lighthouse et les robots. Sur un hébergement
GitHub Pages de type « projet » (sous-dossier), ils ne le sont pas ; un domaine
personnalisé règle le problème.

## Mesurer en local

```bash
# serveur statique avec compression, puis Lighthouse
npx lighthouse http://127.0.0.1:8080/ --form-factor=mobile --screenEmulation.mobile --view
npx lighthouse http://127.0.0.1:8080/ --preset=desktop --view
```
