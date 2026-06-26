# scripts/generate_code.py
import os
import sys
from openai import OpenAI
from spec_parser import parse_spec

def generate_code(spec_body: str) -> str:
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
                "content": spec_body
            }
        ],
        max_tokens=1000,
        temperature=0.0
    )

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    spec_file = sys.argv[1]
    spec = parse_spec(spec_file)

    print(f"要件定義を読み込みました: {spec_file}")
    print(f"出力先: {spec['output_file']}")

    code = generate_code(spec["body"])

    # 出力先ディレクトリを動的に作成
    output_dir = os.path.dirname(spec["output_file"])
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(spec["output_file"], "w", encoding="utf-8") as f:
        f.write(code)

    print(f"コード生成完了: {spec['output_file']}")
    print("--- 生成されたコード ---")
    print(code)
