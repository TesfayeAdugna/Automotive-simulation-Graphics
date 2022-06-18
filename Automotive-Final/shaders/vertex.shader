#version 330 core

layout(location = 0) in vec3 v_pos;
layout(location = 1) in vec2 texture;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

out vec2 v_tex;

void main()
{
gl_Position = projection * view * model * vec4(v_pos, 1);
v_tex = texture;
}