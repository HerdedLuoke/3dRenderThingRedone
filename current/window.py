
import math
from pathlib import Path

import numpy as np
import moderngl as mgl
import moderngl_window as mgl_w
from geometry import triangle
from moderngl_window import resources
from moderngl_window.scene import KeyboardCamera
from moderngl_window.resources import programs, textures, data
from moderngl_window.meta import (
    TextureDescription,
    ProgramDescription,
    DataDescription,
)

from matricies import (
    scalingMtx,
    positionMtx,
    pitchMtx,
    yawMtx,
    rollMtx,
    rotationMtx,
)

from model import meshC, renderObject



# most below code is just for tests and will be nuked from orbit
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
        
        
        triangle1 = triangle([-1, -1,  1, 1], [ 1, -1,  1, 1], [ 1,  1,  1, 1])
        triangle2 = triangle([-1, -1,  1, 1], [ 1,  1,  1, 1], [-1,  1,  1, 1])

        triangle3 = triangle([-1, -1, -1, 1], [-1,  1, -1, 1], [ 1,  1, -1, 1])
        triangle4 = triangle([-1, -1, -1, 1], [ 1,  1, -1, 1], [ 1, -1, -1, 1])

        triangle5 = triangle([-1, -1, -1, 1], [-1, -1,  1, 1], [-1,  1,  1, 1])
        triangle6 = triangle([-1, -1, -1, 1], [-1,  1,  1, 1], [-1,  1, -1, 1])

        triangle7 = triangle([ 1, -1, -1, 1], [ 1,  1, -1, 1], [ 1,  1,  1, 1])
        triangle8 = triangle([ 1, -1, -1, 1], [ 1,  1,  1, 1], [ 1, -1,  1, 1])

        triangle9 = triangle([-1,  1, -1, 1], [-1,  1,  1, 1], [ 1,  1,  1, 1])
        triangle10 = triangle([-1,  1, -1, 1], [ 1,  1,  1, 1], [ 1,  1, -1, 1])

        triangle11 = triangle([-1, -1, -1, 1], [ 1, -1, -1, 1], [ 1, -1,  1, 1])
        triangle12 = triangle([-1, -1, -1, 1], [ 1, -1,  1, 1], [-1, -1,  1, 1])
        
        self.verts = np.array([
            *triangle1.vertices,*triangle2.vertices,*triangle3.vertices,*triangle4.vertices,
            *triangle5.vertices,*triangle6.vertices,*triangle7.vertices,*triangle8.vertices,
            *triangle9.vertices,*triangle10.vertices,*triangle11.vertices,*triangle12.vertices])
        
        self.screenVertices = self.verts
        self.vbo = self.ctx.buffer(self.screenVertices.astype('f4').tobytes())
        self.vao = self.ctx.simple_vertex_array(self.sProgram, self.vbo, 'in_vert')
        
        self.pitchX = pitchMtx(0)
        self.yawY = yawMtx(0)
        self.rollZ = rollMtx(0)
        self.rotation = rotationMtx(self.pitchX,self.yawY,self.rollZ)
        self.pos = positionMtx(0,0,0)
        self.scale = scalingMtx(0.5,0.5,0.5)


    def on_render(self, time: float, frametime: float):
        self.rotateX(p=math.pi/2048)
        self.rotateY(y=math.pi/2048)
        

        self.sProgram["modelMat"].write(self.mainMatrix.transpose().astype('f4').tobytes())
        self.sProgram["cameraMat"].write(self.camera.matrix)
        self.sProgram["projectionMat"].write(self.camera.projection.tobytes())
        self.ctx.program
        self.ctx.screen.use()
        
        self.ctx.screen.clear(0.0, 0.0, 0.0, 1.0)
        self.ctx.enable(mgl.DEPTH_TEST)
        self.vao.render(mgl.TRIANGLES)
        
        
        
    def on_mouse_position_event(self, x, y, dx, dy):
        self.mousePos = (x,y)

    def on_key_event(self, key, action, modifiers):
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