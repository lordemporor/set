from random import randint
# Count, Fill, Color, and Shape will all have integer values representing the value. The following is a key for conversion
No_Fill = 1
Hash = 2
Solid = 3
Diamond = 1
Fish = 2
Pill = 3
Red = 1
Green = 2
Purple = 3
back_conversion = {
    "color": {
        1: "Red",
        2: "Green",
        3: "Purple"
    },
    "shape": {
        1: "Diamond",
        2: "Fish",
        3: "Pill"
    },
    "fill": {
        1: "No_Fill",
        2: "Hash",
        3: "Solid"
    }
}


class Card:
    def __init__(self, countInput, fillInput, colorInput, shapeInput, positionInput=None, cameraInfoInput=None):
        # Converting inputs to card variables. position and cameraInfo are optional, default to null
        self.count = countInput
        self.fill = fillInput
        self.shape = shapeInput
        self.color = colorInput
        self.position = positionInput
        self.cameraInfo = cameraInfoInput

    def getRandomCard():
        return Card(randint(1, 3), randint(1, 3), randint(1, 3), randint(1, 3))
