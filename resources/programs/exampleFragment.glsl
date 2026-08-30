#version 330

#ifdef FRAGMENT_SHADER



out vec4 fragColor;


float distance = sqrt(pow((gl_FragCoord.x/700) - 0.5,2) + pow((gl_FragCoord.y/700) - 0.5,2) + abs(gl_FragCoord.z - 0.2));
float color = (1-(distance));
void main()
{ 
    
    
    fragColor = vec4(color,color,color,1.0);
    
    
}

#endif