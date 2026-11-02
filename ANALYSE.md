# Analyse scientifique du dataset Kenya SACCO

Audit indépendant du record https://doi.org/10.5281/zenodo.18912903 ; récupération : 2026-11-02T10:38:50.541758+00:00

## Conclusion

Le fichier est exploitable pour une expérience méthodologique sous réserve de signaler sa provenance non établie. Son onglet est nommé Synthetic_SACCO_Data alors que la notice décrit des données administratives anonymisées. Ce nom ne suffit pas à établir la génération synthétique. Aucune accusation de fabrication ne peut être tirée de ce seul indice.

## Structure et qualité

Le fichier contient 4850 lignes et 33 colonnes, contre 36 variables annoncées. 4 000 valeurs de cible sont égales à 1 (82,47 %). Aucun doublon de ligne entière n’a été observé. Cela n’exclut pas des prêts répétés pour une même personne.

Les 499 cellules vides d’éducation (10,29 %) et 1 226 cellules vides de garantie (25,28 %) ont été conservées comme vides à la lecture. Leur sens reste indéterminé ; il ne faut pas automatiquement assimiler ces cellules à des modalités « aucune ».

## Provenance et documentation

Les métadonnées API identifient Maurice Wanyonyi, une affiliation déclarée à University of Embu, un ORCID et une licence CC BY 4.0. Le dépôt date du 8 mars 2026. Le DOI versionné et les empreintes favorisent la traçabilité du fichier, sans certifier sa collecte. La notice affirme une collecte de janvier 2015 à avril 2025 auprès de plusieurs SACCOs. Institutions participantes, base de sondage, autorisations, anonymisation, historique de nettoyage et mécanisme de sélection ne sont pas établis dans les éléments examinés.

## Fuite et définition de la cible

Days_Past_Due, Loan_Recovery_Procedure et Default_Rate_Percent sont présentes, contrairement à leur exclusion annoncée. Pour une prédiction à l’octroi, leur disponibilité et leur relation au résultat sont problématiques. Les trois ont été retirées ensemble dans le scénario réduit. Cette expérience ne mesure pas leur contribution individuelle et ne garantit pas que les autres variables soient disponibles au moment de la décision.

La notice définit le défaut par au moins 90 jours de retard ou passage en perte. Dans le fichier, 2 408 défauts ont au moins 90 jours de retard ; 1 592 défauts ont moins de 90 jours. Les 850 non-défauts sont tous sous 90 jours. L’absence d’une variable explicite de passage en perte et de dates empêche de valider entièrement cette définition. Ces 1 592 cas ne constituent pas à eux seuls une contradiction, car le passage en perte est une autre condition possible.

## Expérience prédictive

Validation croisée stratifiée en 5 plis, mélange et graine 42. Les mêmes plis sont utilisés pour tous les modèles. Prétraitements ajustés dans chaque pli : imputation médiane et standardisation des numériques ; imputation modale des catégories vides puis one-hot encoding. Logistique : max_iter=2000 ; forêt : 150 arbres, min_samples_leaf=5, random_state=42. Seuil de classification standard 0,5, sans optimisation ni rééquilibrage.

|Scénario|Modèle|ROC AUC|AP|Exactitude équilibrée|Brier|
|---|---|---:|---:|---:|---:|
|avec_fuites|Régression logistique|1.000000 ± 0.000000|1.000000 ± 0.000000|1.000000 ± 0.000000|0.000332 ± 0.000096|
|avec_fuites|Forêt aléatoire|1.000000 ± 0.000000|1.000000 ± 0.000000|1.000000 ± 0.000000|0.001877 ± 0.000266|
|sans_fuites_identifiees|Régression logistique|0.647153 ± 0.016191|0.889934 ± 0.007247|0.506699 ± 0.005752|0.138859 ± 0.002033|
|sans_fuites_identifiees|Forêt aléatoire|0.612790 ± 0.017412|0.869428 ± 0.008365|0.500000 ± 0.000000|0.140450 ± 0.001335|

Les écarts-types entre plis ne sont pas des intervalles de confiance. Les modèles avec variables à risque atteignent une discrimination parfaite, ce qui soutient la vigilance sur la fuite, sans démontrer l’origine précise de ce résultat. Après retrait, la discrimination devient modeste. À 0,5, la forêt obtient une exactitude équilibrée de 0,50 : la forte exactitude brute est alors celle de la classe majoritaire. AP doit être comparée à la prévalence élevée de 0,824742. Le Brier d’une probabilité constante égale à cette prévalence est environ 0,1445 (repère descriptif calculé sur l’ensemble du fichier).

## Exploration descriptive

Les prêts totalisent 733 634 682,60 KES ; médiane 149 359,58 KES et moyenne 151 264,88 KES. La médiane des revenus mensuels est 59 825,245 KES. Ces montants décrivent uniquement le fichier et ne doivent pas être interprétés comme des estimations nationales. Les comparaisons de comtés et secteurs du dashboard sont des agrégats descriptifs, sans ajustement causal ou validation de représentativité. Les montants ne sont pas ajustés à l’inflation, faute de dates individuelles.

## Limites à déclarer

1. Provenance et caractère réel, synthétique ou hybride non confirmés indépendamment.
2. Divergences entre notice, schéma et variables effectivement fournies.
3. Sélection, nettoyage, anonymisation et horizon du défaut insuffisamment documentés.
4. Absence de dates et d’identifiants pour contrôler les dépendances et la dérive temporelle.
5. Cible déséquilibrée et signification incertaine de certaines cellules vides.
6. Validation interne uniquement ; aucune garantie de transportabilité, causalité, équité ou aptitude au déploiement.

## Intégrité et sources

Source primaire : https://zenodo.org/records/18912903 ; API : https://zenodo.org/api/records/18912903. Fichier source : sacco_loan.xlsx, 908 341 octets.

MD5 : 8226932cc9e11e3acd394171118568b8

SHA-256 : 7791b208d4d733cb1573e2d74da66b5901659f1de8935e8780f2aa0dec29bb07

Les métadonnées récupérées sont conservées dans metadata.json. Les résultats numériques et profils sont dans dist/audit.json. Le script analyse.py permet de les reproduire. Les données sources sont attribuées à Maurice Wanyonyi sous CC BY 4.0 selon l’API. Aucun dossier individuel n’est redistribué.