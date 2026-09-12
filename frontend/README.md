# Frontend

React 19 + TypeScript 5.9 + Vite 7 + Tailwind CSS v4 + shadcn/ui

ディレクトリ構成および依存関係のルールは [docs/architecture.md](../docs/architecture.md)、フロントエンド実装規約は
[docs/frontend.md](../docs/frontend.md)、テスト方針は [docs/frontend-test.md](../docs/frontend-test.md)
を参照してください。

## 環境構築・セットアップ

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

起動後、ブラウザで http://localhost:5173 にアクセスできます。

## API 型定義の生成

バックエンドの API サーバーが起動している状態で、以下のコマンドを実行します:

```bash
npm run generate-api
```

生成される主要ファイル:
- `src/api/schema.d.ts`: openapi-typescript によって自動生成される型定義ファイル（直接の編集は行いません）
- `src/api/constants.ts`: `schema.d.ts` から参照した型エイリアスおよび日本語ラベル定義
- `src/api/fetcher.ts`: openapi-fetch をベースにした型安全な API クライアント、およびレスポンス取り出し用の `unwrap` ヘルパー

## UI コンポーネントの追加

shadcn/ui のコンポーネントを追加する場合は、以下のコマンドを実行します:

```bash
npx shadcn add <component-name>
```

## テストの実行

```bash
npm test           # テスト実行 (Vitest)
npm run test:watch # ファイル変更を監視しながらテスト実行 (ウォッチモード)
```

## その他の開発コマンド

```bash
npm run build   # 本番用ビルド (tsc + vite build)
npm run lint    # ESLint によるコードチェック
npm run preview # 本番ビルド成果物のローカルプレビュー
```
