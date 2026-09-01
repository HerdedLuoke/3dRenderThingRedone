import numpy as np
import math

from matricies import modelmatrix




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
        return self.modelMatrixObject.matrix

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

    def __init__(self, window: "Window", mesh: meshC, modelMatrixObject: modelmatrix, vertexProgram: str, fragmentProgram: str, computeProgram: str | None = None):
        self.window = window
        self.ctx = window.ctx
        self.mesh = mesh

        self.modelTransformObject = modelMatrixObject

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
            self.modelTransformObject.updateScaleX(x)
        if y != None:
            self.modelTransformObject.updateScaleY(y)
        if z != None:
            self.modelTransformObject.updateScaleX(z)

    def incrementScale(self, x=0, y=0, z=0):
        """
        Increase/Decrease the models current scale in (x,y,z) directions
        """
        if x != None:
            self.modelTransformObject.updateScaleX(x + self.modelTransformObject.__scale.xScale)
        if y != None:
            self.modelTransformObject.updateScaleY(z + self.modelTransformObject.__scale.yScale)
        if z != None:
            self.modelTransformObject.updateScaleZ(z + self.modelTransformObject.__scale.zScale)

    def setRadians(self, pitch=None, yaw=None, roll=None):
        """
        Set the models exact rotation in (p,y,r) radians
        """
        if pitch != None:
            self.modelTransformObject.updatePitch(pitch)
        if yaw != None:
            self.modelTransformObject.updateYaw(yaw)
        if roll != None:
            self.modelTransformObject.updateRoll(roll)

    def incrementRadians(self, pitch=0, yaw=0, roll=0):
        """
        Increase/Decrease the models current rotation in (p,y,r) radians
        """
        if pitch != None:
            self.modelTransformObject.updatePitch(pitch + self.modelTransformObject.__rotation.pitch)
        if yaw != None:
            self.modelTransformObject.updateYaw(yaw + self.modelTransformObject.__rotation.yaw)
        if roll != None:
            self.modelTransformObject.updateRoll(roll + self.modelTransformObject.__rotation.roll)

    def setPosition(self, x=None, y=None, z=None):
        """
        Set the models exact position in world (x,y,z)
        """
        if x != None:
            self.modelTransformObject.updateLocalX(x)
        if y != None:
            self.modelTransformObject.updateLocalY(y)
        if z != None:
            self.modelTransformObject.updateLocalZ(z)

    def incrementPosition(self, x=0, y=0, z=0):
        """
        Increase/Decrease the models current position in world (x,y,z)
        """
        if x != None:
            self.modelTransformObject.updateLocalX(x + self.modelTransformObject.__position.xPosition)
        if y != None:
            self.modelTransformObject.updateLocalY(y + self.modelTransformObject.__position.yPosition)
        if z != None:
            self.modelTransformObject.updateLocalZ(z + self.modelTransformObject.__position.zPosition)

    def release(self):
        if self.vao != None:
            self.vao.release()
            self.vao = None

        if self.shader != None:
            self.shader.release()
            self.shader = None