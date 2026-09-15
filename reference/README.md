# reference/

Documents externes, en **lecture seule**, chacun daté de son snapshot. Rien ici
n'est modifié par le projet : ce sont des photographies de sources dont
l'original vit ailleurs.

## En attente — `rsl-squelette-v1.json`

**Statut : manquant.** Le chemin du moteur RSL n'a pas été fourni à la session
d'amorçage (le champ était laissé « à compléter »).

Ce fichier doit être une copie du squelette JSON `rsl-squelette@1`, accompagnée
de sa date de snapshot. Il n'est **pas** le moteur — le moteur reste externe au
dépôt, son mode d'attache sera tranché en phase 10. C'est un document de
spécification : la photographie datée du vocabulaire que le catalogue doit
employer au mot près (`close_stamp`, `granularity_minutes`,
`publication_lag_minutes`, `known_in_advance`, la liste des `root`).

**La phase 01 en a besoin** : le critère « adéquation au moteur » de la décision
données se chiffre en le lisant. Ne pas démarrer la phase 01 sans lui.

Une fois le fichier importé : le rendre en lecture seule, noter ici la date du
snapshot et l'origine exacte (dépôt et commit, ou chemin et date de
modification), puis supprimer cette section.
