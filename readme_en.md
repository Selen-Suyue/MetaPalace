<h2 align="center" style="color: red; font-size: 28px;">🚨 Site Migration Notice 🚨</h2>

<p align="center" style="color: red; font-size: 20px;">
Due to unforeseen circumstances, the original site is temporarily unavailable.<br>
Please visit the new address below (some features may be missing):<br>
<a href="https://metapalacesite.pages.dev" target="_blank"><b>https://metapalacesite.pages.dev</b></a>
</p>


# MetaPalace
[Chinese version](readme.md)

This innovative project breathes digital life into the cultural treasures of the Palace Museum. Our immersive platform invites you to engage with history through cutting-edge interactions: Tap ultra-high-definition cultural relic imagery to activate dynamically generated 3D models, where every artifact unfolds its story through AI-powered 360-degree visual narratives. Enhanced by RAG-optimized knowledge systems and professional audio guides, the experience functions as your personal digital curator, decoding cultural symbols and revealing historical contexts with cinematic clarity. By merging tangible heritage with virtual exploration, we transcend temporal boundaries, democratizing cultural heritage appreciation through reimagined digital encounters.✨

The project was completed by [Yue Su](https://selen-suyue.github.io),[xj63](https://github.com/xj63),[Kai Li](https://github.com/wink-snow),[Zefeng Wu](https://github.com/windansnowman),[Ruihan Wu](https://github.com/cool-chicken),...

Welcome to visit our website [MetaPalaceSite](https://metapalace.xj63.fun/), and here is our [front-end design](https://github.com/xj63/MetaPalaceSite).

## Project Details
1. **High-Precision 3D Model Generation**:
   - Utilize computer vision technology and deep learning algorithms to generate high-precision 3D models from ultra-high-definition images.
   - Through GitHub Actions automated workflows, process user-uploaded images in real-time to generate corresponding 3D models and videos.

2. **AI-Driven Knowledge-Enhanced Explanation System**:
   - Use Google Gemini LLM (Large Language Model) and the Langchain framework to build a knowledge-enhanced explanation system.
   - Integrate a vector database (Qdrant) for efficient information retrieval and semantic understanding, generating detailed historical context, craftsmanship, and cultural significance for each artifact.

3. **Professional Audio Guide**:
   - Integrate speech synthesis technology to provide professional audio guide services, offering users a more vivid explanation experience while browsing artifacts.

4. **Multi-Source Data Fusion**:
   - Use web scraping technology to gather artifact information from multiple sources such as Baidu Baike, followed by data cleaning and processing to ensure accuracy and completeness.

5. **Virtual-Reality Fusion Interaction Design**:
   - Employ front-end technologies like WebGL and Three.js for real-time rendering and interaction with 3D models.
   - Users can interact with 3D models via touchscreens or mouse operations, achieving an immersive experience.

6. **Automated Deployment and Resource Management**:
   - Use GitHub Actions for automated deployment and resource management, automatically deploying generated resources to designated servers to ensure users can access the latest content at any time.

## How to Run

1. **Install required libraries:**

    ```bash
    conda create -n meta python==3.9
    pip install -r requirements.txt 
    ```

2. **Obtain the Google Gemini API key:**

    You need to register a Google account, enable the Gemini API, and obtain an API key. Refer to the official Google AI documentation for details: [Google aistudio api docs](https://aistudio.google.com/apikey)

    Save your API key in `secrets.GITHUB_TOKEN`

## GitHub Actions

- **process_fig_files**: Automatically processes newly added images in the `Fig` folder, triggering the generation of corresponding 3D models and other operations.
- **assets_build**: Automatically extracts resources from the `main` branch to the `assets` branch.
  1. `assets_build` calls `.github/script/extract_assets.py` to extract resources from `main` to the `build` folder.
  2. The `build` folder is automatically written to the `assets` branch.
  3. Files in the `assets` branch are automatically deployed to `assets.metapalace.xj63.fun`.
- **user-upload-auto.yml**: Automatically creates a PR for user uploads.
- **user-upload-pr.yml**: Creates a PR for user uploads.


## File Structure
```
MetaPalace/
├── .github/
│   ├── workflows/
│   │   └── process_fig_files.yml  # GitHub Actions workflow file
│   │   └── assets_build.yml       # Workflow file for automatic resource extraction
│   │   └── user-upload-auto.yml   # Workflow file for automatic user upload PR creation
│   │   └── user-upload-pr.yml     # Workflow file for user upload PR creation
│   └── script/
│       ├── process_fig_files.py       # Python script for processing images and generating 3D models and videos
│       ├── process_fig_files.requirements.txt # Python dependencies file
│       └── extract_assets.py          # Script for extracting resources
├── Fig/                           # Directory for storing original PNG images
├── GLB/                           # Directory for storing generated GLB files
├── Video/                         # Directory for storing generated video files
├── RAG/
│   ├── archive/
│   │   └── archived_assets.txt   # Records names of artifacts that failed to be scraped
│   ├── audio/
│   │   └── hello.wav             # Test audio file
│   ├── data/                     # Directory for storing artifact description text files
│   ├── db/
│   ├── models/
│   │   ├── bge-small-zh-v1.5/    # Configuration files
│   │   ├── bge_embedding.py      # BGE embedding model for generating text vectors
│   │   ├── data_handler.py       # Data processing script for loading, cleaning, and splitting text data
│   │   ├── gemini_llm.py         # Gemini LLM wrapper for calling Google Gemini model
│   │   ├── qdrant_db_manager.py  # Qdrant database management script for creating, connecting, and operating Qdrant database
│   │   ├── session_restore.py
│   │   └── speech_to_text.py 
│   ├── modules/
│   │   └── conversation_gemini.py # Implements user-AI interaction
│   ├── output/
│   ├── scripts/
│   │   ├── baike_spider.py       # Web scraping script for retrieving artifact information from Baidu Baike
│   │   ├── file_handler.py       # File handling script for reading and writing artifact information
│   │   ├── get_proxy.py          # Script for obtaining proxy IPs
│   │   ├── initialize_db.py
│   │   ├── langchain_vector_store.py
│   │   └── glob_assets_name.py   # Script for generating artifact name lists
│   ├── api.py                    # API interface file
│   ├── langchain_gemini.py       # Main file for the RAG chain, using Langchain and Gemini LLM
│   ├── requirements.txt          # Dependencies file for the RAG directory
│   └── test/                     # Test folder
├── meta.py                        # Main application file
├── readme.md                      # Chinese README file
└── readme_en.md                   # English README file
└── requirements.txt               # Project dependencies file
```

## Notes

1. **API Key Security**:

   Ensure that your Google Gemini API key is stored in `secrets.GITHUB_TOKEN`, and avoid committing this file to the version control system to prevent leaks.
