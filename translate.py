from openai import OpenAI

client = OpenAI()

def translate_text(text, target_language):
    """使用 GPT-4 翻譯文本"""
    try:
        # 使用 ChatCompletion API 請求翻譯
        response = client.chat.completions.create(
            model="gpt-4",  # 使用 gpt-4 或 gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "You are a helpful assistant who only provides translations."},
                {"role": "user", "content": f"Translate this text to {target_language}: {text}"}
            ],
            max_tokens=200,
            temperature=0.5,
        )
        # 提取翻譯結果
        translated_text = response.choices[0].message.content.strip()

        # 處理返回值，去掉多餘描述
        if "The translation of" in translated_text or "is" in translated_text:
            translated_text = translated_text.split("is")[-1].strip().strip('"').strip("'")
            
        translated_text = translated_text.replace('"', '').replace("'", '')

        if translated_text.endswith('.'):
            translated_text = translated_text[:-1].strip()

        return translated_text
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # 測試翻譯文本和目標語言
    text_to_translate = "狗、貓、。"  # 要翻譯的文本
    target_language = "English"  # 可選目標語言，例如 "Spanish" 或 "French"

    try:
        # 呼叫翻譯函式
        translated_text = translate_text(text_to_translate, target_language)
        # 輸出結果
        print(f"Original Text: {text_to_translate}")
        print(f"Target Language: {target_language}")
        print(f"Translated Text: {translated_text}")
    except Exception as e:
        print("翻譯過程中出現錯誤：", e)
