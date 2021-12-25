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


def main(objpath, texpath, offset):
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
    obj1.load_model(objpath)
    print(f'vvtvn: {len(obj1.vertex_index_vvtvn)}, vvn: {len(obj1.vertex_index_vvn)}, vvt: {len(obj1.vertex_index_vvt)}')
    shader_vvtvn = compileProgram(
        compileShader(readShader(
            'shaders/vvtvn.vs'), GL_VERTEX_SHADER),
        compileShader(readShader(
            'shaders/vvtvn.fs'), GL_FRAGMENT_SHADER)
    )
    shader_vvt = compileProgram(
        compileShader(readShader(
            'shaders/vvt.vs'), GL_VERTEX_SHADER),
        compileShader(readShader(
            'shaders/vvt.fs'), GL_FRAGMENT_SHADER)
    )
    shader_vvn = compileProgram(
        compileShader(readShader(
            'shaders/vvn.vs'), GL_VERTEX_SHADER),
        compileShader(readShader(
            'shaders/vvn.fs'), GL_FRAGMENT_SHADER)
    )
    screenShader = compileProgram(
        compileShader(readShader(
            'shaders/mix.vs'), GL_VERTEX_SHADER),
        compileShader(readShader(
            'shaders/mix.fs'), GL_FRAGMENT_SHADER)
    )

    tex = defaultTex(texpath)

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

    # --------------------------------- 渲染vvtvn -------------------------------- #

    objVAO = glGenVertexArrays(3)
    objVBO = glGenBuffers(3)
    
    glBindVertexArray(objVAO[0])
    glBindBuffer(GL_ARRAY_BUFFER, objVBO[0])
    glBufferData(GL_ARRAY_BUFFER, obj1.model_vvtvn.itemsize * len(obj1.model_vvtvn),
                 obj1.model_vvtvn, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                          obj1.model_vvtvn.itemsize * 3, ctypes.c_void_p(0))
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,
                          obj1.model_vvtvn.itemsize * 3, ctypes.c_void_p(len(obj1.vertex_index_vvtvn) * 12))
    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE,
                          obj1.model_vvtvn.itemsize * 2, ctypes.c_void_p(len(obj1.vertex_index_vvtvn) * 24))

    # --------------------------------- 渲染vvn -------------------------------- #
    glBindVertexArray(objVAO[1])
    glBindBuffer(GL_ARRAY_BUFFER, objVBO[1])
    glBufferData(GL_ARRAY_BUFFER, obj1.model_vvn.itemsize * len(obj1.model_vvn),
                 obj1.model_vvn, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                          obj1.model_vvn.itemsize * 3, ctypes.c_void_p(0))
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE,
                          obj1.model_vvn.itemsize * 3, ctypes.c_void_p(len(obj1.vertex_index_vvn) * 12))

    # --------------------------------- 渲染vvt -------------------------------- #
    glBindVertexArray(objVAO[2])
    glBindBuffer(GL_ARRAY_BUFFER, objVBO[2])
    glBufferData(GL_ARRAY_BUFFER, obj1.model_vvt.itemsize * len(obj1.model_vvt),
                 obj1.model_vvt, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
                          obj1.model_vvt.itemsize * 3, ctypes.c_void_p(0))
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE,
                          obj1.model_vvt.itemsize * 2, ctypes.c_void_p(len(obj1.vertex_index_vvt) * 12))
    
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

    glUseProgram(shader_vvtvn)
    glDeliverFunc(glUniformMatrix4fv, shader_vvtvn,
                  "projection", projection)

    glUseProgram(shader_vvt)
    glDeliverFunc(glUniformMatrix4fv, shader_vvt,
                  "projection", projection)

    glUseProgram(shader_vvn)
    glDeliverFunc(glUniformMatrix4fv, shader_vvn,
                  "projection", projection)

    glUseProgram(screenShader)
    glUniform1i(glGetUniformLocation(screenShader, "screenTexture1"), 0)
    glUniform1i(glGetUniformLocation(screenShader, "screenTexture2"), 1)

    def draw_vvn(tf):
        glUseProgram(shader_vvn)
        glBindVertexArray(objVAO[1])

        rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfwGetTime())

        glDeliverFunc(glUniformMatrix4fv, shader_vvn,
                      "model", rot_y)

        objectColor_loc = glGetUniformLocation(shader_vvn, "objectColor")
        lightColor_loc = glGetUniformLocation(shader_vvn, "lightColor")
        lightPosLoc = glGetUniformLocation(shader_vvn, "lightPos")
        viewPosLoc = glGetUniformLocation(shader_vvn, "viewPos")
        switcher_loc = glGetUniformLocation(shader_vvn, "switcher")
        glUniform3f(objectColor_loc, 1.0, 0.5, 0.31)
        glUniform3f(lightColor_loc, 1.0, 1.0, 1.0)
        glUniform3f(lightPosLoc, 2.0, 2.0, 2.0)

        glBindFramebuffer(GL_FRAMEBUFFER, PartMapFBO[0])
        glUniform1i(switcher_loc, 0)
        new_c = cam.camera_pos + cam.camera_right*offset*tf
        glUniform3f(viewPosLoc, new_c.x, new_c.y, new_c.z)
        view = cam.get_view_matrix(cam.camera_right*offset*tf)
        glDeliverFunc(glUniformMatrix4fv, shader_vvn,
                      "view", view)
        glDrawArrays(GL_TRIANGLES, 0, len(obj1.vertex_index_vvn))

    def draw_vvt(tf):
        glUseProgram(shader_vvt)
        glBindVertexArray(objVAO[2])

        rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfwGetTime())

        glDeliverFunc(glUniformMatrix4fv, shader_vvt,
                      "model", rot_y)
        
        switcher_loc = glGetUniformLocation(shader_vvt, "switcher")

        glBindFramebuffer(GL_FRAMEBUFFER, PartMapFBO[0])
        glUniform1i(switcher_loc, 0)
        view = cam.get_view_matrix(cam.camera_right*offset*tf)
        glDeliverFunc(glUniformMatrix4fv, shader_vvt,
                      "view", view)
        glDrawArrays(GL_TRIANGLES, 0, len(obj1.vertex_index_vvt))
        # ------------------------------------ 循环 ------------------------------------ #
    while not glfwWindowShouldClose(window):

        glfwPollEvents()

        do_movement()
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 0.0)

        glUseProgram(shader_vvtvn)
        glBindVertexArray(objVAO[0])

        rot_y = pyrr.Matrix44.from_y_rotation(0.8 * glfwGetTime())

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, tex)
        glDeliverFunc(glUniformMatrix4fv, shader_vvtvn,
                      "model", rot_y)

        objectColor_loc = glGetUniformLocation(shader_vvtvn, "objectColor")
        lightColor_loc = glGetUniformLocation(shader_vvtvn, "lightColor")
        lightPosLoc = glGetUniformLocation(shader_vvtvn, "lightPos")
        viewPosLoc = glGetUniformLocation(shader_vvtvn, "viewPos")
        switcher_loc = glGetUniformLocation(shader_vvtvn, "switcher")
        glUniform3f(objectColor_loc, 1.0, 0.5, 0.31)
        glUniform3f(lightColor_loc, 1.0, 1.0, 1.0)
        glUniform3f(lightPosLoc, 2.0, 2.0, 2.0)

        # * 左眼渲染 只写入R
        glBindFramebuffer(GL_FRAMEBUFFER, PartMapFBO[0])
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUniform1i(switcher_loc, 0)
        new_c = cam.camera_pos + cam.camera_right*offset  # 光照模型用左移的摄像机
        glUniform3f(viewPosLoc, new_c.x, new_c.y, new_c.z)
        view = cam.get_view_matrix(cam.camera_right*offset)  # 摄像机左移
        glDeliverFunc(glUniformMatrix4fv, shader_vvtvn,
                      "view", view)
        glDrawArrays(GL_TRIANGLES, 0, len(obj1.vertex_index_vvtvn))

        if len(obj1.vertex_index_vvn):
            draw_vvn(1)

        if len(obj1.vertex_index_vvt):
            draw_vvt(1)
        # * 右眼渲染 只写入GB
        glUseProgram(shader_vvtvn)
        glBindVertexArray(objVAO[0])
        glBindFramebuffer(GL_FRAMEBUFFER, PartMapFBO[1])
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUniform1i(switcher_loc, 1)
        new_c = cam.camera_pos - cam.camera_right*offset  # 光照模型用右移的摄像机
        glUniform3f(viewPosLoc, new_c.x, new_c.y, new_c.z)
        view = cam.get_view_matrix(-cam.camera_right*offset)  # 摄像机右移
        glDeliverFunc(glUniformMatrix4fv, shader_vvtvn,
                      "view", view)
        glDrawArrays(GL_TRIANGLES, 0, len(obj1.vertex_index_vvtvn))
        
        if len(obj1.vertex_index_vvn):
            draw_vvn(-1)

        if len(obj1.vertex_index_vvt):
            draw_vvt(-1)
            
        # * 渲染专门用来结合的四边形
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glDisable(GL_DEPTH_TEST)
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        # * 绑定刚刚画好的俩纹理
        glUseProgram(screenShader)
        glBindVertexArray(quadVAO)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, PartMap[0])
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, PartMap[1])
        glDrawArrays(GL_TRIANGLES, 0, 6)
        glfwSwapBuffers(window)

    glfwTerminate()


if __name__ == "__main__":
    objpath = r'res\FuTo\source\FuToLow.obj'
    texpath = r'res\FuTo\textures\FuToLow_initialShadingGroup_BaseColor.png'

    # objpath = r'res\BaymaxWhiteOBJ\Bigmax_White_OBJ.obj'
    # texpath = r'res\BaymaxWhiteOBJ\EyesWhite.jpg'
    
    # objpath = r'res\spot\spot_triangulated_good.obj'
    # texpath = r'res\spot\spot_texture.png'
    offset = 0.1
    main(objpath, texpath, offset)
