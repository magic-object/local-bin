#!/usr/bin/env python
"""
このプログラムは DNF でチェックを行い更新があれば更新後に再起動する。
cron により、毎晩実行する事で自動的に更新できる様にする。
"""
import subprocess
import os
import sys

# DNF でチェックを行い更新があれば更新後に再起動する。
if __name__ == '__main__':
    # スーパーユーザーかどうか？
    if os.getuid() != 0:
        print('This program is only for super user.', file=sys.stderr)
        exit(1)

    # 更新チェック
    dnf_args = ['dnf', 'check-update']
    return_code = subprocess.run(dnf_args).returncode
    if return_code == 0:
        # 更新なし
        exit(0)
    elif return_code != 100:
        # エラー
        print('subprocess error : ' + str(dnf_args) + 'return code is ' + str(return_code), file=sys.stderr)
        exit(return_code)

    # 更新あり
    dnf_args = ['dnf', 'update', '-y', '--refresh', '--best', '--allowerasing']
    return_code = subprocess.run(dnf_args).returncode
    if return_code != 0:
        # エラー
        print('subprocess error : ' + str(dnf_args) + 'return code is ' + str(return_code), file=sys.stderr)
        exit(return_code)

    # システムの再起動
    reboot_args = ['systemctl', 'reboot']
    return_code = subprocess.run(reboot_args).returncode
    exit(return_code)
