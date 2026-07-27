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

1. **阶段 01：接收用户材料**：接收文件、附件和用户补充说明，确认分析目标、截止时间、输出路径和用户明示的限制；不替用户作出报价或承诺授权。
2. **阶段 02：枚举并识别有效内容**：按 `references/material-classification.md` 逐文件、附件、工作表、页面和内容区域建立记录，保留空白页/表、原始数量文本、采购约束和降级错误，生成 `00-material-index.md`。
3. **阶段 03：读取公司能力基线**：在任何能力分析、工作量、报价或参与建议前，读取 `knowledge/company-profile.md`，逐条核对稳定条目 ID、更新时间、复核期限、状态、可信度、负责人、证据、适用范围、缺失和过期状态。
4. **阶段 04：建立项目画像**：按 `references/project-profiling.md` 建立 `project-analysis.yaml`，只归一化材料直接支持的事实，保留缺失、冲突、解析失败和置信度。
5. **阶段 05：识别采购机制**：按 `references/procurement-mechanism.md` 识别采购类型、资金模式、报价方向、轮次、评审和授标约束，不默认低价中标。
6. **阶段 06：检查条款优先级与冲突**：按采购规则优先级比对版本与条款，将无法裁决的原始矛盾同时写入 `materials.conflicts` 和 `procurement.rule_conflicts`。
7. **阶段 07：检查材料完整度**：逐项检查应有文件、页码、附件、工作表和关键条款，将不可读、空白、加密、缺页和缺件作为可追溯降级项。
8. **阶段 08：默认执行外部调查**：除非用户明示禁止，默认执行外部调查。按 `references/research-rules.md` 拆分原子主张并打开原始来源，再按 `references/evidence-rules.md` 建立证据记录；不直接引用搜索摘要。
9. **阶段 09：拆分标段/采购包/需求项**：按 `references/requirement-analysis.md` 先拆标段与采购包，再按交付物、验收、依赖和责任边界形成可追溯的原子需求。
10. **阶段 10：分析资格及响应合规**：按 `references/evaluation-analysis.md` 识别硬性资格、原厂证明、响应性、可补正性和废标风险，不把未知写成已满足。
11. **阶段 11：逐条能力匹配**：仅在阶段 03 完成后，按 `references/capability-matching.md` 对每条原子需求给出 L0-L3 或待内部确认，并引用一个或多个当前有效的公司基线条目 ID；缺失、无 ID 或过期引用一律降级为待内部确认。
12. **阶段 12：隐藏工作量和风险**：按 `references/requirement-analysis.md` 逐项检查数据、接口、部署、迁移、定制、测试、培训、现场服务、质保和验收，记录触发条件、影响与缓解动作。
13. **阶段 13：竞品和厂商生态**：只基于采购材料或已核验证据识别直接竞品、替代方案、原厂和潜在合作方，记录授权、合作边界和失效影响。
14. **阶段 14：评审与成交路径**：按 `references/evaluation-analysis.md` 选择文件实际规定的评审、排序、谈判和授标路径；没有明确分值时不估算得分。
15. **阶段 15：人天/周期/报价区间**：按 `references/effort-estimation.md` 输出三点人天、人员、周期和报价区间，附假设、不含项和风险储备；未获授权时仅保留内部估算。
16. **阶段 16：参与模式和成立条件**：按 `references/opportunity-strategy.md` 输出推荐、参与身份、成立条件、退出条件和禁止承诺，不用 Conditional Go 弱化 No-Go 或信息不足门槛。
17. **阶段 17：两套澄清清单**：按 `references/clarification-questions.md` 分别生成内部待确认清单和甲方正式澄清清单，两者不混用字段或敏感信息。
18. **阶段 18：内部版和正式版**：按 `references/report-template.md` 先生成完整内部版 Markdown 与 HTML；仅从披露白名单独立生成正式版 Markdown、HTML 和甲方澄清，不通过删减、DOM 隐藏或浏览器脚本处理内部报告生成正式版。
19. **阶段 19：证据/矛盾/完整性/敏感信息质量检查**：对证据状态、来源矛盾、材料完整度、公司基线、资格商业门槛与敏感信息披露逐项记录 `PASS`/`FAIL`、证据、责任人和关闭动作，再确定交付状态。

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

只有 `已由一手来源确认` 或 `已交叉验证` 能支持正式报告中的确定性事实；`单一来源待验证`、`来源冲突` 和 `无法验证` 均禁止作为正式确定事实。证据质量检查必须逐条核对 `source_date`、`accessed_at`、独立来源和循环转载；循环转载只计一个来源。

公司基线门槛 `FAIL` 时，当前 `company_match` 必须为 `待内部确认`，当前 `strategy.recommendation` 必须为 `Insufficient Information`。L0-L2 或 Go/Conditional Go 只能放入明确标注“非当前结论”的条件分支。

| 门槛 | PASS 条件 | 失败处理 |
| --- | --- | --- |
| 材料完整性 | 每个文件、工作表、页面和附件均已索引，影响决策的缺页或不可读内容已关闭。 | 保持草稿。 |
| 事实与证据 | 关键主张有可定位材料或合格 `verification_status`，来源冲突已解决。 | 不得作为确定结论。 |
| 公司基线 | 公司基线当前、可定位且覆盖相关能力、工作量和报价。 | 相关结论待内部确认。 |
| 资格与符合性 | 所有硬性资格和废标项已证明满足，无未关闭的重大缺口。 | 不得给出 Go。 |
| 商业与授权 | 报价、资金、回款、风险暴露和对外承诺均有必要依据与授权。 | 仅保留内部假设或触发 No-Go。 |
| 披露 | 正式报告由披露白名单独立生成，不含内部底价、能力弱项、竞品策略或未验证主张。 | 禁止对外交付。 |

任一关键门槛 `FAIL` 时，整套结果标记为 **草稿—需人工复核**，在内部报告顶部列出失败门槛、影响、责任人和关闭动作；披露门槛失败时不生成可发送的正式版。
