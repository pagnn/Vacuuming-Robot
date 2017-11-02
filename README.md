# Vacuuming-Robot
通过Python的matplotlib库可视化iRobot的清理路线，时间

一、项目介绍

  Vacuuming Robot（http://store.irobot.com） 是iRobot旗下的一款吸尘器机器人，在这个项目中，通过Python的Numpy，Scipy，Matplotlib库的使用，可视化robot在两种不同的清理方案的情况下所用的时间和路径。
  在一个宽为width，长为height的矩形房间中进行作业，机器人随机落在任何一点上，方向也任意忽略机器人自身的大小，并且将该房间的地面分割为width*height块，只要机器人一出现在任何一块上，该块地板便清理完毕（只要将地板分割地机器小，即可实现）。机器人的行进策略有两种，一是只要不碰到墙壁便保持方向不变，二是每一次行进都任意改向。
  
二、项目构想
  以randomWalk的为基础进行构建
  首先确定三个基础对象，RectangularRoom,Robot,Position
  
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
          raise NotImplementedError 
          self.position=self.position.getNewPosition(self.direction, self.speed)
          self.room.cleanTileAtPosition(self.position)
 
 建立Robot的子类，StandardRobot和RandomWalkRobot，两者采取不同的行进方式
 StandardRobot和RandomWalkRobot的updatePositionAndClean()方法不同
 
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
 
 最后，建立完我们所需要的基础对象，我们就可以模拟机器人的行进和清理了
 
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
 

当然我们需要添加上个函数中anim三个语句将其可视化

通过Matplotlib绘图进行对比

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

showPlot1('Time It Takes 1 - 10 Robots To Clean 80% Of A Room','Number of Robots','Time-steps' )
    
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

showPlot2('Time It Takes Two Robots To Clean 80% Of Variously Shaped Rooms','Aspect Ratio','Time-steps' )
 
  
