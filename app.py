import streamlit as st
import pandas as pd
import os
import re
import json
import datetime
import streamlit.components.v1 as components
import qianfan  # 百度千帆SDK

# ==========================================
# 0. 全局配置加载 (必须放在最前面)
# ==========================================
CONFIG_FILE = "config.json"
LOG_FILE = "access_log.csv"
FEEDBACK_FILE = "feedback_log.csv"

def load_config():
    """读取配置文件"""
    default_config = {
        "admin_password": "199266", 
        "user_password": "123456",
        "baidu_api_key": "",
        "baidu_secret_key": "",
        "upload_hint": "⬆️ BI平台下载 - 班级数据（分学科）原文件导入即可",
        "app_title": "AI课堂教学数据分析工具"  # [新增] 软件名称
    }
    
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(default_config, f)
        return default_config
    
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
        # 自动补全缺失字段
        for k, v in default_config.items():
            if k not in config:
                config[k] = v
        return config

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

# 加载配置
current_config = load_config()

# 设置页面 (使用配置中的标题)
st.set_page_config(
    page_title=current_config["app_title"], 
    page_icon="📊", 
    layout="wide"
)

# ==========================================
# 1. 核心工具函数
# ==========================================
def get_remote_ip():
    try:
        from streamlit.web.server.websocket_headers import _get_websocket_headers
        headers = _get_websocket_headers()
        return headers.get("X-Forwarded-For", headers.get("Remote-Addr", "Unknown"))
    except:
        return "Unknown"

def log_access(event_type="用户登录"):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_ip = get_remote_ip()
    if not os.path.exists(LOG_FILE):
        df = pd.DataFrame(columns=["访问时间", "IP地址", "事件"])
        df.to_csv(LOG_FILE, index=False)
    new_entry = pd.DataFrame([{"访问时间": now_time, "IP地址": user_ip, "事件": event_type}])
    new_entry.to_csv(LOG_FILE, mode='a', header=False, index=False)

def save_feedback(rating, comment):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not os.path.exists(FEEDBACK_FILE):
        df = pd.DataFrame(columns=["时间", "评价", "建议"])
        df.to_csv(FEEDBACK_FILE, index=False)
    pd.DataFrame([{"时间": now_time, "评价": rating, "建议": comment}]).to_csv(FEEDBACK_FILE, mode='a', header=False, index=False)

# ==========================================
# 2. [修复版] AI 调用接口 (百度文心)
# ==========================================
def call_ai_service(messages):
    """
    百度文心一言调用 - 增强除错版
    """
    cfg = load_config()
    ak = cfg.get("baidu_api_key", "").strip()
    sk = cfg.get("baidu_secret_key", "").strip()
    
    if not ak or not sk:
        return "⚠️ 未配置百度 API Key，请联系管理员在后台设置。"
    
    # [修复] 使用环境变量方式注入，兼容性更好
    os.environ["QIANFAN_AK"] = ak
    os.environ["QIANFAN_SK"] = sk
    
    try:
        # 实例化客户端
        chat_comp = qianfan.ChatCompletion()
        
        # 发起请求
        # 注意：这里使用 'ERNIE-Speed-8K'，这是百度目前最稳定且通常免费的模型
        # 如果报错 "IAM certification failed"，请检查 AK/SK 是否复制正确
        # 如果报错 "No permission"，请去百度云控制台开通 ERNIE-Speed 模型的权限
        resp = chat_comp.do(
            model="ERNIE-Speed-8K", 
            messages=messages
        )
        
        # 检查返回结果
        if "body" in resp and "result" in resp["body"]:
            return resp["body"]["result"]
        else:
            return f"API 返回异常: {str(resp)}"
            
    except Exception as e:
        return f"❌ AI 调用报错: {str(e)}\n(请检查：1.AK/SK是否正确; 2.是否在百度云开通了 ERNIE-Speed-8K 模型)"

# ==========================================
# 3. 权限控制
# ==========================================
ADMIN_PWD = current_config.get("admin_password", "199266")
USER_PWD = current_config.get("user_password", "123456")

