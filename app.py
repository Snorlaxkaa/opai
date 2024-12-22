from flask import Flask, request, render_template, jsonify
from openai import OpenAI
import os
client = OpenAI()


app = Flask(__name__)

# 首頁路由：渲染 index.html
@app.route('/')
def index():
    return render_template('index.html')

# 圖片生成路由
@app.route('/generate', methods=['POST'])
def generate_image():
    # 從請求中獲取 Prompt
    prompt = request.json.get("prompt")
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        # 使用 DALL·E 3 模型生成圖片
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",#standard or hd 去做切換 hd 會比較貴
            n=1,
        )
        # 獲取生成圖片的 URL
        image_url = response.data[0].url 
        return jsonify({"url": image_url})
    except Exception as e:
        # 返回錯誤訊息
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
