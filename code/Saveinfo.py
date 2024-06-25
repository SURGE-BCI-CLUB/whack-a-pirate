import pygame
import sys 
import csv

class Saveinfo:
    @staticmethod

    def save_user_score_to_csv(nickname, score):
        with open('user_scores.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([nickname, score])