### 安装依赖

`pip3 install -r requirements.txt`

其中pyopengl自动下的是32位的,需要自己下,要不自己改一下requirements.txt的路径和东西(根据不同版本都在文件夹内)

---

### 内部逻辑说明

设置两个帧缓冲,离线渲染左眼右眼两帧,渲染结果分别只取r/gb通道

```python
# 使用帧缓冲1
glBindFramebuffer(GL_FRAMEBUFFER, PartMapFBO[0])
# 清屏
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
# 切换到1(只输出r)
glUniform1i(switcher_loc, 0)
# 光照模型用左移的摄像机
new_c = cam.camera_pos - cam.camera_right*0.05 
glUniform3f(viewPosLoc, new_c.x, new_c.y, new_c.z)
# 摄像机左移
view = cam.get_view_matrix(-cam.camera_right*0.05) 
glDeliverFunc(glUniformMatrix4fv, shader,
                "view", view)
# 绘制
glDrawArrays(GL_TRIANGLES, 0, len(obj1.vertex_index))
```

```glsl
if(switcher == 0) {
    fColor = vec4(result.r, 0.0, 0.0, 1.0);
} else {
    fColor = vec4(0.0, result.g, result.b, 1.0);
}
```

回到屏幕帧,在一个填满屏幕的四边形上,每一个像素都是另外两帧各自rgb值的相加

```glsl
FragColor = vec4(texture(screenTexture1, TexCoords)[0],texture(screenTexture2, TexCoords)[1],texture(screenTexture2, TexCoords)[2], 1.0);
```