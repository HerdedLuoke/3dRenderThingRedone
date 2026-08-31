import numpy as np
import math

from matricies import scalingMtx, positionMtx, rotationMtx




class meshC:
    """
    Contains the vbo and verts for an object
    (also uv/textures once i get there)
    """

    # this contains geometry shared between renderObjects
    # shader and vao are handled in obejct
    def __init__(self, vertices, vbo):
        self.vertices = vertices
        self.vbo = vbo


class renderObject:
    """
    Contains the mesh data for an object, as well as its associated transformations.
    Also contains its own shader and vao.
    """

    @property
    def modelMatrix(self):
        return (self.positionMatrix @ self.rotationMatrix) @ self.scaleMatrix.mtx

    @property
    def cameraMatrix(self):
        return np.frombuffer(self.window.camera.matrix, dtype="f4").reshape((4,4))

    @property
    def projectionMatrix(self):
        return self.window.camera.projection

    @property
    def projectionMatrixBytes(self):
        return self.window.camera.projection.tobytes()

    @property
    def modelMatrixBytes(self):
        return self.modelMatrix.transpose().astype("f4").tobytes()

    @property
    def cameraMatrixBytes(self):
        return self.window.camera.matrix

    def __init__(self, window: "Window", imesh: meshC, scaleMatrix: scalingMtx, positionMatrix: positionMtx, rotationMatrix: rotationMtx, vertexProgram: str, fragmentProgram: str, computeProgram: str | None = None):
        self.window = window
        self.ctx = window.ctx
        self.mesh = imesh

        self.positionMatrix = positionMatrix
        self.scaleMatrix = scaleMatrix
        self.rotationMatrix = rotationMatrix

        self.vertexProgram = vertexProgram
        self.fragmentProgram = fragmentProgram
        self.computeProgram = computeProgram

        self.shader = None
        self.vao = None

        self.shaderUpdate()

    def shaderUpdate(self):
        """
        Reload this objects shader and regenerate its vao.
        """

        if self.vao != None:
            self.vao.release()

        if self.shader != None:
            self.shader.release()

        # my first memory leak resulted in me learning to release resources! yay!

        self.shader = self.window.importProgram(self.vertexProgram, self.fragmentProgram, self.computeProgram)
        self.vao = self.ctx.simple_vertex_array(self.shader, self.mesh.vbo, "in_vert")

    def setScale(self, x=None, y=None, z=None):
        """
        Set the models exact scale in (x,y,z) directions
        """
        if x != None:
            self.scaleMatrix.x = x
        if y != None:
            self.scaleMatrix.y = y
        if z != None:
            self.scaleMatrix.z = z

    def incrementScale(self, x=0, y=0, z=0):
        """
        Increase/Decrease the models current scale in (x,y,z) directions
        """
        self.scaleMatrix.x += x
        self.scaleMatrix.y += y
        self.scaleMatrix.z += z

    def setRadians(self, pitch=None, yaw=None, roll=None):
        """
        Set the models exact rotation in (p,y,r) radians
        """
        if pitch != None:
            self.rotationMatrix.pitch.radians = pitch
        if yaw != None:
            self.rotationMatrix.yaw.radians = yaw
        if roll != None:
            self.rotationMatrix.roll.radians = roll

    def incrementRadians(self, pitch=0, yaw=0, roll=0):
        """
        Increase/Decrease the models current rotation in (p,y,r) radians
        """
        self.rotationMatrix.pitch.radians = (self.rotationMatrix.pitch.radians + pitch) % (2 * math.pi)
        self.rotationMatrix.yaw.radians = (self.rotationMatrix.yaw.radians + yaw) % (2 * math.pi)
        self.rotationMatrix.roll.radians = (self.rotationMatrix.roll.radians + roll) % (2 * math.pi)

    def setPosition(self, x=None, y=None, z=None):
        """
        Set the models exact position in world (x,y,z)
        """
        if x != None:
            self.positionMatrix.x = x
        if y != None:
            self.positionMatrix.y = y
        if z != None:
            self.positionMatrix.z = z

    def incrementPosition(self, x=0, y=0, z=0):
        """
        Increase/Decrease the models current position in world (x,y,z)
        """
        self.positionMatrix.x += x
        self.positionMatrix.y += y
        self.positionMatrix.z += z

    def release(self):
        if self.vao != None:
            self.vao.release()
            self.vao = None

        if self.shader != None:
            self.shader.release()
            self.shader = None