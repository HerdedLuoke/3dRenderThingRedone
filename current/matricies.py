import math
import numpy as np
from numpy.typing import NDArray
from dataclasses import dataclass



# these could be moved into a larger class and i prob should but erm these used to be WAY bigger and got this tiny as
# i slowly neutered their features and now theyre just radians dawg
@dataclass(slots=True)
class pitch:
    radians: float


@dataclass(slots=True)
class yaw:
    radians: float


@dataclass(slots=True)
class roll:
    radians: float


@dataclass(slots=True)
class rotation:
    pitch: pitch
    yaw: yaw
    roll: roll


@dataclass(slots=True)
class position:
    xPosition: float = 0
    yPosition: float = 0
    zPosition: float = 0


@dataclass(slots=True)
class scale:
    xScale: float = 1
    yScale: float = 1
    zScale: float = 1


@dataclass(slots=True)
class modelmatrix:
    @property
    def xPosition(self) -> float:
        return self.__position.xPosition

    @property
    def yPosition(self) -> float:
        return self.__position.yPosition

    @property
    def zPosition(self) -> float:
        return self.__position.zPosition
    
    __position: position
    __rotation: rotation
    __scale: scale

    @property
    def matrix(self) -> NDArray:
        """Container for the position, rotation and scale data"""
        # im so glad ive stopped storing random shit as self. wtf was i doing
        # everything is just stored here and used to OUTPUT a matrix based on the inputs. 
        # this is done to as a pointless way to reduce memory use + computation time vs storing them and remaking 1 by 1 then doing matrix math
        # i stored repeated stuff in the formula to save .000000001 seconds :3
        # using the formula is also better as it gives more consistent results since matrix mult is not communitive (i think thats the term)
        

        xPosition = self.__position.xPosition
        yPosition = self.__position.yPosition
        zPosition = self.__position.zPosition

        xScale = self.__scale.xScale
        yScale = self.__scale.yScale
        zScale = self.__scale.zScale

        pitchRadians = self.__rotation.pitch.radians
        yawRadians = self.__rotation.yaw.radians
        rollRadians = self.__rotation.roll.radians

        sinPitch = math.sin(pitchRadians)
        cosPitch = math.cos(pitchRadians)

        sinYaw = math.sin(yawRadians)
        cosYaw = math.cos(yawRadians)

        sinRoll = math.sin(rollRadians)
        cosRoll = math.cos(rollRadians)
        
        cosPitchSinRoll = cosPitch * sinRoll
        sinPitchCosRoll = sinPitch * cosRoll
        cosPitchCosRoll = cosPitch * cosRoll
        sinPitchSinRoll = sinPitch * sinRoll
        cosYawZScale    = cosYaw * zScale
        sinYawZScale    = sinYaw * zScale

        # thanks wikipedia for this disgusting thing
        return np.array([
            [                             cosYaw * cosRoll * xScale,                             -cosYaw * sinRoll * yScale,             sinYawZScale, xPosition],
            [ (sinYaw * sinPitchCosRoll + cosPitchSinRoll) * xScale, (-sinYaw * sinPitchSinRoll + cosPitchCosRoll) * yScale, -sinPitch * cosYawZScale, yPosition],
            [(-sinYaw * cosPitchCosRoll + sinPitchSinRoll) * xScale,  (sinYaw * cosPitchSinRoll + sinPitchCosRoll) * yScale,  cosPitch * cosYawZScale, zPosition],
            [                                                     0,                                                      0,                        0,         1]])
    

    def updateLocalX(self,xPosition):
        """Update the X location."""
        self.__position.xPosition = xPosition

    def updateLocalY(self,yPosition):
        """Update the Y location."""
        self.__position.yPosition = yPosition

    def updateLocalZ(self,zPosition):
        """Update the Z location."""
        self.__position.zPosition = zPosition
        

    def updatePitch(self,radians:float):
        """Update the pitch rotation."""
        self.__rotation.pitch.radians = radians

    def updateYaw(self,radians:float):
        """Update the yaw rotation."""
        self.__rotation.yaw.radians = radians

    def updateRoll(self,radians:float):
        """Update the roll rotation."""
        self.__rotation.roll.radians = radians
        

    def updateScaleX(self,xScale):
        """Update the X scaling."""
        self.__scale.xScale = xScale

    def updateScaleY(self,yScale):
        """Update the Y scaling"""
        self.__scale.yScale = yScale

    def updateScaleZ(self,zScale):
        """Update the Z scaling."""
        self.__scale.zScale = zScale
        
    def byteForm(self, matrix):
        """returns matrix in byte form. to encourage not recomputing it per frame, it should be sent an external input."""
        return matrix.transpose().astype("f4").tobytes()