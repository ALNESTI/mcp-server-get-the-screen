from mcp.server import FastMCP
import os
import base64
import requests
from PIL import ImageGrab

mcp = FastMCP('DEMO')

@mcp.tool()
def get_screen() -> str:
    """获取屏幕上的内容并使用视觉模型识别"""
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


    # 图像转 base64
    def image_to_base64(file_path):
        with open(file_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")


    image_base64 = image_to_base64("screenshot.jpg")

    # 使用Ollama
    ollama_api_url = "http://localhost:11434/api/chat"  # 你的api
    headers = {
        "Content-Type": "application/json"
    }

    # 芝士payload
    payload = {
        "model": "qwen2.5vl:7b",  # 一定要是视觉模型啊！
        "messages": [
            {
                "role": "user",
                "content": "请描述这张图片的内容，或回答相关问题。",
                "images": [image_base64]
            }
        ],
        "stream": False
    }

    try:
        response = requests.post(ollama_api_url, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json().get("message", {}).get("content", "")
        return result

    except Exception as e:
        print(f"调用 Ollama 失败: {e}")
        return f"识别失败: {str(e)}"

if __name__ == '__main__':
    mcp.run(transport="sse") # 或者用stdio也行（装了uv前提下）