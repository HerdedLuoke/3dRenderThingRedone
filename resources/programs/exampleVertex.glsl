#version 330

#ifdef VERTEX_SHADER


in vec3 in_vert;

uniform mat4 modelMat; 
uniform mat4 cameraMat; 
uniform mat4 projectionMat; 

vec4 transVert = vec4(in_vert, 1);

void main()
{
    gl_Position = projectionMat * cameraMat * modelMat * transVert;
}


#endif
