#!/bin/bash

echo "🚀 AI教学分析系统 - GitHub一键部署脚本"
echo "=========================================="
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 函数：打印带颜色的消息
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 检查必要工具
check_prerequisites() {
    print_info "检查必要工具..."
    
    # 检查git
    if command -v git &> /dev/null; then
        print_success "Git 已安装"
    else
        print_error "Git 未安装，请先安装Git"
        exit 1
    fi
    
    # 检查Python
    if command -v python3 &> /dev/null; then
        python_version=$(python3 --version | cut -d' ' -f2)
        print_success "Python3 已安装 (版本: $python_version)"
    else
        print_error "Python3 未安装，请先安装Python3"
        exit 1
    fi
    
    # 检查pip
    if command -v pip3 &> /dev/null; then
        print_success "pip3 已安装"
    else
        print_warning "pip3 未安装，尝试安装..."
        python3 -m ensurepip --upgrade
    fi
}

# 创建项目结构
create_project_structure() {
    print_info "创建项目结构..."
    
    # 创建目录
    mkdir -p ai-teaching-analysis-system/{app,data,docs,tests,scripts}
    
    # 复制核心文件
    print_info "复制核心文件..."
    
    # 主应用文件
    if [ -f "/home/workspace/final_ai_analysis_app.py" ]; then
        cp "/home/workspace/final_ai_analysis_app.py" "ai-teaching-analysis-system/app/main.py"
        print_success "复制主应用文件"
    else
        print_error "找不到主应用文件"
        exit 1
    fi
    
    # 数据分析模块
    if [ -f "/home/workspace/simple_analysis.py" ]; then
        cp "/home/workspace/simple_analysis.py" "ai-teaching-analysis-system/app/data_analyzer.py"
        print_success "复制数据分析模块"
    else
        print_warning "找不到数据分析模块，创建默认版本"
        cat > "ai-teaching-analysis-system/app/data_analyzer.py" << 'EOF'
import pandas as pd
import numpy as np
from datetime import datetime

def analyze_teaching_data(file_path):
    """分析教学数据"""
    try:
        # 读取Excel文件
        df = pd.read_excel(file_path)
        
        # 基本统计
        file_info = {
            "total_records": len(df),
            "columns_count": len(df.columns),
            "time_range": f"{df['周次'].min()} 至 {df['周次'].max()}",
            "class_count": df['班级'].nunique(),
            "subject_count": df['学科'].nunique()
        }
        
        # 核心指标计算
        if '课时数' in df.columns and '出勤率' in df.columns:
            total_hours = df['课时数'].sum()
            weighted_attendance = (df['出勤率'] * df['课时数']).sum() / total_hours if total_hours > 0 else 0
        else:
            weighted_attendance = df['出勤率'].mean() if '出勤率' in df.columns else 0
        
        overall_metrics = {
            "weighted_attendance_rate": round(weighted_attendance * 100, 1),
            "micro_course_completion_rate": round(df['微课完成率'].mean() * 100, 1) if '微课完成率' in df.columns else 0,
            "question_correct_rate": round(df['题目正确率'].mean() * 100, 1) if '题目正确率' in df.columns else 0
        }
        
        return {
            "file_info": file_info,
            "overall_metrics": overall_metrics,
            "success": True,
            "message": "数据分析完成"
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"数据分析失败: {str(e)}"
        }
EOF
    fi
    
    # AI生成模块
    if [ -f "/home/workspace/ai_report_generator.py" ]; then
        cp "/home/workspace/ai_report_generator.py" "ai-teaching-analysis-system/app/ai_generator.py"
        print_success "复制AI生成模块"
    else
        print_warning "找不到AI生成模块，创建默认版本"
        cat > "ai-teaching-analysis-system/app/ai_generator.py" << 'EOF'
class AIReportGenerator:
    """AI报告生成器"""
    
    def __init__(self):
        self.response_templates = {
            "attendance_analysis": self._attendance_template(),
            "teaching_suggestions": self._suggestions_template(),
            "general_analysis": self._general_template()
        }
    
    def generate_report(self, analysis_data, query_type="general_analysis"):
        """生成报告"""
        template = self.response_templates.get(query_type, self._general_template())
        
        # 填充数据
        report = template.format(
            period=analysis_data.get("file_info", {}).get("time_range", "未知周期"),
            attendance_rate=analysis_data.get("overall_metrics", {}).get("weighted_attendance_rate", 0),
            correct_rate=analysis_data.get("overall_metrics", {}).get("question_correct_rate", 0),
            completion_rate=analysis_data.get("overall_metrics", {}).get("micro_course_completion_rate", 0)
        )
        
        return report
    
    def _attendance_template(self):
        return """📊 出勤率分析报告
{'='*40}

📅 分析周期：{period}
📈 整体出勤率：{attendance_rate}%

🎯 分析要点：
1. 出勤率反映了学生的课堂参与度
2. 建议关注出勤率较低的班级
3. 可通过课堂互动提升学生参与度

💡 改进建议：
• 增加课堂互动环节
• 建立考勤激励机制
• 定期与家长沟通学生出勤情况"""
    
    def _suggestions_template(self):
        return """💡 教学改进建议
{'='*40}

📊 基于数据分析的教学建议：

1️⃣ 针对出勤率（{attendance_rate}%）：
• 开展考勤激励机制
• 优化课堂时间安排

2️⃣ 针对正确率（{correct_rate}%）：
• 加强基础知识教学
• 增加课堂练习环节

3️⃣ 针对完成率（{completion_rate}%）：
• 优化微课内容设计
• 提供个性化学习路径"""
    
    def _general_template(self):
        return """📋 教学数据分析报告
{'='*40}

📅 分析周期：{period}

📊 核心指标：
• 出勤率：{attendance_rate}%
• 题目正确率：{correct_rate}%
• 微课完成率：{completion_rate}%

🎯 总体评估：
基于当前数据分析，教学效果整体{status}。

💡 建议：
1. 持续监控核心指标变化
2. 针对薄弱环节制定改进措施
3. 定期评估教学策略效果"""
EOF
    fi
    
    # 工具函数
    cat > "ai-teaching-analysis-system/app/utils.py" << 'EOF'
import json
import os
from datetime import datetime

def save_analysis_results(results, file_path="data/analysis_results.json"):
    """保存分析结果"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # 添加时间戳
    results["analysis_timestamp"] = datetime.now().isoformat()
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    return file_path

def load_analysis_results(file_path="data/analysis_results.json"):
    """加载分析结果"""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def format_percentage(value):
    """格式化百分比"""
    if isinstance(value, (int, float)):
        return f"{value:.1f}%"
    return value

def get_current_time():
    """获取当前时间"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
EOF
    
    # 示例数据
    print_info "创建示例数据文件..."
    cat > "ai-teaching-analysis-system/data/sample_data.xlsx" << 'EOF'
# 这是一个示例Excel文件的占位符
# 实际使用时，请替换为您的教学数据文件
EOF
    
    # 分析结果缓存
    if [ -f "/home/workspace/analysis_results.json" ]; then
        cp "/home/workspace/analysis_results.json" "ai-teaching-analysis-system/data/analysis_results.json"
        print_success "复制分析结果数据"
    else
        print_info "创建示例分析结果..."
        cat > "ai-teaching-analysis-system/data/analysis_results.json" << 'EOF'
{
  "file_info": {
    "total_records": 804,
    "columns_count": 26,
    "time_range": "2025-09-07 至 2026-01-18",
    "class_count": 19,
    "subject_count": 10
  },
  "overall_metrics": {
    "weighted_attendance_rate": 64.7,
    "micro_course_completion_rate": 39.7,
    "question_correct_rate": 26.1
  },
  "class_analysis": {
    "best_performing_class": {
      "class_name": "2024级10班",
      "attendance_rate": 80.3,
      "correct_rate": 63.2,
      "comprehensive_score": 86.5
    },
    "needs_attention_class": {
      "class_name": "2024级1班",
      "attendance_rate": 77.7,
      "correct_rate": 0.0,
      "comprehensive_score": 38.8
    }
  },
  "analysis_timestamp": "2026-02-09T14:30:00"
}
EOF
    fi
}

