# simonlaugueux.fr

Site vitrine de **Simon Laugueux** — dégustations de vins & spiritueux à Cahors et dans le Lot.
Site statique d'une seule page, publié avec GitHub Pages. Aucun outil à installer pour le modifier : un éditeur de texte suffit.

## Fichiers

| Fichier | Rôle |
|---|---|
| `index.html` | Tout le contenu de la page |
| `assets/css/style.css` | Couleurs, polices, mise en page |
| `assets/js/main.js` | Menu mobile et animations (facultatif) |
| `assets/img/` | Icônes, texture bois, favicon, icône iPhone (`apple-touch-icon.png`), image de partage (`partage.jpg`) |
| `assets/fonts/` | Polices Cormorant Garamond et Lato, hébergées sur le site (aucun appel à Google Fonts) |
| `tools/og_image.py` | Régénère l'image de partage et l'icône iPhone à partir des modèles `tools/og-image.html` et `tools/icone.html` |
| `tests/` | Vérifications automatiques |
| `CNAME` | Nom de domaine pour GitHub Pages |
| `.nojekyll` | Demande à GitHub Pages de servir les fichiers tels quels |
| `.htmlvalidate.json` | Configuration du validateur HTML |

## Modifier le contenu

### Modifier une formule ou un tarif

**Actuellement masquée** : la section formules (et l'encart « De passage dans le Lot ? ») est mise en commentaire dans `index.html`, entre les repères `DÉBUT SECTION FORMULES MASQUÉE` et `FIN SECTION FORMULES MASQUÉE` ; le lien « Formules » du menu est aussi commenté. La marche à suivre pour la réafficher est écrite dans le commentaire.

Section `id="formules"` : chaque formule est un bloc `<article class="formule">`. Le prix est dans `<p class="prix">` et doit contenir « à partir de ». Tant que les tarifs ne sont pas décidés, ils sont affichés « XX € » (les tests refusent un chiffre dans le prix : mettre à jour `test_trois_formules_completes` le jour où les tarifs sont fixés).

### Changer le téléphone ou l'e-mail

Rechercher/remplacer dans `index.html` :
- `+33781631578` (liens `tel:` et données `telephone`) et le numéro affiché, écrit avec des espaces insécables `07&nbsp;81&nbsp;63&nbsp;15&nbsp;78` (dans le texte d'un lien `tel:`, tous les espaces doivent être des `&nbsp;` : le validateur HTML l'exige) ;
- `simonlaugueux@proton.me` (liens `mailto:`, texte affiché et données `email`).

Dans les liens `mailto:`, l'objet et le texte pré-rempli sont **encodés** (`%20` pour un espace, `%C3%A9` pour « é », `%0A` pour un retour à la ligne). Pour encoder un nouveau texte :

```bash
python3 -c "from urllib.parse import quote; print(quote('Votre texte ici'))"
```

Entre `subject=…` et `body=…`, le séparateur s'écrit `&amp;` dans le HTML.

### Couleurs

Les six couleurs sont définies une seule fois en haut de `assets/css/style.css` (`:root`). Tout couple texte/fond doit garder un contraste d'au moins 4,5:1. Les tests vérifient les couples listés dans `PAIRES` (`tests/test_site.py`) : si vous utilisez une nouvelle combinaison texte/fond dans le CSS, ajoutez-la à cette liste.

## Vérifier avant de publier

```bash
python3 -m unittest discover -s tests -v   # structure, contenu, styles, images
node --test tests/main.test.mjs            # comportement du menu et des animations
npx --yes html-validate index.html         # validité HTML
python3 -m http.server 8000                # aperçu sur http://localhost:8000
```

## Aperçu des liens partagés

Quand on partage https://simonlaugueux.fr (WhatsApp, Messenger, LinkedIn, Slack…), l'aperçu affiche le titre, la description et l'image déclarés dans le `<head>` de `index.html` (balises `og:*` et `twitter:*`).

L'image `assets/img/partage.jpg` (1200×630, moins de 300 Ko) est générée à partir du modèle `tools/og-image.html`, qui reprend les couleurs et les polices du site. Le contenu tient dans le carré central, car WhatsApp recadre l'aperçu en carré. Après une modification du modèle, du nom ou des couleurs :

```bash
uv run --with pillow tools/og_image.py   # ou : pip install pillow && python3 tools/og_image.py
```

Il faut Google Chrome, Chromium ou Edge installé (ou leur chemin dans la variable `CHROME`). Le script régénère aussi `assets/img/apple-touch-icon.png` (180×180) depuis `tools/icone.html`.

Les applications gardent l'aperçu en cache pour chaque adresse. Pour en forcer un nouveau après publication : [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/) → « Scrape Again » (vaut pour WhatsApp et Messenger), [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/), ou partager l'adresse avec un paramètre, par exemple `https://simonlaugueux.fr/?v=2`. Si l'image change, lui donner un nouveau nom de fichier évite que l'ancienne reste en cache.

## Contenu à valider par Simon

Les éléments suivants sont **provisoires** :

- Textes de présentation (accroche, « L'univers », descriptions des formules).
- Formules, durées et tailles de groupe. Tarifs non décidés : affichés « XX € ».
- Bandeau d'annonce en haut de page (`<aside class="annonce">`, « le site sera prêt courant octobre ») : à retirer ou modifier une fois le site finalisé.
- Absence de photos : les illustrations SVG pourront être remplacées par de vraies photos.
- Pas de lien WhatsApp pour l'instant.

## Mise en ligne (GitHub Pages)

1. Pousser le dépôt sur GitHub.
2. *Settings → Pages* : « Deploy from a branch », branche `main`, dossier `/ (root)`.
3. *Custom domain* : `simonlaugueux.fr` (déjà renseigné par le fichier `CNAME`).
4. Chez le registrar du domaine, créer les enregistrements DNS :

   | Type | Nom | Valeur |
   |---|---|---|
   | A | `@` | `185.199.108.153` |
   | A | `@` | `185.199.109.153` |
   | A | `@` | `185.199.110.153` |
   | A | `@` | `185.199.111.153` |
   | AAAA | `@` | `2606:50c0:8000::153` |
   | AAAA | `@` | `2606:50c0:8001::153` |
   | AAAA | `@` | `2606:50c0:8002::153` |
   | AAAA | `@` | `2606:50c0:8003::153` |
   | CNAME | `www` | `<utilisateur-github>.github.io` |

5. Une fois le DNS propagé, cocher *Enforce HTTPS*.
