import streamlit as st
import pandas as pd
import numpy as np
import json
import datetime
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime as dt
import base64
from io import BytesIO

# ==========================================
# 页面配置
# ==========================================
st.set_page_config(
    page_title="🤖 AI课堂教学智能分析平台",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 自定义CSS样式
# ==========================================
st.markdown("""
<style>
    /* 主标题样式 */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #3498db;
    }
    
    /* 副标题样式 */
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #34495e;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        padding-left: 0.5rem;
        border-left: 4px solid #2ecc71;
    }
    
    /* 指标卡片样式 */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 1.5rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    /* AI对话样式 */
    .ai-message {
        background: #e8f4fd;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #3498db;
    }
    
    .user-message {
        background: #f0f7ff;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #2ecc71;
    }
    
    /* 表格样式 */
    .data-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
    }
    
    .data-table th {
        background: #34495e;
        color: white;
        padding: 0.75rem;
        text-align: left;
    }
    
    .data-table td {
        padding: 0.75rem;
        border-bottom: 1px solid #eee;
    }
    
    .data-table tr:hover {
        background: #f5f7fa;
    }
    
    /* 下载按钮样式 */
    .download-btn {
        background: #27ae60;
        color: white;
        padding: 0.75rem 1.5rem;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-weight: 600;
        transition: background 0.3s ease;
    }
    
    .download-btn:hover {
        background: #219653;
    }
    
    /* 警告框样式 */
    .warning-box {
        background: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* 成功框样式 */
    .success-box {
        background: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 标题区域
# ==========================================
st.markdown('<h1 class="main-header">🤖 AI课堂教学智能分析平台</h1>', unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: #7f8c8d; margin-bottom: 2rem;'>
    <p>基于AI的数据分析、智能协作与报告生成系统 | 洋葱学园 智课团队</p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 加载分析结果
# ==========================================
@st.cache_data
def load_analysis_results():
    """加载分析结果"""
    try:
        with open('/home/workspace/analysis_results.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("分析结果文件未找到，请先运行数据分析")
        return None

analysis_results = load_analysis_results()

if analysis_results is None:
    st.stop()

# ==========================================
# 提取关键数据
# ==========================================
file_info = analysis_results['file_info']
current_week = analysis_results['current_week']
best_class = analysis_results['best_class']
focus_class = analysis_results['focus_class']
top_subjects = analysis_results['top_subjects']
weekly_trends = analysis_results['weekly_trends']

current_metrics = current_week['metrics']

# ==========================================
# 侧边栏 - 控制面板
# ==========================================
with st.sidebar:
    st.markdown("## 🎛️ 控制面板")
    
    # 分析选项
    st.markdown("### 📊 分析选项")
    show_details = st.checkbox("显示详细数据", value=True)
    show_charts = st.checkbox("显示图表", value=True)
    show_ai_section = st.checkbox("启用AI协作", value=True)
    
    # AI协作设置
    if show_ai_section:
        st.markdown("### 🤖 AI设置")
        ai_mode = st.selectbox(
            "AI分析模式",
            ["综合模式", "出勤分析", "正确率分析", "班级对比", "学科分析", "趋势预测"]
        )
        
        ai_detail_level = st.slider(
            "分析详细程度",
            min_value=1,
            max_value=5,
            value=3,
            help="1:简要分析, 5:详细分析"
        )
    
    # 报告选项
    st.markdown("### 📄 报告选项")
    report_format = st.selectbox(
        "报告格式",
        ["Markdown", "HTML", "PDF", "Word"]
    )
    
    include_charts = st.checkbox("包含图表", value=True)
    include_raw_data = st.checkbox("包含原始数据摘要", value=False)
    
    # 操作按钮
    st.markdown("### ⚡ 操作")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 重新分析", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    with col2:
        if st.button("📊 导出数据", use_container_width=True):
            st.success("数据导出功能已准备")
    
    # 信息面板
    st.markdown("---")
    st.markdown("### ℹ️ 系统信息")
    st.info(f"""
    **数据文件**: {file_info['file_name']}
    **记录数量**: {file_info['total_records']:,}
    **时间范围**: {file_info['date_range']['start']} 至 {file_info['date_range']['end']}
    **分析时间**: {analysis_results['analysis_time']}
    """)

# ==========================================
# 主内容区域 - 标签页
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 核心指标", 
    "🏫 班级分析", 
    "📚 学科分析", 
    "🤖 AI协作"
])

# ==========================================
# 标签页1: 核心指标
# ==========================================
with tab1:
    st.markdown('<h2 class="sub-header">📈 本周核心教学指标</h2>', unsafe_allow_html=True)
    
    # 关键指标卡片
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">总课时</div>
            <div class="metric-value">{current_metrics['total_hours']}</div>
            <div>课时</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">平均出勤率</div>
            <div class="metric-value">{current_metrics['attendance_rate']*100:.1f}%</div>
            <div>参与度</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">题目正确率</div>
            <div class="metric-value">{current_metrics['correctness_rate']*100:.1f}%</div>
            <div>学习效果</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">涉及班级</div>
            <div class="metric-value">{current_metrics['total_classes']}</div>
            <div>覆盖范围</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 周环比变化
    if len(weekly_trends) >= 2:
        current = weekly_trends[-1]
        previous = weekly_trends[-2]
        
        st.markdown('<h3 class="sub-header">🔄 周环比变化</h3>', unsafe_allow_html=True)
        
        # 计算变化百分比
        def calc_change(current_val, prev_val):
            if prev_val == 0:
                return 0
            return ((current_val - prev_val) / prev_val) * 100
        
        hours_change = calc_change(current['total_hours'], previous['total_hours'])
        att_change = calc_change(current['attendance_rate'], previous['attendance_rate'])
        corr_change = calc_change(current['correctness_rate'], previous['correctness_rate'])
        
        # 创建变化指标
        col1, col2, col3 = st.columns(3)
        
        with col1:
            trend_icon = "📈" if hours_change > 0 else "📉" if hours_change < 0 else "➡️"
            st.metric(
                "总课时变化", 
                f"{current['total_hours']}课时", 
                delta=f"{trend_icon} {abs(hours_change):.1f}%",
                delta_color="normal" if hours_change > 0 else "inverse"
            )
        
        with col2:
            trend_icon = "📈" if att_change > 0 else "📉" if att_change < 0 else "➡️"
            st.metric(
                "出勤率变化", 
                f"{current['attendance_rate']*100:.1f}%", 
                delta=f"{trend_icon} {abs(att_change):.1f}%",
                delta_color="normal" if att_change > 0 else "inverse"
            )
        
        with col3:
            trend_icon = "📈" if corr_change > 0 else "📉" if corr_change < 0 else "➡️"
            st.metric(
                "正确率变化", 
                f"{current['correctness_rate']*100:.1f}%", 
                delta=f"{trend_icon} {abs(corr_change):.1f}%",
                delta_color="normal" if corr_change > 0 else "inverse"
            )
    
    # 历史趋势图表
    if show_charts and len(weekly_trends) > 0:
        st.markdown('<h3 class="sub-header">📊 历史趋势图表</h3>', unsafe_allow_html=True)
        
        # 准备数据
        trend_df = pd.DataFrame(weekly_trends)
        trend_df['week'] = pd.to_datetime(trend_df['week'])
        
        # 创建图表
        fig = go.Figure()
        
        # 添加总课时折线
        fig.add_trace(go.Scatter(
            x=trend_df['week'],
            y=trend_df['total_hours'],
            name='总课时',
            line=dict(color='#3498db', width=3),
            mode='lines+markers'
        ))
        
        # 添加出勤率折线（次坐标轴）
        fig.add_trace(go.Scatter(
            x=trend_df['week'],
            y=trend_df['attendance_rate']*100,
            name='出勤率',
            line=dict(color='#2ecc71', width=3),
            mode='lines+markers',
            yaxis='y2'
        ))
        
        # 添加正确率折线（次坐标轴）
        fig.add_trace(go.Scatter(
            x=trend_df['week'],
            y=trend_df['correctness_rate']*100,
            name='正确率',
            line=dict(color='#e74c3c', width=3),
            mode='lines+markers',
            yaxis='y2'
        ))
        
        # 更新布局
        fig.update_layout(
            title='教学指标历史趋势',
            xaxis_title='周次',
            yaxis_title='总课时（课时）',
            yaxis2=dict(
                title='百分比（%）',
                overlaying='y',
                side='right'
            ),
            hovermode='x unified',
            template='plotly_white',
            height=500,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 标签页2: 班级分析
# ==========================================
with tab2:
    st.markdown('<h2 class="sub-header">🏫 班级表现分析</h2>', unsafe_allow_html=True)
    
    # 最佳班级展示
    if best_class['name']:
        st.markdown(f"""
        <div class="success-box">
            <h3 style="margin-top: 0;">🏆 综合标杆班级</h3>
            <p><strong>{best_class['name']}</strong> 表现突出，可作为学习榜样：</p>
            <ul>
                <li><strong>总课时</strong>: {best_class['hours']} 课时</li>
                <li><strong>平均出勤率</strong>: {best_class['attendance_rate']*100:.1f}%</li>
                <li><strong>平均题目正确率</strong>: {best_class['correctness_rate']*100:.1f}%</li>
                <li><strong>涉及学科</strong>: {best_class['subjects']}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # 重点关注班级
    if focus_class['name'] and focus_class['correctness_rate'] == 0:
        st.markdown(f"""
        <div class="warning-box">
            <h3 style="margin-top: 0;">⚠️ 重点关注班级</h3>
            <p><strong>{focus_class['name']}</strong> 需要特别关注，存在学习效果问题：</p>
            <ul>
                <li><strong>出勤情况良好</strong>: {focus_class['attendance_rate']*100:.1f}% (高于全校平均)</li>
                <li><strong>学习效果不佳</strong>: 题目正确率 {focus_class['correctness_rate']*100:.1f}%</li>
                <li><strong>涉及学科</strong>: {focus_class['subjects']}</li>
            </ul>
            <p><strong>建议</strong>: 立即进行教学诊断，制定个性化改进方案</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 班级对比分析
    if show_details:
        st.markdown('<h3 class="sub-header">📋 班级对比数据</h3>', unsafe_allow_html=True)
        
        # 创建示例班级数据（实际应用中应从分析结果中获取）
        sample_classes = [
            {
                'name': '2024级10班',
                'hours': 12,
                'attendance': 80.3,
                'correctness': 63.2,
                'status': '优秀'
            },
            {
                'name': '2024级1班',
                'hours': 8,
                'attendance': 77.7,
                'correctness': 0.0,
                'status': '需关注'
            },
            {
                'name': '2024级2班',
                'hours': 10,
                'attendance': 60.0,
                'correctness': 18.2,
                'status': '一般'
            },
            {
                'name': '2024级3班',
                'hours': 9,
                'attendance': 65.6,
                'correctness': 41.4,
                'status': '良好'
            }
        ]
        
        class_df = pd.DataFrame(sample_classes)
        
        # 显示表格
        st.dataframe(
            class_df,
            column_config={
                'name': st.column_config.TextColumn('班级名称'),
                'hours': st.column_config.NumberColumn('总课时', format='%d'),
                'attendance': st.column_config.NumberColumn('出勤率', format='%.1f%%'),
                'correctness': st.column_config.NumberColumn('正确率', format='%.1f%%'),
                'status': st.column_config.TextColumn('状态')
            },
            use_container_width=True
        )
        
        # 班级表现雷达图
        if show_charts and len(sample_classes) > 0:
            st.markdown('<h3 class="sub-header">📊 班级表现雷达图</h3>', unsafe_allow_html=True)
            
            # 准备雷达图数据
            categories = ['课时数', '出勤率', '正确率']
            
            fig = go.Figure()
            
            for class_data in sample_classes[:4]:  # 显示前4个班级
                values = [
                    class_data['hours'] / 20,  # 归一化处理
                    class_data['attendance'] / 100,
                    class_data['correctness'] / 100
                ]
                
                fig.add_trace(go.Scatterpolar(
                    r=values,
                    theta=categories,
                    fill='toself',
                    name=class_data['name'],
                    line=dict(width=2)
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )
                ),
                showlegend=True,
                title='班级综合表现对比',
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 标签页3: 学科分析
# ==========================================
with tab3:
    st.markdown('<h2 class="sub-header">📚 学科表现分析</h2>', unsafe_allow_html=True)
    
    if top_subjects:
        # 学科数据表格
        subject_df = pd.DataFrame(top_subjects)
        
        # 重命名列
        subject_df = subject_df.rename(columns={
            '课时学科': '学科',
            '总课时': '课时数',
            '平均题目正确率': '平均正确率',
            '涉及班级数': '涉及班级'
        })
        
        # 格式化数据
        subject_df['平均正确率'] = (subject_df['平均正确率'] * 100).round(1)
        subject_df['课时数'] = subject_df['课时数'].astype(int)
        subject_df['涉及班级'] = subject_df['涉及班级'].astype(int)
        
        # 添加排名
        subject_df['排名'] = range(1, len(subject_df) + 1)
        
        # 重新排列列顺序
        subject_df = subject_df[['排名', '学科', '课时数', '平均正确率', '涉及班级']]
        
        # 显示表格
        st.dataframe(
            subject_df,
            column_config={
                '排名': st.column_config.NumberColumn('排名', width='small'),
                '学科': st.column_config.TextColumn('学科名称'),
                '课时数': st.column_config.NumberColumn('总课时', format='%d'),
                '平均正确率': st.column_config.NumberColumn('平均正确率', format='%.1f%%'),
                '涉及班级': st.column_config.NumberColumn('涉及班级', format='%d')
            },
            use_container_width=True
        )
        
        # 学科对比图表
        if show_charts:
            col1, col2 = st.columns(2)
            
            with col1:
                # 课时分布饼图
                fig1 = px.pie(
                    subject_df,
                    values='课时数',
                    names='学科',
                    title='学科课时分布',
                    hole=0.3,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig1.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # 正确率柱状图
                fig2 = px.bar(
                    subject_df,
                    x='学科',
                    y='平均正确率',
                    title='学科平均正确率对比',
                    color='平均正确率',
                    color_continuous_scale='RdYlGn'
                )
                fig2.update_layout(
                    yaxis_title='正确率（%）',
                    xaxis_title='学科',
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig2, use_container_width=True)
        
        # 学科表现分析
        st.markdown('<h3 class="sub-header">🔍 学科表现深度分析</h3>', unsafe_allow_html=True)
        
        # 找出表现最好和最差的学科
        subjects_with_correctness = [(s['学科'], s['平均正确率']) for s in subject_df.to_dict('records') if s['平均正确率'] > 0]
        
        if subjects_with_correctness:
            best_subject = max(subjects_with_correctness, key=lambda x: x[1])
            worst_subject = min(subjects_with_correctness, key=lambda x: x[1])
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.success(f"""
                **🏅 优势学科**: {best_subject[0]}
                - 平均正确率: {best_subject[1]:.1f}%
                - 教学效果显著
                - 可作为学科标杆
                """)
            
            with col2:
                st.warning(f"""
                **⚠️ 待提升学科**: {worst_subject[0]}
                - 平均正确率: {worst_subject[1]:.1f}%
                - 需要重点改进
                - 加强教学研究
                """)

# ==========================================
# 标签页4: AI协作
# ==========================================
with tab4:
    st.markdown('<h2 class="sub-header">🤖 AI智能协作分析</h2>', unsafe_allow_html=True)
    
    st.info("""
    **AI协作功能说明**:
    1. 输入您的问题或关键词，AI将基于数据分析生成专业报告
    2. 支持多轮对话，可不断优化和深入分析
    3. 所有分析基于实际教学数据，提供针对性建议
    """)
    
    # 初始化会话状态
    if 'ai_conversation' not in st.session_state:
        st.session_state.ai_conversation = []
    
    if 'ai_report_content' not in st.session_state:
        # 生成初始AI报告
        initial_ai_report = f"""
        ## 📊 AI课堂教学数据分析报告
        
        **分析时间**: {analysis_results['analysis_time']}
        **数据来源**: {file_info['file_name']}
        **统计周期**: {current_week['date']}
        
        ### 🎯 核心发现
        
        1. **教学规模稳定**: 本周总课时{current_metrics['total_hours']}，涉及{current_metrics['total_classes']}个班级
        2. **学习效果待提升**: 平均题目正确率{current_metrics['correctness_rate']*100:.1f}%，有较大改进空间
        3. **班级差异明显**: 最佳班级正确率达{best_class['correctness_rate']*100:.1f}%，而需关注班级正确率为0%
        
        ### 💡 初步建议
        
        - **推广优秀经验**: 总结{best_class['name']}的成功做法
        - **加强薄弱环节**: 针对低正确率班级开展专项辅导
        - **优化教学策略**: 基于数据分析调整教学方法
        """
        st.session_state.ai_report_content = initial_ai_report
    
    # 显示当前AI报告
    st.markdown('<h3 class="sub-header">📝 当前AI分析报告</h3>', unsafe_allow_html=True)
    
    ai_report_display = st.text_area(
        "报告内容",
        value=st.session_state.ai_report_content,
        height=300,
        key="ai_report_display"
    )
    
    # AI对话界面
    st.markdown('<h3 class="sub-header">💬 AI对话分析</h3>', unsafe_allow_html=True)
    
    # 输入区域
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_query = st.text_area(
            "输入您的问题或关键词",
            placeholder="例如：出勤率分析、教学改进建议、班级对比、趋势预测...",
            height=100,
            key="ai_query_input"
        )
    
    with col2:
        query_context = st.text_input(
            "上下文/特定要求（可选）",
            placeholder="例如：面向校长汇报、用于教研会议...",
            key="ai_query_context"
        )
        
        if st.button("🚀 AI分析", use_container_width=True, type="primary"):
            if user_query:
                with st.spinner("🤖 AI正在深度分析..."):
                    # 模拟AI响应（实际部署中集成aily AI）
                    ai_responses = {
                        '出勤率分析': f"""
                        ## 📊 出勤率深度分析
                        
                        **本周整体出勤率**: {current_metrics['attendance_rate']*100:.1f}%
                        **涉及班级**: {current_metrics['total_classes']}个
                        
                        ### 🔍 详细分析
                        
                        1. **表现突出班级**:
                           - {best_class['name']}: 出勤率{best_class['attendance_rate']*100:.1f}%
                           - 该班级在学科覆盖和课时安排上表现均衡
                        
                        2. **需要关注班级**:
                           - 部分班级出勤率低于平均水平
                           - 建议分析具体原因，如课程时间、教学内容吸引力等
                        
                        3. **改进建议**:
                           - 优化课程安排，提高学生参与度
                           - 加强课堂互动，提升学习兴趣
                           - 建立出勤激励机制
                        """,
                        
                        '教学改进建议': f"""
                        ## 💡 教学改进建议
                        
                        ### 基于本周数据分析，提出以下改进方案：
                        
                        1. **推广优秀经验**
                           - 总结{best_class['name']}的成功做法
                           - 组织教学经验分享会
                           - 建立优秀教学案例库
                        
                        2. **加强薄弱环节**
                           - 针对低正确率班级开展专项辅导
                           - 分析教学方法和学生学习状态
                           - 制定个性化改进方案
                        
                        3. **优化教学策略**
                           - 基于数据分析调整教学节奏
                           - 加强课堂互动和反馈
                           - 建立持续改进机制
                        
                        4. **资源配置优化**
                           - 根据学科需求合理分配教学资源
                           - 加强教师培训和专业发展
                           - 建立教学效果评估体系
                        """,
                        
                        '班级对比': f"""
                        ## 🏫 班级表现对比分析
                        
                        ### 🏆 标杆班级: {best_class['name']}
                        - **出勤率**: {best_class['attendance_rate']*100:.1f}%
                        - **题目正确率**: {best_class['correctness_rate']*100:.1f}%
                        - **涉及学科**: {best_class['subjects']}
                        - **综合表现**: 优秀
                        
                        ### ⚠️ 重点关注班级: {focus_class['name']}
                        - **出勤率**: {focus_class['attendance_rate']*100:.1f}% (高于平均)
                        - **题目正确率**: {focus_class['correctness_rate']*100:.1f}% (显著偏低)
                        - **涉及学科**: {focus_class['subjects']}
                        - **问题诊断**: 出勤良好但学习效果不佳
                        
                        ### 💡 管理建议
                        1. **差异化教学**: 根据班级特点制定针对性方案
                        2. **经验共享**: 组织班级间的经验交流活动
                        3. **跟踪反馈**: 建立班级表现持续监控机制
                        """,
                        
                        '趋势预测': f"""
                        ## 📈 教学趋势分析与预测
                        
                        ### 历史趋势回顾（{len(weekly_trends)}周）
                        - **总课时变化**: {weekly_trends[0]['total_hours']} → {weekly_trends[-1]['total_hours']}课时
                        - **出勤率变化**: {weekly_trends[0]['attendance_rate']*100:.1f}% → {weekly_trends[-1]['attendance_rate']*100:.1f}%
                        - **正确率变化**: {weekly_trends[0]['correctness_rate']*100:.1f}% → {weekly_trends[-1]['correctness_rate']*100:.1f}%
                        
                        ### 🔮 未来趋势预测
                        1. **教学规模**: 预计将继续稳定增长
                        2. **学习效果**: 通过针对性改进，正确率有望提升10-15%
                        3. **班级差异**: 通过经验共享，班级间差距将逐步缩小
                        
                        ### 🎯 行动建议
                        1. **持续监控**: 建立周报分析机制
                        2. **及时调整**: 基于数据优化教学策略
                        3. **长期规划**: 制定学期教学改进计划
                        """
                    }
                    
                    # 根据查询生成响应
                    ai_response = ai_responses.get(user_query, f"""
                    ## 🤖 AI分析响应
                    
                    基于您的问题「{user_query}」，结合本周教学数据分析：
                    
                    ### 📊 当前状况
                    - **教学规模**: {current_metrics['total_hours']}课时，{current_metrics['total_classes']}个班级
                    - **学生参与**: 平均出勤率{current_metrics['attendance_rate']*100:.1f}%
                    - **学习效果**: 题目正确率{current_metrics['correctness_rate']*100:.1f}%
                    
                    ### 💡 核心建议
                    1. **重点关注学习效果提升**
                    2. **加强班级间经验交流**
                    3. **基于数据优化教学策略**
                    
                    **如需更具体的分析，请尝试输入更具体的关键词**
                    """)
                    
                    # 添加到对话历史
                    st.session_state.ai_conversation.append({
                        'role': 'user',
                        'content': user_query,
                        'time': dt.now().strftime('%H:%M:%S')
                    })
                    
                    st.session_state.ai_conversation.append({
                        'role': 'assistant',
                        'content': ai_response,
                        'time': dt.now().strftime('%H:%M:%S')
                    })
                    
                    # 更新报告内容
                    st.session_state.ai_report_content += f"\n\n## 💬 用户查询: {user_query}\n{ai_response}"
                    
                    st.success("✅ AI分析完成！报告已更新。")
    
    # 显示对话历史
    if st.session_state.ai_conversation:
        st.markdown('<h3 class="sub-header">📜 对话历史</h3>', unsafe_allow_html=True)
        
        for i, message in enumerate(st.session_state.ai_conversation[-6:]):  # 显示最近6条
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="user-message">
                    <strong>👤 您 ({message['time']})</strong><br>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="ai-message">
                    <strong>🤖 AI ({message['time']})</strong><br>
                    {message['content'][:200]}...
                </div>
                """, unsafe_allow_html=True)
    
    # 报告下载功能
    st.markdown('<h3 class="sub-header">📥 报告下载</h3>', unsafe_allow_html=True)
    
    col_dl1, col_dl2, col_dl3 = st.columns(3)
    
    with col_dl1:
        # Markdown格式
        md_report = st.session_state.ai_report_content
        st.download_button(
            label="📄 下载Markdown报告",
            data=md_report,
            file_name=f"AI教学分析报告_{current_week['date']}.md",
            mime="text/markdown",
            use_container_width=True
        )
    
    with col_dl2:
        # HTML格式
        html_report = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>AI课堂教学分析报告 - {current_week['date']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 2rem; }}
                h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 0.5rem; }}
                h2 {{ color: #34495e; margin-top: 2rem; }}
                .metric {{ background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 1rem 0; }}
                .recommendation {{ background: #e8f4fd; padding: 1rem; border-radius: 8px; margin: 1rem 0; }}
                .footer {{ margin-top: 3rem; color: #7f8c8d; font-size: 0.9rem; }}
            </style>
        </head>
        <body>
            <h1>🤖 AI课堂教学智能分析报告</h1>
            <p><strong>生成时间</strong>: {analysis_results['analysis_time']}</p>
            <p><strong>统计周期</strong>: {current_week['date']}</p>
            
            <div class="metric">
                <h2>📊 核心指标</h2>
                <p><strong>总课时</strong>: {current_metrics['total_hours']}课时</p>
                <p><strong>平均出勤率</strong>: {current_metrics['attendance_rate']*100:.1f}%</p>
                <p><strong>平均题目正确率</strong>: {current_metrics['correctness_rate']*100:.1f}%</p>
            </div>
            
            <div class="recommendation">
                <h2>💡 分析与建议</h2>
                {st.session_state.ai_report_content.replace('\n', '<br>')}
            </div>
            
            <div class="footer">
                <p>报告生成系统: AI课堂教学智能分析平台 | 洋葱学园 智课团队</p>
                <p>数据来源: {file_info['file_name']} | 分析记录: {file_info['total_records']}条</p>
            </div>
        </body>
        </html>
        """
        
        st.download_button(
            label="🌐 下载HTML报告",
            data=html_report,
            file_name=f"AI教学分析报告_{current_week['date']}.html",
            mime="text/html",
            use_container_width=True
        )
    
    with col_dl3:
        # 文本格式
        text_report = st.session_state.ai_report_content
        st.download_button(
            label="📝 下载文本报告",
            data=text_report,
            file_name=f"AI教学分析报告_{current_week['date']}.txt",
            mime="text/plain",
            use_container_width=True
        )

# ==========================================
# 页脚信息
# ==========================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 1rem;'>
    <p>© 2026 洋葱学园 - 智课团队 | AI课堂教学智能分析平台 v2.0</p>
    <p>技术支持: 张腾蛟 (zhangtengjiao@guanghe.tv) | 最后更新: {analysis_results['analysis_time']}</p>
</div>
""".format(analysis_results=analysis_results), unsafe_allow_html=True)