#version 330

#ifdef VERTEX_SHADER


in vec4 in_vert;
 
uniform mat4 projectionMat; 


void main()
{
    
    gl_Position = projectionMat * in_vert;

}


#endif
