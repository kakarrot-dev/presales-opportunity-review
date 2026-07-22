# 虚构大学商机分析样例

> 状态：**草稿—需人工复核**。本报告纯属虚构，不对应任何真实学校、客户、供应商、网址或参数。

## 材料索引

| id | path | format | content_regions | status | parse_confidence | provenance | errors |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M001 | 虚构采购清单.xlsx | xlsx | 采购清单、备用页 | partial | medium | F001 | 含两个工作表，见子记录 |
| M001-S01 | 虚构采购清单.xlsx#采购清单 | xlsx | 标题、第 3 行表头、分组明细 | partial | medium | F001 | 合并分组与混合单位已保留；利旧边界未知 |
| M001-S02 | 虚构采购清单.xlsx#备用页 | xlsx | 无 | empty | high | 无提取事实 | 空白工作表，已单独保留 |
| M002 | 虚构采购条款.md | markdown | 评审、资格、垫资 | parsed | high | F005 | 最低价与最高报价规则冲突 |
| M003 | 虚构网页文章甲摘录 | markdown | 项目启动主张 | partial | low | F006 | 与 M004 不构成独立来源 |
| M004 | 虚构网页文章乙摘录 | markdown | 项目启动主张 | partial | low | F007 | 与 M003 不构成独立来源 |
| M005 | 虚构技术需求书.docx | docx | 3.2 接口要求 | parsed | high | F002 | 正文段落，不适用表格行 |
| M006 | 虚构评分办法.pdf | pdf | 第 6 页表 2 | parsed | high | F003 | 保留真实 PDF 页码与页面区域 |
| M007 | 虚构授权要求扫描件.png | image | 第 1 页授权要求 | partial | medium | F004 | OCR 结果保留坐标与置信度 |

## 结构化来源事实

以下对象进入 `project-analysis.yaml` 的 `materials.source_facts`；材料、原子需求和材料证据均通过 `source_fact_id` 引用，不能把定位降级为自由文本。

```json
{
  "source_facts": [
    {"id": "F001", "statement": "采购清单中的旧设备接入数量标记为利旧", "source_format": "xlsx", "provenance": {"path": "虚构采购清单.xlsx", "sheet": "采购清单", "cell_or_range": "A8:H8"}},
    {"id": "F002", "statement": "技术需求书提出接口对接要求", "source_format": "docx", "provenance": {"path": "虚构技术需求书.docx", "heading": "3.2 接口要求", "table_row": null}},
    {"id": "F003", "statement": "评分办法要求提供原厂授权", "source_format": "pdf", "provenance": {"path": "虚构评分办法.pdf", "region": "表 2 资格要求", "page": 6}},
    {"id": "F004", "statement": "扫描件包含原厂授权要求", "source_format": "image", "provenance": {"path": "虚构授权要求扫描件.png", "page": 1, "bbox": [120, 240, 1600, 620], "ocr_confidence": 0.96}},
    {"id": "F005", "statement": "采购条款同时出现最低价和最高报价排序", "source_format": "markdown", "provenance": {"path": "虚构采购条款.md", "heading": "报价条款", "line_or_range": "条款 A-B"}},
    {"id": "F006", "statement": "行业媒体甲称项目已启动", "source_format": "markdown", "provenance": {"path": "虚构网页文章甲摘录", "heading": "正文", "line_or_range": "第 1 段"}},
    {"id": "F007", "statement": "行业媒体乙称项目已启动", "source_format": "markdown", "provenance": {"path": "虚构网页文章乙摘录", "heading": "正文", "line_or_range": "第 1 段"}}
  ]
}
```

## 采购机制

- `funding_model`：供应商垫资；还款来源、运营期限、资产归属和验收前现金暴露待澄清。
- `evaluation_method`：未明确。同版本同时规定最低价与最高报价排序，写入 `procurement.rule_conflicts`。
- `award_conditions`：投标时必须具备原厂授权，不得假定中标后补正。

## 原子需求

| 字段 | 内容 |
| --- | --- |
| id | PKG1-R01 |
| 原始要求和出处 | 原文为“利旧”；`source_fact_id`: F001 |
| provenance | `{"path":"虚构采购清单.xlsx","sheet":"采购清单","cell_or_range":"A8:H8"}` |
| deliverable（交付物） | 完成已有设备接入并提交可验收的接入记录 |
| dependencies（依赖） | 旧设备清单、接口文档、现场访问、责任边界 |
| acceptance_criteria（验收） | 待甲方书面明确可观察指标和通过条件 |
| hidden_work（隐含工作） | 设备盘点、接口适配、联调、测试、现场服务 |
| company_match（能力匹配） | `待内部确认`；`company_profile_entry_ids`: []；现有公司基线无有效条目，不支持 L0-L2 当前结论 |
| complexity（复杂度） | 高；利旧对象与接口未知 |
| effort（工作量） | 三点区间待内部基线和现场盘点后补充 |
| risk（风险） | 合作方授权或旧设备接口不可用时无法交付 |
| clarification_question（澄清） | 请提供利旧设备清单、接口文档与验收标准 |

