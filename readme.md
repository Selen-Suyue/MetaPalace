# MetaPalace
[英文版介绍](readme_en.md)

本项目旨在以数字科技唤醒故宫典藏，为千年文物注入现代活力。我们精心构建沉浸式数字互动平台，邀您开启跨时空的文化邂逅：轻触唤醒文物超清影像，360度全维度3D模型即刻呈现。AI技术自动生成的知识增强型讲解系统，配合专业语音导览，为您打造全天候私人文物策展体验。每一道纹路都在讲述文明密码，每件瑰宝皆可对话历史回响。通过虚实融合的交互设计，我们让文化遗产在数字维度焕发新生，构建穿越时空的文明对话。✨

该项目由 [Yue Su](https://selen-suyue.github.io),[xj63](https://github.com/xj63),[Kai Li](https://github.com/wink-snow),[Zefeng Wu](https://github.com/windansnowman),[Ruihan Wu](https://github.com/cool-chicken)完成，...

欢迎访问我们的 [网站](https://metapalace.xj63.fun),以及这是我们的[前端设计](https://github.com/xj63/MetaPalaceSite)。

## 项目详情

**`meta.py` ：**

## 运行方法

  1. **安装所需代码库：**

     ```bash
     conda create -n meta python==3.9
     pip install -r requirements.txt 
     ```

  2. **获取 Google Gemini API 密钥：**

     您需要注册一个 Google 账户，启用 Gemini API 并获取 API 密钥。有关详细信息，请参阅官方 Google AI 文档：[Google aistudio api docs](https://aistudio.google.com/apikey)

     将您的 API 密钥复制到 `api_key.txt` 文件的第一行。**不要将 `api_key.txt` 文件提交到版本控制中！**

  4. **运行应用程序：**

     ```bash
     python meta.py
     ```

## 示例

## 注意事项

## 文件结构
```
MetaPalace/
├── .github/
│   └── workflows/
│       └── process_fig_files.yml  # GitHub Actions 工作流程文件
├── Fig/                           # 存放原始 PNG 图片
├── GLB/                           # 存放生成的 GLB 文件
├── RAG/
│   ├── archive/
│   │   └── archived_assets.txt   # 记录爬取失败的文物名称
│   ├── data/                     # 存放文物描述信息的文本文件
│   ├── db/
│   │   └── qdrant/
│   │       ├── collection        # Qdrant 数据库文件 (向量数据)
│   │       └── meta.json         # Qdrant 数据库元数据，包含集合信息
│   ├── langchain_gemini.py       # RAG 链的主文件，使用 Langchain 和 Gemini LLM
│   ├── models/
│   │   ├── bge_embedding.py      # BGE 嵌入模型，用于生成文本向量
│   │   ├── data_handler.py       # 数据处理脚本，用于加载、清洗和分割文本数据
│   │   ├── gemini_llm.py         # Gemini LLM 封装，用于调用 Google Gemini 模型
│   │   └── qdrant_db_manager.py  # Qdrant 数据库管理脚本，用于创建、连接和操作 Qdrant 数据库
│   ├── RAG.requirements.txt      # RAG 目录的依赖文件
│   └── scripts/
│       ├── baike_spider.py       # 爬虫脚本，用于从百度百科爬取文物信息
│       ├── file_handler.py       # 文件处理脚本，用于读写文物信息
│       ├── get_proxy.py          # 获取代理 IP
│       ├── handle_qdrant_db.py   # Qdrant 数据库处理脚本，用于初始化和获取向量数据库
│       └── glob_assets_name.py    # 用于生成文物名称列表
├── Video/                         # 存放生成的视频文件的目录
├── script/
│   ├── process_fig_files.py       # Python 脚本，用于处理图片并生成 3D 模型和视频
│   └── process_fig_files.requirements.txt # Python 依赖文件
├── api_key.txt                    # 存放 Google Gemini API 密钥的文件 (*需要用户具体配置*)
├── meta.py                        # 主应用程序文件
├── readme.md                      # 中文版 README 文件
└── readme_en.md                   # 英文版 README 文件
└── requirements.txt               # 项目依赖文件
```

## GitHub Actions

- **process_fig_files** 自动处理 `Fig` 文件夹中新增的图片，触发自动生成相应3d模型等操作。
- **assets_build** 自动提取 `main` 分支的资源到 `assets` 分支中。
  1. assets_build 会调用 `.github/script/extract_assets.py` 来提取 `main` 资源到 `build` 文件夹中
  2. `build` 文件夹会自动写入 `assets` 分支
  3. `assets` 分支中的文件会自动部署到 `assets.metapalace.xj63.fun` 中，
