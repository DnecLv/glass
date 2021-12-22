# python 3.7.3
# -*- coding:UTF-8 -*-
# AUTHOR: DnecLv
# FILE: C:\Users\Dnec\Desktop\glasses\glass_withTex.py
# DATE: 2021/12/22 周三
# TIME: 09:39:36

# DESCRIPTION:


from tools.camera import mouse_look_clb, mouse_enter_clb, key_input_clb, do_movement, cam, mouse_button_callback
import pyrr
from tools.init import *
from OpenGL.GL.shaders import compileShader, compileProgram
from tools.ezObjLoader import ObjLoader
from PIL import Image


def defaultTex(file):
    name = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, name)
    image = Image.open(file)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)  # 上下对换
    img_data = image.convert("RGB").tobytes()  # RGBA AND 二进制图
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width,
                 image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glGenerateMipmap(GL_TEXTURE_2D)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                    GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return name

# ------------------------------------ 主程 ------------------------------------ #


window = init()
glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
glfwSetCursorPosCallback(window, mouse_look_clb)
glfwSetMouseButtonCallback(window, mouse_button_callback)
glfwSetKeyCallback(window, key_input_clb)
glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_NORMAL)

# ----------------------------------- 资源管理 ----------------------------------- #

obj1 = ObjLoader()
obj1.load_model("res/spot/spot_triangulated_good.obj")
shader = compileProgram(
    compileShader(readShader(
        'shaders/spot.vs'), GL_VERTEX_SHADER),
    compileShader(readShader(
        'shaders/spot.fs'), GL_FRAGMENT_SHADER)
)
screenShader = compileProgram(
    compileShader(readShader(
        'shaders/mix.vs'), GL_VERTEX_SHADER),
    compileShader(readShader(
        'shaders/mix.fs'), GL_FRAGMENT_SHADER)
)

tex = defaultTex("res/spot/spot_texture.png")
tex_offset = len(obj1.vertex_index) * 12


# --------------------------- 设置两个framebuffer来存储红蓝 --------------------------- #

# * 创建纹理
PartMap = glGenTextures(2)
for i in range(2):
    glBindTexture(GL_TEXTURE_2D, PartMap[i])
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                 0, GL_RGB, GL_UNSIGNED_BYTE, None)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

# * 创建帧缓冲 并绑定纹理
PartMapFBO = glGenFramebuffers(2)
for i in range(2):
    glBindFramebuffer(GL_FRAMEBUFFER, PartMapFBO[i])
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0,
                           GL_TEXTURE_2D, PartMap[i], 0)
    # * 为帧缓冲创建深度缓冲
    RBO = glGenRenderbuffers(1)
    glBindRenderbuffer(GL_RENDERBUFFER, RBO)
    glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, 1280, 720)
    glBindRenderbuffer(GL_RENDERBUFFER, 0)
    glFramebufferRenderbuffer(
        GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, RBO)
    glBindRenderbuffer(GL_RENDERBUFFER, 0)

glBindTexture(GL_TEXTURE_2D, 0)
glBindFramebuffer(GL_FRAMEBUFFER, 0)

# --------------------------------- 渲染牛牛 -------------------------------- #

objVAO = glGenVertexArrays(1)
objVBO = glGenBuffers(1)
glBindVertexArray(objVAO)
glBindBuffer(GL_ARRAY_BUFFER, objVBO)
glBufferData(GL_ARRAY_BUFFER, obj1.model.itemsize * len(obj1.model),
             obj1.model, GL_STATIC_DRAW)
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                      obj1.model.itemsize * 3, ctypes.c_void_p(0))
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,
                      obj1.model.itemsize * 3, ctypes.c_void_p(len(obj1.vertex_index) * 12))
glEnableVertexAttribArray(2)
glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE,
                      obj1.model.itemsize * 2, ctypes.c_void_p(len(obj1.vertex_index) * 24))

