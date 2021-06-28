import pygame
import pygame.gfxdraw
from gameUIClass import *
from cardClass import *
from uiUtils import *

### config defs ###
# card
CARD_WIDTH = 250
CARD_HEIGHT = 160
CARD_BORDER_RADIUS = 4
CARD_COLOR = (255, 255, 255)
CARD_HOVER_COLOR = (240, 240, 240)
CARD_CLICK_COLOR = (230, 230, 230)

# shapes layout
CARD_SHAPE_MARGIN_X = 10

# shapes
CARD_SHAPE_WIDTH = 50
CARD_SHAPE_HEIGHT = 100
CARD_SHAPE_BORDER_WIDTH = 4
CARD_SHAPE_HASH_LINE_WIDTH = 1
CARD_SHAPE_HASH_LINE_SPACING = 7

# pill
PILL_SHAPE_WIDTH = CARD_SHAPE_WIDTH
PILL_SHAPE_HEIGHT = CARD_SHAPE_HEIGHT

# diamond
DIAMOND_SHAPE_WIDTH = CARD_SHAPE_WIDTH
DIAMOND_SHAPE_HEIGHT = CARD_SHAPE_HEIGHT

# fish
# hardcoded points, so must scale
FISH_SHAPE_WIDTH = 50
FISH_SHAPE_HEIGHT = 100
FISH_SHAPE_POINTS = (
    (18, 1),
    (23, 1),
    (29, 3),
    (35, 6),
    (41, 11),
    (43, 15),
    (45, 22),
    (45, 31),
    (44, 39),
    (41, 46),
    (38, 54),
    (37, 58),
    (37, 65),
    (39, 72),
    (42, 79),
    (47, 85),
    (48, 87),
    (48, 90),
    (46, 93), # next page
    (43, 95),
    (38, 97),
    (29, 97),
    (25, 96),
    (19, 93),
    (14, 89), # makes it kinda fat?
    (11, 85),
    (7, 76),
    (5, 67),
    (6, 58),
    (7, 51),
    (9, 47),
    (11, 41),
    (11, 32),
    (9, 26),
    (6, 20),
    (2, 13),
    (2, 8),
    (5, 3),
    (13, 1)
)

# shape colors
CARD_SHAPE_COLOR = {
    Red: (207, 33, 33), #227, 62, 50
    Green: (60, 163, 26),
    Purple: (71, 10, 74)
}

### computed defs ###
# shape layout
TOTAL_CARD_SHAPE_WIDTH = CARD_SHAPE_WIDTH + (CARD_SHAPE_MARGIN_X * 2)
TOTAL_CARD_SHAPE_HEIGHT = CARD_SHAPE_HEIGHT

# shapes
CARD_SHAPE_HASH_WHITEOUT_WIDTH = CARD_SHAPE_HASH_LINE_SPACING
CARD_SHAPE_HASH_WHITEOUT_SPACING = CARD_SHAPE_HASH_LINE_WIDTH
CARD_SHAPE_HASH_TOTAL_WHITEOUT_WIDTH = CARD_SHAPE_HASH_WHITEOUT_WIDTH + CARD_SHAPE_HASH_WHITEOUT_SPACING

# pill
PILL_SHAPE_RADIUS = (PILL_SHAPE_WIDTH - 1) / 2

# diamond
DIAMOND_SHAPE_POINTS = (
    (DIAMOND_SHAPE_WIDTH / 2, 0),
    (DIAMOND_SHAPE_WIDTH, DIAMOND_SHAPE_HEIGHT / 2),
    (DIAMOND_SHAPE_WIDTH / 2, DIAMOND_SHAPE_HEIGHT),
    (0, DIAMOND_SHAPE_HEIGHT / 2)
)

# fish