## 当前能力与策略结论

- `company_match`: `待内部确认`。公司基线过期，当前不能形成 L0-L2 能力结论。
- `strategy.recommendation`: `Insufficient Information`。原厂授权、垫资边界、评审排序与公司基线均未关闭。

## 合规风险

- 原厂授权是硬性资格；当前无已核验授权，存在无效响应风险。
- 最低/最高报价排序冲突将改变定价策略，不得在澄清前假设任一评审路径。
- 垫资项目的还款来源与最坏情景损失未知，商业门槛不通过。

## 证据登记摘要

| id | claim | source | location | url | source_date | accessed_at | verification_status | independent_sources | contradictions | confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E001 | 评审按最低价排序 | M002 | F005 | null | 虚构日期 | 虚构日期 | 来源冲突 | M002 | 报价条款 B 规定最高报价排序 | low |
| E002 | 项目已启动 | 示例行业媒体甲 | F006 | null | 虚构日期 | 虚构日期 | 单一来源待验证 | 虚构采购方新闻稿 | 无 | low |
| E003 | 项目已启动 | 示例行业媒体乙 | F007 | null | 虚构日期 | 虚构日期 | 单一来源待验证 | 虚构采购方新闻稿 | 无 | low |
| E004 | 采购清单包含一项标记为“利旧”的旧设备接入要求 | M001-S01 | F001 | null | 虚构日期 | 虚构日期 | 已由一手来源确认 | M001-S01 | 无 | high |

E002 和 E003 是转载/聚合关系，两条 syndication 记录共享同一一手来源，只计一个独立来源。

## 条件分支（非当前结论）

本分支为**非当前结论**。仅在**基线更新且合作方验证后**，才可按下列条件重新评估：

- `company_match` 条件分支：仅在基线负责人创建并批准可引用的 `company_profile_entry_ids` 后，才可评估为 `L2 合作满足`；同时要求原厂/合作方的授权、供货和交付责任已验证。
- `strategy.recommendation` 条件分支：`Conditional Go`，还必须在投标截止前书面澄清排序规则，并获得垫资模式和最坏情景损失审批。
- 退出条件：原厂授权无法按时取得，或垫资风险超出内部授权。

## 内部待确认清单

| priority | question | current_judgment | impact | owner | deadline |
| --- | --- | --- | --- | --- | --- |
| P0 | 是否有可用的原厂授权路径？ | 未验证 | 决定资格与参与建议 | 生态合作责任角色 | 投标截止前 |
| P0 | 是否批准垫资及最坏损失上限？ | 不批准前不可承诺 | 决定商业模式和退出条件 | 商务审批责任角色 | 报价前 |

## 甲方正式澄清清单

| topic | formal_question | reason | response_format | timing |
| --- | --- | --- | --- | --- |
| 评审排序 | 请明确有效报价按最低价还是最高报价排序。 | 同版本条款冲突 | 书面澄清文件 | 投标前必须确认 |
| 利旧范围 | 请提供利旧设备清单、接口文档和验收标准。 | 决定交付范围与验收 | 书面清单及附件 | 投标前必须确认 |

## 仅限内部的报价假设

- 任何三点报价均依赖利旧盘点、合作方成本、垫资期间、回款来源和最坏情景损失。
- 由于公司工作量及报价基线过期，样例不生成金额，不得将本节复制到对外材料。

## 正式报告摘录

### 项目理解

采购清单包含一项标记为“利旧”的旧设备接入要求 [E004]。现有材料尚未定义利旧设备范围、接口责任和验收标准。

### 风险及前置条件

建议在响应前以书面形式明确评审排序规则、利旧设备清单和验收标准，并按采购文件要求提供可核验的原厂授权。

### 结论和后续建议

建议在上述前置条件书面关闭后，再确定可响应范围和对外输出。

## 质量门槛

| 门槛 | 状态 | 证据/失败原因 | 责任人 | 关闭动作 |
| --- | --- | --- | --- | --- |
| 材料完整性 | FAIL | 利旧范围与验收条件缺失 | 售前负责人 | 甲方书面澄清 |
| 事实与证据 | FAIL | 存在来源冲突和同源转载 | 调研负责人 | 取得优先级更高的文件及原始一手来源 |
| 公司基线 | FAIL | 能力、工作量和报价基线过期 | 公司基线负责人 | 更新并批准基线 |
| 资格与符合性 | FAIL | 原厂授权未验证 | 生态合作负责人 | 投标截止前取得授权原件 |
| 商业与授权 | FAIL | 垫资和最坏情景损失未审批 | 商务审批负责人 | 商务审批 |
| 披露 | PASS | 正式摘录从白名单允许项独立生成 | 报告审核负责人 | 交付前复核 |
