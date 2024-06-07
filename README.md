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
/v1/embeddings エンドポイントで埋め込みを取得できます。

## 使用方法

### 環境構築

```bash
    docker-compose up -d --build
```


### 埋め込み取得

```
    http://localhost:8000/embeddings?input=あなたのテキスト
```

input パラメータに埋め込みを取得したいテキストを指定します。
レスポンスはJSON形式で、embedding フィールドに埋め込みベクトルが含まれます。

### カスタマイズ

SentenceTransformersモデル:
app/main.py 内の model = SentenceTransformer('all-mpnet-base-v2') を変更することで、使用するモデルを変更できます。

Redis設定:
docker-compose.yml 内の REDIS_HOST 環境変数でRedisのホスト名を指定できます。

エンドポイントURL:
app/main.py 内の @app.get("/v1/embeddings") デコレータを変更することで、エンドポイントのURLを変更できます。

## ライセンス

このプロジェクトは MIT ライセンスでライセンスされています。

## 注意

このAPIサーバーはデモ目的で作成されており、本番環境での利用にはセキュリティ対策などを追加する必要があります。
大量のテキストを一度に処理する場合、Redisのメモリ容量に注意してください。

## 作者

u-masao
