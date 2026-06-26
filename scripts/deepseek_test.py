# scripts/deepseek_test.py
import os
from openai import OpenAI

def main():
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("エラー: DEEPSEEK_API_KEYが設定されていません")
        return

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

    print("DeepSeek APIに接続中...")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "あなたは優秀なソフトウェアエンジニアです。"},
            {"role": "user", "content": "Pythonで'Hello, World!'を出力するコードを1行で書いてください。コードのみ返してください。"}
        ],
        max_tokens=50,
        temperature=0.0
    )

    result = response.choices[0].message.content
    print(f"DeepSeekの返答: {result}")
    print(f"使用トークン数: {response.usage.total_tokens}")

if __name__ == "__main__":
    main()
