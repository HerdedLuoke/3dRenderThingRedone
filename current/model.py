import numpy as np
import math
from numpy.typing import NDArray
from matricies import (
    scalingMtx,
    positionMtx,
    rotationMtx,
)



class meshC:
    # this needs a vao, vbo, and verticies element, 
    # in addition to regenerating such after a .shader property is modified.
    def __init__(self):
        pass
    
      


class modelContainer:
    @property
    def modelMatrix(self):
        return (self.positionMatrix @ self.rotationMatrix) @ self.scaleMatrix.mtx
    @property
    def cameraMatrix(self):
        return np.frombuffer(self.__cameraMatrix, dtype='f4').reshape((4,4)) # make get dynamically from the window
    @property
    def projectionMatrix(self):
        return self.__projectionMatrix # make get dynamically from the window
    @property
    def modelMatrixBytes(self):
        return self.modelMatrix.transpose().astype('f4').tobytes()
    @property
    def cameraMatrixBytes(self):
        return self.__cameraMatrix # by default is in byteform 
    @property
    def projectionMatrixBytes(self):
        return self.__projectionMatrix.tobytes()
    
    def __init__(self, imesh:meshC, scaleMatrix: scalingMtx, positionMatrix:positionMtx, rotationMatrix:rotationMtx, cameraMatrix:NDArray, projectionMatrix:NDArray):
        
        self.mesh= imesh
        self.verticies = self.mesh.verticies
        self.vao = self.mesh.vao
        self.vbo = self.mesh.vbo
        
        self.__projectionMatrix = projectionMatrix
        self.__cameraMatrix = cameraMatrix
        
        self.positionMatrix = positionMatrix
        self.scaleMatrix = scaleMatrix
        self.rotationMatrix = rotationMatrix
      
    def setScale(self, x:float|None = None, y:float|None = None, z:float|None = None):
        if x != None:
            self.scaleMatrix.x = x
        if y != None:
            self.scaleMatrix.y = y
        if z != None:
            self.scaleMatrix.z = z
            
    def incrementScale(self, x:float = 0, y:float = 0, z:float = 0):
        self.scaleMatrix.x = x + self.scaleMatrix.x
        self.scaleMatrix.y = y + self.scaleMatrix.y
        self.scaleMatrix.z = z + self.scaleMatrix.z
    
    def setRadians(self, pitch: float|None = None, yaw:float|None = None, roll:float|None = None):
        if pitch != None:
            self.rotationMatrix.pitch.radians = pitch
        if yaw != None:
            self.rotationMatrix.yaw.radians = yaw
        if roll != None:
            self.rotationMatrix.roll.radians = roll
            
    def rotateRadians(self, pitch: float=0, yaw:float=0, roll:float=0):
    
        self.rotationMatrix.pitch.radians = (pitch + self.rotationMatrix.pitch.radians) % (2*math.pi)
        self.rotationMatrix.yaw.radians = (yaw + self.rotationMatrix.yaw.radians) % (2*math.pi)
        self.rotationMatrix.roll.radians = (roll + self.rotationMatrix.roll.radians) % (2*math.pi)
    
    def setPosition(self, x:float|None = None, y:float|None = None, z:float|None = None):
        if x != None:
            self.positionMatrix.x = x
        if y != None:
            self.positionMatrix.y = y
        if z != None:
            self.positionMatrix.z = z
            
    def incrementPosition(self, x:float = 0, y:float = 0, z:float = 0 ):
        
        self.positionMatrix.x = x + self.positionMatrix.x
        self.positionMatrix.y = y + self.positionMatrix.y
        self.positionMatrix.z = z + self.positionMatrix.z
    