import pygame
import pygame.gfxdraw
import math

def drawAARect(surface, rect, color, width=0, borderRadius=0, bgColor=(255, 255, 255)):
    # fill

    if borderRadius <= 0:
        return

    rect.x = int(rect.x)
    rect.y = int(rect.y)
    borderRadius = int(borderRadius)

    # rounded border
    pygame.gfxdraw.aacircle(surface, rect.x + borderRadius, rect.y + borderRadius, borderRadius, color)
    pygame.gfxdraw.aacircle(surface, rect.x + rect.w - borderRadius - 1, rect.y + borderRadius, borderRadius, color)
    pygame.gfxdraw.aacircle(surface, rect.x + rect.w - borderRadius - 1, rect.y + rect.h - borderRadius - 1, borderRadius, color)
    pygame.gfxdraw.aacircle(surface, rect.x + borderRadius, rect.y + rect.h - borderRadius - 1, borderRadius, color)

    pygame.gfxdraw.filled_circle(surface, rect.x + borderRadius, rect.y + borderRadius, borderRadius, color)
    pygame.gfxdraw.filled_circle(surface, rect.x + rect.w - borderRadius - 1, rect.y + borderRadius, borderRadius, color)
    pygame.gfxdraw.filled_circle(surface, rect.x + rect.w - borderRadius - 1, rect.y + rect.h - borderRadius - 1, borderRadius, color)
    pygame.gfxdraw.filled_circle(surface, rect.x + borderRadius, rect.y + rect.h - borderRadius - 1, borderRadius, color)

    # main fill
    tallRect = pygame.Rect(rect)
    tallRect.w -= 2 * borderRadius
    tallRect.center = rect.center
    pygame.draw.rect(surface, color, tallRect)

    #wideRect = pygame.Rect(rect)
    #wideRect.h -= 2 * borderRadius
    #wideRect.center = rect.center
    #pygame.draw.rect(surface, color, wideRect)

    # left and ride side fills
    thinRect = pygame.Rect(rect.x, rect.y + borderRadius, borderRadius, rect.h - (2 * borderRadius))
    pygame.draw.rect(surface, color, thinRect)
    thinRect.x = rect.x + rect.w - borderRadius
    pygame.draw.rect(surface, color, thinRect)

    if width is not 0:
        scaledRect = rect.inflate(-width * 2, -width * 2)
        drawAARect(surface, scaledRect, bgColor, 0, (scaledRect.w / rect.w) * borderRadius)

def drawAAPolygon(surface, points, color, width=0, scaleRect=(0, 0, 0, 0), bgColor=(255, 255, 255)):
    pygame.gfxdraw.aapolygon(surface, points, color)
    pygame.gfxdraw.filled_polygon(surface, points, color)

    if width is not 0:
        scaleRect = pygame.Rect(scaleRect)
        #scaleFactor = (1 - (width / scaleRect.width), 1 - (width / scaleRect.height))
        scaleFactor = (1 - ((width*2) / scaleRect.width), 1 - ((width*2) / scaleRect.width))
        transformOrigin = (scaleRect.x + (scaleRect.width / 2), scaleRect.y + (scaleRect.height / 2))
        scaledPolygonPoints = scalePolygon(points, scaleFactor, transformOrigin)
        drawAAPolygon(surface, scaledPolygonPoints, bgColor)

def scalePolygon(polyPoints, scale, transformOrigin):
    scaleX = scale[0]
    scaleY = scale[1]
    transformOriginX = transformOrigin[0]
    transformOriginY = transformOrigin[1]
    initTranslatedPoints = [(ptX - transformOriginX, ptY - transformOriginY) for (ptX, ptY) in polyPoints]
    scaledPoints = [(ptX * scaleX, ptY * scaleY) for (ptX, ptY) in initTranslatedPoints]
    finalTranslatedPoints = [(ptX + transformOriginX, ptY + transformOriginY) for (ptX, ptY) in scaledPoints]

    return finalTranslatedPoints

def drawAALine(surface, ptA, ptB, color, thickness):
    #fudge it
    thickness = thickness - 1

    centerOfLine = ((ptA[0] + ptB[0]) / 2, (ptA[1] + ptB[1]) / 2)

    length = (((ptA[0] - ptB[0]) ** 2) + ((ptA[1] - ptB[1]) ** 2)) ** .5
    angle = math.atan2(ptA[1] - ptB[1], ptA[0] - ptB[0])

    ul = (centerOfLine[0] + (length / 2.) * math.cos(angle) - (thickness / 2.) * math.sin(angle),
          centerOfLine[1] + (thickness / 2.) * math.cos(angle) + (length / 2.) * math.sin(angle))
    ur = (centerOfLine[0] - (length / 2.) * math.cos(angle) - (thickness / 2.) * math.sin(angle),
          centerOfLine[1] + (thickness / 2.) * math.cos(angle) - (length / 2.) * math.sin(angle))
    bl = (centerOfLine[0] + (length / 2.) * math.cos(angle) + (thickness / 2.) * math.sin(angle),
          centerOfLine[1] - (thickness / 2.) * math.cos(angle) + (length / 2.) * math.sin(angle))
    br = (centerOfLine[0] - (length / 2.) * math.cos(angle) + (thickness / 2.) * math.sin(angle),
          centerOfLine[1] - (thickness / 2.) * math.cos(angle) - (length / 2.) * math.sin(angle))

    drawAAPolygon(surface, (ul, ur, br, bl), color)

def drawAALines(surface, pts, color, thickness):
    for i in range(len(pts)):
        if i == len(pts) - 1:
            drawAALine(surface, pts[i], pts[0], color, thickness)
        else:
            drawAALine(surface, pts[i], pts[i + 1], color, thickness)
