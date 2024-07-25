# SentenceTransformersCachedServer


このプロジェクトは SentenceTransformers による埋め込みを行う API サーバーです。

## 

# SentenceTransformers 埋め込み API サーバー

## はじめに

このリポジトリは、SentenceTransformers を使用してテキストの埋め込みを生成する FastAPI ベースの API サーバーを提供します。Redis キャッシュと Docker コンテナ化により、高速かつスケーラブルな運用が可能です。


## 機能

テキスト入力を受け取り、SentenceTransformers の encode() メソッドで埋め込みを計算します。
計算された埋め込みは Redis にキャッシュされ、次回同じテキストが入力された場合はキャッシュから高速に返されます。
Docker コンテナとして実行できるため、環境構築が容易です。
/embeddings エンドポイントで埋め込みを取得できます。

## 使用方法

### 環境構築

```bash
docker-compose up -d --build
```


### 埋め込み取得

```
curl -X POST http://localhost:8000/embeddings \
    -H 'Content-Type: application/json' \
    -d '{"input":"この文字列は日本語で書かれたテスト文字列です","model":"awesome_embedding_model"}'
```

text パラメータに埋め込みを取得したいテキストを指定します。

レスポンスは JSON 形式で、embedding フィールドに埋め込みベクトルが含まれます。

```
{
  "embedding": [
    0.0025373732205480337,
    -0.008475706912577152,
    -0.005010251421481371,
    -0.0677233338356018,
    0.04533613100647926,
    -0.046973951160907745,
    0.026564622297883034,
    0.10488858073949814,
       ....
    0.0399100000000332
  ]
}
```

### Redis キャッシュの削除

API 起動時にキャッシュをクリアします。キャッシュをクリアする場合は以下のコマンドなどで、API を再起動してください。

```
docker compose restart
```

### カスタマイズ

- SentenceTransformersモデル
  - docker-compose.yaml 内の API_HF_MODEL_NAME を変更することで、使用するモデルを変更できます。

- Redis設定
  - docker-compose.yml 内の API_REDIS_HOST 環境変数でRedisのホスト名を指定できます。

- エンドポイントURL
  - app/main.py 内の @app.post("/embeddings") デコレータを変更することで、エンドポイントの URL を変更できます。

- Listen port
  - docker-compose.yaml 内のポート番号 8000 を変更すると、リッスンするポートを変更できます。


## ライセンス

このプロジェクトは MIT ライセンスでライセンスされています。

## 注意

このAPIサーバーはデモ目的で作成されており、本番環境での利用にはセキュリティ対策などを追加する必要があります。

大量のテキストを一度に処理する場合、Redis の消費メモリ量に注意してください。

この埋め込みサーバーは、512トークン以降の文字列を処理しません。テキスト分割処理はサポートしていません。


## 作者

u-masao
