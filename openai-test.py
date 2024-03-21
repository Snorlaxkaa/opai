import openai
import os

# 確保你的 OpenAI API 密鑰已設定在環境變量中
openai.api_key = "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"

try:
    # 調用 OpenAI API 生成文本
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",  # 替換為當前可用的最新模型
        prompt="世界上最高的山是什麼？",
        temperature=0.7,
        max_tokens=100,
        top_p=1.0,
        frequency_penalty=0,
        presence_penalty=0
    )

    print(response.choices[0].text.strip())

except Exception as e:
    print(f"發生錯誤: {e}")
