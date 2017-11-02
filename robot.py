
import math
import random

import visualize
import pylab


class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)

class RectangularRoom(object):
    def __init__(self, width, height):
        self.width=width
        self.height=height
        self.TileCleaned=[]
    
    def cleanTileAtPosition(self, pos):
        deltaX=math.floor(pos.getX())
        deltaY=math.floor(pos.getY())
        if not self.isTileCleaned(deltaX, deltaY):
            self.TileCleaned.append((deltaX,deltaY))

    def isTileCleaned(self, m, n):
        if (m,n) in self.TileCleaned:
            return True
        else:
            return False
    
    def getNumTiles(self):
        return self.width*self.height

    def getNumCleanedTiles(self):
        return len(self.TileCleaned)

    def getRandomPosition(self):
        deltaX=(random.random())*self.width
        deltaY=(random.random())*self.height
        return Position(deltaX,deltaY)

    def isPositionInRoom(self, pos):
        if 0<=pos.getX()<self.width and 0<=pos.getY()<self.height:
            return True
        else:
            return False

class Robot(object):
    def __init__(self, room, speed):
        self.speed=speed
        self.position=room.getRandomPosition()
        self.direction=random.randint(0,359)
        self.room=room
        self.room.cleanTileAtPosition(self.position)

    def getRobotPosition(self):
        return self.position
    
    def getRobotDirection(self):
        return self.direction

    def setRobotPosition(self, position):
        self.position=position

    def setRobotDirection(self, direction):
        self.direction=direction

    def updatePositionAndClean(self):
        raise NotImplementedError # don't change this!
        self.position=self.position.getNewPosition(self.direction, self.speed)
        self.room.cleanTileAtPosition(self.position)


class StandardRobot(Robot):
    def updatePositionAndClean(self):
        if 1<=math.floor(self.position.getX())<self.room.width-1 and 1<=math.floor(self.position.getY())<self.room.height-1:
            direction=self.direction
            self.position=self.position.getNewPosition(direction, self.speed)
        else:
            flag=True
            while flag:
                self.direction=random.randint(0,359)
                self.position=self.position.getNewPosition(self.direction, self.speed) 
                if 1<=math.floor(self.position.getX())<self.room.width-1 and 1<=math.floor(self.position.getY())<self.room.height-1:
                    flag=False
                else:
                    continue 
        self.room.cleanTileAtPosition(self.position)



def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    steps=[]
    for i in range(num_trials):
        anim =visualize.RobotVisualization(num_robots, width, height)
        room=RectangularRoom(width,height)
        robots=[]
        step=0
        for i in range(num_robots):
            robots.append(robot_type(room,speed))
        while float(room.getNumCleanedTiles())/float(room.getNumTiles()) <= min_coverage:   
            anim.update(room, robots)
            for robot in robots:
                robot.updatePositionAndClean()
            step+=1
        steps.append(step)
        anim.done()
    return float(sum(steps)/len(steps))



# Uncomment this line to see how much your simulation takes on average
print  runSimulation(1, 1.0, 10, 10, 0.75, 30, StandardRobot)


# === Problem 4
class RandomWalkRobot(Robot):

    def updatePositionAndClean(self):
        if 1<=math.floor(self.position.getX())<self.room.width-1 and 1<=math.floor(self.position.getY())<self.room.height-1:
            direction=random.randint(0,359)
            self.position=self.position.getNewPosition(direction, self.speed)
        else:
            flag=True
            while flag:
                self.direction=random.randint(0,359)
                self.position=self.position.getNewPosition(self.direction, self.speed) 
                if 1<=math.floor(self.position.getX())<self.room.width-1 and 1<=math.floor(self.position.getY())<self.room.height-1:
                    flag=False
                else:
                    continue 
        self.room.cleanTileAtPosition(self.position)      

#print  runSimulation(1, 1.0, 10, 10, 0.75, 30, RandomWalkRobot)

def showPlot1(title, x_label, y_label):
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print "Plotting", num_robots, "robots..."
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
#showPlot1('Time It Takes 1 - 10 Robots To Clean 80% Of A Room','Number of Robots','Time-steps' )
    
def showPlot2(title, x_label, y_label):

    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300/width
        print "Plotting cleaning time for a room of width:", width, "by height:", height
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()