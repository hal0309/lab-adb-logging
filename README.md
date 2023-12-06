# Logcat無線取得プログラム (Android, python)

Androidで投げたLogをWi-Fi経由でPC側で拾うプログラムです。  

## 事前準備

### PC側

adbコマンドのパスが通っていること。
> adb導入方法参考  
> https://windroid.work/2022/02/adb-windows11-android-2022.html/


### Android側

ワイヤレスデバッグが設定済み、PCとペアリング済みであること。
> ワイヤレスデバッグ参考  
> https://zenn.dev/ik11235/articles/android-wireless-debug

> [!WARNING]  
> ワイヤレスデバッグはAndroid11以降で可能です。



## 使用方法

### PC側

`main.py`内部の定数`IP`をAndroidのワイヤレスデバッグIPアドレスに変えて実行。  
取得したデータを好きなように加工してください。

> [!IMPORTANT]  
> Wi-Fiに再接続を行った際は毎回IPが変わるので随時再入力してください。


### Android側

以下のようにタグを`MyLogging`としたログを投げてください。
~~~ Kotlin
Log.i("MyLogging", "Hello World!")
~~~

終了する際は、メッセージ内容に`FINISH`を含めてください。
~~~ Kotlin
button.setOnClickListener(){
    Log.i("MyLogging", "FINISH")
}
~~~

