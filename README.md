# これは何？

lambda + OANDA APIで為替レートをDynamoDBに登録します。  
参考：https://takilog.com/oandaapi-get-pricingstream/#OANDA_API

# 使い方

aws cliの設定をする  
https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/cli-chap-welcome.html


OANDA APIのアカウントナンバー、アクセストークンを取得  
https://takilog.com/oandaapi-get-pricingstream/#OANDA_API

code/account.pyを以下内容で作成

```
account_number = "000-000-00000000-000"
access_token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

code/packageフォルダを作成、以下コマンドで必要なパッケージを持ってくる

```
cd code/package
pip install oandapyV20 -t ./
pip install requests -t ./
```

MakefileでS3バケット名、CFスタック名を指定

```
BUCKET_NAME := XXXXX-bucket-for-deploy
STACK_NAME := XXXXX-exchange
```

以下コマンドでデプロイ
```
make all
```

取得する通貨ペアはevent.jsonで指定  

デフォルトではデモ口座でUSDJPYの値を取得  

本口座を使う場合はevent.jsonのpracticeをliveに変更する

DynamoDBのテーブル名は通貨ペア（USD_JPY等）と同じにする  
パーティションキー名はDATETIME（文字列）