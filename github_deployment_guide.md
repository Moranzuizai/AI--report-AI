# 🚀 GitHub部署与使用指南

## 📁 项目结构（GitHub仓库）

```
ai-teaching-analysis-system/
├── README.md                    # 项目说明文档
├── requirements.txt             # Python依赖包
├── .gitignore                   # Git忽略文件
├── app/                         # 应用主目录
│   ├── __init__.py
│   ├── main.py                  # 主应用文件 (final_ai_analysis_app.py)
│   ├── data_analyzer.py         # 数据分析模块 (simple_analysis.py)
│   ├── ai_generator.py          # AI生成模块 (ai_report_generator.py)
│   ├── utils.py                 # 工具函数
│   └── templates/               # HTML模板
│       └── report_template.html
├── data/                        # 数据目录
│   ├── sample_data.xlsx         # 示例数据文件
│   └── analysis_results.json    # 分析结果缓存
├── docs/                        # 文档目录
│   ├── user_guide.md            # 用户指南
│   ├── api_documentation.md     # API文档
│   └── deployment_guide.md      # 部署指南
├── tests/                       # 测试目录
│   ├── test_data_analyzer.py
│   └── test_ai_generator.py
└── scripts/                     # 脚本目录
    ├── setup.sh                 # 安装脚本
    └── deploy.sh                # 部署脚本
```

## 🔧 GitHub部署步骤

### 步骤1：创建GitHub仓库

```bash
# 1. 在GitHub创建新仓库
# 仓库名: ai-teaching-analysis-system
# 描述: AI课堂教学智能分析系统
# 选择: Public仓库，添加README，.gitignore选择Python

# 2. 本地初始化
git init
git add .
git commit -m "初始提交: AI教学分析系统"
git branch -M main
git remote add origin https://github.com/你的用户名/ai-teaching-analysis-system.git
git push -u origin main
```

### 步骤2：配置项目文件

#### `requirements.txt`
```txt
streamlit==1.28.0
pandas==2.1.3
plotly==5.17.0
numpy==1.24.3
openpyxl==3.1.2
python-dotenv==1.0.0
```

#### `README.md`
```markdown
# 🤖 AI课堂教学智能分析系统

## 🎯 项目简介
基于AI的数据分析、智能协作与报告生成系统，专为教育机构设计。

## ✨ 核心功能
- 📊 自动化教学数据分析
- 🤖 AI智能协作报告生成
- 📈 交互式数据可视化
- 📄 多格式报告输出

## 🚀 快速开始

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行应用
```bash
streamlit run app/main.py
```

### 访问应用
打开浏览器访问: http://localhost:8501

## 📁 项目结构
（详细项目结构说明）

## 🔧 配置说明
（配置说明）

## 📖 使用指南
（使用指南链接）

## 🤝 贡献指南
（贡献指南）

## 📄 许可证
MIT License
```

#### `.gitignore`
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# Streamlit
.streamlit/

# Data files
*.csv
*.xlsx
*.xls
*.json
*.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

### 步骤3：配置Streamlit Cloud部署（可选）

#### 创建 `streamlit_app.py`
```python
import sys
import os

# 添加app目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from main import main

if __name__ == "__main__":
    main()
```

#### 创建 `.streamlit/config.toml`
```toml
[theme]
primaryColor = "#3498db"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[browser]
gatherUsageStats = false

[server]
maxUploadSize = 200
enableCORS = false
enableXsrfProtection = true
```

## 🌐 在线部署选项

### 选项1：Streamlit Cloud（推荐）
1. 访问 https://share.streamlit.io
2. 使用GitHub账号登录
3. 选择你的仓库
4. 配置部署设置：
   - **Main file path**: `streamlit_app.py`
   - **Python version**: 3.10+
   - **Requirements file**: `requirements.txt`
5. 点击"Deploy"

### 选项2：Hugging Face Spaces
1. 访问 https://huggingface.co/spaces
2. 创建新的Space
3. 选择"Streamlit" SDK
4. 连接GitHub仓库
5. 配置`app.py`和`requirements.txt`

### 选项3：Railway / Render
1. 创建新项目
2. 连接GitHub仓库
3. 配置启动命令：
   ```bash
   pip install -r requirements.txt && streamlit run app/main.py
   ```
4. 设置环境变量

## 🛠️ 本地开发环境

### 开发环境设置
```bash
# 1. 克隆仓库
git clone https://github.com/你的用户名/ai-teaching-analysis-system.git
cd ai-teaching-analysis-system

# 2. 创建虚拟环境
python -m venv venv

# 3. 激活虚拟环境
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. 安装依赖
pip install -r requirements.txt

# 5. 运行开发服务器
streamlit run app/main.py
```

### 开发脚本
创建 `scripts/setup.sh`：
```bash
#!/bin/bash

echo "🚀 设置AI教学分析系统开发环境..."

# 检查Python版本
python --version

# 创建虚拟环境
echo "📦 创建虚拟环境..."
python -m venv venv

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 升级pip
echo "⬆️ 升级pip..."
pip install --upgrade pip

# 安装依赖
echo "📚 安装依赖包..."
pip install -r requirements.txt

# 安装开发依赖
echo "🔧 安装开发工具..."
pip install black flake8 pytest

echo "✅ 环境设置完成！"
echo "运行以下命令启动应用："
echo "source venv/bin/activate && streamlit run app/main.py"
```

