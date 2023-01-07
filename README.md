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

On va également utilisé le image data generator qui va nous permettre de nous entrainé avec des versions modifiés des images initiales. Il va les faire pivoter, zoomer mais également les shifter légèrement. 

Après avoir enregistrer ces paramètres on va pouvoir entrainer et essayer le modèle.

Lorsque l'on utilise les modèles il est important de faire en sorte de traiter les images d'input pour qu'elle correspondent à ce qui a été appris durnat l'entrainement. Il sera donc utile de les redimensionner et de modifier leur couleur. 

### CNN emmnist :


- Bounding box (LOGAN)
- Page de sortie (LOUIS)
- Historique (LOGAN)


## Sources :
https://www.kaggle.com/code/abdelwahed43/handwritten-digits-recognizer-0-999-simple-model
https://inside-machinelearning.com/le-dropout-cest-quoi-deep-learning-explication-rapide/
https://fr.wikipedia.org/wiki/Max_pooling
https://inside-machinelearning.com/cnn-couche-de-convolution/
https://lesdieuxducode.com/blog/2019/1/prototyper-un-reseau-de-neurones-avec-keras
https://stackoverflow.com/questions/43237124/what-is-the-role-of-flatten-in-keras
https://blog.engineering.publicissapient.fr/2017/04/11/tensorflow-deep-learning-episode-3-modifiez-votre-reseau-de-neurones-en-toute-simplicite/
https://penseeartificielle.fr/tp-reseau-de-neurones-convolutifs/
https://medium.com/analytics-vidhya/a-complete-guide-to-adam-and-rmsprop-optimizer-75f4502d83be
https://www.superdatascience.com/blogs/convolutional-neural-networks-cnn-softmax-crossentropy
https://keras.io/api/metrics/accuracy_metrics/#accuracy-class
https://pytorch.org/docs/stable/generated/torch.optim.lr_scheduler.ReduceLROnPlateau.html

