#インターフェース 2017年4月号 のサンプルプログラム

## SCORER SDK のインストール
下記のページより、SCORER SDK のイメージをダウンロードして、SDカードを作成します。
https://peraichi.com/landing_pages/view/scorersdk

## 環境変数の設定
SCORER を起動し、Cloud9 を立ち上げたら、日本語を扱うためにシェルから下記のコマンドを実行してロケール環境変数を設定します。
```
export LC_CTYPE=ja_JP.utf8
```

## プログラムの取得
下記のコマンドを実行して、プログラムをダウンロードします。
```
git clone https://github.com/kndt84/interface-ai-tutorial.git

cd interface-ai-tutorial
```
## APIキーの設定

### Compute Vision API
下記のページにアクセスし、Computer Vision API のキーを取得します。   
https://www.microsoft.com/cognitive-services/en-US/subscriptions

### Translator API
下記のページを参考にTranslator API のキーを取得します。   
https://www.microsoft.com/ja-jp/translator/getstarted.aspx

### 設定
プログラムの下記の場所に取得したキーを貼り付けます。  
https://github.com/kndt84/interface-ai-tutorial/blob/master/speak_img_caption.py#L18

## プログラムの実行
下記のコマンドを実行することでプログラムが実行されます。
```
python3 speak_img_caption.py
```

