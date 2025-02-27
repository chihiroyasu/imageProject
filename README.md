# imageProject
撮影データの保管方法

quickstart.pyを実行する前にcredentials.jsonをquixkstart.pyと同じディレクトリにおいておく。

`$vim ~/.bashrc`でaliasのところに下記のように記述し`source ~/.bashrc`しておく。
<span>alias = alias credential='export GOOGLE_APPLICATION_CREDENTIALS="/home/qqqlq/yasu_device/credentials.json"'</span>

quickstart.pyをやればtoken.jsonが生成され、ログイン補完的な感じになる。

実装前に下の3コマンドでlogの準備をしておく
<span>$mkdir log</span>
<span>$touch log/fromGoogle.log</span>
<span>$touch log/fromGoogle-error.log</span>

<span>crontab -e</span>してfromGoogle.shを一時間ごとに実行する。
<span>
qqqlq@raspberrypi:~/yasu_device/imageProject $ crontab -l
# Edit this file to introduce tasks to be run by cron.
#
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
#
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').
#
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
#
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
#
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
#
# For more information see the manual pages of crontab(5) and cron(8)
#
# m h  dom mon dow   command

0 * * * * bash [fromGoogleに至るパス]/fromGoogle.sh
0 * * * * /home/qqqlq/pypy/bin/python [sort.pyに至るパス]/sort.py　　　　#これは実行するpythonがどこにあるか　そのpythonでどのファイルを実行するかを示す
</span>

<span>systemctl status cron</span>でcronが動いているか調べる。
