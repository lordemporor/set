import pygame

# configs
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# typedefs
GAME_STATE_RUNNING = 1
GAME_STATE_USER_QUIT = 2


class GameUI:
    def __init__(self):
        self.screen = None
        self.gameState = GAME_STATE_RUNNING
        return

    def init(self):
        # init game library
        pygame.init()

        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.gameState = GAME_STATE_RUNNING

        # main loop
        while self.gameState is GAME_STATE_RUNNING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameState = GAME_STATE_USER_QUIT

            # clear screen
            self.screen.fill(235, 95, 52)

            pygame.draw.rect(self.screen, (0, 0, 255), (250, 250), 75)

            pygame.display.flip()

        pygame.quit()
        return
