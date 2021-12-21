#version 330 core
out vec4 FragColor;

in vec2 TexCoords;

uniform sampler2D screenTexture1;
uniform sampler2D screenTexture2;

void main()
{ 
    FragColor = vec4(texture(screenTexture1, TexCoords)[0],texture(screenTexture2, TexCoords)[1],texture(screenTexture2, TexCoords)[2], 1.0);
    // FragColor = texture(screenTexture1, TexCoords);
    // FragColor = texture(screenTexture2, TexCoords);
    // FragColor = mix(texture(screenTexture1, TexCoords), texture(screenTexture2, TexCoords), 0.2);
}