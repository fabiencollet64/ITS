#!/usr/bin/env python3
"""Génère les pages secondaires de la maquette, le sitemap.xml et llms.txt.

Usage : python3 tools/make-pages.py

Les pages secondaires sont des pages « squelette » : titre, H1, résumé
factuel issu de la page d'accueil et un bloc [À COMPLÉTER]. Elles évitent les
erreurs 404 lors de la démonstration et donnent aux IA une URL stable par
expertise, pathologie et type d'ouvrage.
"""
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://fabiencollet64.github.io/ITS/"
TODAY = date.today().isoformat()

PAGES = {
    "pathologies": ("Pathologies du béton", [
        ("fissures", "Fissures", "Fissures de dalles, poutres, voiles ou poteaux : recherche de la cause, injection et renforcement si nécessaire."),
        ("beton-degrade", "Béton dégradé", "Éclats, épaufrures, béton carbonaté ou désagrégé : purge, hydrodémolition et reconstitution en béton projeté."),
        ("infiltrations-et-fuites", "Infiltrations et fuites", "Venues d'eau dans les sous-sols, parkings, bassins et réservoirs : injection, cuvelage et étanchéité liquide."),
        ("corrosion", "Corrosion des armatures", "Aciers corrodés et béton éclaté : renforcement des aciers, protection cathodique et réparation durable."),
        ("ouvrage-sinistre", "Ouvrage sinistré", "Choc, affaissement ou désordre structurel : étaiement d'urgence, diagnostic puis réparation et renforcement."),
        ("sinistre-incendie", "Sinistre incendie", "Béton et aciers fragilisés par le feu : mise en sécurité, diagnostic structurel et reconstitution de la structure."),
        ("agressions-chimiques", "Agressions chimiques", "Bétons attaqués en milieu industriel ou agricole : réparation, protection et étanchéité des ouvrages."),
        ("changement-de-destination", "Changement de destination", "Nouvelles charges, nouveaux usages : renforcement de la structure par plat carbone, précontrainte ou profilés métalliques."),
    ]),
    "ouvrages": ("Types d'ouvrages", [
        ("ouvrages-d-art", "Ouvrages d'art : ponts, passerelles, tribunes, structures précontraintes", "ITS Travaux Spéciaux répare et renforce les ouvrages d'art en béton armé et précontraint : réparation des bétons, précontrainte additionnelle ou extérieure, plat carbone, béton projeté, hydrodémolition, protection cathodique, étaiement d'urgence et vérinage. Référence : renforcement par précontrainte additionnelle des gradins du Parc des Princes."),
        ("parkings-souterrains", "Parkings souterrains", "Dalles fissurées, infiltrations, poutres à renforcer : travaux phasés, parking maintenu en exploitation. Référence : renforcement de poutres par précontrainte extérieure au parking Charles Lorilleux à Puteaux."),
        ("immeubles-de-logements", "Immeubles de logements", "Réparation des balcons, dalles et structures, intervention en immeuble habité."),
        ("sites-industriels", "Sites industriels", "Bétons soumis aux agressions chimiques et aux fortes charges, interventions sans arrêt de production."),
        ("centres-commerciaux", "Centres commerciaux", "Renforcement de poutres et de dalles pendant l'exploitation du centre. Référence : renforcement d'une poutre de 50 mètres dans un centre commercial à Paris."),
        ("equipements-sportifs", "Équipements sportifs", "Tribunes, gradins et bassins : renforcement par précontrainte additionnelle et étanchéité."),
    ]),
    "expertises": ("Expertises", [
        ("renforcement-de-structures", "Renforcement de structures", "Plat carbone, précontrainte additionnelle et extérieure, béton projeté, profilés métalliques, renforcement des aciers."),
        ("cuvelage", "Cuvelage", "Traitement des parties enterrées contre les venues d'eau."),
        ("injection", "Injection", "Injection de résines ou de coulis dans les fissures, vides et fuites."),
        ("diagnostic-structurel", "Diagnostic structurel", "Relevés, sondages et analyse de l'état de l'ouvrage par notre bureau d'études intégré."),
        ("verinage", "Vérinage", "Levage et remise à niveau de structures par vérins."),
        ("protection-cathodique", "Protection cathodique", "Arrêt de la corrosion des armatures dans le béton armé."),
        ("hydrodemolition", "Hydrodémolition", "Purge du béton dégradé à l'eau très haute pression, sans vibration."),
        ("etaiement-d-urgence", "Étaiement d'urgence", "Mise en sécurité rapide des ouvrages fragilisés ou sinistrés."),
        ("etancheite-liquide", "Étanchéité liquide", "Systèmes d'étanchéité liquide pour dalles, terrasses et toitures."),
        ("etancheite-bassins-reservoirs", "Étanchéité des bassins et réservoirs", "Réparation et étanchéité des ouvrages hydrauliques en béton."),
    ]),
    "": ("", [
        ("recrutement", "Recrutement", "ITS Travaux Spéciaux recrute des équipes de travaux spéciaux pour ses agences de La Roche-sur-Yon, Pantin et La Mézière."),
        ("contact", "Contact et demande de diagnostic", "Décrivez-nous votre ouvrage et ses désordres : notre bureau d'études vous propose un diagnostic et une solution adaptée. Écrivez à contact@its-entreprise.com ou appelez le siège au 02 51 46 99 23 (La Roche-sur-Yon) ou l'agence Île-de-France au 01 64 26 57 00 (Pantin)."),
        ("mentions-legales", "Mentions légales", "Éditeur : ITS Travaux Spéciaux (IVEBAT), 14 impasse Philippe-Gozola, 85000 La Roche-sur-Yon."),
    ]),
}

TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} – ITS Travaux Spéciaux</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#141a21">
<link rel="icon" href="{rel}assets/img/favicon.png" type="image/png" sizes="64x64">
<link rel="preload" href="{rel}assets/fonts/barlow-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{rel}assets/fonts/barlow-sc-700.woff2" as="font" type="font/woff2" crossorigin>
<style>
@font-face{{font-family:Barlow;font-style:normal;font-weight:400;font-display:swap;src:url({rel}assets/fonts/barlow-400.woff2) format("woff2")}}
@font-face{{font-family:Barlow;font-style:normal;font-weight:600;font-display:swap;src:url({rel}assets/fonts/barlow-600.woff2) format("woff2")}}
@font-face{{font-family:"Barlow Semi Condensed";font-style:normal;font-weight:700;font-display:swap;src:url({rel}assets/fonts/barlow-sc-700.woff2) format("woff2")}}
@font-face{{font-family:"Barlow Fallback";src:local("Arial"),local("Liberation Sans"),local("Helvetica");size-adjust:96.9%;ascent-override:103.2%;descent-override:20.6%;line-gap-override:0%}}
@font-face{{font-family:"Barlow SC Fallback";src:local("Arial Bold"),local("Arial"),local("Liberation Sans Bold");size-adjust:84.6%;ascent-override:118.2%;descent-override:23.6%;line-gap-override:0%}}
:root{{--red:#c8102e;--red-dark:#a30d25;--ink:#14181d;--dark:#1b2129;--grey:#f3f4f6;--line:#dfe3e8;--muted:#4b5563}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:Barlow,"Barlow Fallback",Arial,sans-serif;font-size:1.1rem;line-height:1.6;color:var(--ink);background:#fff}}
.wrap{{width:min(100% - 2rem,760px);margin-inline:auto}}
.skip{{position:absolute;left:-999px;top:0;background:var(--ink);color:#fff;padding:.9rem 1.2rem}}
.skip:focus{{left:0}}
header{{border-bottom:1px solid var(--line)}}
header .wrap{{display:flex;align-items:center;gap:1rem;min-height:72px;flex-wrap:wrap}}
.brand{{display:flex;align-items:center;gap:.6rem;text-decoration:none;color:var(--ink);font-weight:800;min-height:48px}}
.brand img{{width:98px;height:50px}}
header nav a{{display:inline-flex;align-items:center;min-height:48px;padding:0 .7rem;color:var(--ink);font-weight:600;text-decoration:none}}
header nav a:hover{{color:var(--red-dark)}}
main{{padding:2.5rem 0 3rem}}
h1,h2{{font-family:"Barlow Semi Condensed","Barlow SC Fallback",Arial,sans-serif;line-height:1.1}}
h1{{font-size:clamp(2rem,4.6vw,2.8rem);margin:0 0 1rem}}
.crumb{{color:var(--muted);font-size:.95rem;margin-bottom:1rem}}
.crumb a{{color:var(--red-dark)}}
.todo{{border:1px dashed #d8b23b;background:#fff4cc;color:#5c4300;border-radius:8px;padding:1rem 1.2rem;margin:1.5rem 0}}
.btn{{display:inline-flex;align-items:center;min-height:48px;padding:.7rem 1.4rem;border-radius:999px;background:var(--red);color:#fff;font-weight:600;text-decoration:none}}
.btn:hover{{background:var(--red-dark)}}
footer{{background:var(--ink);color:#c9d1db;padding:2rem 0;font-size:.95rem}}
footer a{{color:#fff}}
</style>
</head>
<body>
<a class="skip" href="#contenu">Aller au contenu</a>
<header>
  <div class="wrap">
    <a class="brand" href="{rel}"><img src="{rel}assets/img/logo-its.webp" width="98" height="50" alt="ITS Travaux Spéciaux – accueil" decoding="async"></a>
    <nav aria-label="Navigation principale"><a href="{rel}#expertises">Expertises</a><a href="{rel}#pathologies">Pathologies</a><a href="{rel}#ouvrages">Ouvrages</a><a href="{rel}#realisations">Réalisations</a><a href="{rel}contact/">Contact</a></nav>
  </div>
</header>
<main id="contenu">
  <div class="wrap">
    <p class="crumb"><a href="{rel}">Accueil</a>{crumb}</p>
    <h1>{title}</h1>
    <p>{desc}</p>
    {extra}
    <div class="todo"><strong>[À COMPLÉTER]</strong> Page squelette de la maquette : contenu détaillé, photos de chantier et références à rédiger avec ITS Travaux Spéciaux.</div>
    <p><a class="btn" href="{rel}contact/">Demander un diagnostic</a></p>
  </div>
</main>
<footer>
  <div class="wrap">
    <p>ITS Travaux Spéciaux – IVEBAT · 14 impasse Philippe-Gozola, 85000 La Roche-sur-Yon · <a href="mailto:contact@its-entreprise.com">contact@its-entreprise.com</a></p>
    <p>Maquette de démonstration réalisée par Collet Marketing.</p>
  </div>
</footer>
</body>
</html>
"""

EXTRA = {
    "contact": """<ul>
      <li>Siège – La Roche-sur-Yon : 14 impasse Philippe-Gozola, 85000 La Roche-sur-Yon – <a href="tel:+33251469923">02 51 46 99 23</a></li>
      <li>Agence Île-de-France – Pantin : 26 bis rue des Pommiers, 93500 Pantin – <a href="tel:+33164265700">01 64 26 57 00</a></li>
      <li>Agence Bretagne – La Mézière : ZI La Montgervalaise, 35520 La Mézière</li>
      <li>E-mail : <a href="mailto:contact@its-entreprise.com">contact@its-entreprise.com</a></li>
    </ul>""",
    "mentions-legales": """<h2 id="maquette">À propos de cette maquette</h2>
    <p>Cette page d'accueil est une maquette de démonstration réalisée par Collet Marketing pour ITS Travaux Spéciaux. Elle n'utilise aucun cookie ni traceur. Les visuels marqués « Photo de chantier à remplacer » sont des images de substitution.</p>""",
}


def main():
    urls = [(BASE, "1.0")]
    for section, (section_title, pages) in PAGES.items():
        for slug, title, desc in pages:
            path = f"{section}/{slug}/" if section else f"{slug}/"
            depth = path.count("/")
            rel = "../" * depth
            crumb = f' › <a href="{rel}#{section}">{section_title}</a> › {title}' if section else f" › {title}"
            html = TEMPLATE.format(title=title, desc=desc, url=BASE + path, rel=rel, crumb=crumb, extra=EXTRA.get(slug, ""))
            out = ROOT / path / "index.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(html, encoding="utf-8")
            urls.append((BASE + path, "0.7" if section else "0.5"))

    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, prio in urls:
        sitemap.append(f"  <url><loc>{url}</loc><lastmod>{TODAY}</lastmod><priority>{prio}</priority></url>")
    sitemap.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")

    def links(section):
        return "\n".join(f"- [{t}]({BASE}{section}/{s}/): {d}" for s, t, d in PAGES[section][1])

    llms = f"""# ITS Travaux Spéciaux

> ITS Travaux Spéciaux (marque IVEBAT, signature « Ingénierie et Travaux Spéciaux ») est une entreprise française spécialisée dans la réparation, le renforcement et la prolongation de la durabilité des ouvrages en béton armé et précontraint. Bureau d'études intégré, démarche Lean, équipes mobiles intervenant partout en France, sans interrompre l'activité du client.

Noms utilisés : ITS Travaux Spéciaux, ITS, IVEBAT, ITS Ingénierie et Travaux Spéciaux. À ne pas confondre avec d'autres sociétés nommées « ITS ».

## Zones d'intervention

- Île-de-France : Paris et petite couronne (agence de Pantin).
- Grand Ouest : Bretagne, Normandie, Pays de la Loire (siège de La Roche-sur-Yon, agence de La Mézière).
- Équipes mobiles sur toute la France.

## Implantations

- Siège : 14 impasse Philippe-Gozola, 85000 La Roche-sur-Yon – 02 51 46 99 23
- Agence Île-de-France : 26 bis rue des Pommiers, 93500 Pantin – 01 64 26 57 00
- Agence Bretagne : ZI La Montgervalaise, 35520 La Mézière
- Contact : contact@its-entreprise.com – LinkedIn : https://www.linkedin.com/company/its-ivebat-travaux-speciaux

## Expertises

{links("expertises")}

## Pathologies traitées

{links("pathologies")}

## Types d'ouvrages

{links("ouvrages")}

## Réalisations récentes

- Renforcement par précontrainte additionnelle des gradins du Parc des Princes (Paris).
- Renforcement de poutres par précontrainte extérieure au parking Charles Lorilleux à Puteaux.
- Renforcement d'une poutre de 50 mètres dans un centre commercial à Paris.

## Pages clés

- [Page d'accueil]({BASE}): présentation, expertises, pathologies, ouvrages, réalisations, FAQ, implantations
- [FAQ]({BASE}#faq): réponses aux questions fréquentes des maîtres d'ouvrage
- [Contact et demande de diagnostic]({BASE}contact/)
- [Recrutement]({BASE}recrutement/)
- [Plan du site (sitemap.xml)]({BASE}sitemap.xml)
"""
    (ROOT / "llms.txt").write_text(llms, encoding="utf-8")
    print(f"{len(urls) - 1} pages secondaires, sitemap.xml et llms.txt générés.")


if __name__ == "__main__":
    main()
