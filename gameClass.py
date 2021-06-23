from cardClass import *


class Game:
    allCards = []
    # static arrays for use by the findNeededCard function. clever method of referencing known values to look for unknown third value
    staticArrayReferenceCardPossibilities = [
        [1, 3, 2],
        [3, 2, 1],
        [2, 1, 3]
    ]

    # findMatch function: greater function for finding a match for cards. takes no inputs,
    # either outputs a tuple of three cards that are in allCards that are a match, or returns null if there are no matches
    def findMatch(self):
        global staticArrayReferenceCardPossibilities
        global allCards

        # findNeededCard function: given two cards that we know we have, will return a hypothetical card obj that would make a match
        def findNeededCard(cardA, cardB):
            neededCountValue = staticArrayReferenceCardPossibilities[cardA.count][cardB.count]
            neededShapeValue = staticArrayReferenceCardPossibilities[cardA.shape][cardB.shape]
            neededFillValue = staticArrayReferenceCardPossibilities[cardA.fill][cardB.fill]
            neededColorValue = staticArrayReferenceCardPossibilities[cardA.color][cardB.color]
            return Card(countInput=neededCountValue, shapeInput=neededShapeValue, fillInput=neededFillValue, colorInput=neededColorValue)

        # tellMeWhereCardIs function: given a hypothetical card obj, will search for it in allCards ignoring position and cameraInfo
        def tellMeWhereCardIs(needCardC):
            haveCardNeeded = None
            # Searches all cards, tests to see if the count, shape, fill, and color match
            for possibleCardMatch in allCards:
                if possibleCardMatch.count == needCardC.count and possibleCardMatch.shape == needCardC.shape and possibleCardMatch.fill == needCardC.fill and possibleCardMatch.color == needCardC.color:
                    haveCardNeeded = possibleCardMatch
                    break
            return haveCardNeeded

        pass
