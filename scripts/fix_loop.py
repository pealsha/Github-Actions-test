# scripts/fix_loop.py
import os
import subprocess
import sys
from openai import OpenAI
from spec_parser import parse_spec

MAX_RETRIES = 3

def run_tests(test_command: str) -> tuple[bool, str]:
    result = subprocess.run(
        test_command.split(),
        capture_output=True,
        text=True
    )
    output = result.stdout + result.stderr
    return result.returncode == 0, output

def fix_code(current_code: str, error_log: str) -> str:
    client = OpenAI(
        api_key=os.environ["DEEPSEEK_API_KEY"],
        base_url="https://api.deepseek.com"
    )

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "あなたは優秀なPythonエンジニアです。エラーを修正したPythonコードのみを返してください。説明文やマークダウン記法(```など)は含めないでください。"
            },
            {
                "role": "user",
                "content": f"以下のコードでテストが失敗しました。修正してください。\n\nコード:\n{current_code}\n\nエラーログ:\n{error_log}"
            }
        ],
        max_tokens=1000,
        temperature=0.0
    )

    return response.choices[0].message.content.strip()

def main():
    spec_file = sys.argv[1]
    spec = parse_spec(spec_file)
    output_file = spec["output_file"]
    test_command = spec["test_command"]

    for attempt in range(1, MAX_RETRIES + 1):
        print(f"\n--- テスト実行 (試行 {attempt}/{MAX_RETRIES}) ---")
        success, log = run_tests(test_command)

        if success:
            print("✅ テスト成功")
            sys.exit(0)

        print(f"❌ テスト失敗\n{log}")

        if attempt == MAX_RETRIES:
            print("⚠️ 自動修正の上限に達しました。人間のレビューが必要です。")
            sys.exit(1)

        print("DeepSeekに修正を依頼中...")
        with open(output_file, "r", encoding="utf-8") as f:
            current_code = f.read()

        fixed_code = fix_code(current_code, log)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(fixed_code)

        print("修正完了。再テストします...")

if __name__ == "__main__":
    main()
