import pandas as pd
import numpy as np
import json
from datetime import datetime

print("开始分析耀襄全周期数据...")

# 读取Excel文件
try:
    df = pd.read_excel('/home/workspace/attachments/耀襄全周期.xlsx')
    print(f"成功读取数据，行数: {len(df)}, 列数: {len(df.columns)}")
except Exception as e:
    print(f"读取文件失败: {e}")
    exit(1)

# 数据清洗
# 1. 处理周次列
df['周'] = pd.to_datetime(df['周'], errors='coerce')
df = df.dropna(subset=['周'])  # 删除周次为NaN的行

# 2. 填充缺失值
df = df.fillna(0)

# 3. 确保数值列的类型
numeric_cols = ['课时数', '课时平均出勤率', '微课完成率', '题目正确率（自学+快背）']
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        df[col] = df[col].fillna(0)

print(f"数据清洗完成，剩余行数: {len(df)}")

# 分析最新周次
latest_week = df['周'].max()
print(f"\n最新周次: {latest_week.strftime('%Y-%m-%d')}")

# 获取最新周次数据
current_week_data = df[df['周'] == latest_week].copy()
print(f"最新周次数据行数: {len(current_week_data)}")

# 获取前一周次数据（如果存在）
previous_weeks = df[df['周'] < latest_week]
if len(previous_weeks) > 0:
    prev_week = previous_weeks['周'].max()
    prev_week_data = df[df['周'] == prev_week].copy()
    print(f"前一周次: {prev_week.strftime('%Y-%m-%d')}, 数据行数: {len(prev_week_data)}")
else:
    prev_week = None
    prev_week_data = pd.DataFrame()
    print("没有前一周数据")

# 计算核心指标函数
def calculate_core_metrics(data):
    """计算核心教学指标"""
    if len(data) == 0:
        return None
    
    metrics = {
        'total_hours': int(data['课时数'].sum()),
        'total_classes': data['班级名称'].nunique(),
        'total_subjects': data['课时学科'].nunique(),
        'total_records': len(data)
    }
    
    # 计算加权平均值
    def weighted_avg(value_col):
        total_weight = data['课时数'].sum()
        if total_weight == 0:
            return 0
        return (data[value_col] * data['课时数']).sum() / total_weight
    
    # 核心指标
    core_indicators = {
        'attendance_rate': '课时平均出勤率',
        'micro_completion_rate': '微课完成率',
        'correctness_rate': '题目正确率（自学+快背）'
    }
    
    for key, col in core_indicators.items():
        if col in data.columns:
            metrics[key] = float(weighted_avg(col))
        else:
            metrics[key] = 0.0
    
    return metrics

# 计算当前周指标
current_metrics = calculate_core_metrics(current_week_data)
print(f"\n=== 当前周核心指标 ===")
if current_metrics:
    print(f"总课时: {current_metrics['total_hours']}")
    print(f"涉及班级: {current_metrics['total_classes']}个")
    print(f"涉及学科: {current_metrics['total_subjects']}门")
    print(f"平均出勤率: {current_metrics['attendance_rate']*100:.2f}%")
    print(f"微课完成率: {current_metrics['micro_completion_rate']*100:.2f}%")
    print(f"题目正确率: {current_metrics['correctness_rate']*100:.2f}%")

# 计算前一周指标（如果存在）
if len(prev_week_data) > 0:
    prev_metrics = calculate_core_metrics(prev_week_data)
    print(f"\n=== 前一周核心指标 ===")
    if prev_metrics:
        print(f"总课时: {prev_metrics['total_hours']}")
        print(f"平均出勤率: {prev_metrics['attendance_rate']*100:.2f}%")
        print(f"微课完成率: {prev_metrics['micro_completion_rate']*100:.2f}%")
        print(f"题目正确率: {prev_metrics['correctness_rate']*100:.2f}%")
        
        # 计算变化趋势
        print(f"\n=== 周环比变化 ===")
        for key in ['total_hours', 'attendance_rate', 'micro_completion_rate', 'correctness_rate']:
            if key in current_metrics and key in prev_metrics:
                current_val = current_metrics[key]
                prev_val = prev_metrics[key]
                if prev_val != 0:
                    change = ((current_val - prev_val) / prev_val) * 100
                    trend = "↑" if change > 0 else "↓" if change < 0 else "→"
                    print(f"{key}: {trend} {abs(change):.1f}%")

# 班级表现分析
print(f"\n=== 班级表现分析 ===")
class_stats = current_week_data.groupby('班级名称').apply(
    lambda x: pd.Series({
        '总课时': int(x['课时数'].sum()),
        '平均出勤率': (x['课时平均出勤率'] * x['课时数']).sum() / x['课时数'].sum() if x['课时数'].sum() > 0 else 0,
        '平均微课完成率': (x['微课完成率'] * x['课时数']).sum() / x['课时数'].sum() if x['课时数'].sum() > 0 else 0,
        '平均题目正确率': (x['题目正确率（自学+快背）'] * x['课时数']).sum() / x['课时数'].sum() if x['课时数'].sum() > 0 else 0,
        '涉及学科': ', '.join(x['课时学科'].dropna().unique()),
        '记录数': len(x)
    })
).reset_index()

print(f"分析班级数量: {len(class_stats)}")

# 找出最佳班级（综合表现）
if len(class_stats) > 0:
    class_stats['综合得分'] = (
        class_stats['平均出勤率'] * 0.3 +
        class_stats['平均微课完成率'] * 0.3 +
        class_stats['平均题目正确率'] * 0.4
    )
    
    best_class_idx = class_stats['综合得分'].idxmax()
    best_class = class_stats.loc[best_class_idx]
    
    print(f"\n🏆 最佳班级: {best_class['班级名称']}")
    print(f"  综合得分: {best_class['综合得分']:.3f}")
    print(f"  总课时: {best_class['总课时']}")
    print(f"  平均出勤率: {best_class['平均出勤率']*100:.1f}%")
    print(f"  平均题目正确率: {best_class['平均题目正确率']*100:.1f}%")
    print(f"  涉及学科: {best_class['涉及学科']}")

