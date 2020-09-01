# Mobile App Publisher

iTunes Connect/Google Play Consoleへのビルド成果物のアップロード・自動テストを行います

# usage
* Google Play Developer Publishing API

# require
* pyenv
* python 3.8.2

## 参考
https://qiita.com/Horie1024/items/0d3d50405f0b4bef1792

## 設定
```
# global設定
brew install pyenv
pyenv install 3.8.2
brew install pipenv
# pipenv
pipenv install
pipenv shell
```

## 使い方

### Google Play
apkファイルをアップロード
```
pipenv run python bin/upload_apk_service_account.py [service_account_email] [key_file] [package_name] [apk_file] [version_name] 
```

### howto
```
HttpError 400 when requesting returned "Only releases with status draft may be created on draft app"
```
上記の場合、手動で一度google play consoleからアップすること


### iTunes Connect(TODO)

[参考](https://developer.apple.com/documentation/appstoreconnectapi/creating_api_keys_for_app_store_connect_api)

App Store Connect APIは App Store Connectの「ユーザーとアクセス」の「キー」から発行、DLしたキーをJWT(JSON Web Tokens)でアカウントを認証する。権限がない場合は「キー」タブは表示されない。

ちなみにこのキーは１度しかDLできない。

Testflightを準備
```
python bin/testflight_create.py [apple_store_key_id] [key_path] [issue_id]
```