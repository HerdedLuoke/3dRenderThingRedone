import numpy as np
import moderngl as mgl
from dataclasses import dataclass
import moderngl_window as mgl_w
from moderngl_window import (resources, geometry)
from moderngl_window.opengl.vao import VAO
from pathlib import Path
import numpy as np
from numpy.typing import NDArray
import math
import time
from moderngl_window.resources import (programs,textures,scenes,data)
from moderngl_window.meta import (TextureDescription,ProgramDescription,SceneDescription,DataDescription)
from moderngl_window.scene import (KeyboardCamera, mesh)

class matrix:
    """
    General class for a mutable 4x4 matrix. 
    Inherits .shape, .transpose, .invert and .copy from numpy 
    """
    def __init__(self, name: str):
        self.name = str(name)
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

        
class meshC:
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
    


    
    
class triangle:
    @property
    def vertices(self):
        "this returns the list of verticies in a continous style cuz buffer perfers that"
        return np.ascontiguousarray(
            [*self.__vertex1, *self.__vertex2, *self.__vertex3],
            dtype=np.float32,
        )

    @property
    def verticies(self):
        # Backward-compatible alias; prefer .vertices going forward.
        return self.vertices
    def __init__(self, vertex1:tuple[float, float, float, float] | list[float, float, float, float] |  NDArray, vertex2: tuple[float, float, float, float] | list[float, float, float, float] |  NDArray, vertex3:tuple[float, float, float, float] | list[float, float, float, float] |  NDArray):
        self.__vertex1 = np.asarray(vertex1)
        self.__vertex2 = np.asarray(vertex2)
        self.__vertex3 = np.asarray(vertex3)
    














class Window(mgl_w.WindowConfig):
    @property
    def mainMatrix(self):
        temp = self.pos @ self.rotation
        return  temp @ self.scale.mtx
    
    gl_version = (3, 3)
    window_size = (700, 700)
    vsync = True
    aspect_ratio = 4 / 4
    title = "Window"
    resizable = False
    samples = 8

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
        self.camera = KeyboardCamera(
            self.wnd.keys,
            fov=75.0,
            aspect_ratio=self.wnd.aspect_ratio,
            near=0.1,
            far=1000,  
        )
        
        self.actionDict = {
            self.wnd.keys.U: self.rotateX,
            self.wnd.keys.I: self.rotateY,
            self.wnd.keys.O: self.rotateZ,
            self.wnd.keys.W: self.moveZb,
            self.wnd.keys.A: self.moveXl,
            self.wnd.keys.S: self.moveZf,
            self.wnd.keys.D: self.moveXr,
            self.wnd.keys.LEFT_SHIFT: self.moveYd,
            self.wnd.keys.SPACE: self.moveYp
            }
        
        resources.register_program_dir(Path.cwd() / "resources" /  "programs")
        resources.register_data_dir(Path.cwd() / "resources" /  "data")
        resources.register_texture_dir(Path.cwd() / "resources" /  "textures")
       

        self.sProgram = self.importProgram("exampleProgram","exampleVertex.glsl","exampleFragment.glsl")
        
        self.screen = quad(
            [-1, 1, 0,],
            [-1, -1, 0],
            [1, -1, 0]
            )
        self.myquad = quad(
            [-1, 1, 0],
            [-1, -1, 0],
            [1, -1, 0]
            )

        highVerts = self.myquad.triHigh[:3].T
        lowVerts = self.myquad.triLow[:3].T
        
        self.worldVert = np.vstack((highVerts, lowVerts))
        self.screenVertices = np.asarray(self.worldVert)
        self.vbo = self.ctx.buffer(self.screenVertices.astype('f4').tobytes())
        self.vao = self.ctx.simple_vertex_array(self.sProgram, self.vbo, 'in_vert')
        
        self.pitchX = pitchMtx(0)
        self.yawY = yawMtx(0)
        self.rollZ = rollMtx(0)
        self.rotation = rotationMtx(self.pitchX,self.yawY,self.rollZ)
        self.pos = positionMtx(0,0,0)
        self.scale = scalingMtx(0.5,0.5,0.5)


    def on_render(self, time: float, frametime: float):
        self.rotateX(p=math.pi/1024)
        self.rotateY(y=math.pi/1024)
        

        self.sProgram["modelMat"].write(self.mainMatrix.transpose().astype('f4').tobytes())
        self.sProgram["cameraMat"].write(self.camera.matrix)
        self.sProgram["projectionMat"].write(self.camera.projection.tobytes())
        self.ctx.program
        self.ctx.screen.use()
        
    
        self.ctx.screen.clear(0.0, 0.0, 0.0, 1.0)
        self.vao.render(mgl.TRIANGLES)
        
        
        
    def on_mouse_position_event(self, x, y, dx, dy):
        self.mousePos = (x,y)

    def on_key_event(self, key, action, modifiers):
        amspecial = False
        
        if action == self.wnd.keys.ACTION_PRESS:
            function = self.actionDict.get(key)
            if function != None:
                function()
        return super().on_key_event(key, action, modifiers)

    def importProgram(self, programFolder:str, vertexProgram:str | None=None, fragmentProgram:str | None=None , computeProgram:str | None=None):
        
        folder = Path.cwd() / "resources" /  "programs" / programFolder
        
        program = programs.load(ProgramDescription(
            vertex_shader=vertexProgram,
            fragment_shader=fragmentProgram,
            compute_shader=computeProgram
        ))
        
        return program
    
    def importData(self, name, myType):
        dataFile = data.load(DataDescription(
            path=name,
            kind=myType
        ))
        return dataFile
    
    def importTexture(self, name, myType):
        texture = textures.load(TextureDescription(
            path=name,
            kind=myType
        ))
        return texture
    
    def move(self, x:float=0, y:float=0, z:float=0):
        self.pos.x = self.pos.x + x
        self.pos.y = self.pos.y + y
        self.pos.z = self.pos.z + z
        
    def moveYp(self, yi:float=0.1):
        self.move(y=yi)
    def moveYd(self, yi:float=0.1):
        self.move(y=-yi)
    def moveXl(self, xi:float=0.1):
        self.move(x=-xi)
    def moveXr(self, xi:float=0.1):
        self.move(x=xi)
    def moveZf(self, zi:float=0.1):
        self.move(z=zi)
    def moveZb(self, zi:float=0.1):
        self.move(z=-zi)

    def rotateX(self,p=math.pi/64):
        self.rotation.rotateRadians(pitch=p)
    def rotateY(self,y=math.pi/64):
        self.rotation.rotateRadians(yaw=y)
    def rotateZ(self,r=math.pi/64):
        self.rotation.rotateRadians(roll=r)
    
    

Window.run()