class CardUI:
    def __init__(self, gameUI, cardType, x, y):
        self.gameUI = gameUI
        self.cardType = cardType
        self.setXY(x, y)
        return

    def setPos(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.updateBounding()

    def setXY(self, x, y):
        self.x = x
        self.y = y
        self.updateBounding()

    def updateBounding(self):
        self.boundingRect = pygame.Rect(self.x, self.y, CARD_WIDTH, CARD_HEIGHT)

    def isMouseHovering(self):
        return self.boundingRect.collidepoint(pygame.mouse.get_pos())

    def isMouseClicking(self):
        return pygame.mouse.get_pressed()[0] and self.isMouseHovering()

    def render(self):
        self.curBgColor = CARD_COLOR
        if self.isMouseHovering():
            self.curBgColor = CARD_CLICK_COLOR if self.isMouseClicking() else CARD_HOVER_COLOR

        # draw antialiased bg
        self.drawCardBg()

        # convert to regular color
        cardColorRGB = CARD_SHAPE_COLOR[self.cardType.color]

        # draw shapes
        cardCenterX = self.x + (CARD_WIDTH / 2)
        cardCenterY = self.y + (CARD_HEIGHT / 2)

        topLeftOfShapeLayoutX = cardCenterX - ((TOTAL_CARD_SHAPE_WIDTH * self.cardType.count) / 2)
        topLeftOfShapeLayoutY = cardCenterY - (TOTAL_CARD_SHAPE_HEIGHT / 2)

        for shapeIndex in range(self.cardType.count):
            shapeX = topLeftOfShapeLayoutX + (shapeIndex * TOTAL_CARD_SHAPE_WIDTH) + CARD_SHAPE_MARGIN_X
            shapeY = topLeftOfShapeLayoutY

            if self.cardType.shape is Pill:
                self.drawPillShape((shapeX, shapeY), 1, cardColorRGB, self.cardType.fill)
            elif self.cardType.shape is Diamond:
                self.drawDiamondShape((shapeX, shapeY), 1, cardColorRGB, self.cardType.fill)
            elif self.cardType.shape is Fish:
                self.drawFishShape((shapeX, shapeY), 1, cardColorRGB, self.cardType.fill)
            else:
                print(f"Bad card shape type {self.cardType.shape}!")
        return

    # utils
    def drawCardBg(self):
        #pygame.draw.rect(self.gameUI.screen, renderCardColor, self.boundingRect, border_radius=CARD_BORDER_RADIUS)
        drawAARect(self.gameUI.screen, self.boundingRect, self.curBgColor, 0, CARD_BORDER_RADIUS)

    def drawPillShape(self, pos, scale, color, fill):
        if fill is No_Fill:
            drawAARect(self.gameUI.screen, pygame.Rect(pos[0], pos[1], PILL_SHAPE_WIDTH * scale, PILL_SHAPE_HEIGHT * scale), color, CARD_SHAPE_BORDER_WIDTH, PILL_SHAPE_RADIUS * scale, self.curBgColor)
        else:
            drawAARect(self.gameUI.screen, pygame.Rect(pos[0], pos[1], PILL_SHAPE_WIDTH * scale, PILL_SHAPE_HEIGHT * scale), color, 0, PILL_SHAPE_RADIUS * scale)

            if fill is Hash:
                # white out the shape to make thin lines
                self.drawHashedShapeLineMask(pos, scale, self.curBgColor)

                # add thicker border again
                pillCenterX = pos[0] + PILL_SHAPE_RADIUS
                topPillCenterY = pos[1] + PILL_SHAPE_RADIUS
                bottomPillCenterY = pos[1] + PILL_SHAPE_HEIGHT - PILL_SHAPE_RADIUS
                #pygame.draw.arc(surface, color, topPillCenterY, pillCenterX, PILL_SHAPE_RADIUS, 0, 180)
                topSemicircleRect = pygame.Rect((pos[0], pos[1], PILL_SHAPE_WIDTH, PILL_SHAPE_RADIUS * 2))
                pygame.draw.arc(self.gameUI.screen, color, topSemicircleRect, 0, math.pi, CARD_SHAPE_BORDER_WIDTH)

                bottomSemicircleRect = pygame.Rect((pos[0], pos[1] + PILL_SHAPE_HEIGHT - (PILL_SHAPE_RADIUS * 2), PILL_SHAPE_WIDTH, PILL_SHAPE_RADIUS * 2))
                pygame.draw.arc(self.gameUI.screen, color, bottomSemicircleRect, math.pi, 0, CARD_SHAPE_BORDER_WIDTH)

                drawAALine(self.gameUI.screen, (pos[0] + (CARD_SHAPE_BORDER_WIDTH / 2), pos[1] + PILL_SHAPE_RADIUS), (pos[0] + (CARD_SHAPE_BORDER_WIDTH / 2), pos[1] + PILL_SHAPE_HEIGHT - PILL_SHAPE_RADIUS), color, CARD_SHAPE_BORDER_WIDTH)
                drawAALine(self.gameUI.screen, (pos[0] + PILL_SHAPE_WIDTH - (CARD_SHAPE_BORDER_WIDTH / 2), pos[1] + PILL_SHAPE_RADIUS), (pos[0] + PILL_SHAPE_WIDTH - (CARD_SHAPE_BORDER_WIDTH / 2), pos[1] + PILL_SHAPE_HEIGHT - PILL_SHAPE_RADIUS), color, CARD_SHAPE_BORDER_WIDTH)

    def drawDiamondShape(self, pos, scale, color, fill):
        diamondPointsScaled = [(ptX * scale, ptY * scale) for (ptX, ptY) in DIAMOND_SHAPE_POINTS]
        diamondPointsActual = [(ptX + pos[0], ptY + pos[1]) for (ptX, ptY) in diamondPointsScaled]
        polyBoundingBox = (pos[0], pos[1], DIAMOND_SHAPE_WIDTH, DIAMOND_SHAPE_HEIGHT)

        if fill is No_Fill:
            drawAAPolygon(self.gameUI.screen, diamondPointsActual, color, CARD_SHAPE_BORDER_WIDTH, polyBoundingBox, self.curBgColor)
        else:
            drawAAPolygon(self.gameUI.screen, diamondPointsActual, color)

            if fill is Hash:
                self.drawHashedShapeLineMask(pos, scale, self.curBgColor)

                drawAALines(self.gameUI.screen, diamondPointsActual, color, CARD_SHAPE_BORDER_WIDTH)

    def drawFishShape(self, pos, scale, color, fill):
        fishPointsScaled = [(ptX * scale, ptY * scale) for (ptX, ptY) in FISH_SHAPE_POINTS]
        fishPointsActual = [(ptX + pos[0], ptY + pos[1]) for (ptX, ptY) in fishPointsScaled]
        polyBoundingBox = (pos[0], pos[1], FISH_SHAPE_WIDTH, FISH_SHAPE_HEIGHT)

        if fill is No_Fill:
            pygame.draw.polygon(self.gameUI.screen, color, fishPointsActual, CARD_SHAPE_BORDER_WIDTH)
        else:
            drawAAPolygon(self.gameUI.screen, fishPointsActual, color)

            if fill is Hash:
                self.drawHashedShapeLineMask(pos, scale, self.curBgColor)
                drawAALines(self.gameUI.screen, fishPointsActual, color, CARD_SHAPE_BORDER_WIDTH)


    def drawHashedShapeLineMask(self, pos, scale, bgColor):
        drawBoundingBox = pygame.Rect((pos[0], pos[1], CARD_SHAPE_WIDTH * scale, CARD_SHAPE_HEIGHT * scale))

        for lineY in range(drawBoundingBox.top, drawBoundingBox.bottom, CARD_SHAPE_HASH_TOTAL_WHITEOUT_WIDTH):
            pygame.draw.rect(self.gameUI.screen, bgColor, (drawBoundingBox.x, lineY, drawBoundingBox.width, CARD_SHAPE_HASH_WHITEOUT_WIDTH))