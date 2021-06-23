# Count, Fill, Color, and Shape will all have integer values representing the value. The following is a key for conversion
No_Fill = 0
Hash = 1
Solid = 2
Diamond = 0
Fish = 1
Pill = 2
Red = 0
Green = 1
Purple = 2


class Card:
    def __init__(self, countInput, fillInput, colorInput, shapeInput, positionInput=None, cameraInfoInput=None):
        # Converting inputs to card variables. position and cameraInfo are optional, default to null
        self.count = countInput
        self.fill = fillInput
        self.shape = shapeInput
        self.color = colorInput
        self.position = positionInput
        self.cameraInfo = cameraInfoInput
