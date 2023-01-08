# AI_project
## Description du processus
### Explication de l'interface 
L'interface aussi appelée UI dans la suite de ce document à pour but de faciliter l'utilisation de techniques de reconnaissance de caractères.

 L'OCR ou *Optical character recognition* est un terme couvrant l'ensemble des méthodes permettant d'extraire du *texte* présent dans un document. Le *texte* dans ce contexte peut autant être composé des chiffres que des lettres.  
 Nous définissons dans ce rapport un *moteur OCR* comme un système prenant un document en entrée et qui extrait le texte reconnu et le retourne dans un format exploitable par des humains ou des machines.  
 Nous avons choisi que nos moteurs OCR retournent des string compatibles avec le format JSON pour assurer la facilité d'exploitation des résultats ainsi que leur interprétabilité par les utilisateurs. 

Notre UI est une application web, cela permet un usage aisé de la solution sur des appareils de nature différentes tel que des smartphones et des ordinateurs.

Notre application comporte 3 onglets:
- Home: l'interface de préparation du traitement du document
- Historic : présente l'historique des documents scannés
- About : renvoie vers le repository github contenant cette documentation ainsi que le code source

Nous allons nous focaliser en premier lieu sur les fonctionnalités de l'onglet *Home* visible ci-dessous.  
![image upload](screenshots/main_screen.png)
- Chargement d'un document :  
Nous avons un bouton en haut à gauche qui permet à l'utilisateur de sélectionner un document stocké sur son appareil.  
L'utilisateur peux soumettre une image jpeg ou png ainsi qu'un fichier pdf.  
Par contre, tous les autres types de fichiers sont bloqués pour éviter que les moteurs OCR reçoivent des données non interprétables.  
Les fichiers sont filtrés en fonction de leur extension par l'élément html pour éviter ce désagrément. 

- Affichage de l'aperçu :  
En dessous du bouton mentionné dans le paragraphe précédent nous avons deux cadres initialement vides.  
Lorsqu'un fichier est sélectionné par l'utilisateur, un des 2 cadres affichera l'apperçu du document.  
    - S'il s'agit d'une image, celle-ci sera affichée tel que présenté ci-dessous.
    ![crop file](screenshots/cropper_screen.png)
    Le carré bleu montre l'image telle qu'elle sera rognée avant d'être soumise au moteur OCR. La taille et l'emplacement de cette zone est modifiable par l'utilisateur à l'aide de la souris ou de son doigt en respectant les conventions classiques de manipulation de fenêtre sur son appareil. Le bouton *Restore* permet de réinitialiser les paramètres initiaux de la zone en cas de problème.

    - S'il s'agit d'un pdf, celle-ci sera affiché tel que présenté ci-dessous.
    ![pdf preview](screenshots/pdf_preview.png)
    Nous avons accès à une lecteur de pdf assez complet qui permet de parcourir l'ensemble des pages du document ainsi que d'y rechercher des mots clés. Cependant, il n'est plus possible dans ce cas-ci de rogner seulement une partie à soumettre au moteur d'OCR à cause de la nature du format pdf qui rend les modifications compliquées pour assurer un affichage identique sur tous les appareils.

- Choix du moteur OCR :  
L'option la plus à droite de l'écran est un menu déroulant qui permet de sélectionner le moteur OCR auquel on souhaite soumettre notre document.  
Nous avons actuellement 3 moteurs à disposition:
    - Digit
    - Text Typed
    - Hand Written      
 
  Nous expliquerons leurs cas d'utilisations optimaux respectifs ainsi que leur fonctionnement dans la suite du rapport.

- Soumission du document au moteur OCR :  
Le bouton *launch OCR* envoie la requête POST vers le bon url de notre api en fonction du choix de moteur par l'utilisateur en ajoutant le document en tant que form-data pour que le traitement puisse démarrer en backend.  

### Traitement de l'entrée 
Les 3 moteurs commencent par exécuter une même fonction appelée *fileUpload()*. Cette fonction s'occupe de sauvegarder le document reçu avec la requête POST dans un dossier accessible à tous les moteurs dans le backend.  
Lorsque le fichier est un pdf, la fonction sauvegarde en plus une image de chaque page du fichier pour permettre d'afficher les aperçus dans l'onglet *Historic*   

