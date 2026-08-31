import math
from pathlib import Path
import time as timey
import numpy as np
import moderngl as mgl
import moderngl_window as mgl_w
from geometry import triangle
from moderngl_window import resources
from moderngl_window.scene import KeyboardCamera
from moderngl_window.resources import programs, textures, data
from moderngl_window.meta import (TextureDescription, ProgramDescription, DataDescription)

from matricies import (scalingMtx, positionMtx, pitchMtx, yawMtx, rollMtx, rotationMtx)

from model import meshC, renderObject







# most below code is just for tests and will be nuked from orbit
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
        
        
        self.camera = KeyboardCamera(self.wnd.keys, fov=75.0, aspect_ratio=self.wnd.aspect_ratio, near=0.1, far=1000)
        
        self.actionDict = {
            self.wnd.keys.W: lambda: self.camera.move_forward(True),
            self.wnd.keys.A: lambda: self.camera.move_left(True),
            self.wnd.keys.S: lambda: self.camera.move_backward(True),
            self.wnd.keys.D: lambda: self.camera.move_right(True),
            self.wnd.keys.LEFT_SHIFT: lambda: self.camera.move_down(True),
            self.wnd.keys.SPACE: lambda: self.camera.move_up(True)
        }
        
                # lambda is black magic bro
        self.stopDict = {
            self.wnd.keys.W: lambda: self.camera.move_forward(False),
            self.wnd.keys.A: lambda: self.camera.move_left(False),
            self.wnd.keys.S: lambda: self.camera.move_backward(False),
            self.wnd.keys.D: lambda: self.camera.move_right(False),
            self.wnd.keys.LEFT_SHIFT: lambda: self.camera.move_down(False),
            self.wnd.keys.SPACE: lambda: self.camera.move_up(False)
        }
        
        resources.register_program_dir(Path.cwd() / "resources" / "programs")
        resources.register_data_dir(Path.cwd() / "resources" / "data")
        resources.register_texture_dir(Path.cwd() / "resources" / "textures")
       

        # TODO: Make a transformation matrix to make these automatically
        
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
        
        # TODO: END TODO HERE :3
        
        self.screenVertices = np.array([*triangle1.vertices, *triangle2.vertices, *triangle3.vertices, *triangle4.vertices, *triangle5.vertices, *triangle6.vertices, *triangle7.vertices, *triangle8.vertices, *triangle9.vertices, *triangle10.vertices, *triangle11.vertices, *triangle12.vertices], dtype=np.float32)

        self.vbo = self.ctx.buffer(self.screenVertices.astype('f4').tobytes())

        self.cubeMesh = meshC(self.screenVertices, self.vbo)

        self.cube = renderObject(self, self.cubeMesh, scalingMtx(0.5,0.5,0.5), positionMtx(2,0,-2), rotationMtx(pitchMtx(0), yawMtx(0), rollMtx(0)), "exampleVertex.glsl", "exampleFragment.glsl")
        self.cube2 = renderObject(self, self.cubeMesh, scalingMtx(0.5,0.5,0.5), positionMtx(-2,0,-2), rotationMtx(pitchMtx(0), yawMtx(0), rollMtx(0)), "exampleVertex.glsl", "exampleFragment.glsl")
        
        self.wnd.mouse_exclusivity = True
        self.camera.mouse_sensitivity =  1
        self.framelimit = 1/60
        self.movelock = False

    def on_render(self, time: float, frametime: float):
        
        sleeptime = self.framelimit - frametime
        if sleeptime > 0:
            timey.sleep(sleeptime)

        self.cube.incrementRadians(pitch=math.pi/2048, yaw=math.pi/2048)
        self.cube2.incrementRadians(pitch=math.pi/2048, yaw=math.pi/2048)
        
        self.cube.shader["modelMat"].write(self.cube.modelMatrixBytes)
        self.cube.shader["cameraMat"].write(self.cube.cameraMatrixBytes)
        self.cube.shader["projectionMat"].write(self.cube.projectionMatrixBytes)
        self.cube.shader["colordata"].write(np.array([1,0,0,1]).astype('f4').tobytes()) 
        # TODO: ^ this should be sent with the vao since it doesnt change
        
        self.cube2.shader["modelMat"].write(self.cube2.modelMatrixBytes)
        self.cube2.shader["cameraMat"].write(self.cube2.cameraMatrixBytes)
        self.cube2.shader["projectionMat"].write(self.cube2.projectionMatrixBytes)
        self.cube2.shader["colordata"].write(np.array([0,1,0,1]).astype('f4').tobytes())
        
        self.ctx.screen.use()
        
        self.ctx.screen.clear(0.0, 0.0, 0.0, 1.0)
        self.ctx.enable(mgl.DEPTH_TEST)

        self.cube.vao.render(mgl.TRIANGLES)
        self.cube2.vao.render(mgl.TRIANGLES)
    

        
    
        
        
    def on_mouse_position_event(self, x, y, dx, dy):
        if self.movelock == False:
            self.camera.rot_state(-dx,-dy)
            
            
        
        
        


    def on_key_event(self, key, action, modifiers):
        if action == self.wnd.keys.ACTION_PRESS:
            function = self.actionDict.get(key)

            if function != None:
                if self.movelock == False:  
                    function()
                
            elif key == self.wnd.keys.R:
                self.cube.shaderUpdate()
                
            elif key == self.wnd.keys.F:
                self.movelock, self.wnd.mouse_exclusivity = self.wnd.mouse_exclusivity, self.movelock
                # swaps their states
                
                
        elif action == self.wnd.keys.ACTION_RELEASE:
            function = self.stopDict.get(key)
            if function != None:
                function()
                
        return super().on_key_event(key, action, modifiers)


    def importProgram(self, vertexProgram: str | None=None, fragmentProgram: str | None=None, computeProgram: str | None=None):
        program = programs.load(ProgramDescription(vertex_shader=vertexProgram, fragment_shader=fragmentProgram, compute_shader=computeProgram))
        return program
    

    def importData(self, name, myType):
        dataFile = data.load(DataDescription(path=name, kind=myType))
        return dataFile
    

    def importTexture(self, name, myType):
        texture = textures.load(TextureDescription(path=name, kind=myType))
        return texture
    

    def moveCube(self, x:float=0, y:float=0, z:float=0):
        self.cube.incrementPosition(x=x, y=y, z=z)
        
    def rotateX(self, p=math.pi/64):
        self.cube.incrementRadians(pitch=p)


    def rotateY(self, y=math.pi/64):
        self.cube.incrementRadians(yaw=y)

    def rotateZ(self, r=math.pi/64):
        self.cube.incrementRadians(roll=r)