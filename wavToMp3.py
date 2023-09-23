#!/usr/bin/env python
"""
このプログラムは様々な音声ファイルをMP3に変換する。
これによってファイルサイズを半分以下にする。
"""
import magic
import os
import subprocess
import sys
import pathlib
import re
import glob

# ガター内の緑色のボタンを押すとスクリプトを実行します。
if __name__ == '__main__':
    args = sys.argv
    if len(args) < 2:
        # カレントディレクトリに対する処理
        cwd = os.getcwd()
        directory = pathlib.PurePath(cwd)
        directory_name = directory.name

        # wav ファイル一覧取得
        wav_files = glob.glob('*.wav') + glob.glob('*.flac')
        if len(wav_files) < 1:
            print(f'No wav file in "{directory_name}"', file=sys.stderr)
            exit(1)

        wav_files = sorted(wav_files)
        files_count = len(wav_files)

        # 変換コマンドの作成
        ffmpeg_args = ['ffmpeg']
        for file_name in wav_files:
            ffmpeg_args.append('-i')
            ffmpeg_args.append(file_name)

        ffmpeg_args.append('-c:a')
        ffmpeg_args.append('mp3')

        ffmpeg_args.append('-filter_complex')
        ffmpeg_args.append(f'concat=n={files_count}:v=0:a=1')

        ffmpeg_args.append(directory_name + '.mp3')

        return_code = subprocess.run(ffmpeg_args).returncode
        if return_code != 0:
            print('subprocess error : ' + str(ffmpeg_args) + 'return code is ' + str(return_code), file=sys.stderr)
            exit(return_code)

        exit(0)
    else:
        files = args[1:]

        for file_path in files:
            if not pathlib.Path(file_path).is_file():
                print('File error : ' + file_path + ' is a Not file', file=sys.stderr)
                continue
            elif pathlib.Path(file_path).is_symlink():
                print('File error : ' + file_path + ' is a symbolic file', file=sys.stderr)
                continue

            file_magic = magic.detect_from_filename(file_path)
            if not file_magic.mime_type.lower().startswith('video/x-matroska') and not file_magic.mime_type.lower().startswith('audio/'):
                print('File error : ' + file_path + ' is not a audio file', file=sys.stderr)
                continue

            print('PROCESSING : ' + file_path)

            output_file = re.sub( r'\.\w{3,4}$', '.mp3', file_path)

            ffmpeg_args = ['ffmpeg', '-i', file_path, '-c:a', 'mp3', output_file]
            return_code = subprocess.run(ffmpeg_args).returncode
            if return_code != 0:
                print('subprocess error : ' + str(ffmpeg_args) + 'return code is ' + str(return_code), file=sys.stderr)
                exit(return_code)

        exit(0)

# PyCharm のヘルプは https://www.jetbrains.com/help/pycharm/ を参照してください