### Choix du moteur d'OCR par l'utilisateur 
Notre application propose actuellement 3 moteurs : 
- Digit  
Comme son nom l'indique, c'est le moteur à privilégier pour la reconnaissance de chiffres.  
Ce moteur a été conçu pour lire des chiffres manuscrits répartit sur l'ensemble du document grâce au prétraitement appliqué par le moteur avant la reconnaissance du caractère. Il est important d'avoir conscience que ce moteur à été entrainé pour reconnaitre des chiffres et non des nombres donc des chiffres collés les uns aux autres auront tendance à être mal interprétés.  

- Text Typed  
Ce moteur est à utiliser pour tous les textes dactylographiés.  
Le moteur est entrainé pour la langue anglaise mais nos tests n'ont pas remarqué de baisse d'efficacité significative lors de la soumission de documents en français.  
Le prétraitement de ce moteur sépare le texte d'éventuelles images ou autre dans le document pour améliorer la qualité du résultat obtenu.  
Il peut être utile de savoir que ce moteur est plus efficace pour reconnaitre des mots et des phrases que pour reconnaitre des caractères individuels.

- Hand Written  
Comme son nom l'indique, c'est le moteur à privilégier pour la reconnaissance de caractères manuscrits.  
La qualité du résultat obtenu dépend beaucoup de la qualité du document d'entrée. Il est par exemple important de bien rogner l'image pour cibler un caractère unique sinon le moteur ne distinguera probablement que des mots et tentera de les approximer par une lettre chacun.  
Il ne faut pas être trop étonné si le résultat qu'on obtient est un chiffre car ce moteur est aussi capable de reconnaitre des chiffres manuscrits. Cependant, il est bien moins efficace que le moteur *digit* dans ce cas de figure.  


### Affichage du résultat 
Le template de la page de résultat dépend du type de fichier soumis.  
- Pour une image :  
Nous affichons l'impression brute d'un dictionnaire ayant pour clé le numéro de la boundingbox et pour valeur le texte extrait de cette boundingbox.  
Nous affichons également en dessous une copie du document soumis sur laquelle les boundingbox ainsi que leurs numéros respectifs apparaissent. <br />
![img result](screenshots/img_check_screen.png)

- Pour un pdf :  
Nous affichons une version reformatée du contenu extrait. Cet affichage tient compte des retours à la ligne présents dans le résultat obtenu afin que l'affichage du contenu soit le plus fidèle possible au document original.  
Le document soumis est lui-même affiché en dessous, celui-ci est à nouveau présenté dans le même type de lecteur de pdf que celui utilisé sur l'onglet *home* <br />
![pdf result 1](screenshots/pdf_check_1_screen.png)
![pdf result 2](screenshots/pdf_check_2_screen.png)

### Description des moteurs :
#### Tesseract :  
1. Contexte de l'outil  
Tesseract a été développé par HP entre 1984 et 1994 pour améliorer ses scanners.  
Le projet à ensuite été publié en open source par HP en 2005.

2. Architecture globale  
  Le type d'entrée à soumettre à tesseract est une image binaire. Une option est disponible pour y ajouter des définitions de zones de textes de formes polygonales.  
  Le traitement suit un processus en 3 étapes.
    1. *connected component analysis*  
    Cette étape consiste à détecter les contours de composants dans l'image. Cette étape est couteuse en puissance de calcul mais permet de reconnaitre les textes en blanc sur fond noir aussi facilement que ceux dans la version inverse qui est la plus couramment utilisée.  
    Les composants détectés sont assemblés en tant que *blob* qui seront par la suite redivisés en lignes divisées elles-mêmes en mots divisés eux-mêmes en caractères.
    2. Reconnaissance du texte  
    Cette étape consiste à tenter de reconnaitre chaque mot séquentiellement dans le document. Lorsqu'un mot reconnu est considéré comme satisfaisant par le classifieur statique, il est soumis comme donnée d'entrainement au classifieur dynamique pour améliorer les résultats de reconnaissance suivants.  
    L'étape est réalisée en 2 passes pour s'assurer d'avoir pu bénéficier de l'amélioration apportée par le classifieur dynamique sur l'ensemble du document.  
    Les 2 classifieurs sont expliqués plus en détail dans la suite du rapport.
    3. Reconnaissance des caractères restants  
    Cette étape s'occupe de résoudre les problèmes associés aux *fuzzy spaces* expliqués dans la section Reconnaissance des mots de ce rapport. C'est aussi à cette étape que les textes ayant une taille de police plus petite que celle utilisée dans le reste du document sont traités