# --------------------------------- 渲染用四边形 -------------------------------- #
quadVertices = [
    -1.0,  1.0,  0.0, 1.0,  # [posx,posy,tex_x,tex_y]
    -1.0, -1.0,  0.0, 0.0,
    1.0, -1.0,  1.0, 0.0,

    -1.0,  1.0,  0.0, 1.0,
    1.0, -1.0,  1.0, 0.0,
    1.0,  1.0,  1.0, 1.0
]
quadVertices = np.array(quadVertices, dtype=np.float32)

quadVAO = glGenVertexArrays(1)
quadVBO = glGenBuffers(1)
glBindVertexArray(quadVAO)
glBindBuffer(GL_ARRAY_BUFFER, quadVBO)
glBufferData(GL_ARRAY_BUFFER, quadVertices.nbytes,
             quadVertices, GL_STATIC_DRAW)
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE,
                      quadVertices.itemsize * 4, ctypes.c_void_p(0))
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
                      quadVertices.itemsize * 4, ctypes.c_void_p(quadVertices.itemsize * 2))

# ----------------------------------- 全局参数 ----------------------------------- #
projection = pyrr.matrix44.create_perspective_projection_matrix(
    45, 1280/720, 0.1, 100)

glUseProgram(shader)
glDeliverFunc(glUniformMatrix4fv, shader,
              "projection", projection)

glUseProgram(screenShader)
glUniform1i(glGetUniformLocation(screenShader, "screenTexture1"), 0)
glUniform1i(glGetUniformLocation(screenShader, "screenTexture2"), 1)

# flag = 0
# ------------------------------------ 循环 ------------------------------------ #
while not glfwWindowShouldClose(window):

    glfwPollEvents()

    do_movement()
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 0.0)

    glUseProgram(shader)
    glBindVertexArray(objVAO)

    # 旋转矩阵,绕y轴旋转,绕x/z用from_x_rotation/from_z_rotation
    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfwGetTime())
    # rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfwGetTime())
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, tex)
    glDeliverFunc(glUniformMatrix4fv, shader,
                  "model", rot_y)
    # 使用标准model矩阵
    # glDeliverFunc(glUniformMatrix4fv, shader,
    #               "model", pyrr.Matrix44.identity())
    objectColor_loc = glGetUniformLocation(shader, "objectColor")
    lightColor_loc = glGetUniformLocation(shader, "lightColor")
    lightPosLoc = glGetUniformLocation(shader, "lightPos")
    viewPosLoc = glGetUniformLocation(shader, "viewPos")
    switcher_loc = glGetUniformLocation(shader, "switcher")
    glUniform3f(objectColor_loc, 1.0, 0.5, 0.31)
    glUniform3f(lightColor_loc, 1.0, 1.0, 1.0)
    glUniform3f(lightPosLoc, 2.0, 2.0, 2.0)

    # * 左眼渲染 只写入R
    glBindFramebuffer(GL_FRAMEBUFFER, PartMapFBO[0])
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glUniform1i(switcher_loc, 0)
    new_c = cam.camera_pos + cam.camera_right*0.1  # 光照模型用左移的摄像机
    glUniform3f(viewPosLoc, new_c.x, new_c.y, new_c.z)
    view = cam.get_view_matrix(cam.camera_right*0.1)  # 摄像机左移
    glDeliverFunc(glUniformMatrix4fv, shader,
                  "view", view)
    glDrawArrays(GL_TRIANGLES, 0, len(obj1.vertex_index))
    # * 右眼渲染 只写入GB

    glBindFramebuffer(GL_FRAMEBUFFER, PartMapFBO[1])
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glUniform1i(switcher_loc, 1)
    new_c = cam.camera_pos - cam.camera_right*0.1  # 光照模型用右移的摄像机
    glUniform3f(viewPosLoc, new_c.x, new_c.y, new_c.z)
    view = cam.get_view_matrix(-cam.camera_right*0.1)  # 摄像机右移
    glDeliverFunc(glUniformMatrix4fv, shader,
                  "view", view)
    glDrawArrays(GL_TRIANGLES, 0, len(obj1.vertex_index))
    
    
    glfwSwapBuffers(window)

glfwTerminate()
