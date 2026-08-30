import math
import numpy as np
from numpy.typing import NDArray



class matrix:
    """
    General class for a mutable 4x4 matrix. 
    Inherits .shape, .transpose, .invert and .copy from numpy 
    """
    def __init__(self, name: str):
        self.name = str(name)
        # why did i add this again? 
    def __getitem__(self, key):
        return self.mtx[key]
    
    
    @property
    def shape(self):
        return self.mtx.shape
    @property
    def byteForm(self):
        """
        Returns the bytes of the current matrix in Column Vector form
        """
        return self.mtx.transpose().astype("f4").tobytes()
    
    # the below arent even used by theyre fun and ill find a use for them one day. 
    # i prolly could store verts and colors in a generic and output as
    # (row1/vert,row2/vert,row3/vert,row4/color)
    @property
    def c_vec1(self):
        return self.mtx[:,0].copy()
    @property
    def c_vec2(self):
        return self.mtx[:,1].copy()
    @property
    def c_vec3(self):
        return self.mtx[:,2].copy()
    @property
    def c_vec4(self):
        return self.mtx[:,3].copy()
    @property
    def r_vec1(self):
        return self.mtx[0,:].copy()
    @property
    def r_vec2(self):
        return self.mtx[1,:].copy()
    @property
    def r_vec3(self):
        return self.mtx[2,:].copy()
    @property
    def r_vec4(self):
        return self.mtx[3,:].copy()

    def copy(self) -> NDArray:
        return self.mtx.copy()

    def transpose(self) -> NDArray:
        return self.mtx.transpose()

    def inverse(self) -> NDArray:
        return np.linalg.inv(self.mtx)
    
    def __matmul__(self, other) -> NDArray:
        """
        This represents the @ operator added by numpy
        Extended to function with the mtx property
        """
        if isinstance(other, matrix):
            return self.mtx @ other.mtx

        return self.mtx @ other 
        # ^ this could be nested into a new matrix object so it returns the correct type? 
        # likely would also need to check for its variant aswell so it has the correct attributes   
    
    def setterdef(self, value):
        """
        General row/column vector setter. 
        Takes a input and coverts to asarray then checks if input is of (4,) size
        
        """
        value = np.asarray(value)
        if value.shape != (4,):
            raise ValueError("vec must contain 4 values")
        return value

    
    def generic(self,row1=[1.0,0,0,0], row2=[0,1.0,0,0], row3=[0,0,1.0,0], row4=[0,0,0,1.0]):
        """
        By default creates a 4x4 identity matrix
        Returns 4x4 with any modified rows and sets it as the .mtx
        """
        # this can be simplified, its overengineered cuz its leftover code from a old version, 
        # but i dont rlly need to cuz its such a minimal part of the code
        r1 = np.array([row1[0], row1[1], row1[2], row1[3]])
        r2 = np.array([row2[0], row2[1], row2[2], row2[3]])
        r3 = np.array([row3[0], row3[1], row3[2], row3[3]])
        r4 = np.array([row4[0], row4[1], row4[2], row4[3]])
        self.mtx = np.array([r1,r2,r3,r4]) 
         
class mutMatrix(matrix):
    """
    General class for a mutable 4x4 matrix. 
    Inherits .shape, .transpose, .invert and .copy from numpy 
    """
    # not used but i didnt want to throw out the setters fully
    @matrix.r_vec1.setter
    def r_vec1(self, value) -> None:
        self.mtx[0,:] = self.setterdef(value) 
    @matrix.r_vec2.setter
    def r_vec2(self, value) -> None:
        self.mtx[1,:] = self.setterdef(value) 
    @matrix.r_vec3.setter
    def r_vec3(self, value) -> None:
        self.mtx[2,:] = self.setterdef(value)
    @matrix.r_vec4.setter
    def r_vec4(self, value) -> None:
        self.mtx[3,:] = self.setterdef(value)
    @matrix.c_vec1.setter
    def c_vec1(self, value) -> None:
        self.mtx[:,0] = self.setterdef(value)
    @matrix.c_vec2.setter
    def c_vec2(self, value) -> None:
        self.mtx[:,1] = self.setterdef(value)
    @matrix.c_vec3.setter
    def c_vec3(self, value) -> None:
        self.mtx[:,2] = self.setterdef(value)
    @matrix.c_vec4.setter
    def c_vec4(self, value) -> None:
        self.mtx[:,3] = self.setterdef(value)

