
&lt;div align="center"&gt;
  &lt;h1&gt;ComfyUI API Server&lt;/h1&gt;
  &lt;p&gt;
    &lt;a href="README.md"&gt;🇺🇸 English&lt;/a&gt; · 
    &lt;a href="README.zh-CN.md"&gt;🇨🇳 简体中文&lt;/a&gt; · 
    &lt;a href="README.ja.md"&gt;🇯🇵 日本語&lt;/a&gt;
  &lt;/p&gt;
&lt;/div&gt;

---

## 📋 專案簡介

ComfyUI API Server 是一個基於 Flask 的 ComfyUI 遠端控制 API 服務，支援圖像和影片生成任務的管理與監控。該專案提供了完整的工作流程管理、任務佇列、狀態監控等功能，讓您可以輕鬆地將 ComfyUI 整合到自己的應用中。

## ✨ 主要功能

- 🎨 **工作流程管理** - 支援載入、執行和管理多個 ComfyUI 工作流程
- 📊 **任務監控** - 即時查詢任務狀態（等待中/執行中/已完成）
- 🖼️ **媒體取得** - 自動取得生成的圖片和影片
- 🔄 **自動處理** - 背景腳本自動輪詢和處理任務佇列
- 📦 **輕量級** - 基於 Flask，易於部署和擴展

## 📁 專案結構

```
comfyui-api-server/
├── api/
│   └── openapi.json          # OpenAPI 3.0 API 文件
├── image/
│   └── video/                # 影片存放目錄
├── instance/
│   └── users.db              # SQLite 資料庫
├── workflows/                # ComfyUI 工作流程檔案目錄
│   ├── image_z_image_turbo-web.json
│   ├── image_z_image_turbo.json
│   └── video_wan2_2_5B_ti2v.json
├── app.py                    # Flask 主應用
├── config.py                 # 設定管理
├── auto_processor.py         # 自動任務處理腳本
├── index.html                # 前端 Web 客戶端
├── apiDetails.txt            # API 端點清單
├── requirements.txt          # 相依套件清單
└── README.md                 # 專案說明文件
```

## 🛠️ 安裝指南

### 先決條件

- Python 3.8+
- ComfyUI 服務已啟動並執行
- pip 套件管理員

### 安裝步驟

1. **複製專案**

```bash
git clone &lt;your-repo-url&gt;
cd comfyui-api-server
```

2. **安裝相依套件**

```bash
pip install -r requirements.txt
```

## 🚀 快速開始

### 啟動 API 服務

```bash
python app.py
```

服務將在 `http://localhost:5000` 啟動。

### 啟動自動任務處理器 (選用)

```bash
python auto_processor.py
```

該腳本將自動輪詢任務佇列並處理待辦任務。

## 📡 API 文件

### 主要端點

| 端點 | 方法 | 功能 |
|------|------|------|
| `/api/test_comfy` | GET | 測試 ComfyUI 連線 |
| `/api/workflows` | GET | 列出所有工作流程 |
| `/api/workflow/&lt;name&gt;` | POST | 執行指定工作流程 |
| `/api/history` | GET | 取得所有歷史記錄 |
| `/api/history/&lt;prompt_id&gt;` | GET | 取得指定任務歷史 |
| `/api/image/&lt;prompt_id&gt;` | GET | 取得生成的圖片/影片 |
| `/api/status` | GET | 取得系統狀態 |
| `/api/view_queue` | GET | 查看佇列狀態 |
| `/api/task_status/&lt;prompt_id&gt;` | GET | 檢查任務狀態 |

### API 使用範例

**測試連線**

```bash
curl http://localhost:5000/api/test_comfy
```

**取得工作流程清單**

```bash
curl http://localhost:5000/api/workflows
```

**執行工作流程**

```bash
curl -X POST http://localhost:5000/api/workflow/image_z_image_turbo \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a beautiful sunset over the ocean"}'
```

**檢查任務狀態**

```bash
curl http://localhost:5000/api/task_status/&lt;prompt_id&gt;
```

**取得生成的圖片**

```bash
curl http://localhost:5000/api/image/&lt;prompt_id&gt;
```

## 📝 工作流程使用

### 新增工作流程

1. 在 ComfyUI 中建立或匯出您的工作流程
2. 將工作流程 JSON 檔案存儲到 `workflows/` 目錄
3. 確保工作流程中有一個文字節點用於輸入提示詞（支援 `Text Multiline` 或 `CLIPTextEncode` 類型）
4. 在工作流程中將文字節點的內容設定為 `ChangeThisContent`（用於自動替換）

### 執行工作流程

使用 POST 請求呼叫 `/api/workflow/&lt;name&gt;` 並傳遞 `prompt` 參數。

## 🤝 貢獻指南

歡迎貢獻！請遵循以下步驟：

1. Fork 本儲存庫
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 建立 Pull Request

## 📄 授權

本專案採用 MIT 授權 - 詳見 [LICENSE](LICENSE) 檔案。

## 🙏 致謝

- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) - 強大的節點式 AI 圖像生成工具
- [Flask](https://flask.palletsprojects.com/) - 輕量級 Web 框架

---

&lt;div align="center"&gt;
  &lt;p&gt;
    &lt;a href="README.md"&gt;🇺🇸 English&lt;/a&gt; · 
    &lt;a href="README.zh-CN.md"&gt;🇨🇳 简体中文&lt;/a&gt; · 
    &lt;a href="README.ja.md"&gt;🇯🇵 日本語&lt;/a&gt;
  &lt;/p&gt;
&lt;/div&gt;

