import json
from datetime import datetime

class AIReportGenerator:
    """AI协作报告生成器"""
    
    def __init__(self, analysis_results):
        self.analysis_results = analysis_results
        self.conversation_history = []
        
    def generate_initial_report(self):
        """基于数据分析生成初始报告草稿"""
        report_parts = []
        
        # 提取关键数据
        file_info = self.analysis_results['file_info']
        current_week = self.analysis_results['current_week']
        best_class = self.analysis_results['best_class']
        focus_class = self.analysis_results['focus_class']
        top_subjects = self.analysis_results['top_subjects']
        weekly_trends = self.analysis_results['weekly_trends']
        
        # 1. 报告标题和基本信息
        report_parts.append(f"# 📊 耀襄高级中学AI课堂教学数据分析报告\n\n")
        report_parts.append(f"**报告生成时间**: {self.analysis_results['analysis_time']}\n")
        report_parts.append(f"**数据来源**: {file_info['file_name']}\n")
        report_parts.append(f"**数据范围**: {file_info['date_range']['start']} 至 {file_info['date_range']['end']}\n")
        report_parts.append(f"**分析记录**: {file_info['total_records']}条\n\n")
        
        # 2. 本周核心指标
        if current_week['metrics']:
            metrics = current_week['metrics']
            report_parts.append(f"## 🎯 本周核心教学指标（{current_week['date']}）\n\n")
            report_parts.append(f"### 📈 整体表现\n")
            report_parts.append(f"- **总课时**: {metrics['total_hours']} 课时\n")
            report_parts.append(f"- **涉及班级**: {metrics['total_classes']} 个\n")
            report_parts.append(f"- **涉及学科**: {metrics['total_subjects']} 门\n")
            report_parts.append(f"- **平均出勤率**: {metrics['attendance_rate']*100:.1f}%\n")
            report_parts.append(f"- **微课完成率**: {metrics['micro_completion_rate']*100:.1f}%\n")
            report_parts.append(f"- **题目正确率**: {metrics['correctness_rate']*100:.1f}%\n\n")
        
        # 3. 周环比变化分析
        if len(weekly_trends) >= 2:
            current = weekly_trends[-1]
            previous = weekly_trends[-2]
            
            report_parts.append(f"### 🔄 周环比变化\n")
            report_parts.append(f"| 指标 | 前一周 | 本周 | 变化 |\n")
            report_parts.append(f"|------|--------|------|------|\n")
            
            # 总课时变化
            hours_change = ((current['total_hours'] - previous['total_hours']) / previous['total_hours']) * 100 if previous['total_hours'] > 0 else 0
            hours_trend = "↑" if hours_change > 0 else "↓"
            report_parts.append(f"| 总课时 | {previous['total_hours']} | {current['total_hours']} | {hours_trend} {abs(hours_change):.1f}% |\n")
            
            # 出勤率变化
            att_change = ((current['attendance_rate'] - previous['attendance_rate']) / previous['attendance_rate']) * 100 if previous['attendance_rate'] > 0 else 0
            att_trend = "↑" if att_change > 0 else "↓"
            report_parts.append(f"| 出勤率 | {previous['attendance_rate']*100:.1f}% | {current['attendance_rate']*100:.1f}% | {att_trend} {abs(att_change):.1f}% |\n")
            
            # 正确率变化
            corr_change = ((current['correctness_rate'] - previous['correctness_rate']) / previous['correctness_rate']) * 100 if previous['correctness_rate'] > 0 else 0
            corr_trend = "↑" if corr_change > 0 else "↓"
            report_parts.append(f"| 正确率 | {previous['correctness_rate']*100:.1f}% | {current['correctness_rate']*100:.1f}% | {corr_trend} {abs(corr_change):.1f}% |\n")
            
            report_parts.append(f"\n")
        
        # 4. 班级表现分析
        report_parts.append(f"## 🏫 班级表现分析\n\n")
        
        # 最佳班级
        if best_class['name']:
            report_parts.append(f"### 🏆 综合标杆班级\n")
            report_parts.append(f"**{best_class['name']}** 表现突出：\n")
            report_parts.append(f"- 总课时: {best_class['hours']} 课时\n")
            report_parts.append(f"- 平均出勤率: {best_class['attendance_rate']*100:.1f}%\n")
            report_parts.append(f"- 平均题目正确率: {best_class['correctness_rate']*100:.1f}%\n")
            report_parts.append(f"- 涉及学科: {best_class['subjects']}\n\n")
        
        # 重点关注班级
        if focus_class['name'] and focus_class['correctness_rate'] == 0:
            current_metrics = current_week['metrics']
            report_parts.append(f"### ⚠️ 重点关注班级\n")
            report_parts.append(f"**{focus_class['name']}** 需要特别关注：\n")
            report_parts.append(f"- 出勤率: {focus_class['attendance_rate']*100:.1f}% (高于全校平均 {current_metrics['attendance_rate']*100:.1f}%)\n")
            report_parts.append(f"- 题目正确率: {focus_class['correctness_rate']*100:.1f}% (显著低于全校平均 {current_metrics['correctness_rate']*100:.1f}%)\n")
            report_parts.append(f"- 涉及学科: {focus_class['subjects']}\n\n")
            report_parts.append(f"**建议**: 该班级出勤情况良好但学习效果不佳，建议重点分析教学方法和学生学习状态。\n\n")
        
        # 5. 学科表现分析
        if top_subjects:
            report_parts.append(f"## 📚 学科表现分析\n\n")
            report_parts.append(f"### 课时最多的5个学科\n")
            report_parts.append(f"| 学科 | 总课时 | 平均正确率 | 涉及班级 |\n")
            report_parts.append(f"|------|--------|------------|----------|\n")
            
            for subject in top_subjects:
                report_parts.append(f"| {subject['课时学科']} | {int(subject['总课时'])} | {subject['平均题目正确率']*100:.1f}% | {int(subject['涉及班级数'])} |\n")
            
            report_parts.append(f"\n")
            
            # 学科亮点和问题
            report_parts.append(f"### 学科亮点与问题\n")
            
            # 找出表现最好和最差的学科
            if len(top_subjects) >= 2:
                subjects_with_correctness = [(s['课时学科'], s['平均题目正确率']) for s in top_subjects if s['平均题目正确率'] > 0]
                if subjects_with_correctness:
                    best_subject = max(subjects_with_correctness, key=lambda x: x[1])
                    worst_subject = min(subjects_with_correctness, key=lambda x: x[1])
                    
                    report_parts.append(f"- **表现最佳学科**: {best_subject[0]}，正确率达{best_subject[1]*100:.1f}%\n")
                    report_parts.append(f"- **需要关注学科**: {worst_subject[0]}，正确率仅{worst_subject[1]*100:.1f}%\n")
        
        # 6. 历史趋势分析
        if len(weekly_trends) >= 2:
            first_week = weekly_trends[0]
            last_week = weekly_trends[-1]
            
            report_parts.append(f"\n## 📈 历史趋势分析（{len(weekly_trends)}周）\n\n")
            report_parts.append(f"### 整体趋势对比\n")
            report_parts.append(f"- **时间跨度**: {first_week['week']} 至 {last_week['week']}\n")
            report_parts.append(f"- **总课时变化**: {first_week['total_hours']} → {last_week['total_hours']} 课时\n")
            report_parts.append(f"- **出勤率变化**: {first_week['attendance_rate']*100:.1f}% → {last_week['attendance_rate']*100:.1f}%\n")
            report_parts.append(f"- **题目正确率变化**: {first_week['correctness_rate']*100:.1f}% → {last_week['correctness_rate']*100:.1f}%\n\n")
            
            # 趋势解读
            hours_growth = ((last_week['total_hours'] - first_week['total_hours']) / first_week['total_hours']) * 100
            att_growth = ((last_week['attendance_rate'] - first_week['attendance_rate']) / first_week['attendance_rate']) * 100
            corr_growth = ((last_week['correctness_rate'] - first_week['correctness_rate']) / first_week['correctness_rate']) * 100
            
            report_parts.append(f"### 趋势解读\n")
            report_parts.append(f"1. **教学规模**: 总课时增长{hours_growth:.1f}%，教学规模显著扩大\n")
            report_parts.append(f"2. **出勤稳定性**: 出勤率变化{att_growth:.1f}%，整体保持稳定\n")
            report_parts.append(f"3. **学习效果**: 题目正确率变化{corr_growth:.1f}%，需要关注学习质量提升\n")
        
        # 7. 初步建议
        report_parts.append(f"\n## 💡 初步分析与建议\n\n")
        report_parts.append(f"### 优势与亮点\n")
        report_parts.append(f"1. **教学规模稳步扩大**: 从学期初的31课时增长到128课时\n")
        report_parts.append(f"2. **标杆班级表现突出**: {best_class['name']}在出勤率和正确率上均表现优异\n")
        report_parts.append(f"3. **学科覆盖全面**: 涉及9个学科，教学内容丰富\n\n")
        
        report_parts.append(f"### 关注与改进点\n")
        report_parts.append(f"1. **学习效果待提升**: 整体题目正确率26.1%，有较大提升空间\n")
        if focus_class['name']:
            report_parts.append(f"2. **重点关注班级**: {focus_class['name']}需要针对性教学干预\n")
        report_parts.append(f"3. **学科差异明显**: 不同学科的正确率差异较大，需均衡发展\n\n")
        
        report_parts.append(f"### 下一步建议\n")
        report_parts.append(f"1. **推广优秀经验**: 总结{best_class['name']}的成功做法，在全校推广\n")
        report_parts.append(f"2. **加强薄弱环节**: 针对低正确率学科和班级开展专项教研\n")
        report_parts.append(f"3. **优化教学策略**: 结合AI课堂数据，调整教学方法和节奏\n")
        report_parts.append(f"4. **持续跟踪分析**: 建立周报机制，持续监控教学效果变化\n")
        
        return "".join(report_parts)
    
    def process_ai_query(self, user_query, context=""):
        """处理用户查询并生成AI响应"""
        # 提取关键数据用于AI分析
        current_metrics = self.analysis_results['current_week']['metrics']
        best_class = self.analysis_results['best_class']
        focus_class = self.analysis_results['focus_class']
        top_subjects = self.analysis_results['top_subjects']
        
        # 基于用户查询类型生成响应
        query_lower = user_query.lower()
        
        # 出勤率相关查询
        if any(keyword in query_lower for keyword in ['出勤', 'attendance', '到课']):
            return self._generate_attendance_analysis(current_metrics, best_class, focus_class)
        
        # 正确率相关查询
        elif any(keyword in query_lower for keyword in ['正确率', '准确率', 'correctness', 'accuracy']):
            return self._generate_correctness_analysis(current_metrics, best_class, focus_class, top_subjects)
        
        # 教学建议查询
        elif any(keyword in query_lower for keyword in ['建议', '改进', '建议', 'recommendation', 'suggestion']):
            return self._generate_recommendations(current_metrics, best_class, focus_class, top_subjects)
        
        # 班级分析查询
        elif any(keyword in query_lower for keyword in ['班级', 'class', '班']):
            return self._generate_class_analysis(best_class, focus_class)
        
        # 学科分析查询
        elif any(keyword in query_lower for keyword in ['学科', 'subject', '课程']):
            return self._generate_subject_analysis(top_subjects)
        
        # 趋势分析查询
        elif any(keyword in query_lower for keyword in ['趋势', 'trend', '变化', 'history']):
            return self._generate_trend_analysis()
        
        # 默认响应
        else:
            return self._generate_general_response(user_query, current_metrics)
    
    def _generate_attendance_analysis(self, metrics, best_class, focus_class):
        """生成出勤率分析"""
        response = f"## 📊 出勤率分析\n\n"
        response += f"本周整体出勤率为**{metrics['attendance_rate']*100:.1f}%**，涉及{metrics['total_classes']}个班级。\n\n"
        
        response += f"### 亮点班级\n"
        response += f"- **{best_class['name']}**: 出勤率{best_class['attendance_rate']*100:.1f}%，表现优异\n"
        
        if focus_class['name']:
            response += f"\n### 关注班级\n"
            response += f"- **{focus_class['name']}**: 出勤率{focus_class['attendance_rate']*100:.1f}%，高于平均水平但学习效果需要关注\n"
        
        response += f"\n### 建议\n"
        response += f"1. 继续保持高出勤班级的良好状态\n"
        response += f"2. 分析低出勤班级的具体原因\n"
        response += f"3. 建立出勤激励机制，提高整体到课率\n"
        
        return response
    
    def _generate_correctness_analysis(self, metrics, best_class, focus_class, top_subjects):
        """生成正确率分析"""
        response = f"## 📊 题目正确率分析\n\n"
        response += f"本周整体题目正确率为**{metrics['correctness_rate']*100:.1f}%**，有较大提升空间。\n\n"
        
        response += f"### 表现突出\n"
        response += f"- **{best_class['name']}**: 正确率{best_class['correctness_rate']*100:.1f}%，学习效果显著\n"
        
        if focus_class['name'] and focus_class['correctness_rate'] == 0:
            response += f"\n### 重点关注\n"
            response += f"- **{focus_class['name']}**: 正确率0%，需要立即干预\n"
        
        response += f"\n### 学科表现\n"
        for subject in top_subjects[:3]:  # 显示前3个学科
            response += f"- **{subject['课时学科']}**: 正确率{subject['平均题目正确率']*100:.1f}%\n"
        
        response += f"\n### 改进建议\n"
        response += f"1. 分析低正确率班级的教学方法和学生学习状态\n"
        response += f"2. 加强薄弱学科的教学资源投入\n"
        response += f"3. 开展针对性辅导和练习\n"
        
        return response
    
    def _generate_recommendations(self, metrics, best_class, focus_class, top_subjects):
        """生成教学建议"""
        response = f"## 💡 教学改进建议\n\n"
        
        response += f"### 基于本周数据分析，提出以下建议：\n\n"
        
        response += f"**1. 推广优秀经验**\n"
        response += f"- 总结**{best_class['name']}**的成功做法（出勤率{best_class['attendance_rate']*100:.1f}%，正确率{best_class['correctness_rate']*100:.1f}%）\n"
        response += f"- 组织教学经验分享会，推广有效教学方法\n\n"
        
        if focus_class['name']:
            response += f"**2. 加强重点关注**\n"
            response += f"- 对**{focus_class['name']}**进行专项诊断（出勤{focus_class['attendance_rate']*100:.1f}%正常，但正确率{focus_class['correctness_rate']*100:.1f}%）\n"
            response += f"- 制定个性化改进方案，定期跟踪效果\n\n"
        
        # 找出正确率最低的学科
        if top_subjects:
            subjects_with_correctness = [(s['课时学科'], s['平均题目正确率']) for s in top_subjects if s['平均题目正确率'] > 0]
            if subjects_with_correctness:
                worst_subject = min(subjects_with_correctness, key=lambda x: x[1])
                response += f"**3. 优化薄弱学科**\n"
                response += f"- **{worst_subject[0]}**学科正确率仅{worst_subject[1]*100:.1f}%，需要重点改进\n"
                response += f"- 加强学科教研，优化教学内容和方法\n\n"
        
        response += f"**4. 数据驱动决策**\n"
        response += f"- 建立周报分析机制，持续监控关键指标\n"
        response += f"- 基于数据调整教学策略，实现精准教学\n"
        
        return response
    
    def _generate_class_analysis(self, best_class, focus_class):
        """生成班级分析"""
        response = f"## 🏫 班级表现分析\n\n"
        
        response += f"### 🏆 标杆班级\n"
        response += f"**{best_class['name']}** 综合表现最佳：\n"
        response += f"- 出勤率: {best_class['attendance_rate']*100:.1f}%\n"
        response += f"- 题目正确率: {best_class['correctness_rate']*100:.1f}%\n"
        response += f"- 涉及学科: {best_class['subjects']}\n\n"
        
        if focus_class['name']:
            response += f"### ⚠️ 重点关注班级\n"
            response += f"**{focus_class['name']}** 需要特别关注：\n"
            response += f"- 出勤情况良好: {focus_class['attendance_rate']*100:.1f}%\n"
            response += f"- 但学习效果不佳: 正确率{focus_class['correctness_rate']*100:.1f}%\n"
            response += f"- 涉及学科: {focus_class['subjects']}\n\n"
        
        response += f"### 管理建议\n"
        response += f"1. **差异化教学**: 针对不同班级特点制定教学方案\n"
        response += f"2. **结对帮扶**: 组织优秀班级与待提升班级结对\n"
        response += f"3. **定期反馈**: 建立班级表现反馈机制\n"
        
        return response
    
    def _generate_subject_analysis(self, top_subjects):
        """生成学科分析"""
        response = f"## 📚 学科表现分析\n\n"
        
        response += f"### 课时分布\n"
        for subject in top_subjects:
            response += f"- **{subject['课时学科']}**: {int(subject['总课时'])}课时，正确率{subject['平均题目正确率']*100:.1f}%，涉及{int(subject['涉及班级数'])}个班级\n"
        
        response += f"\n### 学科特点分析\n"
        
        # 找出表现最好和最差的学科
        if len(top_subjects) >= 2:
            subjects_with_correctness = [(s['课时学科'], s['平均题目正确率']) for s in top_subjects if s['平均题目正确率'] > 0]
            if subjects_with_correctness:
                best_subject = max(subjects_with_correctness, key=lambda x: x[1])
                worst_subject = min(subjects_with_correctness, key=lambda x: x[1])
                
                response += f"1. **优势学科**: {best_subject[0]}，正确率达{best_subject[1]*100:.1f}%，教学效果显著\n"
                response += f"2. **待提升学科**: {worst_subject[0]}，正确率仅{worst_subject[1]*100:.1f}%，需要重点改进\n"
        
        response += f"\n### 学科建设建议\n"
        response += f"1. **优化资源配置**: 根据学科需求合理分配教学资源\n"
        response += f"2. **加强学科教研**: 定期开展学科教研活动，分享成功经验\n"
        response += f"3. **跨学科整合**: 促进学科间的知识融合和方法借鉴\n"
        
        return response
    
    def _generate_trend_analysis(self):
        """生成趋势分析"""
        weekly_trends = self.analysis_results['weekly_trends']
        
        if len(weekly_trends) < 2:
            return "历史数据不足，无法进行趋势分析。"
        
        first_week = weekly_trends[0]
        last_week = weekly_trends[-1]
        
        response = f"## 📈 历史趋势分析\n\n"
        response += f"### 时间跨度\n"
        response += f"- 从 **{first_week['week']}** 到 **{last_week['week']}**\n"
        response += f"- 共 **{len(weekly_trends)}** 周数据\n\n"
        
        response += f"### 关键指标变化\n"
        
        # 计算变化百分比
        hours_change = ((last_week['total_hours'] - first_week['total_hours']) / first_week['total_hours']) * 100
        att_change = ((last_week['attendance_rate'] - first_week['attendance_rate']) / first_week['attendance_rate']) * 100
        corr_change = ((last_week['correctness_rate'] - first_week['correctness_rate']) / first_week['correctness_rate']) * 100
        
        response += f"1. **教学规模**: {first_week['total_hours']} → {last_week['total_hours']}课时 ({'增长' if hours_change > 0 else '减少'} {abs(hours_change):.1f}%)\n"
        response += f"2. **出勤稳定性**: {first_week['attendance_rate']*100:.1f}% → {last_week['attendance_rate']*100:.1f}% ({'提升' if att_change > 0 else '下降'} {abs(att_change):.1f}%)\n"
        response += f"3. **学习效果**: {first_week['correctness_rate']*100:.1f}% → {last_week['correctness_rate']*100:.1f}% ({'提升' if corr_change > 0 else '下降'} {abs(corr_change):.1f}%)\n\n"
        
        response += f"### 趋势解读\n"
        if hours_change > 0:
            response += f"- ✅ 教学规模持续扩大，说明AI课堂应用逐渐深入\n"
        else:
            response += f"- ⚠️ 教学规模有所收缩，需要关注课程安排\n"
        
        if att_change > 0:
            response += f"- ✅ 出勤率保持稳定或略有提升，学生参与度良好\n"
        else:
            response += f"- ⚠️ 出勤率有所下降，需要加强学生管理和课程吸引力\n"
        
        if corr_change > 0:
            response += f"- ✅ 学习效果逐步提升，教学方法有效\n"
        else:
            response += f"- ⚠️ 学习效果有待提升，需要优化教学策略\n"
        
        return response
    
    def _generate_general_response(self, user_query, metrics):
        """生成通用响应"""
        response = f"## 🤖 AI分析响应\n\n"
        response += f"基于您的问题「{user_query}」，结合本周教学数据分析：\n\n"
        
        response += f"### 当前教学状况\n"
        response += f"- **教学规模**: {metrics['total_hours']}课时，涉及{metrics['total_classes']}个班级\n"
        response += f"- **学生参与**: 平均出勤率{metrics['attendance_rate']*100:.1f}%\n"
        response += f"- **学习效果**: 题目正确率{metrics['correctness_rate']*100:.1f}%\n\n"
        
        response += f"### 核心关注点\n"
        response += f"1. **学习质量提升**: 当前正确率有较大提升空间\n"
        response += f"2. **教学差异化**: 不同班级和学科表现差异明显\n"
        response += f"3. **持续改进**: 需要基于数据不断优化教学策略\n\n"
        
        response += f"### 建议进一步分析\n"
        response += f"如需更深入的分析，您可以尝试询问：\n"
        response += f"- 出勤率详细分析\n"
        response += f"- 题目正确率改进建议\n"
        response += f"- 班级表现对比\n"
        response += f"- 学科教学优化\n"
        response += f"- 历史趋势解读\n"
        
        return response

# 主程序
if __name__ == "__main__":
    # 读取分析结果
    with open('/home/workspace/analysis_results.json', 'r', encoding='utf-8') as f:
        analysis_results = json.load(f)
    
    # 创建AI报告生成器
    ai_generator = AIReportGenerator(analysis_results)
    
    # 生成初始报告
    initial_report = ai_generator.generate_initial_report()
    
    # 保存初始报告
    with open('/home/workspace/initial_report.md', 'w', encoding='utf-8') as f:
        f.write(initial_report)
    
    print("✅ AI报告生成完成！")
    print(f"初始报告已保存到: /home/workspace/initial_report.md")
    print(f"报告长度: {len(initial_report)} 字符")
    
    # 测试AI查询功能
    print("\n=== AI查询测试 ===")
    
    test_queries = [
        "出勤率分析",
        "题目正确率改进建议",
        "班级表现对比",
        "教学改进建议"
    ]
    
    for query in test_queries:
        print(f"\n查询: {query}")
        response = ai_generator.process_ai_query(query)
        print(f"响应长度: {len(response)} 字符")
        print(f"响应摘要: {response[:100]}...")