3. Reconnaissance des lignes  
La technique utilisée par Tesseract est capable d'identifier les alignements de textes même dans les cas ou ceux-ci ne sont pas horizontaux sans nécessiter de redresser l'image. Cela permet d'éviter une perte de qualité qui pourrait impacter la qualité des résultats obtenus par des étapes subséquentes.  
En faisant l'hypothèse que des zones de textes ont été soumises en entrée, nous pouvons utiliser la hauteur moyenne de celles-ci pour déterminer la hauteur moyenne des caractères. Cette taille moyenne de caractère peut être utilisée pour filtrer les *blobs* identifiés par la *connected components analysis*.  
Les *blobs* filtrés peuvent ensuite être triés en fonction de leur coordonée x pour les assigner à une ligne et calculer la pente de la ligne grâce à l'utilisation de la technique *least median of squares fit* [2]. Les *blobs* qui avaient été rejetés par le filtres sont ensuite assigné à la bonne ligne.  
Le traitement des lignes se poursuit en approximant la *baseline* de chaque ligne de texte par une spline quadratique. Cette *baseline* peut donc être courbe.
4. Reconnaissance des mots
Les mots doivent être divisés en caractères pour être reconnus. Cette division peut se faire de 2 manières: 
  - texte à espacement fixe :  Dans ce cas, il suffit de diviser le texte en cases de tailles fixes  
  ![fixed pitch text](screenshots/fixed_pitch.png)
  - texte proportionnel : La taille des espaces dans ces textes est variable, il faut donc déterminer un pas moyen et les espaces proche de cette moyenne sont indiqués comme *fuzzy space*. Dans l'image ci-dessous, l'espace entre "of" et "financial" est un des fuzzy space présent. Le marquage en tant que *fuzzy space* retarde la prise de décision sur le mot après qu'il ait analysé par les classifieurs.  
  ![fixed pitch text](screenshots/proportional_text.png)
5. Classifieurs  
Le classifieur statique se base sur les segments des approximations polygonales pour créer ses *features* des différents caractères lors de l'entrainement. Cependant, cette méthode n'est pas suffisante pour reconnaitre des caractères dont des parties sont anormalement disjointes. Pour y remédier, les *features* sont déterminées par des segments courts ayant des longueurs normalisées issus du contour du caractère lors de la reconnaissance. Ces nouvelles *features* sont comparées aux prototypes générés par le classifieur lors de son entrainement.  
Le problème principal de cette méthode est l'importante puissance de calcul nécessaire pour comparer des données tellement différentes. En effet, les *features* obtenues lors de la reconnaissance sont en 3 dimensions (x, y position, angle) à raison de 50 à 100 *features* par caractères. Les prototypes quant à eux sont en 4 dimensions (x, y, position, angle, length) à raison de 10 à 20 *features* par configuration.  
La robustesse de ce classifieur face aux caractères à parties manquantes a permis d'éviter de devoir inclure ce type de caractère dans le set d'entrainement. L'entrainement n'a nécessiter que 20 échantillons de 94 caractères issus de 8 polices en une taille unique. Par contre chaque échantillon était décliné en 4 variantes (normal, **gras**, *italique*, ***gras et italique***) portant le total d'échantillon à 60160.

    Le classifieur dynamique utilise les mêmes *features* que le classifieur statique mais il se base sur des données d'entrainement différentes tel que précisé dans la section Reconnaissance du texte de ce rapport. Cette différence de données d'entrainement permet à ce classifieur d'être plus spécifique aux polices utilisées dans le document que le classifieur statique à conditions qu'il n'y ai pas un nombre trop important de polices différentes dans le document.  
    L'aspect spécifique du classifieur dynamique lui permet aussi d'être plus précis dans la reconnaissance de caractères ainsi que dans le rejet du bruit.  
    L'autre différence entre les 2 classifieurs est l'utilisation de la *baseline/x-height normalization* par le classifieur dynamique au lieu de la *moment normalization". La *baseline/x-height normalization* a l'avantage de réduire l'impact des rapports de proportions et de l'épaisseur des traits de la police. Cette technique permet également de reconnaitre efficacement la case des caractères à condition qu'il ne soit pas en indice ou en exposant bien que ces caractères soient reconnus.

