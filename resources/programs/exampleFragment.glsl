#version 330

#ifdef FRAGMENT_SHADER


out vec4 fragColor;

uniform vec4 colordata;

float distance = sqrt(pow((gl_FragCoord.x/700) - 0.5,2) + pow((gl_FragCoord.y/700) - 0.5,2) + abs(gl_FragCoord.z - 0.2));
float color = (1-distance);

vec4 colorOut = vec4(colordata.x * color + 0.5, colordata.y * color, colordata.z * color, 1 * color);
void main()
{ 
    
    
    fragColor = colorOut;
    
    
}

#endif