from openai import OpenAI
import os


def main():
    try:
        # 測試使用 ChatCompletion 接口
        response = openai.ChatCompletion.create(
            model="gpt-4",  # 替換為你需要測試的模型名稱
            messages=[
                {"role": "system", "content": "你是一個友好的助手。"},
                {"role": "user", "content": "Hello! How are you?"}
            ],
            max_tokens=50,  # 減少測試時的 Token 消耗
            temperature=0.5
        )

        # 打印生成的回應
        print("API 測試成功！生成的回應如下：")
        print(response["choices"][0]["message"]["content"].strip())

    except Exception as e:
        print("API 測試失敗，發生錯誤：")
        print(e)

if __name__ == "__main__":
    main()