6. Analyse linguistique  
  Tesseract défini les catégories linguistiques suivantes :
      - Top frequent word
      - Top dictionary word
      - Top numeric word
      - Top UPPER case word
      - Top lower case word (with optional initial upper) 
      - Top classifier choice word  

   Le meilleur mot est calculé pour chaque catégorie.  
   Le mot reconnu est celui qui à la distance globale la plus faible avec l'ensemble des catégories. La distance avec chaque catégorie est pondérée avec un facteur différent dans le calcul de la distance globale.  

#### CNN mnist :
Pour le moteur de reconnaissance de chiffre manuscrit, un CNN alimenté par le dataset de mnist semblait être la meilleure solution. Nous n'avons bien évidemment pas créé de toute pièce l'architecture du CNN mais nous nous sommes inspirés d'une solution trouvée sur Kaggle : 
https://www.kaggle.com/code/abdelwahed43/handwritten-digits-recognizer-0-999-simple-model

La première étape a été de préparer les données du dataset à être traitée :
- Séparation des labels et des données associées
- Normalisation des données 
- Reshapping des données 
- Transformation des labels en classe binaires ( 1 devient par exemple 0001 ), on les sépare en dix classe différentes. Une pour chacun des chiffres. 
- On transforme 10% des données d'entrainement en données de validation. Ces données de validation vont être utile durant l'entrainement afin de surveiller que le modèle ne s'habitue pas trop aux données d'entrainement.

On va ensuite définir les différentes couches de notre modéle, on expliquera par la suite ce que fait chacune des couches : 
- Conv2D, filtré 32 fois avec un kernel de 5x5
- Conv2D, filtré 32 fois avec un kernel de 5x5
- MaxPool2D, avec un pool de taille 2x2
- DropOut(0.25)
- Conv2D, filtré 64 fois avec un kernel de 3x3
- Conv2D, filtré 64 fois avec un kernel de 3x3
- MaxPool2D, avec un pool de taille 2x2
- DropOut(0.25)
- Flatten
- Dense(256,"relu")
- Dropout(0.5)
- Dense(10, "softmax")
<br />

