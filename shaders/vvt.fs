#version 330
in vec2 v_texture;

out vec4 fColor;

uniform sampler2D s_texture;
uniform int switcher;

void main()
{
    vec4 result = texture(s_texture, v_texture);
    if(switcher == 0) {
        fColor = vec4(result.r, 0.0, 0.0, 1.0);
    } else {
        fColor = vec4(0.0, result.g, result.b, 1.0);
    }
}