# 创建配置文件
create_config_files() {
    print_info "创建配置文件..."
    
    # requirements.txt
    cat > "ai-teaching-analysis-system/requirements.txt" << 'EOF'
streamlit==1.28.0
pandas==2.1.3
plotly==5.17.0
numpy==1.24.3
openpyxl==3.1.2
python-dotenv==1.0.0
EOF
    
    # README.md
    cat > "ai-teaching-analysis-system/README.md" << 'EOF'
# 🤖 AI课堂教学智能分析系统

## 🎯 项目简介
基于AI的数据分析、智能协作与报告生成系统，专为教育机构设计。系统能够自动分析教学数据，生成专业报告，并提供AI协作功能。

## ✨ 核心功能
- 📊 **自动化数据分析**：自动读取Excel/CSV文件，计算核心教学指标
- 🤖 **AI智能协作**：支持自然语言查询，生成专业分析报告
- 📈 **交互式可视化**：使用Plotly生成美观的交互式图表
- 📄 **多格式报告输出**：支持Markdown、HTML、文本格式报告下载
- 🔒 **权限管理系统**：管理员和普通用户双密码验证

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行应用
```bash
streamlit run app/main.py
```

### 3. 访问应用
打开浏览器访问：http://localhost:8501

### 4. 登录系统
- **管理员密码**：admin123
- **普通用户密码**：user123

## 📁 项目结构
```
ai-teaching-analysis-system/
├── app/                         # 应用主目录
│   ├── main.py                  # 主应用文件
│   ├── data_analyzer.py         # 数据分析模块
│   ├── ai_generator.py          # AI报告生成模块
│   └── utils.py                 # 工具函数
├── data/                        # 数据目录
│   ├── sample_data.xlsx         # 示例数据文件
│   └── analysis_results.json    # 分析结果缓存
├── requirements.txt             # Python依赖包
├── README.md                    # 项目说明文档
└── .gitignore                   # Git忽略配置
```

## 🔧 使用指南

### 数据上传
1. 支持Excel (.xlsx/.xls) 和 CSV格式
2. 文件应包含：班级、学科、周次、课时数、出勤率等字段
3. 系统自动识别数据列并进行分析

### AI协作功能
1. 在"🤖 AI智能协作"标签页输入问题
2. 支持的问题类型：
   - 出勤率分析
   - 教学改进建议
   - 班级对比
   - 趋势预测
   - 报告生成
3. 支持多轮对话优化报告内容

### 报告下载
1. AI生成的报告支持三种格式：
   - 📄 Markdown（适合文档编辑）
   - 🌐 HTML（包含完整样式）
   - 📝 文本（简洁易用）
2. 点击相应按钮即可下载

## 🛠️ 开发指南

### 环境设置
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 安装开发依赖
pip install -r requirements.txt
```

### 运行测试
```bash
# 运行所有测试
python -m pytest tests/
```

## 🤝 贡献指南
1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证
本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 支持
如有问题或建议，请提交 [Issue](https://github.com/yourusername/ai-teaching-analysis-system/issues)

---

**开始使用AI教学分析系统，提升教学管理效率！** 🚀
EOF
    
    # .gitignore
    cat > "ai-teaching-analysis-system/.gitignore" << 'EOF'
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

# Logs
*.log

# Virtual environment
venv/
.env
EOF
    
    # 启动脚本
    cat > "ai-teaching-analysis-system/scripts/start.sh" << 'EOF'
#!/bin/bash

echo "🚀 启动AI教学分析系统..."
echo ""

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "⚠️  未找到虚拟环境，正在创建..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# 运行Streamlit应用
echo "🔧 启动Streamlit应用..."
echo "📱 应用地址：http://localhost:8501"
echo "📝 按 Ctrl+C 停止应用"
echo ""

streamlit run app/main.py
EOF
    
    chmod +x "ai-teaching-analysis-system/scripts/start.sh"
    
    # 测试文件
    cat > "ai-teaching-analysis-system/tests/test_basic.py" << 'EOF'
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../app'))

from data_analyzer import analyze_teaching_data

def test_analysis_function():
    """测试数据分析函数"""
    # 这里可以添加实际测试
    print("✅ 测试框架就绪")
    
if __name__ == "__main__":
    test_analysis_function()
EOF
}

# 初始化Git仓库
init_git_repository() {
    print_info "初始化Git仓库..."
    
    cd "ai-teaching-analysis-system"
    
    # 初始化Git
    git init
    
    # 配置Git
    git config user.name "AI Teaching Analysis System"
    git config user.email "system@example.com"
    
    # 添加所有文件
    git add .
    
    # 提交初始版本
    git commit -m "初始提交: AI教学分析系统 v2.0"
    
    print_success "Git仓库初始化完成"
    
    cd ..
}

# 部署到GitHub
deploy_to_github() {
    print_info "部署到GitHub..."
    
    read -p "请输入您的GitHub用户名: " github_username
    
    if [ -z "$github_username" ]; then
        print_warning "未输入用户名，跳过GitHub部署"
        return
    fi
    
    read -p "请输入仓库名称 (默认: ai-teaching-analysis): " repo_name
    repo_name=${repo_name:-ai-teaching-analysis}
    
    print_info "创建GitHub仓库: https://github.com/$github_username/$repo_name"
    
    # 提示用户手动创建仓库
    echo ""
    print_warning "请按照以下步骤操作："
    echo "1. 登录 GitHub (https://github.com)"
    echo "2. 点击右上角 '+' → 'New repository'"
    echo "3. 仓库名称: $repo_name"
    echo "4. 描述: AI课堂教学智能分析系统"
    echo "5. 选择: Public"
    echo "6. 不要勾选 'Initialize this repository with a README'"
    echo "7. 点击 'Create repository'"
    echo ""
    read -p "按回车键继续，当您在GitHub上创建好仓库后..." dummy
    
    # 添加远程仓库
    cd "ai-teaching-analysis-system"
    
    git remote add origin "https://github.com/$github_username/$repo_name.git"
    
    # 推送到GitHub
    print_info "推送到GitHub..."
    git branch -M main
    
    if git push -u origin main; then
        print_success "✅ 成功部署到GitHub！"
        echo ""
        echo "🌐 访问地址：https://github.com/$github_username/$repo_name"
        echo "🚀 在线运行：https://share.streamlit.io/$github_username/$repo_name/main/app/main.py"
    else
        print_error "推送失败，请检查网络连接和GitHub权限"
        print_info "您可以手动推送："
        echo "  cd ai-teaching-analysis-system"
        echo "  git push -u origin main"
    fi
    
    cd ..
}

# 提供使用说明
provide_usage_instructions() {
    echo ""
    print_success "🎉 AI教学分析系统部署完成！"
    echo ""
    echo "📁 项目已创建在：ai-teaching-analysis-system/"
    echo ""
    echo "🚀 快速启动："
    echo "1. 进入项目目录："
    echo "   cd ai-teaching-analysis-system"
    echo ""
    echo "2. 安装依赖："
    echo "   pip install -r requirements.txt"
    echo ""
    echo "3. 运行应用："
    echo "   streamlit run app/main.py"
    echo ""
    echo "4. 访问应用："
    echo "   http://localhost:8501"
    echo ""
    echo "🔑 登录信息："
    echo "   • 管理员密码：admin123"
    echo "   • 普通用户密码：user123"
    echo ""
    echo "🤖 AI功能体验："
    echo "   在'AI智能协作'标签页输入问题，如："
    echo "   • '分析一下各班级的出勤情况'"
    echo "   • '生成教学改进建议'"
    echo "   • '预测下个月的趋势'"
    echo ""
    echo "📊 数据上传："
    echo "   将您的教学数据文件（Excel/CSV）拖到上传区域"
    echo ""
    
    if [ -n "$github_username" ] && [ -n "$repo_name" ]; then
        echo "🌐 GitHub仓库："
        echo "   https://github.com/$github_username/$repo_name"
        echo ""
        echo "💡 在线部署选项："
        echo "   1. Streamlit Cloud: https://share.streamlit.io"
        echo "   2. Hugging Face Spaces: https://huggingface.co/spaces"
        echo "   3. Railway: https://railway.app"
        echo ""
    fi
}

# 主函数
main() {
    echo ""
    print_info "🚀 AI教学分析系统部署流程开始"
    echo "=========================================="
    echo ""
    
    # 步骤1：检查前提条件
    check_prerequisites
    
    # 步骤2：创建项目结构
    create_project_structure
    
    # 步骤3：创建配置文件
    create_config_files
    
    # 步骤4：初始化Git
    init_git_repository
    
    # 步骤5：询问是否部署到GitHub
    echo ""
    read -p "是否要部署到GitHub？(y/n): " deploy_choice
    
    if [[ "$deploy_choice" =~ ^[Yy]$ ]]; then
        deploy_to_github
    else
        print_info "跳过GitHub部署"
    fi
    
    # 步骤6：提供使用说明
    provide_usage_instructions
    
    echo ""
    print_success "✅ 部署流程完成！"
    echo ""
    echo "🎯 现在您可以开始使用AI教学分析系统了！"
    echo ""
}

# 运行主函数
main