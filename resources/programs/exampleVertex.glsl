#version 330

#ifdef VERTEX_SHADER


in vec4 in_vert;


uniform mat4 modelMat; 
uniform mat4 cameraMat; 
uniform mat4 projectionMat; 


void main()
{
    
    gl_Position = projectionMat * cameraMat * modelMat * in_vert;

}


#endif
