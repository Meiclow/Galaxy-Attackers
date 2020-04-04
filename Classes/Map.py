from secrets import randbelow

class Map:
    def __init__(self, x, y, barrier_botom_y, barrier_top_y, player_range_bottom_y = 0, player_range_top_y = -1):
        self.x = x
        self.y = y
        self.barrier_botom_y = barrier_botom_y
        self.barrier_top_y = barrier_top_y
        self.player_range_bottom_y = player_range_bottom_y
        if(player_range_top_y == -1):
            self.player_range_top_y = barrier_botom_y - 1
        else:
            self.player_range_top_y = player_range_top_y

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def getBarrierBottomY(self):
        return self.barrier_botom_y

    def getBarrierTopY(self):
        return self.getBarrierTopY

    def getPlayerRangeBottomY(self):
        return self.player_range_bottom_y

    def getPlayerRangeTopY(self):
        return self.player_range_top_y

#Obstacle dojdzie później
    def generateObstacle(self):
        Obstacle(randbelow(self.player_range_top_y - self.player_range_bottom_y) + self.player_range_bottom_y, self.x)