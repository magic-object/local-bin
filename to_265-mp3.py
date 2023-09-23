#!/usr/bin/env python
"""
このプログラムは H.264 を x265 に変換し、音声をMP3にする。
これにより動画のファイルサイズを半分以下にする。
"""

import magic
import os
import subprocess
import sys
import pathlib
import re

if __name__ == '__main__':
    args = sys.argv
    if len( args ) < 2:
        exit( 1 )

    for filePath in args[1:]:
        if not pathlib.Path( filePath ).is_file():
            print( 'File error : ' + filePath + ' is a Not file', file=sys.stderr )
            continue
        elif pathlib.Path( filePath ).is_symlink():
            print( 'File error : ' + filePath + ' is a symbolic file', file=sys.stderr )
            continue

        fileMagic = magic.detect_from_filename( filePath )
        if not fileMagic.mime_type.lower().startswith('video/'):
            print( 'File error : ' + filePath + ' is not a movie file', file=sys.stderr )
            continue

        print( 'PROCESSING : ' + filePath )
        
        fileName = pathlib.Path( filePath ).name
        target = re.search( '(264)|((?=\s)AVC(?=\s))', fileName )
        if target:
            outFileName = re.sub( '(264)|((?=\s)AVC(?=\s))', '265', fileName )
            fileName = outFileName
            outFile = pathlib.Path( filePath ).parent.joinpath( outFileName )
        else:
            outFileName = re.sub( r'\.(?=[0-9a-zA-Z]+$)', '-x265.', fileName )
            fileName = outFileName
            outFile = pathlib.Path( filePath ).parent.joinpath( outFileName )

        target = re.search( '(FLAC)', fileName )
        if target:
            outFileName = re.sub( '(FLAC)', 'MP3', fileName )
            fileName = outFileName
            outFile = pathlib.Path( filePath ).parent.joinpath( outFileName )

        if outFile.suffix == '.m2ts':
            outFile = outFile.with_suffix('.mp4')

        ffmpegArgs = [ 'ffmpeg', '-i', filePath, '-map', '0', '-c:v', 'libx265', '-c:a', 'mp3', '-c:s', 'copy', str( outFile ) ]
        returnCode =  subprocess.run( ffmpegArgs ).returncode
        if returnCode != 0:
            print( 'subprocess error : '  + str( ffmpegArgs ) + 'return code is ' + str( returnCode ), file=sys.stderr )
            exit( returnCode )


    exit( 0 )
