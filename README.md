# Presales Opportunity Review

商机售前审查 Skill：把异构招标/采购材料转成可追溯的参与决策、双版本报告和澄清清单。

## 做什么

给定招标文件、竞争性谈判材料、采购清单、技术需求、评分办法、预算/报价表或商机说明，按固定 19 阶段流程输出：

- 内部直白版审查报告
- 正式对外版报告（独立生成，不靠删减内部版）
- 内部待确认清单 + 甲方正式澄清清单
- 响应合规矩阵与证据台账
- `project-analysis.yaml` 结构化分析对象

核心原则：**不推测补全缺失信息**；关键质量门槛未过时，整套结果保持「草稿—需人工复核」。

## 不做什么

- 合同逐条法务审查或法律意见
- 自动生成完整投标文件
- 中标后的项目管理 / 验收编制
- 未经授权的正式报价

## 仓库结构

```text
SKILL.md                 # 触发条件与 19 阶段编排（薄入口）
knowledge/
  company-profile.md     # 公司能力/商务基线（可编辑，条目级可信度）
references/              # 各阶段规则契约（一文件一决策边界）
examples/                # 虚构样例输入与期望输出形态
tests/                   # 包结构与契约静态校验
docs/superpowers/        # 设计规格与实现计划
```

`SKILL.md` 只编排；细则在 `references/`。改规则时优先改对应 reference，避免把细则复制进 `SKILL.md`。

## 怎么用

1. 维护 `knowledge/company-profile.md`：每条能力/案例/报价参考必须有稳定 `id`、`updated_at`、`status`、`confidence`、`review_due` 等字段；空基线或过期条目会阻断确定性 Go / 报价结论。
2. 在支持 Skill 的 Agent（Codex / Cursor 等）中启用本仓库的 `presales-opportunity-review`。
3. 提供商机材料（Excel / Word / PDF / Markdown / 图片 / 多文件均可），说明分析目标、截止时间、输出路径和是否禁止外部调查。
4. 产物默认落在 `outputs/<项目简称>-<日期>/`：

| 文件 | 用途 |
| --- | --- |
| `00-material-index.md` | 材料索引与降级记录 |
| `01-opportunity-review-internal.md` | 内部审查报告 |
| `02-opportunity-review-formal.md` | 正式对外报告 |
| `03-clarification-internal.md` | 内部待确认 |
| `04-clarification-customer.md` | 甲方澄清 |
| `05-response-compliance-matrix.md` | 响应合规矩阵 |
| `06-evidence-register.md` | 证据台账 |
| `project-analysis.yaml` | 统一分析对象 |

## 校验

包契约由标准库 Python 校验，无需第三方依赖：

```bash
PYTHONPATH=tests python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 tests/check_skill_package.py .
```

期望：全部测试通过；CLI 输出 `skill package valid`。

## 样例

- 输入约定：`examples/sample-input.md`（虚构大学场景，含冲突条款、循环转载、OCR/多格式定位）
- 输出形态：`examples/sample-report.md`

**不要**把真实客户招标原件提交进仓库。

## 设计文档

- 规格：`docs/superpowers/specs/2026-07-22-presales-opportunity-review-design.md`
- 计划：`docs/superpowers/plans/2026-07-22-presales-opportunity-review.md`
