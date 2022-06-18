#version 330 core

out vec4 out_color;
in vec2 v_tex;
uniform sampler2D s_tex;

void main()
{
out_color = texture(s_tex, v_tex);
}