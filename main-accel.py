import subprocess
import json
import pickle
import time
import os

# IP = "192.168.1.12:41293"
IP = "10.35.103.81:43923"
TAG = "MyLogging"
START_STATUS = "start"
START_ACC_STATUS = "startAcc"
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

        subprocess.run(cmd_logcast_rest, shell=True)

        # フィルタ済みログデータを出力
        for output_line in process.stdout:

            try:
                splited_line = output_line.strip().split(TAG + ":")
                print(splited_line[1])
                json_full = json.loads(splited_line[1])

                if(json_full["status"] == START_STATUS):
                    continue

                json_log.append(json_full)

                if(json_full["status"] == START_ACC_STATUS):
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

        json_log = []

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





""" 
sample of log
{"status":"startAcc","n":1}
{"mag":{"x":-9.0402,"y":23.985199,"z":-30.719599,"accuracy":3,"timestamp":1877107269432907},"acc":{"status":"accel","x":0.09688127,"y":-0.015049115,"z":0.014573097,"timestamp":1877107267066512},"gyro":{"status":"gyro","x":-0.018020526,"y":-0.028099801,"z":0.0021380284,"timestamp":1877107267066512}}
{"mag":{"x":-9.3452,"y":23.326399,"z":-30.317,"accuracy":3,"timestamp":1877107369432663},"acc":{"status":"accel","x":-0.029610693,"y":0.008819729,"z":-0.025092125,"timestamp":1877107338431320},"gyro":{"status":"gyro","x":-1.5271631E-4,"y":0.015882496,"z":-4.5814895E-4,"timestamp":1877107338431320}}
{"mag":{"x":-9.2109995,"y":23.4972,"z":-31.219799,"accuracy":3,"timestamp":1877107469432907},"acc":{"status":"accel","x":0.005079031,"y":-0.020370468,"z":0.012656212,"timestamp":1877107445469222},"gyro":{"status":"gyro","x":0.012064588,"y":0.013897184,"z":-0.0015271631,"timestamp":1877107445469222}}
{"mag":{"x":-8.662,"y":22.6798,"z":-30.073,"accuracy":3,"timestamp":1877107569433151},"acc":{"status":"accel","x":-0.019732773,"y":-0.0071486533,"z":-0.035375595,"timestamp":1877107552507247},"gyro":{"status":"gyro","x":0.0047342055,"y":0.0047342055,"z":-6.1086525E-4,"timestamp":1877107552507247}}
{"mag":{"x":-8.9426,"y":23.326399,"z":-30.597599,"accuracy":3,"timestamp":1877107669432418},"acc":{"status":"accel","x":0.025838971,"y":-0.0039746463,"z":0.0074834824,"timestamp":1877107659544784},"gyro":{"status":"gyro","x":9.162979E-4,"y":0.0012217305,"z":3.0543262E-4,"timestamp":1877107659544784}}
{"mag":{"x":-9.0646,"y":23.4362,"z":-29.8046,"accuracy":3,"timestamp":1877107769433151},"acc":{"status":"accel","x":4.5108795E-4,"y":-0.0018246174,"z":-0.040638924,"timestamp":1877107766582930},"gyro":{"status":"gyro","x":0.0021380284,"y":0.0032070426,"z":1.5271631E-4,"timestamp":1877107766582930}}
{"mag":{"x":-9.1256,"y":23.4118,"z":-31.0124,"accuracy":3,"timestamp":1877107869428024},"acc":{"status":"accel","x":-0.008680165,"y":0.0016961694,"z":-0.016719818,"timestamp":1877107837941146},"gyro":{"status":"gyro","x":-4.5814895E-4,"y":-3.0543262E-4,"z":-1.5271631E-4,"timestamp":1877107837941146}}
{"mag":{"x":-9.028,"y":23.2166,"z":-30.9026,"accuracy":3,"timestamp":1877107969432907},"acc":{"status":"accel","x":-0.011339784,"y":0.002046436,"z":-0.036088943,"timestamp":1877107944979293},"gyro":{"status":"gyro","x":-0.0033597588,"y":-0.001985312,"z":3.0543262E-4,"timestamp":1877107944979293}}
{"mag":{"x":-9.15,"y":23.8022,"z":-30.219398,"accuracy":3,"timestamp":1877108069432907},"acc":{"status":"accel","x":0.08927429,"y":0.13153213,"z":-0.099163055,"timestamp":1877108052017318},"gyro":{"status":"gyro","x":-0.011759156,"y":-0.0096211275,"z":-1.5271631E-4,"timestamp":1877108052017318}}
{"status":"finish"}
"""