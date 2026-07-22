# 输出与双报告模板

以完整的 `project-analysis.yaml`、证据核验状态和策略决策为唯一分析输入。在 `outputs/<项目简称>-<日期>/` 下生成以下七个 Markdown 文件及一个结构化分析文件：

1. `00-material-index.md`
2. `01-opportunity-review-internal.md`
3. `02-opportunity-review-formal.md`
4. `03-clarification-internal.md`
5. `04-clarification-customer.md`
6. `05-response-compliance-matrix.md`
7. `06-evidence-register.md`
8. `project-analysis.yaml`

所有结论必须追溯到材料、公司基线、已核验的 `evidence` 或明确的待确认事项；不得将缺失信息补写为事实。

## 01-opportunity-review-internal.md

内部报告包含以下固定章节：

1. 决策摘要
2. 参与建议
3. 项目与采购包拆解
4. 能力匹配
5. 资格和废标风险
6. 评审路径
7. 隐藏工作量
8. 人天和报价区间
9. 商业模式和资金风险
10. 竞品生态
11. 投标及谈判策略
12. 禁止承诺
13. 退出条件
14. 内部待确认事项
15. 行动时间表
16. 证据说明

## 02-opportunity-review-formal.md

正式报告包含以下固定章节：

1. 项目理解
2. 建设目标
3. 需求和采购包分析
4. 建议技术与实施边界
5. 关键依赖
6. 工作量和周期
7. 风险及前置条件
8. 正式澄清事项
9. 服务与验收关注点
10. 结论和后续建议

## 正式报告白名单

`02-opportunity-review-formal.md`、`04-clarification-customer.md` 和对甲方交付的响应片段只能使用白名单中的内容：采购材料直接支持的项目事实、已核验的能力与证据、明确标注的方案边界、正式澄清问题、风险及前置条件、经批准的工作量和周期表述，以及已批准的结论和后续建议。

正式版严禁包含：内部底价、能力弱项、竞品策略、未经验证的主张、仅供内部审批的条件、原始推理笔记。无法进入白名单的内容只保留在内部报告或内部待确认清单中。

## 05-response-compliance-matrix.md

合规矩阵至少包含：需求编号、原始要求和出处、响应结论、证据引用、责任人、状态。`响应结论` 必须区分直接满足、配置满足、合作满足、不建议承诺和待确认；不得将待确认或无法验证事项标为已满足。

## 06-evidence-register.md

证据登记表逐条保留 `id`、`claim`、`source`、`location`、`url`、`source_date`、`accessed_at`、`verification_status`、`independent_sources`、`contradictions` 和 `confidence`。`verification_status` 使用：已由一手来源确认、已交叉验证、单一来源待验证、来源冲突、无法验证。单一来源待验证、来源冲突和无法验证不得写成正式报告的确定性事实。