def check_auth():
    password = st.sidebar.text_input("🔒 请输入访问密码", type="password")
    if password == ADMIN_PWD: return 2
    elif password == USER_PWD:
        if 'logged_in' not in st.session_state:
            log_access("普通用户登录")
            st.session_state['logged_in'] = True
        return 1
    else: return 0

auth_status = check_auth()

if auth_status == 0:
    st.warning("⚠️ 请在左侧输入密码以访问系统。")
    st.info("提示：输入普通密码进入功能，输入管理员密码进入后台。")
    st.stop()

# ==========================================
# 4. 管理员后台
# ==========================================
if auth_status == 2:
    st.sidebar.success("🔑 管理员")
    st.title("🔧 管理员控制台")
    
    tab1, tab2, tab3 = st.tabs(["📝 日志", "💬 反馈", "⚙️ 设置"])
    
    with tab1:
        if os.path.exists(LOG_FILE):
            df = pd.read_csv(LOG_FILE).sort_values(by="访问时间", ascending=False)
            st.dataframe(df, use_container_width=True)
            st.download_button("下载日志", df.to_csv(index=False).encode('utf-8-sig'), "log.csv")
    with tab2:
        if os.path.exists(FEEDBACK_FILE):
            df = pd.read_csv(FEEDBACK_FILE).sort_values(by="时间", ascending=False)
            st.dataframe(df, use_container_width=True)
    with tab3:
        st.subheader("系统参数配置")
        with st.form("sys_config"):
            # [新增] 软件名称修改
            new_title = st.text_input("🏠 软件名称 (网页标题)", value=current_config.get("app_title"))
            
            c1, c2 = st.columns(2)
            with c1:
                new_u_pwd = st.text_input("普通密码", value=USER_PWD)
                new_a_pwd = st.text_input("管理员密码", value=ADMIN_PWD)
            with c2:
                new_ak = st.text_input("百度 API Key", value=current_config.get("baidu_api_key",""))
                new_sk = st.text_input("百度 Secret Key", value=current_config.get("baidu_secret_key",""), type="password")
            
            st.markdown("---")
            new_hint = st.text_input("📂 上传提示语", value=current_config.get("upload_hint", ""))
            
            if st.form_submit_button("💾 保存所有配置"):
                current_config.update({
                    "app_title": new_title,
                    "user_password": new_u_pwd,
                    "admin_password": new_a_pwd,
                    "baidu_api_key": new_ak,
                    "baidu_secret_key": new_sk,
                    "upload_hint": new_hint
                })
                save_config(current_config)
                st.success("配置已更新！请刷新页面查看标题变化。")
    st.stop()

# ==========================================
# 5. 普通用户界面
# ==========================================
st.title(current_config["app_title"])  # 使用配置的标题

# --- 辅助函数 ---
def natural_sort_key(s):
    s = str(s)
    for k, v in {'七':'07','八':'08','九':'09','高一':'10','高二':'11','高三':'12'}.items():
        if k in s: s = s.replace(k, v)
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', s)]

def clean_percentage(x):
    s = str(x).strip()
    return float(s.rstrip('%'))/100 if '%' in s else (float(s) if s else 0.0)

def get_grade(n):
    m = re.search(r'(.*?级)', str(n))
    return m.group(1) if m else "其他"

def weighted_avg(x, c, w='课时数'):
    try: return (x[c]*x[w]).sum()/x[w].sum() if x[w].sum()!=0 else 0
    except: return 0

def get_trend_html(curr, prev, is_pct=False):
    if not prev: return ""
    d = curr - prev
    c, s = ("#2ecc71", "↑") if d>0 else ("#e74c3c", "↓")
    v = f"{abs(d)*100:.1f}%" if is_pct else f"{int(abs(d))}"
    return f'<span style="color:{c};font-weight:bold;">{s} {v}</span>'