## 📦 Docker部署

### 创建 `Dockerfile`
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY app/ ./app/
COPY data/ ./data/
COPY .streamlit/ ./.streamlit/

# 创建非root用户
RUN useradd -m -u 1000 streamlit
USER streamlit

# 暴露端口
EXPOSE 8501

# 健康检查
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# 启动命令
ENTRYPOINT ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 创建 `docker-compose.yml`
```yaml
version: '3.8'

services:
  ai-teaching-analysis:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
      - ./app:/app/app
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
    restart: unless-stopped
```

### Docker部署命令
```bash
# 构建镜像
docker build -t ai-teaching-analysis .

# 运行容器
docker run -p 8501:8501 ai-teaching-analysis

# 使用docker-compose
docker-compose up -d
```

## 🔐 环境变量配置

创建 `.env` 文件：
```env
# 应用配置
APP_NAME=AI教学分析系统
APP_VERSION=2.0.0
DEBUG=False

# 数据配置
DATA_PATH=./data
MAX_FILE_SIZE=104857600  # 100MB

# AI配置（未来扩展）
AI_API_KEY=your_api_key_here
AI_MODEL=gpt-4
AI_TEMPERATURE=0.7

# 安全配置
ADMIN_PASSWORD=your_admin_password
USER_PASSWORD=your_user_password
```

## 📊 数据管理

### 数据文件结构
```
data/
├── uploads/                    # 用户上传文件
│   ├── 2024-01/
│   ├── 2024-02/
│   └── temp/
├── analysis/                   # 分析结果
│   ├── weekly/
│   ├── monthly/
│   └── yearly/
├── reports/                    # 生成报告
│   ├── markdown/
│   ├── html/
│   └── pdf/
└── cache/                      # 缓存文件
    ├── ai_responses/
    └── charts/
```

### 数据备份策略
```python
# scripts/backup.py
import shutil
import datetime
import os

def backup_data():
    """备份数据文件"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backups/{timestamp}"
    
    os.makedirs(backup_dir, exist_ok=True)
    
    # 备份重要数据
    shutil.copytree("data/analysis", f"{backup_dir}/analysis")
    shutil.copytree("data/reports", f"{backup_dir}/reports")
    
    print(f"✅ 数据备份完成: {backup_dir}")
```

## 🔄 持续集成/持续部署

### GitHub Actions配置
创建 `.github/workflows/deploy.yml`：
```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/ -v
    
    - name: Deploy to Streamlit Cloud
      if: github.ref == 'refs/heads/main'
      run: |
        # 这里可以添加自动部署到Streamlit Cloud的逻辑
        echo "部署到Streamlit Cloud..."
```

## 📈 监控与日志

### 日志配置
```python
# app/utils/logger.py
import logging
import sys
from datetime import datetime

def setup_logger():
    """设置日志系统"""
    logger = logging.getLogger("ai_teaching_analysis")
    logger.setLevel(logging.INFO)
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # 文件处理器
    file_handler = logging.FileHandler(
        f"logs/app_{datetime.now().strftime('%Y%m%d')}.log"
    )
    file_handler.setLevel(logging.DEBUG)
    
    # 格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger
```

## 🎯 使用流程示例

### 团队协作流程
```
1. 团队成员上传教学数据
2. 系统自动分析并生成核心指标
3. 使用AI协作功能生成分析报告
4. 下载报告并分享给相关人员
5. 基于报告制定改进措施
6. 持续监控效果并优化
```

### 典型工作场景
```python
# 示例：自动化周报生成
def generate_weekly_report():
    """自动生成周报"""
    # 1. 上传本周数据
    upload_data("本周教学数据.xlsx")
    
    # 2. 运行分析
    analysis_results = analyze_data()
    
    # 3. 使用AI生成报告
    report = ai_generate_report(
        analysis_results,
        query="生成本周教学分析报告，包含亮点和改进建议"
    )
    
    # 4. 保存报告
    save_report(report, format="html")
    
    # 5. 发送通知
    send_notification("周报已生成", report_url)
```

## 🔧 故障排除

### 常见问题

#### 1. 依赖安装失败
```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 2. 端口冲突
```bash
# 指定其他端口
streamlit run app/main.py --server.port=8502
```

#### 3. 文件上传问题
- 检查文件格式（支持.xlsx, .xls, .csv）
- 检查文件编码（CSV建议UTF-8）
- 检查文件大小（默认最大100MB）

#### 4. AI响应慢
- 检查网络连接
- 减少单次查询复杂度
- 使用缓存机制

## 📞 支持与反馈

### 获取帮助
1. 查看项目文档
2. 提交GitHub Issue
3. 查看常见问题解答

### 提交反馈
```bash
# 提交功能请求
git checkout -b feature/your-feature-name
# 开发完成后提交PR
git push origin feature/your-feature-name
```

## 🎉 部署完成检查清单

- [ ] GitHub仓库创建完成
- [ ] 项目文件结构正确
- [ ] 依赖包安装成功
- [ ] 本地运行测试通过
- [ ] 在线部署配置完成
- [ ] 数据备份策略就绪
- [ ] 监控日志系统工作正常
- [ ] 团队使用培训完成

---

**现在您的AI教学分析系统已经准备好部署到GitHub！** 🚀