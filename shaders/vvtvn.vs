# version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec3 normal;
layout (location = 2) in vec2 aTexCoords;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

out vec3 Normal;
out vec3 FragPos;
out vec2 TexCoords;

void main()
{
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    FragPos = vec3(model * vec4(a_position, 1.0));
    Normal = mat3(transpose(inverse(model))) * normal;
    TexCoords = aTexCoords;
    // Normal = normal;
}