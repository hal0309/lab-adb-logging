import subprocess

IP = "192.168.X.X:XXXXX"
TAG = "MyLogging"
FINISH_CODE = "FINISH"

def main():
    cmd_connect = f"adb connect {IP}" # 接続
    cmd_logcast_rest = f"adb -s {IP} logcat -c" # ログキャッシュのクリア
    cmd_logcast = f"adb -s {IP} logcat {TAG} *:S" # ログの取得&フィルタ

    subprocess.run(cmd_connect, shell=True)
    subprocess.run(cmd_logcast_rest, shell=True)
    process = subprocess.Popen(cmd_logcast, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8")

    # フィルタ済みログデータを出力
    for output_line in process.stdout:
        print(output_line.strip())
        """
        ここに好きな処理を書く
        """
        if FINISH_CODE in output_line:
            process.kill()
            break

    # 終了コードを取得
    result_code = process.wait()
    print(f"finish status: {result_code}")


if __name__ == "__main__":
    main()