from flask import Flask, request, render_template, jsonify
from openai import OpenAI
import os
from threading import Thread
from speak import record_audio  # 確保這裡的路徑和模組名稱正確
from speak import transcribe_audio

client = OpenAI()


app = Flask(__name__)
def background_recording():
    try:
        print("開始錄音...")
        output_file = "recorded_audio.wav"
        record_audio(output_file)  # 錄音
        print("錄音完成，開始進行語音轉文字...")

        transcription_text = transcribe_audio(output_file)  # 語音轉文字
        print(f"轉錄結果：{transcription_text}")

        # 將轉錄結果寫入文件
        with open("transcription.txt", "w", encoding="utf-8") as f:
            f.write(transcription_text)
        print("轉錄結果已寫入 transcription.txt")
    except Exception as e:
        print(f"錄音或轉錄時發生錯誤: {e}")
        raise


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
    
@app.route('/transcription', methods=['GET'])
def get_transcription():
    try:
        # 檢查是否存在 transcription.txt 文件
        transcription_file = "transcription.txt"
        if os.path.exists(transcription_file):
            with open(transcription_file, "r", encoding="utf-8") as file:
                transcription_text = file.read()
            return jsonify({"text": transcription_text})
        else:
            return jsonify({"error": "Transcription file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/start-recording', methods=['POST'])
def start_recording():
    try:
        # 啟動錄音
        recording_thread = Thread(target=background_recording)
        recording_thread.start()
        return jsonify({"success": True})
    except Exception as e:
        print(f"錄音路由錯誤: {e}")
        return jsonify({"success": False, "error": str(e)})


if __name__ == '__main__':
    app.run(debug=True)
