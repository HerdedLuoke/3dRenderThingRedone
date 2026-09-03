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

from matricies import modelmatrix, position, rotation, pitch, yaw, roll, scale
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
            self.wnd.keys.NUMBER_1: lambda: self.deform(),
        }
        
        # lambda is black magic bro
        self.stopDict = {
            self.wnd.keys.W: lambda: self.camera.move_forward(False),
            self.wnd.keys.A: lambda: self.camera.move_left(False),
            self.wnd.keys.S: lambda: self.camera.move_backward(False),
            self.wnd.keys.D: lambda: self.camera.move_right(False),
            self.wnd.keys.LEFT_SHIFT: lambda: self.camera.move_down(False),

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
        
        self.cubeVertices = np.array([*triangle1.vertices, *triangle2.vertices, *triangle3.vertices, *triangle4.vertices, *triangle5.vertices, *triangle6.vertices, *triangle7.vertices, *triangle8.vertices, *triangle9.vertices, *triangle10.vertices, *triangle11.vertices, *triangle12.vertices], dtype=np.float32)

        self.cubevbo = self.ctx.buffer(self.cubeVertices.astype('f4').tobytes())
        self.cubeMesh = meshC(self.cubeVertices, self.cubevbo)
        
        triangle100 = triangle([-1, -1,  1, 1], [ 1, -1,  1, 1], [ 1, -1, -1, 1])
        triangle200 = triangle([-1, -1,  1, 1], [-1, -1, -1, 1], [ 1, -1, -1, 1])
        
        self.triangle = triangle([-1, -1,  1, 1], [ 1, -1,  1, 1], [ 1, -1, -1, 1])

        
        self.floorverts = np.array([*triangle100.vertices, *triangle200.vertices])
        self.floorvbo = self.ctx.buffer(self.floorverts.astype('f4').tobytes())
        self.floorMesh = meshC(self.floorverts, self.floorvbo)
        
        
        cubeModelMatrix =  modelmatrix(position(-10,10,-2), rotation(pitch(0), yaw(0), roll(0)), scale(10,10,10))
        cube2ModelMatrix = modelmatrix(position(-2,10,-10), rotation(pitch(0), yaw(0), roll(0)), scale(10,10,10))



        tileSize = 1
        xScale, yScale = tileSize/2,tileSize/2
        
        floorModelMatrix = modelmatrix(position(0,0,0), rotation(pitch(0), yaw(0), roll(0)), scale(xScale,1,yScale))
        tileModelMatrix = modelmatrix(position(tileSize,0,0), rotation(pitch(0), yaw(0), roll(0)), scale(xScale,1,yScale))
        tile2ModelMatrix = modelmatrix(position(-tileSize,0,0), rotation(pitch(0), yaw(0), roll(0)), scale(xScale,1,yScale))
        tile3ModelMatrix = modelmatrix(position(0,0,tileSize), rotation(pitch(0), yaw(0), roll(0)), scale(xScale,1,yScale))
        tile4ModelMatrix = modelmatrix(position(0,0,-tileSize), rotation(pitch(0), yaw(0), roll(0)), scale(xScale,1,yScale))
        
        self.cube = renderObject(self, self.cubeMesh, cubeModelMatrix, "exampleVertex.glsl", "exampleFragment.glsl")
        self.cube2 = renderObject(self, self.cubeMesh, cube2ModelMatrix, "exampleVertex.glsl", "exampleFragment.glsl")
        self.floor = renderObject(self, self.floorMesh, floorModelMatrix, "exampleVertex.glsl", "exampleFragment.glsl")
        self.tile = renderObject(self, self.floorMesh, tileModelMatrix, "exampleVertex.glsl", "exampleFragment.glsl")
        self.tile2 = renderObject(self, self.floorMesh, tile2ModelMatrix, "exampleVertex.glsl", "exampleFragment.glsl")
        self.tile3 = renderObject(self, self.floorMesh, tile3ModelMatrix, "exampleVertex.glsl", "exampleFragment.glsl")
        self.tile4 = renderObject(self, self.floorMesh, tile4ModelMatrix, "exampleVertex.glsl", "exampleFragment.glsl")    

        self.wnd.mouse_exclusivity = True
        self.camera.mouse_sensitivity = 1
        self.framelimit = 1/60
        self.movelock = False
        self.jumpend = True
        self.jumpvel = 0
        self.i = 0
        
        evilModelMatrix = modelmatrix(position(self.camera.position[0], self.camera.position[1], self.camera.position[2]), rotation(pitch(0), yaw(0), roll(0)), scale(3,3,3))
        
        
        self.renderVertices = self.cubeVertices.copy()
        self.rendervbo = self.ctx.buffer(self.renderVertices.astype('f4').tobytes())
        self.renderMesh = meshC(self.renderVertices, self.rendervbo)
        
        self.render = renderObject(self, self.renderMesh, evilModelMatrix, "exampleVertex.glsl", "exampleFragment.glsl")
        
        self.lastframetime=0
        self.framedrop = 0
        
        
        self.identity = np.identity(4)
        
        self.tiles = [self.tile, self.tile2, self.tile3, self.tile4]
        
         
    def on_render(self, time: float, frametime: float):
        debug = True
        self.windowMatrix = np.array(self.camera.projection.matrix * self.camera.matrix)
        
        self.sleeptime = self.framelimit - self.lastframetime

        if debug == True:
            if  self.sleeptime > 0:
                if frametime < 0.0001:
                    #print("Total extra verts: ") 
                    #print(np.size(self.renderVertices))

                    #print("Last frametime: ") 
                    #print(self.lastframetime)
                    #self.addRender()
                    pass
                else:
                    
                    timey.sleep(self.sleeptime)
                    #print("slept: " + str(self.sleeptime))
                
            else: 
                #print("Dropped Frame: ")
                self.framedrop += 1
                #print(self.framedrop)
                #print("Dropped frametime: ") 
                #print(self.lastframetime)

        
        
        self.net = np.array([math.pi/90, math.pi/90]) + self.i*np.array([math.pi/90, math.pi/90])

        self.cube.setRadians(pitch=self.net[0], yaw=self.net[1])
        self.cube2.setRadians(pitch=self.net[1], yaw=self.net[0])
        
        #self.render.setRadians(pitch=self.net[0], yaw=self.net[1])

        self.i += 1
        
        #self.render.shader["projectionMat"].write((self.windowMatrix @ self.render.modelMatrix).transpose().astype('f4').tobytes())
        #self.render.shader["colordata"].write(np.array([1,0,0,1]).astype('f4').tobytes())
        self.cube.shader["projectionMat"].write((self.windowMatrix @ self.cube.modelMatrix).transpose().astype('f4').tobytes())
        self.cube.shader["colordata"].write(np.array([1,0,0,1]).astype('f4').tobytes()) 
        self.cube2.shader["projectionMat"].write((self.windowMatrix @ self.cube2.modelMatrix).transpose().astype('f4').tobytes())
        self.cube2.shader["colordata"].write(np.array([0,1,0,1]).astype('f4').tobytes())
        self.floor.shader["projectionMat"].write((self.windowMatrix @ self.floor.modelMatrix).transpose().astype('f4').tobytes())
        self.floor.shader["colordata"].write(np.array([0,0,1,1]).astype('f4').tobytes())
        
        
        
        
        
        firsttile = 0
        last = 0
        
        
        
        
        
        
        for tile in self.tiles:
            tile.shader["projectionMat"].write((self.windowMatrix @ tile.modelMatrix).transpose().astype('f4').tobytes())

                
                
    
        
        self.tile.shader["colordata"].write(np.array([1,0,0,1]).astype('f4').tobytes())
        self.tile2.shader["colordata"].write(np.array([1,0,0,1]).astype('f4').tobytes())
        self.tile3.shader["colordata"].write(np.array([0,1,0,1]).astype('f4').tobytes())
        self.tile4.shader["colordata"].write(np.array([0,1,0,1]).astype('f4').tobytes())
        
        
        firsttile = 0
        self.ctx.screen.use()
        
        self.ctx.screen.clear(0.0, 0.0, 0.0, 1.0)
        self.ctx.enable(mgl.DEPTH_TEST)
   
        #self.cube.vao.render(mgl.TRIANGLES)
        #self.cube2.vao.render(mgl.TRIANGLES)
        self.floor.vao.render(mgl.TRIANGLES)
        #self.render.vao.render(mgl.TRIANGLES)
        
        self.tile.vao.render(mgl.TRIANGLES)
        self.tile2.vao.render(mgl.TRIANGLES)
        self.tile3.vao.render(mgl.TRIANGLES)
        self.tile4.vao.render(mgl.TRIANGLES)
            
        self.lastframetime = frametime
      
      
      
      
      
      
      
      
      
      
      
      
      
      
    def deform(self):
        num = np.dot(np.append((self.camera.dir/np.linalg.norm(np.array(self.camera.dir))),0), self.triangle.directionV)
        print(num)
        if num >= -1 and num <= 0.1:
        
            self.floor.setPosition(y=self.tile.ypos-0.5) 
            #print("secondary")
            #print(self.camera.dir)
            self.floor.shader["projectionMat"].write((self.windowMatrix @ self.tile.modelMatrix).transpose().astype('f4').tobytes())
            #self.tile.setPosition(y=self.tile.ypos+0.5) 
        elif num <= 1.0 and num >= -0.1:
            self.floor.setPosition(y=self.tile.ypos+0.5)  
            #print("secondary")
            #print(self.camera.dir)
            self.floor.shader["projectionMat"].write((self.windowMatrix @ self.tile.modelMatrix).transpose().astype('f4').tobytes())
            
        else:
            self.floor.shader["projectionMat"].write((self.windowMatrix @ self.tile.modelMatrix).transpose().astype('f4').tobytes())
        
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
                self.cube.instanceShader("exampleVertex.glsl", "exampleFragment.glsl")
                
            elif key == self.wnd.keys.F:
                self.movelock, self.wnd.mouse_exclusivity = self.wnd.mouse_exclusivity, self.movelock
                # im proud of this lol
                
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