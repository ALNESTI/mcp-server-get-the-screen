from mcp.server import FastMCP
import os
import base64
from openai import OpenAI
from PIL import ImageGrab


mcp = FastMCP('DEMO')

@mcp.tool()
def get_screen() -> str:
    """获取屏幕上的内容（无需传入信息）"""
    # 捕获整个屏幕
    img = ImageGrab.grab()

    # 这里写缩放倍数
    scale_factor = 0.5

    # 计算新的尺寸
    new_width = int(img.width * scale_factor)
    new_height = int(img.height * scale_factor)

    # 调整图像大小
    img = img.resize((new_width, new_height))

    # 保存截图
    img.save('screenshot.jpg')
    print('已截屏！')

    # 将本地图片转换为 base64 编码的 data URL
    def image_to_data_url(file_path):
        with open(file_path, "rb") as image_file:
            encoded_str = base64.b64encode(image_file.read()).decode("utf-8")
        mime_type = "image/jpeg"  # 根据你的图片类型修改，如 image/png
        return f"data:{mime_type};base64,{encoded_str}"

    # 初始化客户端
    client = OpenAI(
        api_key='YOUR_API_KEY',  # 请先设置环境变量
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    try:
        # 本地图片路径
        local_image_path = "screenshot.jpg"  # 替换为你的图片路径

        # 转换为 data URL
        image_data_url = image_to_data_url(local_image_path)

        # 调用模型
        completion = client.chat.completions.create(
            model="qwen-vl-plus",  # 可替换为 qwen-vl-max 等
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": image_data_url}},
                        {"type": "text", "text": "这是什么？(简单回答一下)"},
                    ],
                }
            ],
        )

        # 输出模型的回答
        # print(completion.choices[0].message.content)
        return completion.choices[0].message.content

    except Exception as e:
        print(f"调用失败: {e}")

if __name__ == '__main__':
    mcp.run(transport="sse") # 可以配置为stdio或者sse

