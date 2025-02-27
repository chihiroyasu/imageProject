import os
import subprocess
import time

roots = ["/mnt"]
targets = ["nas/redundant"]

year = time.strftime("%Y")
mon = time.strftime("%m")

for root_path in roots:
    for t in targets:
        dir_path = os.path.join(root_path, t, year, mon)
        cmd = f"mkdir -p {dir_path}"
        subprocess.call(cmd, shell=True)

        # root_path/t/ 直下にあるディレクトリ以外のファイルを移動
        cmd = f'find "{root_path}/{t}" -maxdepth 1 -type f -exec mv {{}} "{dir_path}" \;'
        subprocess.call(cmd, shell=True)

