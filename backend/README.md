# Backend

FastAPI + SQLAlchemy + Alembic / Python 3.14 / パッケージ管理: uv

機能（ドメイン）単位でディレクトリを分割し、レイヤー（層）ごとの横断的なディレクトリ分割は行いません。1つの機能に関するコードを1つのディレクトリ内に集約して管理します。

新規機能の追加手順は [docs/new-api.md](../docs/new-api.md)、テーブルの追加手順は [docs/new-model.md](../docs/new-model.md) を参照してください。また、アーキテクチャ設計規約は [docs/architecture.md](../docs/architecture.md)、バックエンド実装規約は [docs/backend.md](../docs/backend.md)、データベース設計規約は [docs/database.md](../docs/database.md)、テスト方針は [docs/backend-test.md](../docs/backend-test.md) を参照してください。

## ディレクトリ構成

```
backend/
├── main.py                     FastAPI アプリケーションのエントリーポイント
├── dependencies.py             コンポジションルート（具象クラスを注入する唯一の場所）
│
├── user/                       機能ディレクトリ（最小の実装サンプル）
│   ├── router.py
│   ├── service.py
│   ├── _pure.py
│   ├── protocol.py             ★ 抽象インターフェースはここだけに定義
│   ├── repository.py
│   ├── types.py
│   └── dto.py
│
├── invoice/                    機能ディレクトリ（DB・S3・非同期ジョブを利用するサンプル）
│   ├── router.py service.py _pure.py protocol.py repository.py types.py dto.py
│   └── gateway.py              この機能のみで使用する外部連携処理（PDF 生成など）
│
├── review/                     機能ディレクトリ（LLM を利用するサンプル）
│   ├── router.py service.py _pure.py protocol.py repository.py types.py dto.py
│   └── prompts.py              プロンプト定義（文言のみ）
│
├── common/
│   ├── db/
│   │   ├── entities/           全テーブル定義（マイグレーションの都合上ここだけ横断管理）
│   │   └── session.py
│   ├── gateway/
│   │   ├── protocol.py         ★ 共通の外部連携インターフェース（Storage / LLM / JobQueue）
│   │   ├── storage_s3.py
│   │   ├── llm_claude.py
│   │   └── job_queue_celery.py
│   ├── errors.py               ドメイン例外定義
│   └── config.py               環境変数・設定
│
├── worker/
│   ├── app.py                  Celery アプリケーション
│   └── tasks.py
│
├── alembic/                    マイグレーション設定および履歴
└── tests/                      機能ディレクトリに対応するテストコード
    ├── fakes.py                テスト用の Fake 実装（FakeStorage, FakeLLM, InMemory*Repository）
    ├── conftest.py
    └── user/ invoice/ review/
```

※ ★ 印が付いているファイルのみが抽象インターフェース（Protocol）を定義しており、それ以外のファイルはすべて具象実装です。

## 遵守すべき3つの依存ルール

1. **`_pure.py` が import してよいのは `types.py`、`prompts.py`、`common/errors.py` のみです。**
2. **`service.py` は具象実装ファイルを import せず、`protocol.py` のインターフェースのみを参照します。**
3. **他機能の `protocol.py` を直接呼び出さず、必ず対象機能の `service.py` の関数を経由して呼び出します。**

これにより、すべての依存関係が抽象である `protocol.py` に向かって一方向に流れます。具象実装クラスが他から直接参照されることはなく、`dependencies.py`（コンポジションルート）のみが具象クラスを参照して依存性を注入します。

## 提供 API 一覧

| メソッド | パス | 説明 |
|---------|------|------|
| GET | `/users/` | ユーザー一覧の取得 |
| POST | `/users/` | ユーザーの作成 |
| GET | `/invoices/` | 請求書一覧の取得 |
| POST | `/invoices/` | 請求書の作成（下書き） |
| POST | `/invoices/{id}/issue` | 請求書の発行（PDF を生成して S3 に保存） |
| POST | `/invoices/{id}/issue-async` | 請求書発行ジョブのエンキュー（非同期処理） |
| GET | `/invoices/{id}/pdf-url` | PDF 取得用の署名付き URL を発行 |
| GET | `/reviews/` | レビュー一覧の取得 |
| POST | `/reviews/` | 契約書レビューの実行（LLM を呼び出し） |
| GET | `/reviews/{uid}` | 特定レビューの詳細取得 |

