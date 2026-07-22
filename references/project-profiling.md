# 项目归一化

将 `material-classification.md` 输出的材料记录按其 `content_regions`、`status`、`parse_confidence`、`provenance` 和 `errors` 归一为一个 `project-analysis.yaml`。只记录材料直接支持的事实；冲突、缺失和解析失败必须保留，不得用推测补全。

```yaml
project: {name: null, customer: null, industry: null, procurement_type: null, funding_model: null, current_stage: null, budget: null, delivery_scope: null, timeline: null}
materials: {provided: [], missing: [], parse_failures: [], conflicts: [], confidence: null}
procurement: {lots: [], joint_bid_policy: null, subcontract_policy: null, pricing_direction: null, quotation_rounds: [], evaluation_method: null, award_conditions: [], rule_conflicts: []}
packages: []
competitors: {direct: [], substitutes: [], partners: []}
bid: {qualification_items: [], compliance_items: [], rejection_risks: [], scoring_items: [], estimated_score: null}
strategy: {recommendation: null, participation_mode: null, conditions: [], exit_conditions: [], prohibited_commitments: [], pricing: null, negotiation: null, clarification_questions: []}
evidence: []
```

## 填充规则

- `project` 归集项目名称、客户、行业、采购类型、资金来源、阶段、预算、交付范围和时间线；无法确认则保持 `null`。
- `materials` 以材料记录为准：成功输入进入 `provided`，缺件进入 `missing`，不可解析材料进入 `parse_failures`，互相矛盾的说法进入 `conflicts`；`confidence` 反映可用材料的总体可信度。
- `procurement` 由采购文件中的标段、联合体、分包、报价、轮次、评审、授标和规则冲突字段填充；具体解释遵循 `procurement-mechanism.md`。
- `packages` 每项对应一个可独立报价或授标的标段/包件，保留范围、预算、资格、报价和评审约束。
- `competitors` 只记录有材料证据的直接竞争者、替代方案和潜在合作伙伴；未知不等于无竞争。
- `bid` 逐项列出资格、符合性、废标风险和评分要求；无评分表时 `scoring_items` 为空且 `estimated_score` 为 `null`。
- `strategy` 的参与、报价和谈判建议必须受公司能力基线及采购规则约束；证据不足时转为 `clarification_questions` 或退出条件。
- `evidence` 对每一项可追溯结论记录材料 `id`、`path`、位置/页码、摘录和可信度；规则冲突同时写入 `procurement.rule_conflicts`。
