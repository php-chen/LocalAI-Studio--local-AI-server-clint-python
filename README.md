
# ComfyUI API Server

[🇨🇳 简体中文](README.zh-CN.md) · [🇹🇼 繁體中文](README.zh-TW.md) · [🇯🇵 日本語](README.ja.md)

---

## 📋 Project Overview

ComfyUI API Server is a Flask-based remote control API service for ComfyUI, supporting management and monitoring of image and video generation tasks. This project provides complete workflow management, task queuing, status monitoring, and more, making it easy to integrate ComfyUI into your own applications.

## ✨ Key Features

- 🎨 **Workflow Management** - Load, execute, and manage multiple ComfyUI workflows
- 📊 **Task Monitoring** - Real-time query of task status (pending/running/completed)
- 🖼️ **Media Retrieval** - Automatically fetch generated images and videos
- 🔄 **Auto Processing** - Background script for automatic task queue polling and processing
- 📦 **Lightweight** - Flask-based, easy to deploy and extend

## 📁 Project Structure

```
comfyui-api-server/
├── api/
│   └── openapi.json          # OpenAPI 3.0 API documentation
├── image/
│   └── video/                # Video storage directory
├── instance/
│   └── users.db              # SQLite database
├── workflows/                # ComfyUI workflow files directory
│   ├── image_z_image_turbo-web.json
│   ├── image_z_image_turbo.json
│   └── video_wan2_2_5B_ti2v.json
├── app.py                    # Flask main application
├── config.py                 # Configuration management
├── auto_processor.py         # Auto task processing script
├── index.html                # Frontend web client
├── apiDetails.txt            # API endpoint list
├── requirements.txt          # Dependency list
└── README.md                 # Project documentation
```

## 🛠️ Installation Guide

### Prerequisites

- Python 3.8+
- ComfyUI service running
- pip package manager

### Installation Steps

1. **Clone the project**

```bash
git clone &lt;your-repo-url&gt;
cd comfyui-api-server
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

### Start API Service

```bash
python app.py
```

Service will start at `http://localhost:5000`.

### Start Auto Task Processor (Optional)

```bash
python auto_processor.py
```

This script will automatically poll the task queue and process pending tasks.

## 📡 API Documentation

### Main Endpoints

| Endpoint | Method | Function |
|----------|--------|----------|
| `/api/test_comfy` | GET | Test ComfyUI connection |
| `/api/workflows` | GET | List all workflows |
| `/api/workflow/&lt;name&gt;` | POST | Run specified workflow |
| `/api/history` | GET | Get all history records |
| `/api/history/&lt;prompt_id&gt;` | GET | Get specified task history |
| `/api/image/&lt;prompt_id&gt;` | GET | Get generated images/videos |
| `/api/status` | GET | Get system status |
| `/api/view_queue` | GET | View queue status |
| `/api/task_status/&lt;prompt_id&gt;` | GET | Check task status |

### API Usage Examples

**Test Connection**

```bash
curl http://localhost:5000/api/test_comfy
```

**Get Workflow List**

```bash
curl http://localhost:5000/api/workflows
```

**Run Workflow**

```bash
curl -X POST http://localhost:5000/api/workflow/image_z_image_turbo \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a beautiful sunset over the ocean"}'
```

**Check Task Status**

```bash
curl http://localhost:5000/api/task_status/&lt;prompt_id&gt;
```

**Get Generated Images**

```bash
curl http://localhost:5000/api/image/&lt;prompt_id&gt;
```

## 📝 Workflow Usage

### Adding Workflows

1. Create or export your workflow in ComfyUI
2. Save the workflow JSON file to the `workflows/` directory
3. Ensure there's a text node in the workflow for prompt input (supports `Text Multiline` or `CLIPTextEncode` types)
4. Set the text node content to `ChangeThisContent` in the workflow (for automatic replacement)

### Running Workflows

Use POST request to call `/api/workflow/&lt;name&gt;` and pass the `prompt` parameter.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [ComfyUI](https://github.com/comfyanonymous/ComfyUI) - Powerful node-based AI image generation tool
- [Flask](https://flask.palletsprojects.com/) - Lightweight web framework

---

&lt;div align="center"&gt;
  &lt;p&gt;
    &lt;a href="README.zh-CN.md"&gt;🇨🇳 简体中文&lt;/a&gt; · 
    &lt;a href="README.zh-TW.md"&gt;🇹🇼 繁體中文&lt;/a&gt; · 
    &lt;a href="README.ja.md"&gt;🇯🇵 日本語&lt;/a&gt;
  &lt;/p&gt;
&lt;/div&gt;

