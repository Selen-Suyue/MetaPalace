# MetaPalace
[Chinese version](readme.md)

This innovative project breathes digital life into the cultural treasures of the Palace Museum. Our immersive platform invites you to engage with history through cutting-edge interactions: Tap ultra-high-definition cultural relic imagery to activate dynamically generated 3D models, where every artifact unfolds its story through AI-powered 360-degree visual narratives. Enhanced by RAG-optimized knowledge systems and professional audio guides, the experience functions as your personal digital curator, decoding cultural symbols and revealing historical contexts with cinematic clarity. By merging tangible heritage with virtual exploration, we transcend temporal boundaries, democratizing cultural heritage appreciation through reimagined digital encounters.✨

The project was completed by [Yue Su](https://selen-suyue.github.io),[xj63](https://github.com/xj63),[Kai Li](https://github.com/wink-snow),[Zefeng Wu](https://github.com/windansnowman),[Ruihan Wu](https://github.com/cool-chicken),...

Welcome to visit our [website]

## Project Details


 **`meta.py`:** 

## How to Run

1. **Install required libraries:**

    ```bash
    conda create -n meta python==3.9
    pip install -r requirements.txt 
    ```

2. **Obtain the Google Gemini API key:**

    You need to register a Google account, enable the Gemini API, and obtain an API key. Refer to the official Google AI documentation for details: [Google aistudio api docs](https://aistudio.google.com/apikey)


    Copy your API key into the `api_key.txt` file's first line. **Do not commit the `api_key.txt` file to version control!**

4. **Run the application:**

    ```bash
    python meta.py
    ```



## Example



## Notes



## File Structure
```
MetaPalace/
├── .github/
│   └── workflows/
│       └── process_fig_files.yml  # GitHub Actions workflow file
├── Fig/                           # Directory for storing original PNG images
├── GLB/                           # Directory for storing generated GLB files
├── RAG/
│   ├── archive/
│   │   └── archived_assets.txt   # Records names of artifacts for which scraping failed
│   ├── data/                     # Text files storing artifact description information
│   ├── db/
│   │   └── qdrant/
│   │       ├── collection        # Qdrant database file (vector data)
│   │       └── meta.json         # Qdrant database metadata, including collection information
│   ├── langchain_gemini.py       # Main file for the RAG chain, using Langchain and Gemini LLM
│   ├── models/
│   │   ├── bge_embedding.py      # BGE embedding model, used to generate text vectors
│   │   ├── data_handler.py       # Data processing script, used to load, clean, and split text data
│   │   ├── gemini_llm.py         # Gemini LLM wrapper, used to call the Google Gemini model
│   │   └── qdrant_db_manager.py  # Qdrant database management script, used to create, connect to, and operate the Qdrant database
│   ├── RAG.requirements.txt      # Dependency file for the RAG directory
│   └── scripts/
│       ├── baike_spider.py       # Crawler script, used to scrape artifact information from Baidu Baike
│       ├── file_handler.py       # File processing script, used to read and write artifact information
│       ├── get_proxy.py          # Get proxy IP
│       ├── handle_qdrant_db.py   # Qdrant database processing script, used to initialize and get the vector database
│       └── glob_assets_name.py    # Used to generate a list of artifact names
├── Video/                         # Directory for storing generated video files
├── script/
│   ├── process_fig_files.py       # Python script, used to process images and generate 3D models and videos
│   └── process_fig_files.requirements.txt # Python dependency file
├── api_key.txt                    # File for storing the Google Gemini API key (*requires user configuration*)
├── meta.py                        # Main application file
├── readme.md                      # Chinese README file
└── readme_en.md                   # English README file
└── requirements.txt               # Project dependency file
```