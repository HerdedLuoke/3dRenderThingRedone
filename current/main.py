import moderngl as mgl
from dataclasses import dataclass
import moderngl_window as mgl_w
from moderngl_window import resources
from pathlib import Path
import numpy as np
from numpy.typing import NDArray
import math
import time
from moderngl_window.resources import (programs,textures,scenes,data)
from moderngl_window.meta import (TextureDescription,ProgramDescription,SceneDescription,DataDescription)
from moderngl_window.scene import (KeyboardCamera, mesh)

class matrix:
    "General class for a 4x4 matrix. Inherits some numpy array methods. Row/Column vectors are not mutable"
    def __init__(self, name: str):
        self.name = str(name)
    def __getitem__(self, key):
        return self.mtx[key]
    
    @property
    def shape(self):
        return self.mtx.shape
    @property
    def byteForm(self):
        return self.mtx.astype("f4").tobytes(order="F")
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
        if isinstance(other, matrix):
            return self.mtx @ other.mtx

        return self.mtx @ other
    
    def setterdef(self, value):
        value = np.asarray(value)
        if value.shape != (4,):
            raise ValueError("vec must contain 4 values")
        return value

    
    def generic(self,row1=[1.0,0,0,0], row2=[0,1.0,0,0], row3=[0,0,1.0,0], row4=[0,0,0,1.0]):
        r1 = np.array([row1[0], row1[1], row1[2], row1[3]])
        r2 = np.array([row2[0], row2[1], row2[2], row2[3]])
        r3 = np.array([row3[0], row3[1], row3[2], row3[3]])
        r4 = np.array([row4[0], row4[1], row4[2], row4[3]])
        self.mtx = np.array([r1,r2,r3,r4]) 
        
   
    
    
class mutMatrix(matrix):
    "General class for a 4x4 matrix. Inherits some numpy array methods. Row/Column vectors are mutable"
  
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
    
    @property
    def scale(self) -> tuple[float,float,float]:
        return (self.r_vec1[0].copy(), self.r_vec2[1].copy(), self.r_vec3[2].copy())

    @property
    def x(self) -> float:
        return self.mtx[0,0]
    @x.setter
    def x(self, value: float):
        self.mtx[0,0] = value

    @property
    def y(self) -> float:
        return self.mtx[1,1]
    @y.setter
    def y(self, value: float):
        self.mtx[1,1] = value

    @property
    def z(self) -> float:
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
    @property
    def radians(self) -> float:
        return math.acos(self.r_vec1[0])
    @radians.setter
    def radians(self, radians: float):
        s,c = math.sin(radians),math.cos(radians)
        self.mtx[0,:] = [ c,0,s,0] 
        self.mtx[2,:] = [-s,0,c,0]  
         
    def __init__(self, radians: float):
        self.generic()
        self.radians = radians
        
class yawMtx(matrix):
    @property
    def radians(self) -> float:
        return math.acos(self.r_vec2[1])
    @radians.setter
    def radians(self, radians: float):
        s,c = math.sin(radians),math.cos(radians)
        self.mtx[1,:] = [0,c,-s,0] 
        self.mtx[2,:] = [0,s, c,0] 
    def __init__(self, radians: float):
        self.generic()
        self.radians = radians

class rollMtx(matrix):
    @property
    def radians(self) -> float:
        return math.acos(self.r_vec1[0]) 
    @radians.setter
    def radians(self, radians: float):
        s = math.sin(radians)
        c = math.cos(radians)
        self.mtx[0,:] = [c,-s,0,0] 
        self.mtx[1,:] = [s, c,0,0]  
        
    def __init__(self, radians: float):
        self.generic()
        self.radians = radians
        
    
    
class rotationMtx(matrix):
    @property 
    def mtx(self) -> NDArray:
       return self.pitch.mtx @ self.yaw.mtx @ self.roll.mtx
        
        
    @property
    def radians(self) -> tuple[float,float,float]:
        return (self.pitch.radians,self.yaw.radians,self.roll.radians)
    @radians.setter
    def radians(self, pitch: float|None = None, yaw:float|None = None, roll:float|None = None):
        if pitch != None:
            self.pitch.radians = pitch
        if yaw != None:
            self.yaw.radians = yaw
        if roll != None:
            self.roll.radians = roll
        
    def __init__(self, pitchMatrix: pitchMtx, yawMatrix:   yawMtx, rollMatrix:  rollMtx):
        self.pitch = pitchMatrix
        self.yaw = yawMatrix
        self.roll = rollMatrix
        
