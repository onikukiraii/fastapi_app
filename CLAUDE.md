# fastapi_app - FastAPI プロジェクトテンプレート

## プロジェクト構成

- `backend/` - FastAPI (Python 3.14, SQLAlchemy, Alembic)。機能ごとにディレクトリを分割しています。
- `frontend/` - React 19 + TypeScript + Vite + Tailwind CSS v4
- `docs/` - 設計規約と作業手順

## 規約（MUST）

コードを書く前に、触る場所に対応するドキュメントを読むこと。

| 触る場所 | 読むもの |
|---------|---------|
| `backend/` または `frontend/` に新しいファイルを足すとき | [docs/architecture.md](docs/architecture.md) |
| `backend/**/*.py` | [docs/backend.md](docs/backend.md) |
| `backend/common/db/entities/`, `backend/alembic/`, `repository.py` | [docs/database.md](docs/database.md) |
| `backend/tests/` | [docs/backend-test.md](docs/backend-test.md) |
| `frontend/src/` | [docs/frontend.md](docs/frontend.md) |
| `frontend/src/**/__tests__/` | [docs/frontend-test.md](docs/frontend-test.md) |

新しい機能を作るときは [docs/new-api.md](docs/new-api.md)、テーブルを作るときは
[docs/new-model.md](docs/new-model.md) の手順に従ってください。

## 開発コマンド

```bash
mise install              # Python, uv, Node のセットアップ
docker compose up -d      # 全サービス起動 (API:8000, Frontend:5173, MySQL:3309)
mise run migrate          # マイグレーション実行
mise run migrate-gen "xxx" # マイグレーション生成
mise run lint             # バックエンドの Lint チェック (Ruff + mypy)
mise run lint:front       # フロントエンドの Lint チェック (ESLint + tsc)
mise run lint:all         # 全体の Lint チェック
mise run format           # バックエンドのコード整形
mise run format:front     # フロントエンドのコード自動修正
mise run dev              # バックエンド開発サーバー起動
mise run dev:front        # フロントエンド開発サーバー起動
mise run worker           # 非同期ワーカー起動 (Celery)
mise run test             # バックエンドテスト実行
mise run test:front       # フロントエンドテスト実行
mise run test:all         # 全テスト実行
mise run generate-api     # OpenAPI から TypeScript 型を生成 (API サーバー起動が必要)
mise run build:front      # フロントエンド本番ビルド
```

## コミット規約

コミット時は `/commit` スキルを使用してください。
