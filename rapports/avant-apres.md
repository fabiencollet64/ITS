# Avant / après – its-entreprise.com contre la maquette

« Avant » : scores PageSpeed Insights de https://www.its-entreprise.com/ fournis
dans le brief (l'API PageSpeed n'était pas joignable depuis l'environnement de
génération : quota dépassé). « Après » : Lighthouse 13.5 en local sur la maquette
(serveur statique avec compression gzip), mêmes réglages que PageSpeed
(émulation mobile Moto G Power, réseau 4G lent simulé ; preset bureau).
À confirmer sur PageSpeed Insights une fois la maquette en ligne.

## Mobile

| Indicateur | its-entreprise.com (avant) | Maquette (après) |
| --- | --- | --- |
| Performance | 52 | 100 |
| Accessibilité | 84 | 100 |
| Bonnes pratiques | non fourni | 100 |
| SEO | non fourni | 100 |
| Navigation agentique | 0/2 | 2/2 (3/3 avec llms.txt à la racine du domaine) |
| LCP | 6,2 s | 0,9 s |
| CLS | 0,246 | 0 |
| TBT | non fourni | 0 ms |
| FCP | non fourni | 0,7 s |
| Speed Index | non fourni | 0,7 s |

## Bureau

| Indicateur | its-entreprise.com (avant) | Maquette (après) |
| --- | --- | --- |
| Performance | 94 | 100 |
| Accessibilité | non fourni | 100 |
| Bonnes pratiques | non fourni | 100 |
| SEO | non fourni | 100 |
| Navigation agentique | non fourni | 2/2 |
| LCP | non fourni | 0,3 s |
| CLS | non fourni | 0 |
| TBT | non fourni | 0 ms |

## Poids de la page d'accueil de la maquette (mobile)

| Ressource | Poids transféré |
| --- | --- |
| HTML (CSS critique et JSON-LD inclus, gzip) | ≈ 11 Ko |
| Image du hero (AVIF 800 px) | ≈ 9 Ko |
| Script du menu (gzip) | < 1 Ko |
| Images des réalisations (AVIF 400 px, chargées à la demande) | ≈ 4 Ko chacune |

Rapports complets : `lighthouse-mobile.html`, `lighthouse-bureau.html`, `resume.json`.
