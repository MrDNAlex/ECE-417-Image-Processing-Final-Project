import math
import json
from ObjectTracker import ObjectTracker

#
# Direct Translations of what is necessary from TrackInstance and TrackSequence
#

class ObjectInstance:

    uID: int
    timeSec: float
    frameNumber: int
    
    X: float
    Y: float
    width: int
    height: int
    
    size:float

    def __init__(self, uid: int, frameNum: int, timeS: float, x: int, y: int, width: int, height: int):
        
        self.uID = uid
        self.frameNumber = frameNum
        self.timeSec = timeS
        self.X = x
        self.Y = y
        self.width = width
        self.height = height
        self.size = width * height
        
    def getCenter(self):
        return (self.X + self.width / 2.0, self.Y + self.height / 2.0)
    
    def getJSON(self):
        obj: json = {}
        
        obj["uID"] = self.uID
        obj["FrameNumber"] = self.frameNumber
        obj["TimeSeconds"] = self.timeSec
        obj["PosX"] = self.X
        obj["PosY"] = self.Y
        obj["Width"] = self.width
        obj["Height"] = self.height
        obj["Size"] = self.size
        
        return obj
        
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
        
    def getJSON(self):
        
        obj: json = {}
        
        obj["uID"] = self.uID
        obj["MinX"] = self.minX
        obj["MinY"] = self.minY
        obj["MaxX"] = self.maxX
        obj["MaxY"] = self.maxY
        
        instancesJSON = []
        for instance in self.instances:
            instancesJSON.append(instance.getJSON())
        
        obj["Instances"] = instancesJSON
        
        return obj
        
class Tracker:
    sequences : list[ObjectSequence]
    nextUID: int
    distanceThreshold: float
    labeler: ObjectTracker
    
    def __init__(self, distanceThreshold = 50.0):
        
        self.sequences = []
        self.nextUID = 0
        self.distanceThreshold = distanceThreshold
        self.labeler = ObjectTracker()
        
    def getCenter(self, instance: ObjectInstance):
        return (instance.X + instance.width / 2.0, instance.Y + instance.height / 2.0)
    
    def getDistance(self, center1, center2):
        return math.sqrt((center2[0] - center1[0])**2 + (center2[1] - center1[1])**2)
    
    def processMask(self, mask, frameNum: int, timeSec: float):
        
        boxes = self.labeler.process(mask)
        
        # Create Object Instances
        currentInstances = []
        for (x, y, w, h) in boxes:
            instance = ObjectInstance(-1, frameNum, timeSec, x, y, w, h)
            currentInstances.append(instance)
        
        for newInstance in currentInstances:
            bestSequence = None
            shortestDistance = float("inf")
            newCenter = self.getCenter(newInstance)
            
            for seq in self.sequences:
                if len(seq.instances) == 0:
                    continue
                
                lastInstance = seq.instances[-1]
                lastCenter = self.getCenter(lastInstance)
                distance = self.getDistance(lastCenter, newCenter)
                
                if distance < shortestDistance and distance < self.distanceThreshold:
                    shortestDistance = distance
                    bestSequence = seq
                
            if bestSequence is not None:
                newInstance.uID = bestSequence.uID
                bestSequence.addInstance(newInstance)
                
            else:
                newInstance.uID = self.nextUID
                newSequence = ObjectSequence(self.nextUID)
                newSequence.addInstance(newInstance)
                
                self.sequences.append(newSequence)
                self.nextUID += 1
            
        return (self.sequences, currentInstances) 
    