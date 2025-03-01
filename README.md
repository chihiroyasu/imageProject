# imageProject 
## Google Drive API実装編

#### <ins>1. `credentials.json`の移動</ins>
`quickstart.py`を実行する前に`credentials.json`を`quickstart.py`と同じディレクトリにおいておく。このディレクトリを以下で作業ディレクトリと呼ぶ。


#### <ins>2. 環境変数の設定</ins>
```$vim ~/.bashrc```でaliasのところに下記のように記述し```$source ~/.bashrc```しておく。
```
alias = alias credential='export GOOGLE_APPLICATION_CREDENTIALS="<作業ディレクトリのパス>/credentials.json"'
```


#### <ins>3. `quickstart.py`の実行</ins>
`token.json`が生成され、ログイン補完的な感じになる。


#### <ins>4. logの準備</ins>
```
$mkdir log
$touch log/fromGoogle.log
$touch log/fromGoogle-error.log
```


#### 5. 　<ins>スクリプトの用意</ins>
`fromGoogle.sh`、`redundant.py`、`sort.py`を作業ディレクトリにこのプロジェクト同様のものを用意する。
   - **`redundant.py`の編集**\
     ① Google Driveのマイドライブ下に、とりあえず同期させたいファイルをブッコムフォルダとGoogle Driveにも残しておきたいファイルを置いておく用フォルダを作成する。\
     ② それぞれのフォルダにブラウザ上からアクセスしたときのfolder_idをコピーしておく。\
       (https://drive.google.com/drive/folders/<ここの文字列>)\
     ③ 変数`temp_folder_id`と変数`star_foder`の値を変更する。\
       とりあえず同期させたいファイルをブッコムフォルダのidを`temp_folder_id`に、残しておきたいファイルを置いておく用フォルダのidを`star_folder`に入れる。
     
   - **`fromGoogle.sh`の編集**\
     ① `/home/qqqlq/pypy/bin/python`の部分を自分のマシンで設定し仮想環境のPythonのパスに変更する。\
     ② `/home/qqqlq/yasu_device/imageProject/redundant.py`を<作業ディレクトリのパス>/redundant.pyに変更する。\
     ③ `/home/qqqlq/yasu_device/imageProject/log/fromGoogle.log`と`/home/qqqlq/yasu_device/imageProject/fromGoogle-error.log`をそれぞれ作成した`fromGoogle.log`と`fromGoogle-error.log`のパスに変更する。
     
   - **`sort.py`の編集**\
     ① 変数`roots`と変数`targets`を変更する。\
     使用するSSD等が複数の場合はそれぞれの記憶媒体のマウントで使用したパスが(ルートディレクトリから)同じところまでを`roots`に、\
     違うところからを`targets`に入れる。


#### <ins>6. 定期実行</ins>
```
$ crontab -e
```
```
0 * * * * bash [fromGoogleに至るパス]/fromGoogle.sh
0 * * * * /home/qqqlq/pypy/bin/python [sort.pyに至るパス]/sort.py　　　　#これは実行するpythonがどこにあるか　そのpythonでどのファイルを実行するかを示す
```


#### 7. <ins>cron動作状況</ins>
```
$ systemctl status cron
```
