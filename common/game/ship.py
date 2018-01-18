class Ship:
    "A battleship"
    def __init__ (self, name, length):
        self.name = name
        self.length = length
        self.hitCount = 0
        self.sinked = False
    def __str__(self):
        name = self.name
        hit = ", hit " + str(self.hitCount) + " times"
        if (self.sinked):
            name = "SINKED" + self.name
            hit = ""
        return  name + ": " + str(self.length) + " long" + hit 
    def getShot (self):
        self.hitCount += 1
        self.sinked = (self.hitCount>=self.length)
        return self.sinked
