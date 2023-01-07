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
- On transforme 10% des données d'entrainement en données de test

On va ensuite définir les différentes couches de notre model : 




- CNN emmnist (LOGAN)
- Bounding box (LOGAN)
- Page de sortie (LOUIS)
- Historique (LOGAN)


## Sources :
https://www.kaggle.com/code/abdelwahed43/handwritten-digits-recognizer-0-999-simple-model