※ `user` と `invoice` は初期実装例として連番の `id` を返却していますが、新規に作成する機能では `review` のように UUID（`uid`）を使用することを推奨します。

## 開発コマンド

```bash
uv run fastapi dev                    # 開発サーバー起動
uv run celery -A worker.app worker    # 非同期ワーカー起動
uv run pytest -v                      # テスト実行
uv run ruff check . && uv run ruff format --check . && uv run mypy .  # Lint チェック
uv run alembic upgrade head           # マイグレーション実行
uv run alembic revision --autogenerate -m "xxx"  # マイグレーションファイル生成
```

リポジトリのルートディレクトリからも、`mise run dev`、`mise run test`、`mise run lint`、`mise run migrate` などのコマンドで同様に実行可能です。

## 環境変数

`.env.template` をコピーして `.env` を作成します。必須の設定項目は `DATABASE_URL` のみで、その他の項目にはローカル開発用のデフォルト値があらかじめ設定されています。

| 変数 | 用途 |
|------|------|
| `DATABASE_URL` | MySQL 接続情報 |
| `S3_BUCKET` `S3_ENDPOINT_URL` `S3_REGION` | オブジェクトストレージ設定（ローカル環境では MinIO を使用） |
| `AWS_ACCESS_KEY_ID` `AWS_SECRET_ACCESS_KEY` | boto3 が使用する AWS 認証情報（本番環境では IAM ロール等を利用するため空で問題ありません） |
| `ANTHROPIC_API_KEY` | LLM 連携用 API キー（`review` 機能を使用する場合のみ必須） |
| `LLM_MODEL` `LLM_MAX_TOKENS` | 使用する LLM モデルおよび最大トークン数の設定 |
| `CELERY_BROKER_URL` | 非同期ジョブのブローカー URL（Redis） |
| `CORS_ORIGINS` | CORS で許可するオリジン（JSON 配列形式で指定） |

## 不要な機能の削除

本テンプレートにはすべてのサンプル機能が含まれています。プロジェクトで使用しない機能は、開発初期の段階で削除することを推奨します（独自コードを追加する前であれば、最小限の手間で安全に削除できます）。

| 削除する機能 | あわせて削除するもの |
|-------------|---------------------|
| `invoice/` | `common/db/entities/invoice.py` および `__init__.py` 内の該当行、`tests/invoice/`、`dependencies.py` 内の `get_invoice_repository` と `get_pdf_renderer`、`main.py` のルーター読み込み、`worker/tasks.py` 内のタスク、`pyproject.toml` の `reportlab` 依存関係 |
| `review/` | `common/db/entities/review.py` および `__init__.py` 内の該当行、`tests/review/`、`dependencies.py` 内の `get_review_repository` と `get_llm`、`common/gateway/llm_claude.py`、`common/gateway/protocol.py` の `LLM` 定義、`pyproject.toml` の `anthropic` 依存関係 |
| `worker/` | `common/gateway/job_queue_celery.py`、`common/gateway/protocol.py` の `JobQueue` 定義、`dependencies.py` の `get_job_queue`、`compose.yaml` の `worker` および `redis` サービス、`pyproject.toml` の `celery` 依存関係 |
| S3 を使用しない場合 | `common/gateway/storage_s3.py`、`common/gateway/protocol.py` の `Storage` 定義、`dependencies.py` の `get_storage`、`compose.yaml` の `minio` および `minio-init` サービス、`pyproject.toml` の `boto3` 依存関係 |

不要な機能を削除した後は、`uv run pytest` と `uv run mypy .` を実行して削除漏れや型エラーがないか確認してください。

`alembic/versions/` ディレクトリは初期状態では空になっています。不要な機能の削除が完了した後に `mise run migrate-gen "initial"` を実行することで、必要な entity のみを含んだ初期マイグレーションファイルを生成できます。先にマイグレーションファイルを生成してしまうと、削除予定のテーブル定義がマイグレーション履歴に含まれてしまうため注意してください。
