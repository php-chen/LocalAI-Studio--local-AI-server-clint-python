
&lt;div align="center"&gt;
  &lt;h1&gt;ComfyUI API Server&lt;/h1&gt;
  &lt;p&gt;
    &lt;a href="README.md"&gt;🇺🇸 English&lt;/a&gt; · 
    &lt;a href="README.zh-TW.md"&gt;🇹🇼 繁體中文&lt;/a&gt; · 
    &lt;a href="README.ja.md"&gt;🇯🇵 日本語&lt;/a&gt;
  &lt;/p&gt;
&lt;/div&gt;

---

## 📋 项目简介

ComfyUI API Server 是一个基于 Flask 的 ComfyUI 远程控制 API 服务，支持图像和视频生成任务的管理和监控。该项目提供了完整的工作流管理、任务队列、状态监控等功能，让你可以轻松地将 ComfyUI 集成到自己的应用中。

## ✨ 主要特性

- 🎨 **工作流管理** - 支持加载、执行和管理多个 ComfyUI 工作流
- 📊 **任务监控** - 实时查询任务状态（等待中/执行中/已完成）
- 🖼️ **媒体获取** - 自动获取生成的图片和视频
- 🔄 **自动处理** - 后台脚本自动轮询和处理任务队列
- 📦 **轻量级** - 基于 Flask，易于部署和扩展

## 📁 项目结构

```
comfyui-api-server/
├── api/
│   └── openapi.json          # OpenAPI 3.0 API文档
├── image/
│   └── video/                # 视频存储目录
├── instance/
│   └── users.db              # SQLite数据库
├── workflows/                # ComfyUI工作流文件目录
│   ├── image_z_image_turbo-web.json
│   ├── image_z_image_turbo.json
│   └── video_wan2_2_5B_ti2v.json
├── app.py                    # Flask主应用
├── config.py                 # 配置管理
├── auto_processor.py         # 自动任务处理脚本
├── index.html                # 前端Web客户端
├── apiDetails.txt            # API端点清单
├── requirements.txt          # 依赖列表
└── README.md                 # 项目说明文档
```

## 🛠️ 安装指南

### 前置要求

- Python 3.8+
- ComfyUI 服务已启动并运行
- pip 包管理器

### 安装步骤

1. **克隆项目**

```bash
git clone &lt;your-repo-url&gt;
cd comfyui-api-server
```

2. **安装依赖**

```bash
pip install -r requirements.txt
```

## 🚀 快速开始

### 启动 API 服务

```bash
python app.py
```

服务将在 `http://localhost:5000` 启动。

### 启动自动任务处理器 (可选)

```bash
python auto_processor.py
```

该脚本将自动轮询任务队列并处理待办任务。

## 📡 API 文档

### 主要端点

| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/test_comfy` | GET | 测试 ComfyUI 连接 |
| `/api/workflows` | GET | 列出所有工作流 |
| `/api/workflow/&lt;name&gt;` | POST | 运行指定工作流 |
| `/api/history` | GET | 获取所有历史记录 |
| `/api/history/&lt;prompt_id&gt;` | GET | 获取指定任务历史 |
| `/api/image/&lt;prompt_id&gt;` | GET | 获取生成的图片/视频 |
| `/api/status` | GET | 获取系统状态 |
| `/api/view_queue` | GET | 查看队列状态 |
| `/api/task_status/&lt;prompt_id&gt;` | GET | 检查任务状态 |

### API 使用示例

**测试连接**

```bash
curl http://localhost:5000/api/test_comfy
```

**获取工作流列表**

```bash
curl http://localhost:5000/api/workflows
```

**运行工作流**

```bash
curl -X POST http://localhost:5000/api/workflow/image_z_image_turbo \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a beautiful sunset over the ocean"}'
```

**检查任务状态**

```bash
curl http://localhost:5000/api/task_status/&lt;prompt_id&gt;
```

**获取生成的图片**

```bash
curl http://localhost:5000/api/image/&lt;prompt_id&gt;
```

## 📝 工作流使用

### 添加工作流

1. 在 ComfyUI 中创建或导出你的工作流
2. 将工作流 JSON 文件保存到 `workflows/` 目录
3. 确保工作流中有一个文本节点用于输入提示词（支持 `Text Multiline` 或 `CLIPTextEncode` 类型）
4. 在工作流中将文本节点的内容设置为 `ChangeThisContent`（用于自动替换）

### 运行工作流

使用 POST 请求调用 `/api/workflow/&lt;name&gt;` 并传递 `prompt` 参数。

## 🤝 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) - 强大的节点式 AI 图像生成工具
- [Flask](https://flask.palletsprojects.com/) - 轻量级 Web 框架

---

&lt;div align="center"&gt;
  &lt;p&gt;
    &lt;a href="README.md"&gt;🇺🇸 English&lt;/a&gt; · 
    &lt;a href="README.zh-TW.md"&gt;🇹🇼 繁體中文&lt;/a&gt; · 
    &lt;a href="README.ja.md"&gt;🇯🇵 日本語&lt;/a&gt;
  &lt;/p&gt;
&lt;/div&gt;

