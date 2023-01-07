# AI_project
## Description du processus
- Explication de l'interface ( LOUIS )
- Traitement de l'entrée ( LOUIS )
- Choix du moteur d'OCR par l'utilisateur ( LOUIS )
- Description des moteurs :
- Tesseract ( LOUIS )
### CNN mnist :
Pour le moteur de reconnaissance de chiffre manuscrit, un CNN alimenté par le dataset de mnist semblait être la meilleure solution. Nous n'avons bien évidemment pas créer de toute pièce l'architecture du CNN mais nous nous sommes inspirés d'une solution trouvée sur Kaggle : 
https://www.kaggle.com/code/abdelwahed43/handwritten-digits-recognizer-0-999-simple-model

La première étape a été de préparée les données du dataset a être traitée :
- Séparation des labels et des données associées
- Normalisation des données 
- Reshapping des données 
- Transformation des labels en classe binaires ( 1 devient par exemple 0001 ), on les sépare en dix classe différentes. Une pour chacun des chiffre 
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

Conv2D : Cette couche va nous permettre de créer un kernel qui va etre convolué avec l'input pour donner l'output. Cette couche va nous permettre de nous focaliser sur les détails de l'image. 

MaxPool2D : Cette couche va nous permettre de diminuer le nombre de paramètre sans pour autant perdre de l'information. Elle va subdiser notre input en un grand nombre de sous groupe et ne garder pour ces sous groupe que la valeur maximale. 

DropOut : Cette étape permet d'éviter l'overfitting en désactiver de manière aléatoire certains neurones durant un epoch. Un dropout de 0.25 fait en sorte que les neurones on 25 pourcents de chance de se désactiver. 

Flatten : La couche flatten va nous permettre de préparer les données à être analysé par la couhe suivante. Elle va "applatir" les données c'est à dire que l'on va passer d'un input en plusieurs dimension à un output en une seule dimension. 

Dense : Elle prend une entrée et applique une modification à l'aide de sa fonction d'activation dans ce cas-ci relu afin de nous doonée un pourcentage de chance. Elle est connecté à tous les neurones de la zone précédente. 

Le créateur du CNN a décidé d'utiliser l'algorithme RMSprop comme optimiser, l'optimiser va nous permettre de diminuer la loss en modifier le CNN. Rmsprop est un optimiser qui va utiliser un taux d'apprentissage adaptatif. Il utilise une fonction de loss de type cross-entropie, celle mesure l'écart entre la distribution de probabilité prévue du modèle et celle réelle attendue. Il utilise également des métrics "Accuracy", qui ont un rôle semblable à la loss, qui permettent d'évaluer le système. Dans ce cas-ci, l'évaluation ce déroule en regardant la fréquence à laquelle les prédictions du modèle correspondent aux labels réels. 

On va également utiler la fonction ReduceLROnPlateau qui va nous permettre de réduire le taux d'apprentissage du modèle lorsque celui-ci cesse de s'améliorer. Le taux d'apprentisse étant la vitesse à laquelle se met à jour le modèle durant l'entrainement. 

Pour éviter l'overfitting on a décidé de ne faire que 3 epoch, en ayant fait des tests au delà le modèle devient bien moins compétant pour les figures qu'il n'a pas eu dans son dataset. Il est trop spécialisé. 

On utilise le imageDataGenerator qui va nous permettre de nous entrainé avec des versions modifiés des images initiales. Il va les faire pivoter, zoomer mais également les shifter légèrement. 

Après avoir enregistrer ces paramètres on va pouvoir entrainer et essayer le modèle.

Lorsque l'on utilise les modèles il est important de faire en sorte de traiter les images d'input pour qu'elle correspondent à ce qui a été appris durnat l'entrainement. Il sera donc utile de les redimensionner et de modifier leur couleur. 

### CNN emnist :
Pour le moteur de reconnaissance de lettre manuscrite, un CNN alimenté par le dataset de emnist semblait être la meilleure solution. Nous n'avons bien évidemment pas créer de toute pièce l'architecture du CNN mais nous nous sommes inspirés d'une autre solution trouvée sur Kaggle : 
https://www.kaggle.com/code/achintyatripathi/emnist-letter-dataset-97-9-acc-val-acc-91-78
Malheureusement il est beaucoup moins performant que celui utilisé précédement pour mnist.

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

