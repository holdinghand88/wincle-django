# Wincleシステム
#### Wincleはあらゆる業種の予約・物販・マーケティングをLINE公式アカウントで自動化、情報の一元管理ができるシステムです。
## バックエンド
### Django 4.0.6, python 3.10
## フロントエンド
### LIFF, Javascript, HTML/CSS

## MacOSにDjangoをインストールする手順
### Pythonの仮想環境を作成します。
#### python3 -m venv <仮想環境名>
### パッケージ設置
#### pip3 install -r requirements.txt
### マイグレーション
#### python3 manage.py makemigrations
#### python3 manage.py migrate
### super-admin創造
#### python3 manage.py createsuperuser
### RUN
#### python3 manage.py runserver
