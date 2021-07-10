import os
import pygame


def readSprites(resolution):
    screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)
    tempImages = {"images_alpha":{},"images_nostretch":{}}
    images ={}
    imagekeys = []
    dirPath = "sprites"
    print("Another hello from Bohemian.")
    for file in sorted(os.listdir(dirPath)):
        if file.endswith("_A"):
            tempImages["images_alpha"][int(file[:4])] = (pygame.image.load(os.path.join("sprites",file)))
            imagekeys.append(int(file[:4]))
        elif file.endswith("_nostretch"):
            tempImages["images_nostretch"][int(file[:4])] = (pygame.image.load(os.path.join("sprites",file)))
            imagekeys.append(int(file[:4]))
        else:
            images[int(file[:4])] = (pygame.image.load(os.path.join("sprites",file)))
            imagekeys.append(int(file[:4]))

    for number in imagekeys:
        if number in images:
            images[number] = pygame.transform.scale(images[number],(32,32))
            images[number] = images[number].convert()
        elif number in tempImages["images_alpha"]:
            tempImages["images_alpha"][number] = pygame.transform.scale(tempImages["images_alpha"][number], (32, 32))
            images[number] = tempImages["images_alpha"][number].convert_alpha()
        elif number in tempImages["images_nostretch"]:
            images[number] = tempImages["images_nostretch"][number].convert_alpha()
    return images