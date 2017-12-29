# READEZ MOI
Jehan-Antoine Vayssade, Hugo Rens et Rémi Maigné
(Et l'autre groupe ?)

## Projet

Le projet consiste à identifier individuellement un brochet, c'est à dire à **pouvoir, à partir de deux images, dire si ils sont du même poisson ou non**. Des informations plus amples sont disponibles à l'adresse-que-vous-connaissez.

## Collaboration
Un autre groupe a pour but de trouver des brochets dans une image. Nos données en entrée sont donc celles qu'ils obtiennent. Afin de réaliser le projet, nous créerons dans un premier temps les données terrain ensemble (soit 6 personnes). Notre groupe pourra ensuite utiliser cette vérité terrain et éviter d'être dépendant des résultats de l'autre groupe.

Ces données seront dans un fichier JSON.

## Pros & Cons des langages:

* Python:
	* **OpenCV**
	* Grosses libs
	* Facile à programmer
	* Prototype
	* **Lent**

* MATLABⓡ:
	* ~~Chiant~~ Fastidieux à programmer
	* Aucune lib externe/*gratuite*/*libre*
	* **Tout le monde ne l'a pas**
	* Lent

* C/C++:
	* **OpenCV**
	* Grosses libs
	* Long à programmer
	* Produit fini
	* **Rapide**

* Lisp:
	* Qui sait programmer en LISP de manière fluide et productive ?

* JavaScript:
	* ...

## Création des fichiers JSON

Les fichiers JSON des campagnes 1 et 2 ont été réalisées avec [imglab](https://github.com/davisking/dlib/tree/master/tools/imglab) en XML puis converties avec le script présent dans le dossier `groundtruth/`, et celles des campagnes 3 et 4 avec le "viewer" en C++/Qt dans `viewer/`.
