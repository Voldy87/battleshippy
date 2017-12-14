class Ship:
    "A battleship"
    def __init__ (self, name, player, length):
        self.name = name
        self.length = length
        self.hitCount = 0
        self.sinked = False
        print("just built a ship!!")
    def getShot (self):
        self.hitCount += 1
        self.sinked = (self.hitCount>=self.length)
        return self.sinked