p = pitchMtx(math.pi)
y = yawMtx(0)
r = rollMtx(0)
rot = rotationMtx(p,y,r)

print("rows")
print(rot.r_vec1)
print(rot.r_vec2)
print(rot.r_vec3)
print(rot.r_vec4)
print("columns")
print(rot.c_vec1)
print(rot.c_vec2)
print(rot.c_vec3)
print(rot.c_vec4)
print("inverse")
print(rot.inverse())
print("transpose")
print(rot.transpose())
print("shape")
print(rot.shape)




class model:
    def __init__(self, mesh, scale, worldMatrix):
        self.mesh = mesh
        self.scale = scale
        self.worldMatrix = worldMatrix
    def getWorld(self):
        #self.worldCenter =
        pass
    def scale(self, x, y, z):
        matrix
        pass
    def translate(self, x, y, z):
        pass
    def recenter(self, x, y, z):
        pass
    def yawRotate(self, deg):
        pass
    def pitchRotate(self, deg):
        pass
    def rollRotate(self, deg):
        pass
    
            
        

    
    
    






class transformer:
    def __init__(self):
        pass

            
class quad():
    def __init__(self, v1,v2,v3):
        
        self.triHigh = np.array(
        [
            [v1[0], v3[0], v3[0]],
            [v1[1], v1[1], v3[1]],
            [v1[2], v1[2], v3[2]],
            [1,1,1]
        ])
        
        self.triLow = np.array(
        [
            [v1[0], v2[0], v3[0]],
            [v1[1], v2[1], v3[1]],
            [v1[2], v2[2], v3[2]],
            [1,1,1]
        ])
        
        self.base = np.array([self.triHigh, self.triLow])

class Window(mgl_w.WindowConfig):
    
    gl_version = (3, 3)
    window_size = (700, 700)
    vsync = True
    aspect_ratio = 4 / 4
    title = "Window"
    resizable = False
    samples = 8

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trans = transformer()
        
        self.camera = KeyboardCamera(
            self.wnd.keys,
            fov=75.0,
            aspect_ratio=self.wnd.aspect_ratio,
            near=0.1,
            far=1000,  
        )
        
        
        
        
        
        
        
        
        self.actionDict = {
            self.wnd.keys.U: "U",
            self.wnd.keys.I: "U",
            self.wnd.keys.O: "U",
            self.wnd.keys.W: "U",
            self.wnd.keys.A: "U",
            self.wnd.keys.S: "U",
            self.wnd.keys.D: "U",
            self.wnd.keys.DOWN: "U",
            self.wnd.keys.UP: "U",
            self.wnd.keys.RIGHT: "U",
            self.wnd.keys.LEFT: "U",
            self.wnd.keys.LEFT_SHIFT: "U",
            self.wnd.keys.SPACE: "U"
            }
        resources.register_program_dir(Path.cwd() / "resources" /  "programs")
        resources.register_data_dir(Path.cwd() / "resources" /  "data")
        resources.register_texture_dir(Path.cwd() / "resources" /  "textures")


        self.sProgram = self.importProgram("exampleProgram","exampleVertex.glsl","exampleFragment.glsl")
        
        self.screen = quad(
            [-1, 1, 0],
            [-1, -1, 0],
            [1, -1, 0]
            )
        self.myquad = quad(
            [-1, 1, 0],
            [-1, -1, 0],
            [1, -1, 0]
            )
        

        self.screenVertices = np.array([
            *(self.myquad.triHigh[:3].transpose()),
            *(self.myquad.triLow[:3].transpose())
        ]) 
        
        
        self.vbo = self.ctx.buffer(self.screenVertices.astype('f4').tobytes())
        self.vao = self.ctx.simple_vertex_array(self.sProgram, self.vbo, 'in_vert')
        self.mousePos = (0,0)
        self.ctx.screen.use()
        self.mouseNum = 0

    def on_render(self, time: float, frametime: float):
        
        self.ctx.screen.clear(0, 0, 0, 1.0)
        self.vao.render(mgl.TRIANGLES)
        
    def on_mouse_position_event(self, x, y, dx, dy):
        self.mousePos = (x,y)

    def on_key_event(self, key, action, modifiers):
        
        
        
        
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
        
         

#Window.run()