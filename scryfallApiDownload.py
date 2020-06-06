import json
import requests as req
import os

allCardsJsonPath = "data/mtgUniqueArtwork.json"
strippedDataJsonPath = "data/strippedData.json"

def getAllImageUris():
    allCardsFile = open(allCardsJsonPath, "rb")
    allCardsJson = json.load(allCardsFile)
    allCardsFile.close()

    allCardsStripped = {}

    #print(allCardsJson[0])


    for card in allCardsJson:
        if card['layout'] == 'normal':
            allCardsStripped[card['set']+'_'+card['name']+'_'+card['lang']] = { 'image_uri' :  card['image_uris']['normal'] }

    print(allCardsStripped)

    with open(strippedDataJsonPath, 'w') as fp:
        json.dump(allCardsStripped, fp)


def downloadImages():
    allCardsStrippedFile = open(strippedDataJsonPath, "rb")
    allCardsStrippedJson = json.load(allCardsStrippedFile)
    allCardsStrippedFile.close()



    for key in list(allCardsStrippedJson)[0:1000]:
        print("Downloading", key, "from", allCardsStrippedJson[key]['image_uri'])

        imageRequest = req.get(allCardsStrippedJson[key]['image_uri'])
        imageRequest.raise_for_status()

        img_file = "images/scryfall/"+key+".jpg"
        with open(os.path.join(os.getcwd(), img_file), 'wb') as f:
            f.write(imageRequest.content)


#getAllImageUris()
#downloadImages()