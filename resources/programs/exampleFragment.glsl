#version 330

#ifdef FRAGMENT_SHADER


out vec4 fragColor;

uniform vec4 colordata;

float distance = sqrt(pow((gl_FragCoord.x/700) - 0.5,2) + pow((gl_FragCoord.y/700) - 0.5,2) + abs(gl_FragCoord.z - 0.2));
float color = (1-(pow(distance,10) * colordata.w));
float colormod = (0.5 + 0.5*colordata.w);
vec4 colorOut = vec4(colormod * colordata.x * color, colormod * colordata.y * color, colormod * colordata.z * color, colormod);
void main()
{ 
    
    
    fragColor = colorOut;
    
    
}

#endif