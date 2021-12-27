class Cell:
    def __init__(self, color) -> None:
        self.color = color
        pass

    def die(self):
        self.color = "white"
    
    def appear(self):
        self.color = "black"
