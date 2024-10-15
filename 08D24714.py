# [情報システム工学演習 課題提出用ファイル]

# 説明
# 本ファイルに実装し、`{学籍番号}.py`にリネームの上、必要な入力データ（あれば）とあわせて`{学籍番号}.zip`にまとめること。
# この際、`{学籍番号}.py`を実行したらそのまま読み込める場所に入力データを配置しておくことが望ましい（それが難しい場合はどこかにその旨記載しておくこと）。
# レポートをコンパイルしたもの（`{学籍番号}.pdf`）と合わせてCLEから提出すること。

# ---
# 課題情報
#
# 提出者（以下を書き換え）
submission_id = '08D24714'
# 氏名（以下を書き換え）
submission_name = '山脇颯太'

# 概要
# 実装したアプリ・システム・ツールの概要・アピールポイント（簡潔に。詳細はレポートに記入すること）：
submission_highlights = '...'
#
# 実行に準備（インストールや実行環境）が必要な場合、内容をここに記入。pipで入るものなら、requirements.txtを同梱してくれると更にありがたい：
submission_requirements = '...'
# ---

import cv2
import numpy as np  # PythonのOpenCVでは、画像はnumpyのarrayとして管理される
from PIL import Image
import matplotlib.pyplot as plt

import sys
from utils import add_lipstick, hide_save_message, reveal_message, decorate, help_message

# 加工元ファイルの読み込み
if len(sys.argv) < 3:
    help_message()
    sys.exit(1)

command = sys.argv[1]
src_name = sys.argv[2]

if command == "help":
    help_message()
elif command == "hide":
    if len(sys.argv) < 4:
        help_message()
        sys.exit(1)
    msg = sys.argv[3]
    hide_save_message(src_name,msg)
elif command == "reveal":
    print(reveal_message(src_name))
elif command == "deco":
    if len(sys.argv) < 4:
        help_message()
        sys.exit(1)
    output_path = sys.argv[3]
    decorate(src_name, output_path)
