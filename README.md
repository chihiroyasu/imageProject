# imageProject
撮影データの保管方法

quickstart.pyを実行する前にcredentials.jsonをquixkstart.pyと同じディレクトリにおいておく。

$vim ~/.bashrcでaliasのところに下記のように記述しsource ~/.bashrcしておく。
alias = alias credential='export GOOGLE_APPLICATION_CREDENTIALS="/home/qqqlq/yasu_device/credentials.json"'

quickstart.pyをやればtoken.jsonが生成され、ログイン補完的な感じになる。

実装前に下の3コマンドでlogの準備をしておく
$mkdir log
$touch log/fromGoogle.log
$touch log/fromGoogle-error.log

crontab -eしてfromGoogle.shを一時間ごとに実行する。

qqqlq@raspberrypi:~/yasu_device/imageProject $ crontab -e
0 * * * * bash [fromGoogleに至るパス]/fromGoogle.sh
0 * * * * /home/qqqlq/pypy/bin/python [sort.pyに至るパス]/sort.py　　　　#これは実行するpythonがどこにあるか　そのpythonでどのファイルを実行するかを示す


systemctl status cronでcronが動いているか調べる。
