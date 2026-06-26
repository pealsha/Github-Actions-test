# scripts/generate_code.py
import os
import sys
from openai import OpenAI

def generate_code(spec_text: str) -> str:
    client = OpenAI(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com"
    )

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "あなたは優秀なPythonエンジニアです。要件定義に従い、Pythonコードのみを返してください。説明文やマークダウン記法(```など)は含めないでください。"
            },
            {
                "role": "user",
                "content": spec_text
            }
        ],
        max_tokens=1000,
        temperature=0.0
    )

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    spec_file = sys.argv[1]

    with open(spec_file, "r", encoding="utf-8") as f:
        spec = f.read()

    print(f"要件定義を読み込みました: {spec_file}")
    code = generate_code(spec)
    print("コード生成完了")

    os.makedirs("output", exist_ok=True)
    with open("output/fizzbuzz.py", "w", encoding="utf-8") as f:
        f.write(code)

    print("output/fizzbuzz.py に保存しました")
    print("--- 生成されたコード ---")
    print(code)
