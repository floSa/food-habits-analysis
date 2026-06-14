# 03 — L'espace social alimentaire (Analyse des Correspondances Multiples)

L'**ACM** (Analyse des Correspondances Multiples) projette dans un plan les individus et
les modalités de réponse, de sorte que des habitudes qui « vont ensemble » se retrouvent
proches. C'est l'outil de la sociologie de la consommation (Bourdieu) : il révèle les
**oppositions structurantes** dans la manière de manger.

On construit l'espace à partir des **fréquences de consommation** (variables actives),
puis on y projette l'âge, le diplôme et le Score Santé (variables illustratives) pour voir
comment ils s'y inscrivent.

## 1. Préparation et variables actives

Les variables actives sont les huit fréquences de consommation. Les valeurs manquantes
sont traitées comme une modalité à part entière (« Non répondu »), comme dans
l'application.

    1681 individus × 8 variables actives


## 2. Ajustement du modèle et inertie brute

On ajuste l'ACM sur cinq axes et on lit la part d'inertie (variance) portée par chacun.


|   component |   eigenvalue | % of variance   | % of variance (cumulative)   |
|------------:|-------------:|:----------------|:-----------------------------|
|           0 |        0.292 | 4.86%           | 4.86%                        |
|           1 |        0.267 | 4.44%           | 9.30%                        |
|           2 |        0.243 | 4.04%           | 13.34%                       |
|           3 |        0.222 | 3.70%           | 17.04%                       |
|           4 |        0.202 | 3.37%           | 20.41%                       |


Les pourcentages bruts paraissent dérisoires (4,9 % pour le premier axe). C'est un
**artefact bien connu de l'ACM** : le codage disjonctif gonfle artificiellement le nombre
de dimensions et écrase mécaniquement les pourcentages. Les comparer à ceux d'une ACP
serait une erreur — il faut les **corriger**.

## 3. Correction de Benzécri

La correction de Benzécri ne retient que les axes dont la valeur propre dépasse 1/K et
recalcule des pourcentages d'inertie réalistes.


| Axe   |   % brut |   % Benzécri |   % Benzécri cumulé |
|:------|---------:|-------------:|--------------------:|
| Axe 1 |     4.86 |         36.1 |                36.1 |
| Axe 2 |     4.44 |         26.1 |                62.1 |
| Axe 3 |     4.04 |         18   |                80.1 |
| Axe 4 |     3.7  |         12.2 |                92.3 |
| Axe 5 |     3.37 |          7.7 |               100   |



    
![png](03_sociologie_acm_files/03_sociologie_acm_11_1.png)
    


Après correction, le **plan 1-2 capte environ 62 % de l'inertie** (36 % + 26 %) : il est
largement suffisant pour une lecture en deux dimensions. On peut interpréter les deux
premiers axes en confiance.

## 4. Le plan des modalités

Chaque point est une réponse possible (ex. « Viande rouge = Jamais »). Les modalités
proches sont souvent choisies par les mêmes personnes.


    
![png](03_sociologie_acm_files/03_sociologie_acm_15_0.png)
    


Un fait saute aux yeux : **toutes les modalités « Jamais » se regroupent à droite**, loin
du nuage. L'axe 1 n'oppose donc pas tant un aliment à un autre qu'il **isole une minorité
qui déclare ne (presque) rien consommer** des répondants engagés. Les fréquences élevées de
viande et de poisson, elles, s'étirent vers le haut (axe 2).

## 5. Interprétation des axes par les contributions

Pour interpréter rigoureusement un axe, on regarde les modalités qui y **contribuent** le
plus (en % de l'inertie de l'axe), avec le signe de leur coordonnée.


**Axe 1 — les plus contributives**



