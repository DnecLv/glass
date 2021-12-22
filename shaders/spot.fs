#version 330

in vec3 Normal;
in vec3 FragPos;
in vec2 TexCoords;

out vec4 fColor;

uniform vec3 lightPos;
uniform vec3 viewPos;
uniform vec3 lightColor;
uniform vec3 objectColor;
uniform int switcher;

uniform sampler2D Texture1;

void main() {
    // Ambient
    float ambientStrength = 0.1f;
    vec3 ambient = ambientStrength * lightColor;

    // Diffuse 
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = lightColor * diff * vec3(texture(Texture1, TexCoords));

    // Specular
    float specularStrength = 0.5f;
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    // vec3 specular = specularStrength * spec * lightColor;
    vec3 specular = specularStrength * spec * lightColor * vec3(texture(Texture1, TexCoords));

    vec3 result = (ambient + diffuse + specular) * objectColor;

    if(switcher == 0) {
        fColor = vec4(result.r, 0.0, 0.0, 1.0);
    } else {
        fColor = vec4(0.0, result.g, result.b, 1.0);
    }
}