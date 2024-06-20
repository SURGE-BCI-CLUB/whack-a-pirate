import pygame


class Button:
    def __init__(self, text, x, y):
        self.text = text
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, 36)
        self.text_surf = self.font.render(self.text, True, (255, 255, 255))
        self.rect = self.text_surf.get_rect(center=(self.x, self.y))

    def draw(self, surface):
        surface.blit(self.text_surf, self.rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)