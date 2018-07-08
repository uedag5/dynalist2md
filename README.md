# dynalist2md
Dynalist data export to Markdown

## 利用前にAPI Tokenを生成ください
[Dynalist Developer Page](https://dynalist.io/developer)でSecret tokenを生成してください。
生成したTokenを`.bashrc`などで

`export Dynalist_API_KEY='生成したSecretToken here'`

として、環境変数にexportしてください。

---

## 利用方法

### filename2dyna_id.py → ファイル名からID特定

`python3 filename2dyna_id.py`

でDynalistに登録しているファイル（フォルダーは除く）の全IDを表示します。

`python3 filename2dyna_id.py 'ファイル名'`

で特定のファイルのIDを表示します。このIDは途中で変化しません。
APIがそれほど速くないこともあり、一度生成し、使い回すことが出来るようにツールを分割しました。

### id2md.py → ID指定したファイルをMarkdownへ（標準出力）

一度、ファイルIDを調べておいて（変化しないものなので）、

`python3 id2md.py 'ファイルID'`

で指定したファイルをMarkdownに出力します（標準出力）。


