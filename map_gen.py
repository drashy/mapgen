import random

class level(object):
    def __init__(self, width=50, height=50):
        self.width = width
        self.height = height

        # Zero out the map
        self._mapdata = [0]*(self.height*self.width)

        self.RandomFillMap(percentage=50, seed="2")
        self.MakeLevelBorders()
        self.SmoothMap(repetitions=10)
        self.RemoveStrays()
        self.RenderMap()

        assert 0


    def MapSet(self, x, y, value):
        assert (x>=0 and x<self.width and y>=0 and y<self.height), 'Invalid coords {0}, {1}'.format(x, y)
        self._mapdata[x+(y*self.width)] = value


    def MapGet(self, x, y):
        assert (x>=0 and x<self.width and y>=0 and y<self.height), 'Invalid coords {0}, {1}'.format(x, y)
        return self._mapdata[x+(y*self.width)]


    def GetSurroundingWalls(self, sourcex, sourcey, debug=False):
        counter = 0
        for y in range(sourcey-1, sourcey+1+1):
            for x in range(sourcex-1, sourcex+1+1):
                if x >= 0 and x < self.width and y >= 0 and y < self.height: # Make sure x and y is in the map!
                    if x==sourcex or y==sourcey and not (x==sourcex and y==sourcey):
                        counter += self.MapGet(x, y)
                        if debug:
                            print("{0},{1} = {2}".format(x, y, self.MapGet(x, y)))
        return counter


    def SmoothMap(self, repetitions=1):
        for i in range(repetitions):
            for y in range(self.height):
                for x in range(self.width):
                    wallCount = self.GetSurroundingWalls(x, y)
                    if wallCount > 2:
                        self.MapSet(x, y, 1)
                    else:
                        self.MapSet(x, y, 0)


    def RemoveStrays(self):
        for y in range(self.height):
            for x in range(self.width):
                wallCount = self.GetSurroundingWalls(x, y)
                if not wallCount:
                    self.MapSet(x, y, 0)
                elif wallCount == 4:
                    self.MapSet(x, y, 1)


    def RandomFillMap(self, percentage=50, seed=None):
        if seed:
            random.seed(seed)

        for y in range(self.height):
            for x in range(self.width):
                if random.randint(0, 99) <= percentage:
                    self.MapSet(x, y, 1)


    def MakeLevelBorders(self):
        # Set the borders
        for x in range(self.width):
            self.MapSet(x, 0, 1)
            self.MapSet(x, self.height-1, 1)
        for y in range(self.height):
            self.MapSet(0, y, 1)
            self.MapSet(self.width-1, y, 1)


    def RenderMap(self):
        # Print the map
        for y in range(self.height):
            line = [str(i) for i in self._mapdata[y*self.width:(y*self.width)+self.width]]
            print ' '.join(line).replace('0', ' ').replace('1', '@')


if __name__ == "__main__":
    a = level()