"""
Test of pythonista features
"""

from scene import *
from scene_drawing import *
import random
import math

class MyScene (Scene):
    def setup(self):
        self.taps = 0
    
    def did_change_size(self):
        pass
    
    def update(self):

        stroke(1,1,1)
        fill(1,0,0)
        stroke_weight(self.taps)
        rect(100,100,self.size.w-200,self.size.w-200)
        image("test:Boat", 120, 120, self.size.w-240, self.size.w-240 )
    
    def touch_began(self, touch):	
        self.taps += 1
    
    def touch_moved(self, touch):
        pass
    
    def touch_ended(self, touch):
        pass

if __name__ == '__main__':
    run(MyScene())