# need to go through and map out all accessible properties for variants and simplify/make more consistent
class scalingMtx(matrix):
    "Matrix for scaling x,y,z coordinates"
    
    @property
    def scale(self) -> tuple[float,float,float]:
        return (self.r_vec1[0].copy(), self.r_vec2[1].copy(), self.r_vec3[2].copy())

    @property
    def x(self) -> float:
        """The x axis scale. Is mutable"""
        return self.mtx[0,0]
    @x.setter
    def x(self, value: float):
        self.mtx[0,0] = value

    @property
    def y(self) -> float:
        """The y axis scale. Is mutable"""
        return self.mtx[1,1]
    @y.setter
    def y(self, value: float):
        self.mtx[1,1] = value

    @property
    def z(self) -> float:
        """The z axis scale. Is mutable"""
        return self.mtx[2,2]
    @z.setter
    def z(self, value: float):
        self.mtx[2,2] = value
    
    def __init__(self, x: float=1.0, y:float=1.0, z:float=1.0): 
        self.generic(  
            row1=  [x,0,0,0], 
            row2=  [0,y,0,0], 
            row3=  [0,0,z,0])
        
class positionMtx(matrix):
    "Matrix for translating x,y,z coordinates"
    @property
    def position(self) -> tuple[float, float, float]:
        return (self.r_vec1[3], self.r_vec2[3], self.r_vec3[3])

    @property
    def x(self) -> float:
        return self.mtx[0,3]
    @x.setter
    def x(self, value: float):
        self.mtx[0,3] = value

    @property
    def y(self) -> float:
        return self.mtx[1,3]
    @y.setter
    def y(self, value: float):
        self.mtx[1,3] = value

    @property
    def z(self) -> float:
        return self.mtx[2,3]
    @z.setter
    def z(self, value: float):
        self.mtx[2,3] = value
    
    def __init__(self, x: float=1.0, y:float=1.0, z:float=1.0):
        self.generic(
        row1 =[1.0,0,0,x], 
        row2 =[0,1.0,0,y],
        row3 =[0,0,1.0,z])
        
class pitchMtx(matrix):
    "Matrix for rotation around the X axis"
    @property
    def radians(self) -> float:
        return self.__radians 
    @radians.setter
    def radians(self, radians: float):
        self.__radians = radians
        s,c = math.sin(radians), math.cos(radians)
        self.mtx[1,:] = [0,c,-s,0]
        self.mtx[2,:] = [0,s,c,0]  
         
    def __init__(self, radians: float):
        self.generic()
        self.radians = radians
        
class yawMtx(matrix):
    "Matrix for rotation around the Y axis"
    @property
    def radians(self) -> float:
        return self.__radians 
    @radians.setter
    def radians(self, radians: float):
        self.__radians = radians
        s,c = math.sin(radians), math.cos(radians)
        
        self.mtx[0,:] = [c,0,s,0]
        self.mtx[2,:] = [-s,0,c,0] 
    def __init__(self, radians: float):
        self.generic()
        self.radians = radians

class rollMtx(matrix):
    "Matrix for rotation around the Z axis"
    @property
    def radians(self) -> float:
        return self.__radians 
    @radians.setter
    def radians(self, radians: float):
        self.__radians = radians
        s,c = math.sin(radians), math.cos(radians)
        
        self.mtx[0,:] = [c,-s,0,0] 
        self.mtx[1,:] = [s, c,0,0]  
        
    def __init__(self, radians: float):
        self.generic()
        self.radians = radians 
         
class rotationMtx(matrix):
    "Matrix for rotation around the X(Pitch), Y(Yaw), and Z(Roll) axis."
    @property 
    def mtx(self) -> NDArray:
        """
        The numpy array representing the matrix.
        This computes pitch * yaw * roll then returns the result. 
        """
        return self.pitch.mtx @ self.yaw.mtx @ self.roll.mtx
 
    @property
    def radians(self) -> tuple[float,float,float]:
        return (self.pitch.radians,self.yaw.radians,self.roll.radians)

    def __init__(self, pitchMatrix:pitchMtx, yawMatrix:yawMtx, rollMatrix:rollMtx):
        
        self.pitch = pitchMatrix
        self.yaw = yawMatrix
        self.roll = rollMatrix

    def rotateRadians(self, pitch: float = 0, yaw: float = 0, roll: float = 0):
        self.pitch.radians = (self.pitch.radians + pitch) % (2 * math.pi)
        self.yaw.radians = (self.yaw.radians + yaw) % (2 * math.pi)
        self.roll.radians = (self.roll.radians + roll) % (2 * math.pi)
    # why wasnt this removed? (i swore i did) should be but ill wait and check for later