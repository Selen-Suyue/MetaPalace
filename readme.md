# MetaPalace
[英文版介绍](readme_en.md)

本项目旨在以数字科技唤醒故宫典藏，为千年文物注入现代活力。我们精心构建沉浸式数字互动平台，邀您开启跨时空的文化邂逅：轻触唤醒文物超清影像，360度全维度3D模型即刻呈现。AI技术自动生成的知识增强型讲解系统，配合专业语音导览，为您打造全天候私人文物策展体验。每一道纹路都在讲述文明密码，每件瑰宝皆可对话历史回响。通过虚实融合的交互设计，我们让文化遗产在数字维度焕发新生，构建穿越时空的文明对话。✨

该项目由 [Yue Su](https://selen-suyue.github.io),[xj63](https://github.com/xj63),[Kai Li](https://github.com/wink-snow),[Zefeng Wu](https://github.com/windansnowman),[Ruihan Wu](https://github.com/cool-chicken)完成，...

欢迎访问我们的网站 [MetaPalaceSite](https://metapalace.xj63.fun/),以及这是我们的[前端设计](https://github.com/xj63/MetaPalaceSite)。


## 项目详情
1. **高精度 3D 模型生成**：
   - 利用计算机视觉技术和深度学习算法，从超高清图片生成高精度的 3D 模型。
   - 通过 GitHub Actions 自动化工作流，实时处理用户上传的图片，生成对应的 3D 模型和视频。

2. **AI 驱动的知识增强型讲解系统**：
   - 使用 Google Gemini LLM（大型语言模型）和 Langchain 框架，构建知识增强型讲解系统。
   - 结合向量数据库（Qdrant），实现高效的信息检索和语义理解，为每件文物生成详细的历史背景、制作工艺和文化意义的讲解。

3. **专业语音导览**：
   - 集成语音合成技术，提供专业的语音导览服务，让用户在浏览文物时获得更生动的讲解体验。

4. **多源数据融合**：
   - 通过爬虫技术，从百度百科等多个数据源获取文物信息，并进行数据清洗和处理，确保信息的准确性和完整性。

5. **虚实融合的交互设计**：
   - 采用 WebGL 和 Three.js 等前端技术，实现 3D 模型的实时渲染和交互。
   - 用户可以通过单击鼠标操作，与 3D 模型进行互动，获得沉浸式的体验。

6. **自动化部署和资源管理**：
   - 使用 GitHub Actions 实现自动化部署和资源管理，将生成的资源自动部署到指定的服务器，确保用户可以随时访问最新的内容。


## 运行方法

  1. **安装所需代码库：**

     ```bash
     conda create -n meta python==3.9
     pip install -r requirements.txt 
     ```

  2. **获取 Google Gemini API 密钥：**

     您需要注册一个 Google 账户，启用 Gemini API 并获取 API 密钥。有关详细信息，请参阅官方 Google AI 文档：[Google aistudio api docs](https://aistudio.google.com/apikey)

     将您的 API 密钥保存到`secrets.GITHUB_TOKEN`中

## GitHub Actions

- **process_fig_files** 自动处理 `Fig` 文件夹中新增的图片，触发自动生成相应3d模型等操作。
- **assets_build** 自动提取 `main` 分支的资源到 `assets` 分支中。
  1. assets_build 会调用 `.github/script/extract_assets.py` 来提取 `main` 资源到 `build` 文件夹中
  2. `build` 文件夹会自动写入 `assets` 分支
  3. `assets` 分支中的文件会自动部署到 `assets.metapalace.xj63.fun` 中
- **user-upload-auto.yml** 自动创建用户上传 PR 的工作流文件
- **user-upload-pr.yml** 创建用户上传 PR 的工作流文件


## 文件结构
```
MetaPalace/
├── .github/
│   ├── workflows/
│   │   └── process_fig_files.yml  # GitHub Actions 工作流程文件
│   │   └── assets_build.yml       # 自动提取资源的工作流文件
│   │   └── user-upload-auto.yml   # 自动创建用户上传 PR 的工作流文件
│   │   └── user-upload-pr.yml     # 创建用户上传 PR 的工作流文件
│   └── script/
│       ├── process_fig_files.py       # Python 脚本，用于处理图片并生成 3D 模型和视频
│       ├── process_fig_files.requirements.txt # Python 依赖文件
│       └── extract_assets.py          # 提取资源的脚本
├── Fig/                           # 存放原始 PNG 图片
├── GLB/                           # 存放生成的 GLB 文件
├── Video/                         # 存放生成的视频文件的目录
├── RAG/
│   ├── archive/
│   │   └── archived_assets.txt   # 记录爬取失败的文物名称
│   ├── audio/
│   │   └── hello.wav             # 测试音频文件
│   ├── data/                     # 存放文物描述信息的文本文件
│   ├── db/
│   ├── models/
│   │   ├── bge-small-zh-v1.5/    # 配置文件
│   │   ├── bge_embedding.py      # BGE 嵌入模型，用于生成文本向量
│   │   ├── data_handler.py       # 数据处理脚本，用于加载、清洗和分割文本数据
│   │   ├── gemini_llm.py         # Gemini LLM 封装，用于调用 Google Gemini 模型
│   │   ├── qdrant_db_manager.py  # Qdrant 数据库管理脚本，用于创建、连接和操作 Qdrant 数据库
│   │   ├── session_restore.py
│   │   └── speech_to_text.py 
│   ├── modules/
│   │   └── conversation_gemini.py # 实现用户与AI交互会话
│   ├── output/
│   ├── scripts/
│   │   ├── baike_spider.py       # 爬虫脚本，用于从百度百科爬取文物信息
│   │   ├── file_handler.py       # 文件处理脚本，用于读写文物信息
│   │   ├── get_proxy.py          # 获取代理 IP
│   │   ├── initialize_db.py
│   │   ├── langchain_vector_store.py
│   │   └── glob_assets_name.py   # 用于生成文物名称列表
│   ├── api.py                    # API 接口文件
│   ├── langchain_gemini.py       # RAG 链的主文件，使用 Langchain 和 Gemini LLM
│   ├── requirements.txt          # RAG 目录的依赖文件
│   └── test/                     # 测试文件夹
├── meta.py                        # 主应用程序文件
├── readme.md                      # 中文版 README 文件
└── readme_en.md                   # 英文版 README 文件
└── requirements.txt               # 项目依赖文件
```

## 注意事项

1. **API 密钥安全**：

   请确保您的 Google Gemini API 密钥保存在`secrets.GITHUB_TOKEN`中，并且不要将该文件提交到版本控制系统中避免泄露。




