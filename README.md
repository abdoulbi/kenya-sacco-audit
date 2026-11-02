# Kenya SACCO — audit et dashboard scientifique

Analyse indépendante du dataset de Maurice Wanyonyi, *SACCO Loan Data for Women Entrepreneurs in Kenya (2015–2025)*, Zenodo v1, DOI https://doi.org/10.5281/zenodo.18912903.

## Consulter le dashboard

Ouvrir `dist/index.html` dans un navigateur après extraction complète du projet. Les résultats sont embarqués, sans service externe ni exécution Python. Une connexion n'est nécessaire que pour les liens sources et la police facultative.

Filtres par comté, secteur et localisation ; export CSV des cohortes sélectionnées ; dictionnaire avec recherche ; qualité du fichier ; comparaison de modèles et documentation des limites. Les filtres n'affectent que l'exploration des cohortes. Aucun dossier individuel n'est publié.

## Résultat principal

4 850 lignes et 33 colonnes. L'onglet `Synthetic_SACCO_Data` impose de clarifier la nature des données ; son nom ne prouve pas à lui seul leur génération synthétique. Trois variables déclarées exclues sont présentes. Avec elles, l'AUC de validation interne atteint 1,00. Après leur retrait, elle vaut environ 0,647 (logistique) et 0,613 (forêt). Aucune performance en conditions réelles n'est démontrée.

Lire `ANALYSE.md` pour les résultats, le protocole et les limites.

## Reproduire

Python 3, pandas, numpy, openpyxl et scikit-learn sont requis. Les versions utilisées figurent dans `dist/audit.json` et `requirements.txt`.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python analyse.py
```

Le script télécharge la version Zenodo, vérifie son MD5, examine le fichier en mémoire et régénère `dist/audit.json`, `dist/data.js` et `metadata.json`. Le timestamp de récupération peut varier. L'empreinte SHA-256 permet de vérifier l'identité des données. Les champs de catégories vides sont comptés comme cellules vides ; leur signification n'est pas présumée.

## Publication sur GitHub Pages

Créer un dépôt `kenya-sacco-audit`, y importer ces fichiers puis, dans Settings → Pages, choisir « Deploy from a branch », branche `main`, dossier `/docs`. Copier préalablement le contenu de `dist/` dans `docs/`. Le dépôt seul rend le code accessible ; GitHub Pages doit être activé séparément pour servir le dashboard comme site.

## Attribution et droits

Source : Maurice Wanyonyi, University of Embu (affiliation déclarée), 2026, Zenodo v1. Licence des données : CC BY 4.0 selon les métadonnées API. Ce projet contient des agrégats et analyses dérivés, et non le classeur source. Les conclusions critiques appartiennent à cette analyse indépendante ; aucune affiliation avec le déposant ou les SACCOs n'est revendiquée. Code et rapport de ce projet proposés sous MIT (voir LICENSE) ; les droits des données sources restent ceux de leur licence.