![image](https://user-images.githubusercontent.com/75576766/211188929-baa9a43f-f432-4060-920a-55fcad16ca47.png)


Conv2D : Cette couche va nous permettre de créer un kernel qui va être convolué avec l'input pour donner l'output. Cette couche va nous permettre de nous focaliser sur les détails de l'image. 

MaxPool2D : Cette couche va nous permettre de diminuer le nombre de paramètre sans pour autant perdre de l'information. Elle va subdiviser notre input en un grand nombre de sous-groupes et ne garder pour ces sous-groupes que la valeur maximale. 

DropOut : Cette étape permet d'éviter l'overfitting en désactiver de manière aléatoire certains neurones durant un epoch. Un dropout de 0.25 fait en sorte que les neurones on 25 pourcents de chance de se désactiver. 

Flatten : La couche flatten va nous permettre de préparer les données à être analysé par la couche suivante. Elle va "aplatir" les données c'est à dire que l'on va passer d'un input en plusieurs dimension à un output en une seule dimension. 

Dense : Elle prend une entrée et applique une modification à l'aide de sa fonction d'activation dans ce cas-ci relu afin de nous donner un pourcentage de chance. Elle est connectée à tous les neurones de la zone précédente. 

Le créateur du CNN a décidé d'utiliser l'algorithme RMSprop comme optimiser, l'optimiser va nous permettre de diminuer la loss en modifier le CNN. Rmsprop est un optimiser qui va utiliser un taux d'apprentissage adaptatif. Il utilise une fonction de loss de type cross-entropie, celle mesure l'écart entre la distribution de probabilité prévue du modèle et celle réelle attendue. 

Il utilise également des métrics "Accuracy", qui ont un rôle semblable à la loss, qui permettent d'évaluer le système. Dans ce cas-ci, l'évaluation se déroule en regardant la fréquence à laquelle les prédictions du modèle correspondent aux labels réels. 

On va également utiliser la fonction ReduceLROnPlateau qui va nous permettre de réduire le taux d'apprentissage du modèle lorsque celui-ci cesse de s'améliorer. Le taux d'apprentissage étant la vitesse à laquelle se met à jour le modèle durant l'entrainement. 

Pour éviter l'overfitting on a décidé de ne faire que 3 epoch, en ayant fait des tests au-delà le modèle devient bien moins compétant pour les figures qu'il n'a pas eu dans son dataset. Il est trop spécialisé. 

On utilise le imageDataGenerator qui va nous permettre de nous entrainer avec des versions modifiés des images initiales. Il va les faire pivoter, zoomer mais également les shifter légèrement. 

Après avoir enregistrer ces paramètres on va pouvoir entrainer et essayer le modèle.

Lorsque l'on utilise les modèles il est important de faire en sorte de traiter les images d'input pour qu'elles correspondent à ce qui a été appris durant l'entrainement. Il sera donc utile de les redimensionner et de modifier leur couleur. 

#### CNN emnist :
Pour le moteur de reconnaissance de lettre manuscrite, un CNN alimenté par le dataset de emnist semblait être la meilleure solution. Nous n'avons bien évidemment pas créé de toute pièce l'architecture du CNN mais nous nous sommes inspirés d'une autre solution trouvée sur Kaggle : 
https://www.kaggle.com/code/achintyatripathi/emnist-letter-dataset-97-9-acc-val-acc-91-78
Malheureusement il est beaucoup moins performant que celui utilisé précédemment pour mnist.

La première étape la préparation des données : 
- On va séparer les labels et les données 
- On va ensuite normaliser les données et les reshape
- Catégoriser les labels en classes binaires
- Splitter les données d'entrainement en donnée d'entrainement et de validation

On va ensuite définir les différentes couches de notre modèle :

- Conv2D, filtré 32 fois avec un kernel de 3x3
- MaxPooling2D, avec un pool de 2x2
- Flatten
- Dense(521)
- Dense(128)
- Dense(27)

<br />

![emnist](https://user-images.githubusercontent.com/75576766/211189465-c0a095d9-0640-4d59-9eef-d3d86a8b3371.png)

Nous utilisons un optimiser RMSprop, avec une fonction de loss categorical_crossentropy et les mêmes metrics que pour mnist. 

On a mis en place de l'earlystoping et ReduceLROnPlateau, on a fait 5 epoch.

L'earlystopping va être utilisé pour éviter l'overfitting, il arrête l'apprentissage quand il s'aperçoit que le nombre d'erreur sur les datas de validation augmentent alors qu'ils descendent sur les datas de test. Lorsque c'est le cas le modèle commence à overfitter. 

On a ensuite entrainé le modèle et on l'a tester. Il est moins performant que mnist, tout d'abord le modèle comporte beaucoup moins de couche et pas de générateur d'images. De plus le sujet de emnist est beaucoup moins en vogue sur internet et nous n'avons pas su trouver de modèle plus efficace. 

### Bounding Box :
Pour la détection automatique de texte sur la page nous avons réutilisé un des principes de traitement d'image que nous avions vu en cours lors de l'année précédente. Il s'agit non pas de détection de texte mais plus de détection de "zone de couleur plus foncée", ce qui limite notre cas d'utilisation à de l'écriture blanc sur noir ou du moins foncé sur clair. 

Il va falloir traité l'image afin de détecter les zones de texte:
- On va tout d'abord lire l'image avec OpenCV
- On va ensuite la transformer en nuance de gris
- On ajoute un flou gaussien pour que les différentes zones soit moins distinctes et que l'on puisse trouver des mots/phrase/paragraphes entiers. 
-  Vient l'étape du treshold qui va nous permettre de "binariser" chacun des pixels de l'image, ceux-ci deviendront blanc ou noir selon l'intensité du gris
-  On va ensuite dilaté les différentes zones pour évité d'encadrer lettre par lettre. 
-  On va ensuite pouvoir dessiner des rectangles autour des différentes zones.

Maintenant que l'on connait les coordonnées de ses rectangles, nous pouvons effectuer des recherches directement dans l'image initiale avec nos moteurs de recherches. 

Nous avons décidé de dessiner les rectangles ainsi que de leur donnée un numéro pour que ce soit plus simple à comprendre lors de l'affichage des données. 

### Historique
Nous avons décidé de sauvegarder chacun des traitements d'image dans un json afin de garder une trace de ce qui a été travailler. Il s'agit d'un historique global et il serait intéressant de penser à un historique propre dans le futur du projet. 
Pour ce faire lorsque nous avons analysé un fichier, qu'il soit pdf ou image, avant de faire un retour visuel à l'utilisateur nous le faisons passer dans notre fonction de log. 
Celle-ci va prendre en paramètres, l'emplacement du fichier traiter ainsi que le contenu qui lui est attribuer. Elle va ensuite sauvegarder dans un fichier de log :
- La date
- L'heure
- Le nom du fichier 
- L'emplacement du fichier
- Le contenu du fichier

Nous avons ensuite créé une nouvelle page dans notre frontend qui va rechercher dans ce fichier de log, les différentes données d'historique et les afficher de manière correcte avec un peu de CSS.


## Sources :

- [1] Abdelwahed43. (n.d.). Handwritten Digits Recognizer 0-999 - Simple Model. Kaggle. Retrieved January 8, 2023, from https://www.kaggle.com/code/abdelwahed43/handwritten-digits-recognizer-0-999-simple-model
- [2] Le Dropout, c'est quoi ? (n.d.). Inside Machine Learning. Retrieved January 8, 2023, from https://inside-machinelearning.com/le-dropout-cest-quoi-deep-learning-explication-rapide/
- [3] Max pooling. (n.d.). Wikipedia. Retrieved January 8, 2023, from https://fr.wikipedia.org/wiki/Max_pooling
- [4] La couche de convolution. (n.d.). Inside Machine Learning. Retrieved January 8, 2023, from https://inside-machinelearning.com/cnn-couche-de-convolution/
- [5] Prototyper un réseau de neurones avec Keras. (2019, January). Les Dieux du Code. Retrieved January 8, 2023, from https://lesdieuxducode.com/blog/2019/1/prototyper-un-reseau-de-neurones-avec-keras
- [6] What is the role of Flatten in Keras? (n.d.). Stack Overflow. Retrieved January 8, 2023, from https://stackoverflow.com/questions/43237124/what-is-the-role-of-flatten-in-keras
- [7] Modifiez votre réseau de neurones en toute simplicité. (2017, April 11). Engineering Blog. Retrieved January 8, 2023, from https://blog.engineering.publicissapient.fr/2017/04/11/tensorflow-deep-learning-episode-3-modifiez-votre-reseau-de-neurones-en-toute-simplicite/
- [8] TP: Réseau de neurones convolutionnels. (n.d.). Pensee Artificielle. Retrieved January 8, 2023, from https://penseeartificielle.fr/tp-reseau-de-neurones-convolutifs/
- [9] A Complete Guide to Adam and RMSprop Optimizer. (n.d.). Analytics Vidhya. Retrieved January 8, 2023, from https://medium.com/analytics-vidhya/a-complete-guide-to-adam-and-rmsprop-optimizer-75f4502d83be
- [10] Convolutional Neural Networks (CNN) - Softmax & CrossEntropy. (n.d.). Super Data Science. Retrieved January 8, 2023, from https://www.superdatascience.com/blogs/convolutional-neural-networks-cnn-softmax-crossentropy
- [11] Keras API Reference - Metrics - Accuracy. (n.d.). Keras. Retrieved January 8, 2023, from https://keras.io/api/metrics/accuracy_metrics/#accuracy-class
- [12] torch.optim.lr_scheduler.ReduceLROnPlateau. (n.d.). PyTorch. Retrieved January 8, 2023, from https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.ReduceLROnPlateau.html
- [13] How to detect paragraphs in a text document image for a non-consistent text structure? (n.d.). Stack Overflow. Retrieved January 8, 2023, from https://stackoverflow.com/questions/57249273/how-to-detect-paragraphs-in-a-text-document-image-for-a-non-consistent-text-stru
- [14] Thresholding. (n.d.). OpenCV documentation. Retrieved January 8, 2023, from https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html
- [15] SMITH, Ray. An overview of the Tesseract OCR engine. In : Ninth international conference on document analysis and recognition (ICDAR 2007). IEEE, 2007. p. 629-633.
- [16] ROUSSEEUW, Peter J. et LEROY, Annick M. Robust regression and outlier detection. John wiley & sons, 2005.
- [17] Simple Cropper.js Demo (n.d). codepen.io Retrieved January 8, 2023, from https://codepen.io/blackjacques/pen/bqgNoa
- [18] Using files from web applications - Web APIs | MDN (n.d). developer.mozilla.org Retrieved January 8, 2023, from https://developer.mozilla.org/en-US/docs/Web/API/File_API/Using_files_from_web_applications#example_using_object_urls_to_display_images
- [19] PyMuPDF Documentation — PyMuPDF 1.21.1 documentation (n.d). pymupdf.readthedocs.io Retrieved January 8, 2023, from https://pymupdf.readthedocs.io/en/latest/toc.html
