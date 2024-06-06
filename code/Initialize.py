import pygame

class Initialize:

    @staticmethod
    def populateImgArr(filePath, imgArr):
        tempImg = pygame.image.load(filePath)
        imgArr.append(tempImg)