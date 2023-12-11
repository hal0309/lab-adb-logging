import subprocess
import json
import pickle

IP = "192.168.1.11:38501"
TAG = "MyLogging"
FINISH_CODE = "FINISH"

def main():
    cmd_connect = f"adb connect {IP}" # 接続
    cmd_logcast_rest = f"adb -s {IP} logcat -c" # ログキャッシュのクリア
    cmd_logcast = f"adb -s {IP} logcat {TAG} *:S" # ログの取得&フィルタ

    subprocess.run(cmd_connect, shell=True)
    subprocess.run(cmd_logcast_rest, shell=True)
    process = subprocess.Popen(cmd_logcast, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8")

    json_log = []

    

    # フィルタ済みログデータを出力
    for output_line in process.stdout:

        try:
            splited_line = output_line.strip().split(TAG + ":")
            print(splited_line[1])
            json_full = json.loads(splited_line[1])

            json_log.append(json_full)

            if(json_full["status"] == "finish"):
                print("finished")
                process.kill()
                break

            print(json_full["status"])
            json_mf = json_full["magneticField"]

        except Exception as e:
            print("error", e)
            continue
        
        

        """
        ここに好きな処理を書く
        """
        if FINISH_CODE in output_line:
            process.kill()
        
            break

    f = open('log.pickle', 'wb')    
    pickle.dump(json_log, f)
    f.close()

    f = open('log.pickle', 'rb')
    data_list = pickle.load(f)
    for data in data_list:
        print(data["status"])
    f.close()


    # 終了コードを取得
    result_code = process.wait()
    print(f"finish status: {result_code}")

    

if __name__ == "__main__":
    main()