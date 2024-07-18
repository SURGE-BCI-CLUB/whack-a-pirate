import csv
import pygame

class Scoreboard:
    def read_scores_from_csv(csv_file):
        scores = []
        with open(csv_file, newline='') as csvfile:
            score_reader = csv.reader(csvfile)
            for row in score_reader:
                if row:
                    scores.append((row[0], int(row[1])))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

    def display_scoreboard(screen, scores):
        # Adjust the size of the scoreboard screen for a bigger display
        scoreboard_screen = pygame.Surface((1000, 800))  # Increased size
        scoreboard_screen.fill((0, 0, 0))

        font = pygame.font.Font(None, 48)  # Increase font size for better visibility
        title_text = font.render("Scoreboard", True, (255, 255, 255))
        # Center the title on the scoreboard
        title_pos = title_text.get_rect(center=(scoreboard_screen.get_width() / 2, 75))
        scoreboard_screen.blit(title_text, title_pos)

        start_y = 150  # Start a bit lower to accommodate the larger title
        gap = 50  # Increase the gap between scores for better readability

        for nickname, score in scores[:10]:
            score_text = font.render(f"{nickname}: {score}", True, (255, 255, 255))
            # Center each score on the scoreboard
            score_pos = score_text.get_rect(center=(scoreboard_screen.get_width() / 2, start_y))
            scoreboard_screen.blit(score_text, score_pos)
            start_y += gap

        # Center the scoreboard screen on the main screen
        scoreboard_pos = scoreboard_screen.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(scoreboard_screen, scoreboard_pos)
        pygame.display.flip()