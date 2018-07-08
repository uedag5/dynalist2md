# dynalist2md
Dynalist data export to Markdown

`python3 filename2dyna_id.py`

でDynalistに登録しているファイル（フォルダーは除く）の全IDを表示します。

`python3 filename2dyna_id.py 'ファイル名'`

で特定のファイルのIDを表示します。

一度、ファイルIDを調べておいて（変化しないものなので）、

`python3 id2md.py 'ファイルID'`

で指定したファイルをMarkdownに出力します（標準出力）。


