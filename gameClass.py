from cardClass import *

class Game:
    def __init__(self):
        self.allCards = []
        # static arrays for use by the findNeededCard function. clever method of referencing known values to look for unknown third value
        self.staticArrayReferenceCardPossibilities = [
            [1, 3, 2],
            [3, 2, 1],
            [2, 1, 3]
        ]

    # findMatch function: greater function for finding a match for cards. takes no inputs,
    # either outputs a tuple of three cards that are in allCards that are a match, or returns null if there are no matches
    def findMatch(self):
        # findNeededCard function: given two cards that we know we have, will return a hypothetical card obj that would make a match
        def findNeededCard(cardA, cardB):
            neededCountValue = self.staticArrayReferenceCardPossibilities[cardA.count - 1][cardB.count - 1]
            neededShapeValue = self.staticArrayReferenceCardPossibilities[cardA.shape - 1][cardB.shape - 1]
            neededFillValue = self.staticArrayReferenceCardPossibilities[cardA.fill - 1][cardB.fill - 1]
            neededColorValue = self.staticArrayReferenceCardPossibilities[cardA.color - 1][cardB.color - 1]
            return Card(countInput=neededCountValue, shapeInput=neededShapeValue, fillInput=neededFillValue, colorInput=neededColorValue)

        # tellMeWhereCardIs function: given a hypothetical card obj, will search for it in allCards ignoring position and cameraInfo
        def tellMeWhereCardIs(needCardC):
            haveCardNeeded = None
            # Searches all cards, tests to see if the count, shape, fill, and color match
            for possibleCardMatch in self.allCards:
                if possibleCardMatch.count == needCardC.count and possibleCardMatch.shape == needCardC.shape and possibleCardMatch.fill == needCardC.fill and possibleCardMatch.color == needCardC.color:
                    haveCardNeeded = possibleCardMatch
                    break
            return haveCardNeeded

        # center of findMatch, searches through each card in allCards. this first card is called cardA
        # within allCards, it will search through each card in allCards after cardA such that no search is repeated, this is cardB
        # once we have cardA and cardB, we can use our functions to look for the final card (cardC)
        # if cardC exists then we will return it as an obj with position to match whats in allCards, otherwise return null
        for cardAIndex in range(len(self.allCards) - 1):
            for cardBIndex in range(cardAIndex+1, len(self.allCards) - 1):
                neededCardC = findNeededCard(self.allCards[cardAIndex], self.allCards[cardBIndex])
                foundNeededCardC = tellMeWhereCardIs(neededCardC)
                if foundNeededCardC:
                    return self.allCards[cardAIndex], self.allCards[cardBIndex], foundNeededCardC
        return None

    # addCards function: sticks the entered cards into allCards. if a card is already in that position, delete it
    def addCards(self, cardsToAdd):
        cardPositions = {}
        for cardForPositioning in self.allCards:
            cardPositions.update({int(cardForPositioning.position): cardForPositioning})
        try:
            for newCardForPositioning in cardsToAdd:
                cardPositions.update({int(newCardForPositioning.position): newCardForPositioning})
        except TypeError:
            int("You need to give the cards position values!")
        self.allCards = cardPositions.values()
        return True

    # removeCards function: removes all entered cards
    def removeCards(self, cardObjs):
        for cardToRemove in cardObjs:
            self.allCards.remove(cardToRemove)
        return True

    # resetCards function: empties out allCards. if randomSet is set to True, it will randomize the cards in allCards
    def resetCards(self, randomSet=False):
        self.allCards = []
        if randomSet:
            for newRandomCard in range(12):
                self.allCards.append(Card(randint(1, 3), randint(1, 3), randint(1, 3), randint(1, 3), newRandomCard))
        return True

    # getCards function: returns allCards
    def getCards(self):
        return self.allCards

    # fitCards function: re-organizes the positions of cards in allCards. if cards are entered,
    # it will try to fit them into their position. if somethings already there, the new card goes to the closest available position to 0
    def fitCards(self, newCardsToFit):
        # sortByKey function: sorts allCards by position for use later in fitCards
        def sortByKey(value):
            reversedCardPositionsDict = dict((v, k) for k, v in cardPositions.items())
            return reversedCardPositionsDict[value]
        cardPositions = {}
        bumpedCards = []
        # Tries to fit all cards currently in allCards into positions in case there are duplicates.
        # If a card tries to go into a place that another card is already at, it goes to the bumpedCards list
        for cardToFit in self.allCards:
            if cardToFit.position in cardPositions:
                bumpedCards.append(cardToFit)
            else:
                cardPositions.update({cardToFit.position: cardToFit})
        # Tries to fit the new entered cards into positions. if it can't, they go into bumpedCards
        for newCardToFit in newCardsToFit:
            if newCardToFit.position in cardPositions:
                bumpedCards.append(newCardToFit)
            else:
                cardPositions.update({newCardToFit.position: newCardToFit})
        # Searches through the remains available positions (including ones at the end) and tries to fit remaining cards in bumpedCards
        bumpAvailableSearchIndex = 0
        while bumpedCards:
            if bumpAvailableSearchIndex not in cardPositions:
                bumpedCards[0].position = bumpAvailableSearchIndex
                cardPositions.update({bumpAvailableSearchIndex: bumpedCards[0]})
                bumpedCards.pop(0)
            bumpAvailableSearchIndex += 1
        sortCardPositionValues = list(cardPositions.values())
        sortCardPositionValues.sort(key=sortByKey)
        self.allCards = sortCardPositionValues
        return True
