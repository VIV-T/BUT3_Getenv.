from traitement_DeepFace import compte_visages_img
from PIL import Image

### Tests :
if __name__=="__main__" :
    # 1 personne
    img_1_personne = Image.open("1_personne.jpg")
    nb_visage = compte_visages_img(img_1_personne)
    print(f"{nb_visage} ont été trouvés sur l'image : 1_personne.jpg")

    # 2 personnes
    img_2_personnes = Image.open("2_personnes.jpg")
    nb_visage = compte_visages_img(img_2_personnes)
    print(f"{nb_visage} ont été trouvés sur l'image : 2_personnes.jpg")

    # 3 personnes
    img_3_personnes = Image.open("3_personnes.jpg")
    nb_visage = compte_visages_img(img_3_personnes)
    print(f"{nb_visage} ont été trouvés sur l'image : 3_personne.jpg")