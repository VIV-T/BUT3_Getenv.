from deepface import DeepFace
import numpy as np
from PIL import Image

# pour modifier la variable d'environnement
import os

# Modifier/Creer une variable d'environnement (recommandé par python lors de l'execution)
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'


def compte_visages_img(img : Image) :
    # conversion de l'image en un tableau numpy analisable par DeepFace
    image_np = np.array(img)
    visages = DeepFace.extract_faces(image_np, detector_backend = 'opencv', enforce_detection = False)

    nb_visages = int(len(visages))
    return nb_visages


