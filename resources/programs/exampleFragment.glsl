#version 330

#ifdef FRAGMENT_SHADER


out vec4 fragColor;

uniform vec4 colordata;

float distance = sqrt(pow((gl_FragCoord.x/700) - 0.5,2) + pow((gl_FragCoord.y/700) - 0.5,2) + abs(gl_FragCoord.z));
float color = 1- (0.5 *distance);

//vec4 colorOut = vec4(abs(sin(colormod * colordata.x * color + gl_FragCoord.x  + gl_FragCoord.z)), abs(cos(colormod * colordata.y * color + gl_FragCoord.y + gl_FragCoord.z)), colormod * colordata.z * color, colormod);

vec4 colorOut = vec4(color * colordata.x, color * colordata.y, color * colordata.z, 1.0);

void main()
{ 
    
    
    fragColor = colorOut;
    
    
}

#endif