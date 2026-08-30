#version 330

#ifdef VERTEX_SHADER


in vec3 in_vert;


void main()
{
    gl_Position = vec4(in_vert, 1.0);
}

#endif
