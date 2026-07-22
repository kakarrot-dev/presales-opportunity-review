---
name: presales-opportunity-review
description: Analyze heterogeneous tender and opportunity materials for presales qualification, delivery fit, effort, commercial risk, clarification, and bid strategy. Use when a user provides tender documents, procurement lists, technical requirements, scoring rules, budgets, quotations, or opportunity notes and asks whether or how the company should participate.
---

# Presales Opportunity Review

将用户提供的商机材料转换为可追溯的参与决策、双报告和澄清清单。不用推测补全缺失信息；未通过关键门槛的交付统一保持草稿状态。

## 规则索引

执行相应阶段时读取并遵循下列契约，不在本文中复制其字段和判定细则：

- `references/material-classification.md`
- `references/project-profiling.md`
- `references/procurement-mechanism.md`
- `references/research-rules.md`
- `references/evidence-rules.md`
- `knowledge/company-profile.md`
- `references/requirement-analysis.md`
- `references/capability-matching.md`
- `references/effort-estimation.md`
- `references/evaluation-analysis.md`
- `references/opportunity-strategy.md`
- `references/clarification-questions.md`
- `references/report-template.md`

## 19 阶段工作流

严格按下列顺序执行。后续阶段不得改写上游事实或证据状态。

1. **阶段 01：建立任务边界**：确认分析目标、截止时间、输出路径、材料范围和用户明示的限制；不替用户作出报价或承诺授权。
2. **阶段 02：盘点输入材料**：枚举所有文件、附件、工作表、页面和内容区域，不忽略空白或疑似重复内容。
3. **阶段 03：提取与降级处理**：按 `references/material-classification.md` 提取文本、表格、结构、数量原文与采购约束，对不可完整解析的内容执行降级规则。
4. **阶段 04：生成材料索引**：先生成 `00-material-index.md`，为每个材料保存状态、可解析区域、可信度、来源、错误和降级记录。
5. **阶段 05：归一化项目事实**：按 `references/project-profiling.md` 建立 `project-analysis.yaml`，保留缺失、冲突、解析失败与置信度。
6. **阶段 06：识别采购机制**：按 `references/procurement-mechanism.md` 拆分标段、资金模式、报价方向、评审和授标约束，将原始规则冲突保留到 `procurement.rule_conflicts`。
7. **阶段 07：执行外部检索**：除非用户明示禁止，默认执行外部检索。按 `references/research-rules.md` 将会影响参与决策的外部结论拆为原子主张，打开可追溯原始来源，不引用搜索摘要。
8. **阶段 08：建立证据登记**：按 `references/evidence-rules.md` 为每个可核验主张建立证据记录，检查独立性、时效、适用范围和矛盾，不将转载数量当作独立来源数量。
9. **阶段 09：读取公司基线**：在任何能力分析、工作量、报价或参与建议前，读取 `knowledge/company-profile.md`，记录其更新时间、可信度和缺失章节。
10. **阶段 10：原子化需求**：按 `references/requirement-analysis.md` 按包件、交付物、验收、依赖和责任边界拆分需求，同时识别隐藏工作。
11. **阶段 11：匹配公司能力**：仅在阶段 09 完成后，按 `references/capability-matching.md` 给出 L0-L3 或待内部确认，并引用公司基线。
12. **阶段 12：估算工作量与报价**：按 `references/effort-estimation.md` 输出三点范围、假设与风险储备；未获授权时仅保留内部估算，不生成正式报价。
13. **阶段 13：分析资格与符合性**：先识别硬性资格、原厂证明、响应性和废标风险，不把未知写成已满足。
14. **阶段 14：路由评审机制**：按 `references/evaluation-analysis.md` 选择文件实际规定的评审路径；没有明确分值时不估算得分。
15. **阶段 15：形成参与策略**：按 `references/opportunity-strategy.md` 输出推荐、参与身份、前置条件、退出条件和禁止承诺，不弱化 No-Go 门槛。
16. **阶段 16：生成两类澄清清单**：按 `references/clarification-questions.md` 分别生成内部待确认清单和甲方正式澄清清单，两者不混用字段或敏感信息。
17. **阶段 17：生成内部报告**：按 `references/report-template.md` 生成完整内部报告、符合性矩阵、证据登记和结构化分析。
18. **阶段 18：独立生成正式报告**：仅从 `references/report-template.md` 的披露白名单独立生成正式报告和甲方澄清，不通过删减内部报告生成。
19. **阶段 19：执行质量门槛并定稿**：执行下述质量门槛，写明每项 `PASS`/`FAIL`、证据和责任人，再确定交付状态。

## 降级处理

降级不等于丢弃材料。对下列每项都保留原始对象、可读范围、错误、已采取的替代方法、剩余影响和补救动作：

| 触发情形 | 处理 |
| --- | --- |
| 不可读文件 | 标记 `unreadable`，不根据文件名推测内容，请求可读原件。 |
| 需要 OCR 的扫描件 | 保留页码与 OCR 置信度，低置信字段不作确定事实。 |
| 畸形表格 | 保留原单元格、标题、表头、分组与合计范围，无法确认的回填保持为空。 |
| 加密或缺失页 | 记录密码/页码缺口及其可能影响的条款，请求解密或完整版本。 |
| 多文件冲突 | 按采购规则优先级识别可用版本；无法裁决时保留双方并生成澄清。 |
| 互联网不可用 | 继续分析用户材料，外部主张标记为无法验证，不将搜索缺失视为反证。 |
| 过期公司基线 | 能力匹配、工作量、报价和参与建议降级为待内部确认。 |

所有降级必须同时出现在 `00-material-index.md`、内部报告与正式报告的适用范围/风险中；正式报告只披露对方可见且会影响范围、依赖、验收或结论的降级结果，不披露内部推理。

## 质量门槛

| 门槛 | PASS 条件 | 失败处理 |
| --- | --- | --- |
| 材料完整性 | 每个文件、工作表、页面和附件均已索引，影响决策的缺页或不可读内容已关闭。 | 保持草稿。 |
| 事实与证据 | 关键主张有可定位材料或合格 `verification_status`，来源冲突已解决。 | 不得作为确定结论。 |
| 公司基线 | 公司基线当前、可定位且覆盖相关能力、工作量和报价。 | 相关结论待内部确认。 |
| 资格与符合性 | 所有硬性资格和废标项已证明满足，无未关闭的重大缺口。 | 不得给出 Go。 |
| 商业与授权 | 报价、资金、回款、风险暴露和对外承诺均有必要依据与授权。 | 仅保留内部假设或触发 No-Go。 |
| 披露 | 正式报告由披露白名单独立生成，不含内部底价、能力弱项、竞品策略或未验证主张。 | 禁止对外交付。 |

任一关键门槛 `FAIL` 时，整套结果标记为 **草稿—需人工复核**，在内部报告顶部列出失败门槛、影响、责任人和关闭动作；披露门槛失败时不生成可发送的正式版。