# --- 界面交互 ---
upload_hint_text = current_config.get("upload_hint", "⬆️ BI平台下载 - 班级数据（分学科）原文件导入即可")
uploaded_file = st.file_uploader("上传文件", type=['xlsx', 'xls', 'csv'])
st.caption(upload_hint_text)

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            try: df = pd.read_csv(uploaded_file, encoding='utf-8')
            except: df = pd.read_csv(uploaded_file, encoding='gbk')
        else: df = pd.read_excel(uploaded_file)
        
        st.success(f"✅ 已读取：{uploaded_file.name}")
        
        # --- 数据清洗 ---
        df = df.fillna(0)
        cols = {}
        if '周' in df.columns: cols['t'] = '周'
        else: cols['t'] = df.columns[0]
        
        for c in df.columns:
            if '出勤' in c: cols['a'] = c
            elif '正确' in c: cols['c'] = c
            elif '微课' in c and '率' in c: cols['m'] = c
            elif '课时' in c and '数' in c: cols['h'] = c
            elif '班级' in c: cols['cls'] = c
            elif '学科' in c: cols['s'] = c
            
        cols.setdefault('cls', '班级名称'); cols.setdefault('h', '课时数')
        cols.setdefault('a', '课时平均出勤率'); cols.setdefault('c', '题目正确率')

        for k in ['a','c','m']: 
            if k in cols and cols[k] in df.columns: df[cols[k]] = df[cols[k]].apply(clean_percentage)
            
        t_col = cols['t']
        df = df[df[t_col].astype(str) != '合计']
        periods = sorted([str(x) for x in df[t_col].unique()], key=natural_sort_key)
        
        if not periods: st.error("时间数据无效"); st.stop()
        
        cur_w = periods[-1]
        pre_w = periods[-2] if len(periods)>1 else None
        
        df_cur = df[df[t_col].astype(str)==cur_w].copy()
        df_pre = df[df[t_col].astype(str)==pre_w].copy() if pre_w else None
        df_cur['G'] = df_cur[cols['cls']].apply(get_grade)
        
        def get_m(d): 
            if d is None or d.empty: return None
            return {'h':int(d[cols['h']].sum()), 'a':weighted_avg(d,cols['a'],cols['h']), 'c':weighted_avg(d,cols['c'],cols['h'])}
        
        m_cur = get_m(df_cur)
        m_pre = get_m(df_pre)
        
        th, ta, tc = "", "", ""
        if m_pre:
            th = get_trend_html(m_cur['h'], m_pre['h'])
            ta = get_trend_html(m_cur['a'], m_pre['a'], True)
            tc = get_trend_html(m_cur['c'], m_pre['c'], True)
            
        cls_stats = df_cur.groupby(['G', cols['cls']]).apply(lambda x: pd.Series({
            'h': int(x[cols['h']].sum()),
            'a': weighted_avg(x, cols['a'], cols['h']),
            'm': weighted_avg(x, cols['m'], cols['h']) if 'm' in cols else 0,
            'c': weighted_avg(x, cols['c'], cols['h']),
            's': ','.join(x[cols['s']].astype(str).unique()) if 's' in cols else '-'
        })).reset_index()
        
        cls_stats['key'] = cls_stats.apply(lambda r: (natural_sort_key(r['G']), natural_sort_key(r[cols['cls']])), axis=1)
        cls_stats = cls_stats.sort_values('key')
        
        best = cls_stats.sort_values(['h','c'], ascending=False).iloc[0]
        focus = cls_stats[(cls_stats['a']>m_cur['a']) & (cls_stats['c']<m_cur['c'])]
        focus_row = focus.iloc[0] if not focus.empty else None
        
        best_html = f'<div class="highlight-box success-box">🏆 <strong>综合标杆：{best[cols["cls"]]}</strong> (课时:{best["h"]} / 正确率:{best["c"]*100:.1f}%)</div>'
        focus_html = ""
        if focus_row is not None:
            focus_html = f'<div class="highlight-box warning-box">⚠️ <strong>重点关注：{focus_row[cols["cls"]]}</strong> (出勤:{focus_row["a"]*100:.1f}% 正常，但正确率 {focus_row["c"]*100:.1f}% 偏低)</div>'

        tbl_html = ""
        for g in sorted(cls_stats['G'].unique(), key=natural_sort_key):
            sub = cls_stats[cls_stats['G']==g].sort_values(['h','c'], ascending=False)
            tbl_html += f"<h3>{g}</h3><table><thead><tr><th>班级</th><th>学科</th><th>课时</th><th>出勤</th><th>微课</th><th>正确率</th></tr></thead><tbody>"
            for _, r in sub.iterrows():
                ca = 'alert' if r['a']<m_cur['a'] else 'good'
                cc = 'alert' if r['c']<m_cur['c'] else 'good'
                tbl_html += f"<tr><td><b>{r[cols['cls']]}</b></td><td style='color:#999;font-size:12px'>{r['s']}</td><td>{r['h']}</td><td class='{ca}'>{r['a']*100:.1f}%</td><td>{r['m']*100:.1f}%</td><td class='{cc}'>{r['c']*100:.1f}%</td></tr>"
            tbl_html += "</tbody></table>"

        hist = df.groupby(t_col).apply(lambda x: pd.Series({
            'h':int(x[cols['h']].sum()), 'a':weighted_avg(x,cols['a'],cols['h']), 'c':weighted_avg(x,cols['c'],cols['h'])
        })).reset_index()
        hist['sk'] = hist[t_col].apply(lambda x: natural_sort_key(str(x)))
        hist = hist.sort_values('sk')
        
        js_cls = json.dumps([str(x) for x in cls_stats[cols['cls']].tolist()], ensure_ascii=False)
        js_h = json.dumps(cls_stats['h'].tolist())
        js_a = json.dumps([round(x*100,1) for x in cls_stats['a'].tolist()])
        js_c = json.dumps([round(x*100,1) for x in cls_stats['c'].tolist()])
        
        js_td = json.dumps([str(x) for x in hist[t_col].tolist()], ensure_ascii=False)
        js_th = json.dumps(hist['h'].tolist())
        js_ta = json.dumps([round(x*100,1) for x in hist['a'].tolist()])
        js_tc = json.dumps([round(x*100,1) for x in hist['c'].tolist()])

        # --- AI 交互模块 ---
        st.markdown("---")
        st.subheader("🤖 AI 教学反馈 (文心一言)")
        
        if 'ai_summary' not in st.session_state:
            prompt = f"""
            周期：{cur_w}。全校数据：总课时{m_cur['h']}，平均出勤{m_cur['a']*100:.1f}%，正确率{m_cur['c']*100:.1f}%。
            标杆：{best[cols["cls"]]}。关注：{focus_row[cols["cls"]] if focus_row is not None else "无"}。
            请写一段简短教学周报总结（200字内），包含整体评价、表扬和建议。
            """
            st.session_state['ai_msg'] = [{"role": "user", "content": prompt}]
            with st.spinner("AI 思考中..."):
                res = call_ai_service(st.session_state['ai_msg'])
                st.session_state['ai_msg'].append({"role": "assistant", "content": res})
                st.session_state['ai_summary'] = res

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**与 AI 对话修改：**")
            for m in st.session_state['ai_msg'][1:]:
                with st.chat_message(m["role"]): st.write(m["content"])
            if ui := st.chat_input("输入修改意见..."):
                st.session_state['ai_msg'].append({"role": "user", "content": ui})
                with st.chat_message("user"): st.write(ui)
                with st.spinner("AI重写中..."):
                    r = call_ai_service(st.session_state['ai_msg'])
                    st.session_state['ai_msg'].append({"role": "assistant", "content": r})
                    st.session_state['ai_summary'] = r
                    st.rerun()
        with c2:
            st.markdown("**最终确认文案：**")
            final_txt = st.text_area("编辑确认", value=st.session_state['ai_summary'], height=300)

        html = f"""
        <!DOCTYPE html><html><head><meta charset="UTF-8">
        <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
        <style>
            body {{ font-family: "Microsoft YaHei", sans-serif; max-width: 1000px; margin: 0 auto; padding: 20px; background: #f4f6f9; }}
            .card {{ background: #fff; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
            .kpi {{ display: flex; justify-content: space-around; text-align: center; }}
            .kpi div strong {{ font-size: 30px; color: #2980b9; display: block; }}
            .highlight-box {{ padding: 15px; margin: 10px 0; border-radius: 5px; font-size: 14px; }}
            .success-box {{ background: #d4edda; color: #155724; border-left: 5px solid #28a745; }}
            .warning-box {{ background: #fff3cd; color: #856404; border-left: 5px solid #ffc107; }}
            .ai-box {{ background: #e8f4fd; border-left: 5px solid #3498db; color: #2c3e50; padding: 20px; line-height: 1.8; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 14px; }}
            th {{ background: #eee; padding: 10px; border-bottom: 2px solid #ddd; }} td {{ padding: 10px; border-bottom: 1px solid #eee; text-align: center; }}
            .alert {{ color: #e74c3c; font-weight: bold; }} .good {{ color: #27ae60; }}
            .chart {{ height: 400px; width: 100%; }}
            .footer {{ text-align:center; color:#999; font-size:12px; margin-top:20px; }}
        </style></head><body>
            <h2 style="text-align:center">AI课堂教学数据分析周报</h2>
            <div style="text-align:center;color:#666;margin-bottom:20px">周期: <b>{cur_w}</b> {f'(对比: {pre_w})' if pre_w else ''}</div>
            <div class="card">
                <h3>📊 本周核心指标</h3>
                <div class="kpi">
                    <div><strong>{m_cur['h']}{th}</strong>总课时</div>
                    <div><strong>{m_cur['a']*100:.1f}%{ta}</strong>出勤率</div>
                    <div><strong>{m_cur['c']*100:.1f}%{tc}</strong>正确率</div>
                </div>{best_html}{focus_html}
            </div>
            <div class="card"><h3>🤖 智能教学反馈</h3><div class="ai-box">{final_txt.replace(chr(10), '<br>')}</div></div>
            <div class="card"><h3>🏫 班级效能分析</h3><div id="c1" class="chart"></div></div>
            <div class="card"><h3>📋 详细数据</h3><p style="text-align:right;color:#999;font-size:12px">* 红字低于校均</p>{tbl_html}</div>
            <div class="card"><h3>📈 历史趋势</h3><div id="c2" class="chart"></div></div>
            <div class="footer">Generated by AI Agent (Web Edition)</div>
            <script>
                var c1 = echarts.init(document.getElementById('c1'));
                c1.setOption({{
                    tooltip: {{trigger:'axis'}}, legend: {{bottom:0}}, grid: {{left:'3%',right:'4%',bottom:'10%',containLabel:true}},
                    xAxis: {{type:'category',data:{js_cls},axisLabel:{{rotate:30}}}},
                    yAxis: [{{type:'value',name:'课时'}},{{type:'value',name:'%',max:100}}],
                    series: [
                        {{type:'bar',name:'课时',data:{js_h},itemStyle:{{color:'#3498db'}}}},
                        {{type:'line',yAxisIndex:1,name:'出勤',data:{js_a},itemStyle:{{color:'#2ecc71'}}}},
                        {{type:'line',yAxisIndex:1,name:'正确',data:{js_c},itemStyle:{{color:'#e74c3c'}}}}
                    ]
                }});
                var c2 = echarts.init(document.getElementById('c2'));
                c2.setOption({{
                    tooltip: {{trigger:'axis'}}, legend: {{bottom:0}}, grid: {{left:'3%',right:'4%',bottom:'10%',containLabel:true}},
                    xAxis: {{type:'category',data:{js_td}}},
                    yAxis: [{{type:'value',name:'课时'}},{{type:'value',name:'%',max:100}}],
                    series: [
                        {{type:'bar',name:'课时',data:{js_th},itemStyle:{{color:'#9b59b6'}}}},
                        {{type:'line',yAxisIndex:1,name:'出勤',data:{js_ta},itemStyle:{{color:'#2ecc71'}}}},
                        {{type:'line',yAxisIndex:1,name:'正确',data:{js_tc},itemStyle:{{color:'#e74c3c'}}}}
                    ]
                }});
                window.onresize = function(){{c1.resize();c2.resize();}};
            </script>
        </body></html>
        """
        
        bn = os.path.splitext(uploaded_file.name)[0]
        st.download_button("📥 下载报表", html, f"{bn}_报表.html", "text/html")
        st.subheader("👁️ 预览"); components.html(html, height=800, scrolling=True)
        
        st.markdown("---"); st.subheader("💬 反馈")
        c_fb1, c_fb2 = st.columns([1,2])
        with c_fb1: score = st.radio("满意度", ["👍", "😐", "👎"], horizontal=True)
        with c_fb2: txt = st.text_input("建议")
        if st.button("提交"): save_feedback(score, txt); st.success("已提交")
        
    except Exception as e: st.error(f"错误: {e}")