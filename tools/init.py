from glfw.GLFW import *
from OpenGL.GL import *
import numpy as np

height = 720
width = 1280
def init():
    # initial glfw library
    
    if not glfwInit():
        raise Exception("glfwInit error")

    # * 四倍抗锯齿
    # glfwWindowHint(GLFW_SAMPLES, 4)
    # create window
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)

    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE)
    
    window = glfwCreateWindow(width, height, "My OpenGL Window", None, None)

    # set the positon
    glfwSetWindowPos(window, 400, 200)
    # make the context current
    glfwMakeContextCurrent(window)
    # resize when the window changes
    def window_resize(window, width, height):
        glViewport(0, 0, width, height)

    glfwSetWindowSizeCallback(
        window,
        lambda window, width, height: glViewport(0, 0, width, height)
    )
    return window

# while not glfwWindowShouldClose(window):
#     # 检查事件
#     glfwPollEvents()

#     # 交换缓冲
#     glfwSwapBuffers(window)

# glfwTerminate()


def glDeliverFunc(func, programe, name, value):
    func(
        glGetUniformLocation(programe, name), 1, GL_FALSE, value
    )


def readShader(s):
    t = ''
    with open(s, 'r',encoding='UTF-8') as f:
        t += f.read()
    return t
