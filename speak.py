import pyaudio
import wave
import numpy as np
from openai import OpenAI

# 初始化 OpenAI 客戶端
client = OpenAI()

def record_audio(output_file, sample_rate=44100, channels=1, chunk_size=1024, silence_threshold=600, silence_duration=2):#如果靜音檢測太靈敏就把silence_threshold調高一點
    """錄音功能，當檢測到用戶無聲音時自動停止"""
    audio = pyaudio.PyAudio()
    print("錄音開始... 當您停止說話時錄音將自動結束")

    # 開啟錄音流
    stream = audio.open(format=pyaudio.paInt16,  # 音頻格式
                        channels=channels,      # 通道數
                        rate=sample_rate,       # 取樣率
                        input=True,             # 輸入模式
                        frames_per_buffer=chunk_size)  # 緩衝區大小

    frames = []
    silent_chunks = 0  # 記錄連續無聲音的塊數
    max_silent_chunks = silence_duration * sample_rate // chunk_size  # 無聲塊數閾值

    try:
        while True:
            data = stream.read(chunk_size, exception_on_overflow=False)
            frames.append(data)

            # 計算當前塊的音量（振幅）
            audio_data = np.frombuffer(data, dtype=np.int16)
            amplitude = np.max(np.abs(audio_data))

            # 判斷是否是靜音
            if amplitude < silence_threshold:
                silent_chunks += 1
            else:
                silent_chunks = 0

            # 如果超過靜音閾值，停止錄音
            if silent_chunks > max_silent_chunks:
                print("檢測到靜音，錄音結束")
                break

    finally:
        # 結束錄音
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # 將錄音儲存為 wav 檔案
        with wave.open(output_file, 'wb') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(frames))

def transcribe_audio(file_path):
    """使用 OpenAI Whisper API 進行語音轉文字"""
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcription.text

if __name__ == "__main__":
    # 錄音參數
    output_file = r"sound\recorded_audio.wav"

    # 開始錄音
    record_audio(output_file)

    # 語音轉文字
    transcription_text = transcribe_audio(output_file)

    # 輸出轉錄結果
    print("語音轉文字結果：")
    print(transcription_text)
        # 將轉錄結果保存到 UTF-8 編碼的文件中
    with open("transcription.txt", "w", encoding="utf-8") as f:
        f.write(transcription_text)

