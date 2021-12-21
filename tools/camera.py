from pyrr import Vector3, matrix44, vector, vector3
from math import sin, cos, radians
from glfw.GLFW import *
from OpenGL.GL import *


class Camera:
    def __init__(self):
        self.camera_pos = Vector3([0.0, 0.0, 3.0])
        self.camera_front = Vector3([0.0, 0.0, -1.0])
        self.camera_up = Vector3([0.0, 1.0, 0.0])
        self.camera_right = Vector3([1.0, 0.0, 0.0])

        self.mouse_sensitivity = 0.25
        self.jaw = -90.0
        # 倾斜度
        self.pitch = 0.0

    def get_view_matrix(self, posoffset=Vector3([0.0, 0.0, 0.0])):
        return matrix44.create_look_at(
            self.camera_pos+posoffset, self.camera_pos +
            posoffset + self.camera_front, self.camera_up
        )

    def process_keyboard(self, direction, velocity):
        if direction == "FORWARD":
            self.camera_pos += self.camera_front * velocity
        if direction == "BACKWARD":
            self.camera_pos -= self.camera_front * velocity
        if direction == "LEFT":
            self.camera_pos -= self.camera_right * velocity
        if direction == "RIGHT":
            self.camera_pos += self.camera_right * velocity

    def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=False):
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity

        self.jaw += xoffset
        self.pitch += yoffset

        if constrain_pitch:
            if self.pitch > 45.0:
                self.pitch = 45.0
            if self.pitch < -45.0:
                self.pitch = -45.0

        self.update_camera_vectors()

    def update_camera_vectors(self):
        front = Vector3([0.0, 0.0, 0.0])
        front.x = cos(radians(self.jaw)) * cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.jaw)) * cos(radians(self.pitch))

        self.camera_front = vector.normalise(front)
        self.camera_right = vector.normalise(
            vector3.cross(self.camera_front, Vector3([0.0, 1.0, 0.0]))
        )
        self.camera_up = vector.normalise(
            vector3.cross(self.camera_right, self.camera_front)
        )
        # self.camera_front = front
        # self.camera_right = vector3.cross(
        #     self.camera_front, Vector3([0.0, 1.0, 0.0]))
        # self.camera_up = (
        #     vector3.cross(self.camera_right, self.camera_front))


cam = Camera()
WIDTH, HEIGHT = 1280, 720
lastX, lastY = WIDTH / 2, HEIGHT / 2
first_mouse = True
left, right, forward, backward = False, False, False, False
Pressed = False


def key_input_clb(window, key, scancode, action, mode):
    global left, right, forward, backward

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, True)

    if key == GLFW_KEY_W and action == GLFW_PRESS:
        forward = True
    elif key == GLFW_KEY_W and action == GLFW_RELEASE:
        forward = False

    if key == GLFW_KEY_S and action == GLFW_PRESS:
        backward = True
    elif key == GLFW_KEY_S and action == GLFW_RELEASE:
        backward = False

    if key == GLFW_KEY_A and action == GLFW_PRESS:
        left = True
    elif key == GLFW_KEY_A and action == GLFW_RELEASE:
        left = False

    if key == GLFW_KEY_D and action == GLFW_PRESS:
        right = True
    elif key == GLFW_KEY_D and action == GLFW_RELEASE:
        right = False


def do_movement():
    if forward:
        cam.process_keyboard("FORWARD", 0.05)
    if backward:
        cam.process_keyboard("BACKWARD", 0.05)
    if left:
        cam.process_keyboard("LEFT", 0.05)
    if right:
        cam.process_keyboard("RIGHT", 0.05)


def mouse_button_callback(window, button, action, mods):
    global Pressed, lastY, lastX, first_mouse

    if (button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS):
        Pressed = True
        first_mouse = True
        glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_HIDDEN)

    elif (button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_RELEASE):
        Pressed = False
        glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_NORMAL)


def mouse_look_clb(window, xpos, ypos):
    global first_mouse, lastX, lastY, Pressed
    if Pressed:
        if first_mouse:
            lastX = xpos
            lastY = ypos
            first_mouse = False

        xoffset = xpos - lastX
        yoffset = lastY - ypos

        lastX = xpos
        lastY = ypos
        cam.process_mouse_movement(xoffset, yoffset, False)
    # else:
    #     data = glReadPixels(xpos, ypos, 1, 1, GL_RGB, GL_UNSIGNED_BYTE)
    #     print(data[0],data[1],data[2])


def mouse_enter_clb(window, entered):
    global first_mouse
    if entered:
        first_mouse = False
    else:
        first_mouse = True
