import subprocess
import json
import pickle
import time
import os

IP = "192.168.1.12:41293"
# IP = "10.35.103.81:41029"
TAG = "MyLogging"
START_STATUS = "startAcc"
FINISH_STATUS = "finish"

FILEDIR = f"log\{time.time()}"

def main():
    os.makedirs(FILEDIR, exist_ok=True)

    cmd_connect = f"adb connect {IP}" # 接続
    cmd_logcast_rest = f"adb -s {IP} logcat -c" # ログキャッシュのクリア
    cmd_logcast = f"adb -s {IP} logcat {TAG} *:S" # ログの取得&フィルタ

    subprocess.run(cmd_connect, shell=True)
    subprocess.run(cmd_logcast_rest, shell=True)
    process = subprocess.Popen(cmd_logcast, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8")

    json_log = []

    while True:

        n = 0

        # フィルタ済みログデータを出力
        for output_line in process.stdout:

            try:
                splited_line = output_line.strip().split(TAG + ":")
                print(splited_line[1])
                json_full = json.loads(splited_line[1])

                json_log.append(json_full)

                if(json_full["status"] == START_STATUS):
                    print("started")
                    n = json_full["n"]
                    continue
                elif(json_full["status"] == FINISH_STATUS):
                    print("finished")
                    process.kill()
                    break
                else:
                    print(json_full["status"])
                    json_mf = json_full

            except Exception as e:
                print("error", e)
                continue

        fname = f'{FILEDIR}/acc-{n}.pickle'
        f = open(fname, 'wb')    
        pickle.dump(json_log, f)
        f.close()

        f = open(fname, 'rb')
        data_list = pickle.load(f)
        for data in data_list:
            print(data)
        f.close()


        # 終了コードを取得
        result_code = process.wait()
        print(f"finish status: {result_code}")

    

if __name__ == "__main__":
    main()