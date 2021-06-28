import pygame
import math
from random import randint

from cardClass import *
from cardUIClass import *

### configs defs ###
# screen
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 960

# basic ui
RENDER_MAX_FPS = 30
BG_COLOR = (240, 117, 79)

# card layout
NUM_CARDS_PER_ROW = 3
CARD_MARGIN_X = 10
CARD_MARGIN_Y = 10

# typedefs
GAME_STATE_RUNNING = 1
GAME_STATE_USER_QUIT = 2

### computed defs ###
# screen
SCREEN_DIMENSIONS = (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_CENTER_X = SCREEN_WIDTH / 2
SCREEN_CENTER_Y = SCREEN_HEIGHT / 2
SCREEN_CENTER = (SCREEN_CENTER_X, SCREEN_CENTER_Y)

# card layout
TOTAL_CARD_WIDTH = CARD_WIDTH + (2 * CARD_MARGIN_X)
TOTAL_CARD_HEIGHT = CARD_HEIGHT + (2 * CARD_MARGIN_Y)


class GameUI:
    def __init__(self, game):
        self.screen = None
        self.game = game
        self.gameState = GAME_STATE_RUNNING
        self.lastRenderTick = 0
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

            if(pygame.time.get_ticks() - self.lastRenderTick > (1000 / RENDER_MAX_FPS)):
                self.lastRenderTick = pygame.time.get_ticks()
                self.render()

        pygame.quit()
        return

    def render(self):
        # clear screen
        self.screen.fill(BG_COLOR)

        # pygame.draw.rect(self.screen, CARD_COLOR, pygame.Rect(30, 30, CARD_HEIGHT, CARD_WIDTH), border_radius=CARD_BORDER_RADIUS)
        self.drawCardLayout()

        pygame.display.flip()

    def drawCardLayout(self):
        numCardRows = math.ceil(len(self.game.allCards) / NUM_CARDS_PER_ROW)
        numCardCols = NUM_CARDS_PER_ROW

        topLeftOfLayoutX = SCREEN_CENTER_X - ((numCardCols * TOTAL_CARD_WIDTH) / 2)
        topLeftOfLayoutY = SCREEN_CENTER_Y - ((numCardRows * TOTAL_CARD_HEIGHT) / 2)

        for card in self.game.allCards:
            cardRow = math.floor(card.position / NUM_CARDS_PER_ROW)
            cardCol = card.position % NUM_CARDS_PER_ROW

            cardX = topLeftOfLayoutX + (cardCol * TOTAL_CARD_WIDTH) + CARD_MARGIN_X
            cardY = topLeftOfLayoutY + (cardRow * TOTAL_CARD_HEIGHT) + CARD_MARGIN_Y

            cardDrawable = CardUI(self, card, cardX, cardY)
            cardDrawable.render()


    def drawCardOfTypeAt(self, cardType, pos):
        # draw card bg
        pass

    def randomColor(self):
        return (randint(0, 255), randint(0, 255), randint(0, 255))