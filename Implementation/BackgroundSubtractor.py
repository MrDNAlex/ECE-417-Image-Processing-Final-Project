import numpy as np
from VideoProcessorSettings import VideoProcessorSettings
from PixelModel import PixelModel

class BackgroundSubtractor:
    
    width: int
    height: int
    
    grid: list[list[PixelModel]]
    
    def __init__(self, settings : VideoProcessorSettings):
        
        self.width = settings.width
        self.height = settings.height
        
        self.grid = []
        for y in range(settings.height):
            row = []
            for x in range(settings.width):
                row.append(PixelModel(settings.K, settings.alpha, settings.threshold))
            self.grid.append(row)
        
    def apply(self, frame):
        
        mask = np.zeros((self.height, self.width), dtype=np.uint8)
        
        for y in range(self.height):
            for x in range(self.width):
                mask[y, x] = self.grid[y][x].processPixel(frame[y, x])
                
        return mask
        