| Modalité                         |   Contribution % |   Coordonnée |
|:---------------------------------|-----------------:|-------------:|
| Viande blanche = Jamais          |             23.9 |         2.75 |
| Viande rouge = Jamais            |             23.3 |         2.41 |
| Poisson = Jamais                 |             13.7 |         1.98 |
| Laitiers = Jamais                |              5.5 |         2.12 |
| Féculents = Jamais               |              4.7 |         6.07 |
| Légumes = Jamais                 |              3.1 |         3.92 |
| Légumes = A tous les repas       |              2.4 |         0.4  |
| Viande blanche = 3 x par semaine |              2.1 |        -0.36 |



**Axe 2 — les plus contributives**



| Modalité                         |   Contribution % |   Coordonnée |
|:---------------------------------|-----------------:|-------------:|
| Poisson = 5 x par semaine        |             11.2 |         2.24 |
| Viande rouge = 5 x par semaine   |             11.1 |         1.66 |
| Viande blanche = 1 x par jour    |              7.1 |         1.52 |
| Viande blanche = 5 x par semaine |              7   |         0.94 |
| Viande rouge = 1 x par jour      |              6.4 |         2.23 |
| Poisson = 1 x par jour           |              5.8 |         2.32 |
| Féculents = 3 x par semaine      |              3.5 |        -0.69 |
| Poisson = Très rarement          |              3.2 |        -0.51 |


L'**axe 1** est presque entièrement construit par les « Jamais » (viande blanche, viande
rouge, poisson, laitiers, féculents, légumes), tous du même côté : c'est un **axe de
non-consommation / désengagement alimentaire**. L'**axe 2** est porté par les consommations
**fréquentes de protéines animales** (poisson et viandes à 5×/semaine ou plus) : c'est un
**axe d'intensité carnée**.

## 6. Où se situent les profils sociaux et le Score Santé ?

On projette les individus et on les colore par variable illustrative (âge, puis Score
Santé) pour voir si la position dans l'espace est socialement structurée.


    
![png](03_sociologie_acm_files/03_sociologie_acm_23_0.png)
    


On chiffre ces tendances par des corrélations de Spearman entre coordonnées et variables.


- Corrélation **Axe 1 ↔ Score Santé** : ρ = 0.44
- Corrélation **Axe 2 ↔ Score Santé** : ρ = 0.43
- **Axe 2 moyen par âge** : {'-18': 0.08, '18-34': -0.05, '35-60': 0.08, '+60': 0.17}


Deux enseignements. D'une part, les deux axes corrèlent modérément avec le Score Santé
(ρ ≈ 0,44) : l'espace de consommation et le score racontent des choses voisines mais pas
identiques. D'autre part, **l'axe 2 croît avec l'âge** (les +60 ans sont les plus « carnés »
en fréquence), mais le nuage par âge reste **largement superposé** : aucune tranche d'âge
n'occupe une région propre.

## 7. Synthèse

**La structure de l'espace alimentaire.** Une fois l'inertie corrigée (Benzécri), deux
dimensions suffisent (≈ 62 %) :

- **Axe 1 — l'engagement** : oppose une petite minorité déclarant « ne jamais » consommer
  la plupart des aliments au reste des répondants. C'est d'abord un axe de
  non-consommation (et possiblement de style de réponse au questionnaire).
- **Axe 2 — l'intensité carnée** : sépare les gros consommateurs de viande et de poisson des
  plus modérés ; il augmente avec l'âge.

**Le point sociologique central.** Contrairement à l'hypothèse bourdieusienne forte, les
**variables socio-démographiques structurent faiblement** cet espace : les nuages par âge
ou par diplôme se recouvrent très largement, et l'axe principal tient surtout à des
réponses « Jamais ». Cela **converge avec le notebook 02** (la régression n'expliquait que
~9 % du Score Santé) : dans cet échantillon jeune et homogène, *ce qu'on mange* ne se déduit
guère de *qui l'on est* socialement.

La piste suivante n'est donc plus sociale mais **cognitive** : et si les différences se
jouaient dans les **croyances et connaissances** nutritionnelles ? C'est l'objet du
notebook 04.
