        


import numpy as np
from numpy.typing import NDArray
    
    
class triangle:
    @property
    def vertices(self):
        "this returns the list of verticies in a continous style cuz buffer perfers that"
        return np.ascontiguousarray([*self.__vertex1, *self.__vertex2, *self.__vertex3],dtype=np.float32, )
        # triangles can be combined via this method for larger constructs by hand
    def __init__(self, vertex1:tuple[float, float, float, float] | list[float, float, float, float] |  NDArray, vertex2: tuple[float, float, float, float] | list[float, float, float, float] |  NDArray, vertex3:tuple[float, float, float, float] | list[float, float, float, float] |  NDArray):
        self.__vertex1 = np.asarray(vertex1)
        self.__vertex2 = np.asarray(vertex2)
        self.__vertex3 = np.asarray(vertex3)
    