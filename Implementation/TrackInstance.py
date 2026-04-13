from numpy import long

#
# Direct Translations of what is necessary from TrackInstance and TrackSequence
#

class ObjectInstance:

    uID: int
    timeSec: long
    frameNumber: int
    
    X: float
    Y: float
    width: int
    height: int
    
    size:float

    def __init__(self, uid: int, frameNum: int, timeS: long, x: int, y: int, width: int, height: int):
        
        self.uID = uid
        self.frameNumber = frameNum
        self.timeSec = timeS
        self.X = x
        self.Y = y
        self.width = width
        self.height = height
        self.size = width * height
        
class ObjectSequence:
    
    uID: int
    instances: list[ObjectInstance]
    
    minX: float
    minY: float
    maxX: float
    maxY: float
    
    sumSize: float
    
    def __init__(self, uid: int):
        self.uID = uid
        self.instances = []
        
        self.minX = 1.0
        self.minY = 1.0
        self.maxX = 1.0
        self.maxY = 1.0
        
        self.sumSize = 0.0
        
    def addInstance(self, instance: ObjectInstance):
        i = 0
        while (i < len(self.instances) and (self.instances[i].timeSec < instance.timeSec)):
            i += 1
        
        self.sumSize += instance.size
        self.instances.insert(i, instance)
    