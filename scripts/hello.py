# scripts/hello.py
import sys
import platform

def main():
    print("Pythonスクリプトが正常に実行されました")
    print(f"Pythonバージョン: {platform.python_version()}")
    print(f"実行引数: {sys.argv}")

if __name__ == "__main__":
    main()
