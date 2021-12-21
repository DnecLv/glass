from tools.camera import mouse_look_clb,mouse_enter_clb,key_input_clb,do_movement
import pyrr
from tools.init import *
from OpenGL.GL.shaders import compileShader, compileProgram

vertex_src = '''
# version 330

void main()
{
    gl_Position = model * vec4(a_position, 1.0);
}
'''

fragment_src = '''
# version 330

void main()
{
}
'''

window = init()
glfwSetCursorPosCallback(window, mouse_look_clb)
glfwSetCursorEnterCallback(window, mouse_enter_clb)
glfwSetKeyCallback(window, key_input_clb)
glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_HIDDEN)
glEnable(GL_DEPTH_TEST)

while not glfwWindowShouldClose(window):
    glfwPollEvents()
    do_movement()
    glClearColor(0.1, 0.1, 0.1, 0.1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
glfwTerminate()