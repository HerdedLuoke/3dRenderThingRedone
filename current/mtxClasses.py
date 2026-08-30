
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
        