# 找出需要关注的班级（出勤正常但正确率低）
if current_metrics and len(class_stats) > 0:
    focus_classes = class_stats[
        (class_stats['平均出勤率'] > current_metrics['attendance_rate']) & 
        (class_stats['平均题目正确率'] < current_metrics['correctness_rate'])
    ]
    
    if len(focus_classes) > 0:
        focus_class = focus_classes.iloc[0]
        print(f"\n⚠️ 重点关注班级: {focus_class['班级名称']}")
        print(f"  出勤率: {focus_class['平均出勤率']*100:.1f}% (高于平均 {current_metrics['attendance_rate']*100:.1f}%)")
        print(f"  题目正确率: {focus_class['平均题目正确率']*100:.1f}% (低于平均 {current_metrics['correctness_rate']*100:.1f}%)")
        print(f"  涉及学科: {focus_class['涉及学科']}")

# 学科分析
print(f"\n=== 学科表现分析 ===")
subject_stats = current_week_data.groupby('课时学科').apply(
    lambda x: pd.Series({
        '总课时': int(x['课时数'].sum()),
        '平均出勤率': (x['课时平均出勤率'] * x['课时数']).sum() / x['课时数'].sum() if x['课时数'].sum() > 0 else 0,
        '平均题目正确率': (x['题目正确率（自学+快背）'] * x['课时数']).sum() / x['课时数'].sum() if x['课时数'].sum() > 0 else 0,
        '涉及班级数': x['班级名称'].nunique(),
        '记录数': len(x)
    })
).reset_index()

print(f"分析学科数量: {len(subject_stats)}")

# 显示课时最多的学科
if len(subject_stats) > 0:
    top_subjects = subject_stats.sort_values('总课时', ascending=False).head(5)
    print(f"\n📚 课时最多的5个学科:")
    for _, row in top_subjects.iterrows():
        print(f"  {row['课时学科']}: {row['总课时']}课时, 正确率:{row['平均题目正确率']*100:.1f}%, 涉及{row['涉及班级数']}个班级")

# 历史趋势分析
print(f"\n=== 历史趋势分析 ===")
weekly_trends = []
for week in sorted(df['周'].unique()):
    week_data = df[df['周'] == week]
    metrics = calculate_core_metrics(week_data)
    if metrics:
        weekly_trends.append({
            'week': week.strftime('%Y-%m-%d'),
            'total_hours': metrics['total_hours'],
            'attendance_rate': metrics['attendance_rate'],
            'correctness_rate': metrics['correctness_rate'],
            'class_count': metrics['total_classes']
        })

print(f"分析周次数: {len(weekly_trends)}")

if len(weekly_trends) >= 2:
    first_week = weekly_trends[0]
    last_week = weekly_trends[-1]
    
    print(f"\n📈 整体趋势对比:")
    print(f"  从 {first_week['week']} 到 {last_week['week']}")
    print(f"  总课时: {first_week['total_hours']} → {last_week['total_hours']}")
    print(f"  出勤率: {first_week['attendance_rate']*100:.1f}% → {last_week['attendance_rate']*100:.1f}%")
    print(f"  题目正确率: {first_week['correctness_rate']*100:.1f}% → {last_week['correctness_rate']*100:.1f}%")

# 保存分析结果
analysis_results = {
    'file_info': {
        'file_name': '耀襄全周期.xlsx',
        'total_records': len(df),
        'date_range': {
            'start': df['周'].min().strftime('%Y-%m-%d'),
            'end': df['周'].max().strftime('%Y-%m-%d')
        }
    },
    'current_week': {
        'date': latest_week.strftime('%Y-%m-%d'),
        'metrics': current_metrics,
        'class_stats_count': len(class_stats) if 'class_stats' in locals() else 0,
        'subject_stats_count': len(subject_stats) if 'subject_stats' in locals() else 0
    },
    'best_class': {
        'name': best_class['班级名称'] if 'best_class' in locals() else None,
        'hours': int(best_class['总课时']) if 'best_class' in locals() else 0,
        'attendance_rate': float(best_class['平均出勤率']) if 'best_class' in locals() else 0,
        'correctness_rate': float(best_class['平均题目正确率']) if 'best_class' in locals() else 0,
        'subjects': best_class['涉及学科'] if 'best_class' in locals() else ''
    },
    'focus_class': {
        'name': focus_class['班级名称'] if 'focus_class' in locals() else None,
        'attendance_rate': float(focus_class['平均出勤率']) if 'focus_class' in locals() else 0,
        'correctness_rate': float(focus_class['平均题目正确率']) if 'focus_class' in locals() else 0,
        'subjects': focus_class['涉及学科'] if 'focus_class' in locals() else ''
    },
    'top_subjects': top_subjects[['课时学科', '总课时', '平均题目正确率', '涉及班级数']].to_dict('records') if 'top_subjects' in locals() and len(top_subjects) > 0 else [],
    'weekly_trends': weekly_trends,
    'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
}

# 保存到JSON文件
output_file = '/home/workspace/analysis_results.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(analysis_results, f, ensure_ascii=False, indent=2, default=str)

print(f"\n✅ 分析完成!")
print(f"分析结果已保存到: {output_file}")
print(f"总分析记录: {len(df)}条")
print(f"涉及周次: {len(weekly_trends)}周")
print(f"涉及班级: {df['班级名称'].nunique()}个")
print(f"涉及学科: {df['课时学科'].nunique()}门")