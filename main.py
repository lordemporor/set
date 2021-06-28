from cardClass import *
from gameClass import *
from gameUIClass import *

game = Game()
gameUI = GameUI(game)

testCards = [
    Card(3, No_Fill, Red, Pill, 0),
    Card(1, Solid, Purple, Pill, 1),
    Card(2, Hash, Green, Diamond, 2), #No Fill
    Card(3, No_Fill, Purple, Diamond, 3),
    Card(3, No_Fill, Green, Pill, 4),
    Card(2, No_Fill, Purple, Pill, 5),
    Card(2, Hash, Green, Pill, 6),
    Card(1, Hash, Red, Pill, 7),
    Card(1, Hash, Purple, Fish, 8), #No Fill
    Card(1, Hash, Purple, Pill, 9),
    Card(1, Hash, Green, Pill, 10),
    Card(2, Solid, Purple, Pill, 11)
]

game.allCards = testCards

gameUI.init()