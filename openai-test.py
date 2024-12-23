import pyaudio
import wave
from openai import OpenAI

# 初始化 OpenAI 客戶端
client = OpenAI()

def record_audio(output_file, record_seconds=10, sample_rate=44100, channels=1, chunk_size=1024):
    """錄音功能"""
    audio = pyaudio.PyAudio()
    print("錄音開始...")

    # 開啟錄音流
    stream = audio.open(format=pyaudio.paInt16,  # 音頻格式
                        channels=channels,      # 通道數
                        rate=sample_rate,       # 取樣率
                        input=True,             # 輸入模式
                        frames_per_buffer=chunk_size)  # 緩衝區大小

    frames = []

    # 錄音迴圈
    for _ in range(0, int(sample_rate / chunk_size * record_seconds)):
        data = stream.read(chunk_size)
        frames.append(data)

    # 結束錄音
    print("錄音結束")
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
    output_file = r"C:\Users\USER\Desktop\opAI\recorded_audio.wav"
    record_seconds = 5  # 錄音時長 (秒)

    # 開始錄音
    record_audio(output_file, record_seconds)

    # 語音轉文字
    transcription_text = transcribe_audio(output_file)

    # 輸出轉錄結果
    print("語音轉文字結果：")
    print(transcription_text)
