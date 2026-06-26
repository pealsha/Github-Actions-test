# scripts/spec_parser.py
import re

def parse_spec(filepath: str) -> dict:
    """
    要件定義ファイルからメタ情報と本文を分離して返す
    戻り値: {"output_file": str, "test_command": str, "body": str}
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Front Matter(---で囲まれた部分)を抽出
    pattern = r"^---\n(.*?)\n---\n(.*)$"
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        raise ValueError(f"Front Matterが見つかりません: {filepath}")

    meta_text = match.group(1)
    body = match.group(2).strip()

    # メタ情報をパース(PyYAMLを使わずシンプルに処理)
    meta = {}
    for line in meta_text.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()

    required_keys = ["output_file", "test_command"]
    for key in required_keys:
        if key not in meta:
            raise ValueError(f"Front Matterに '{key}' がありません: {filepath}")

    return {
        "output_file": meta["output_file"],
        "test_command": meta["test_command"],
        "body": body
    }

if __name__ == "__main__":
    import sys
    result = parse_spec(sys.argv[1])
    print(f"output_file : {result['output_file']}")
    print(f"test_command: {result['test_command']}")
    print(f"body(先頭50文字): {result['body'][:50]}")
