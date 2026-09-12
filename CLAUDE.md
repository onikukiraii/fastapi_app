# fastapi_app - FastAPI プロジェクトテンプレート

## プロジェクト構成

- `backend/` - FastAPI (Python 3.14, SQLAlchemy, Alembic)。機能ごとにディレクトリを分割しています。
- `frontend/` - React 19 + TypeScript + Vite + Tailwind CSS v4
- `docs/` - 設計規約と作業手順

## 規約（MUST）

規約の実体は `docs/` にあります。ここは読み込みの目次で、以下の3本は常に適用されます。

@docs/architecture.md
@docs/backend.md
@docs/frontend.md

以下は該当する作業をするときに読んでください。

| 作業 | 読むもの |
|------|---------|
| テーブル定義・クエリ・マイグレーションを触る | `docs/database.md` |
| `backend/tests/` にテストを書く | `docs/backend-test.md` |
| `frontend/src/**/__tests__/` にテストを書く | `docs/frontend-test.md` |
| 新しい機能を作る | `docs/new-api.md` |
| 新しいテーブルを作る | `docs/new-model.md` |

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