Nous utilisons un optimiser RMSprop, avec une fonction de loss categorical_crossentropy et les mêmes metrics que pour mnist. 

On a mis en place de l'earlystoping et ReduceLROnPlateau, on a fait 5 epoch.

L'earlystopping va être utilisé pour éviter l'overfitting, il arrête l'apprentissage quand il s'apperçoit que le nombre d'erreur sur les datas de validation augmententent alors qu'ils descendent sur les datas de test. Lorsque c'est le cas le modèle commence à overfitter. 

On a ensuite entrainer le modèle et on l'a tester. Il est moins perfomant que mnist, tout d'abord le modèle comporte beaucoup moins de couche et pas de générateur d'images. De plus le sujet de emnist est beaucoup moins en vogue sur internet et nous n'avons pas su trouver de modèle plus efficace. 

### Bounding Box :
Pour la détection automatique de texte sur la page nous avons réutilisé un des principes de traitement d'image que nous avions vu en cours lors de l'année précédente. Il s'agit non pas de détection de texte mais plus de détection de "zone de couleur plus foncée", ce qui limite notre cas d'utilisation à de l'écriture blanc sur noir ou du moins foncé sur clair. 

Il va falloir traité l'image afin de détecter les zones de textes:
- On va tout d'abord lire l'image avec OpenCV
- On va ensuite la transformer en nuance de gris
- On ajoute un flou gaussien pour que les différentes zonnes soit moins distinctes et que l'on puisse trouver des mots/phrase/paragraphes entiers. 
-  Vient l'étape du treshold qui va nous permettre de "binariser" chacun des pixels de l'image, ceux-ci deviendront blanc ou noir selon l'intensité du gris
-  on va ensuite dilaté les différentes taches pour évité d'encadrer lettre par lettre. 
-  On va ensuite pouvoir dessiner des rectangles autour des différentes taches.

Maintenant que l'on connait les coordonnées de ses rectangles, nous pouvons faire des recherches directement dans l'image initiale avec nos moteurs de recherches. 

Nous avons décidé de dessiner les rectangles ainsi que de leur donnée un numéro pour que ce soit plus simple à comprendre lors de l'affichage des données. 

- Page de sortie (LOUIS)

### Historique
NOus avons décidé de sauvegarder chacun des traitements d'image dans un json afin de garder une trace de ce qui a été travailler. Il s'agit d'un historique global et il serait intéressant de penser à un historique propre dans le futur du projet. 
Pour ce faire lorsque nous avons analysé un fichier, qu'il soit pdf ou image, avant de faire un retour visuel à l'utilisateur nous le faison passer dans notre fonciton de log. 
Celle-ci va prendre en paramètres, l'emplacement du fichier traiter ainsi que le contenu qui lui est attribuer. Elle va ensuite sauvegarder dans un fichier de log :
- La date
- L'heure
- Le nom du fichier 
- L'emplacement du fichier
- Le contenu du fichier

Nous avons ensuite créer une nouvelle page dans notre frontend qui va rechercher dans ce fichier de log, les différentes données d'historique et les afficher de manière correcte avec un peu de CSS.


## Sources :
- https://www.kaggle.com/code/abdelwahed43/handwritten-digits-recognizer-0-999-simple-model
- https://inside-machinelearning.com/le-dropout-cest-quoi-deep-learning-explication-rapide/
- https://fr.wikipedia.org/wiki/Max_pooling
- https://inside-machinelearning.com/cnn-couche-de-convolution/
- https://lesdieuxducode.com/blog/2019/1/prototyper-un-reseau-de-neurones-avec-keras
- https://stackoverflow.com/questions/43237124/what-is-the-role-of-flatten-in-keras
- https://blog.engineering.publicissapient.fr/2017/04/11/tensorflow-deep-learning-episode-3-modifiez-votre-reseau-de-neurones-en-toute-simplicite/
- https://penseeartificielle.fr/tp-reseau-de-neurones-convolutifs/
- https://medium.com/analytics-vidhya/a-complete-guide-to-adam-and-rmsprop-optimizer-75f4502d83be
- https://www.superdatascience.com/blogs/convolutional-neural-networks-cnn-softmax-crossentropy
- https://keras.io/api/metrics/accuracy_metrics/#accuracy-class
- https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.ReduceLROnPlateau.html
- https://stackoverflow.com/questions/57249273/how-to-detect-paragraphs-in-a-text-document-image-for-a-non-consistent-text-stru
- https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html
