
# ComfyUI API Server

[🇺🇸 English](README.md) · [🇨🇳 简体中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md)

---

## 📋 プロジェクト概要

ComfyUI API Server は、Flask ベースの ComfyUI リモートコントロール API サービスで、画像と動画の生成タスクの管理と監視をサポートします。このプロジェクトは、ワークフロー管理、タスクキュー、状態監視などの完全な機能を提供し、ComfyUI を自分のアプリケーションに簡単に統合できるようにします。

## ✨ 主な特徴

- 🎨 **ワークフロー管理** - 複数の ComfyUI ワークフローの読み込み、実行、管理をサポート
- 📊 **タスク監視** - タスク状態のリアルタイムクエリ（待機中/実行中/完了）
- 🖼️ **メディア取得** - 生成された画像と動画を自動的に取得
- 🔄 **自動処理** - タスクキューを自動的にポーリングして処理するバックグラウンドスクリプト
- 📦 **軽量** - Flask ベースで、デプロイと拡張が容易

## 📁 プロジェクト構成

```
comfyui-api-server/
├── api/
│   └── openapi.json          # OpenAPI 3.0 API ドキュメント
├── image/
│   └── video/                # 動画保存ディレクトリ
├── instance/
│   └── users.db              # SQLite データベース
├── workflows/                # ComfyUI ワークフローファイルディレクトリ
│   ├── image_z_image_turbo-web.json
│   ├── image_z_image_turbo.json
│   └── video_wan2_2_5B_ti2v.json
├── app.py                    # Flask メインアプリケーション
├── config.py                 # 設定管理
├── auto_processor.py         # 自動タスク処理スクリプト
├── index.html                # フロントエンド Web クライアント
├── apiDetails.txt            # API エンドポイント一覧
├── requirements.txt          # 依存関係リスト
└── README.md                 # プロジェクトドキュメント
```

## 🛠️ インストールガイド

### 前提条件

- Python 3.8+
- ComfyUI サービスが実行中
- pip パッケージマネージャー

### インストール手順

1. **プロジェクトをクローン**

```bash
git clone &lt;your-repo-url&gt;
cd comfyui-api-server
```

2. **依存関係をインストール**

```bash
pip install -r requirements.txt
```

## 🚀 クイックスタート

### API サービスを起動

```bash
python app.py
```

サービスは `http://localhost:5000` で起動します。

### 自動タスクプロセッサーを起動 (オプション)

```bash
python auto_processor.py
```

このスクリプトは、タスクキューを自動的にポーリングして保留中のタスクを処理します。

## 📡 API ドキュメント

### 主なエンドポイント

| エンドポイント | メソッド | 機能 |
|----------------|----------|------|
| `/api/test_comfy` | GET | ComfyUI 接続をテスト |
| `/api/workflows` | GET | すべてのワークフローを一覧表示 |
| `/api/workflow/&lt;name&gt;` | POST | 指定したワークフローを実行 |
| `/api/history` | GET | すべての履歴レコードを取得 |
| `/api/history/&lt;prompt_id&gt;` | GET | 指定したタスクの履歴を取得 |
| `/api/image/&lt;prompt_id&gt;` | GET | 生成された画像/動画を取得 |
| `/api/status` | GET | システム状態を取得 |
| `/api/view_queue` | GET | キュー状態を表示 |
| `/api/task_status/&lt;prompt_id&gt;` | GET | タスク状態をチェック |

### API 使用例

**接続テスト**

```bash
curl http://localhost:5000/api/test_comfy
```

**ワークフロー一覧を取得**

```bash
curl http://localhost:5000/api/workflows
```

**ワークフローを実行**

```bash
curl -X POST http://localhost:5000/api/workflow/image_z_image_turbo \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a beautiful sunset over the ocean"}'
```

**タスク状態をチェック**

```bash
curl http://localhost:5000/api/task_status/&lt;prompt_id&gt;
```

**生成された画像を取得**

```bash
curl http://localhost:5000/api/image/&lt;prompt_id&gt;
```

## 📝 ワークフローの使用

### ワークフローを追加

1. ComfyUI でワークフローを作成またはエクスポート
2. ワークフロー JSON ファイルを `workflows/` ディレクトリに保存
3. プロンプト入力用のテキストノードがワークフローにあることを確認（`Text Multiline` または `CLIPTextEncode` タイプをサポート）
4. ワークフローでテキストノードの内容を `ChangeThisContent` に設定（自動置換用）

### ワークフローを実行

POST リクエストで `/api/workflow/&lt;name&gt;` を呼び出し、`prompt` パラメータを渡します。

## 🤝 コントリビューション

コントリビューションは大歓迎です！以下の手順に従ってください：

1. このリポジトリを Fork
2. 機能ブランチを作成 (`git checkout -b feature/AmazingFeature`)
3. 変更をコミット (`git commit -m 'Add some AmazingFeature'`)
4. ブランチにプッシュ (`git push origin feature/AmazingFeature`)
5. Pull Request を開く

## 📄 ライセンス

このプロジェクトは MIT ライセンスの下でライセンスされています - 詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 🙏 謝辞

- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) - 強力なノードベースの AI 画像生成ツール
- [Flask](https://flask.palletsprojects.com/) - 軽量な Web フレームワーク

---

[🇺🇸 English](README.md) · [🇨🇳 简体中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md)

