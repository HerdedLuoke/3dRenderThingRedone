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
    def xpos(self): 
        return self.__modelTransformObject.xPosition 

    @property 
    def ypos(self): 
        return self.__modelTransformObject.yPosition 

    @property 
    def zpos(self): 
        return self.__modelTransformObject.zPosition 


    @property
    def xscale(self): 
        return self.__modelTransformObject.xScale 

    @property
    def yscale(self): 
        return self.__modelTransformObject.yScale 

    @property
    def zscale(self): 
        return self.__modelTransformObject.zScale 


    @property
    def pitch(self): 
        return self.__modelTransformObject.pitch 

    @property
    def yaw(self): 
        return self.__modelTransformObject.yaw 

    @property
    def roll(self): 
        return self.__modelTransformObject.roll



    @property
    def shader(self):
        return self.__shader

    @property
    def vao(self):
        return self.__vao



    @property
    def modelMatrixBytes(self):
        matrix = self.__modelTransformObject.matrix
        return self.__modelTransformObject.byteForm(matrix)
    @property
    def modelMatrix(self):
        return self.__modelTransformObject.matrix


    def __init__(self, window, mesh: meshC, modelMatrixObject: modelmatrix, vertexProgram: str, fragmentProgram: str, computeProgram: str | None = None):

        self.__window = window
        self.__vbo = mesh.vbo
        self.__modelTransformObject = modelMatrixObject

        self.__shader = None
        self.__vao = None

        self.instanceShader(vertexProgram, fragmentProgram, computeProgram)



    def instanceShader(self, vertexProgram: str, fragmentProgram: str, computeProgram: str | None = None):

        """
        Instance this objects shader and regenerate its vao.
        """

        if self.__vao != None:
            self.__vao.release()

        if self.__shader != None:
            self.__shader.release()

        # my first memory leak resulted in me learning to release resources! yay!

        self.__shader = self.__window.importProgram(vertexProgram, fragmentProgram, computeProgram)
        self.__vao = self.__window.ctx.simple_vertex_array(self.__shader, self.__vbo, "in_vert")



    def setScale(self, x=None, y=None, z=None):

        """
        Set the models exact scale in (x,y,z) directions
        """

        if x != None:
            self.__modelTransformObject.updateScaleX(x)

        if y != None:
            self.__modelTransformObject.updateScaleY(y)

        if z != None:
            self.__modelTransformObject.updateScaleZ(z)



    def setRadians(self, pitch=None, yaw=None, roll=None):

        """
        Set the models exact rotation in (p,y,r) radians
        """

        if pitch != None:
            self.__modelTransformObject.updatePitch(pitch)

        if yaw != None:
            self.__modelTransformObject.updateYaw(yaw)

        if roll != None:
            self.__modelTransformObject.updateRoll(roll)



    def setPosition(self, x=None, y=None, z=None):

        """
        Set the models exact position in world (x,y,z)
        """

        if x != None:
            self.__modelTransformObject.updateLocalX(x)

        if y != None:
            self.__modelTransformObject.updateLocalY(y)

        if z != None:
            self.__modelTransformObject.updateLocalZ(z)



    def release(self):

        if self.__vao != None:
            self.__vao.release()
            self.__vao = None

        if self.__shader != None:
            self.__shader.release()
            self.__shader = None