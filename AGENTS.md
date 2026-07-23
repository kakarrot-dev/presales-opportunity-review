# AGENTS.md

本仓库是 **Codex/Cursor Skill 包**，不是可运行应用。改动以 Markdown 规则契约 + Python 静态校验为主。

## 项目心智模型

| 层 | 职责 | 禁止 |
| --- | --- | --- |
| `SKILL.md` | 触发条件、19 阶段顺序、降级与质量门槛总览 | 复制各阶段字段细则 |
| `references/*.md` | 单一决策边界的完整契约 | 一个文件塞多个无关阶段 |
| `knowledge/company-profile.md` | 可引用公司基线条目 | 用章节级元数据冒充条目级核验 |
| `examples/` | 虚构样例，锁定行为期望 | 写入真实客户材料 |
| `tests/` | 包结构与跨模块契约 | 依赖第三方库；提交客户文档 |

执行 Skill 时严格按 `SKILL.md` 的 19 阶段顺序；后续阶段不得改写上游事实或证据状态。

## 动手前必读

- 改编排 → `SKILL.md` + 对应 `references/`
- 改输出形态/披露 → `references/report-template.md`
- 改证据/外调 → `references/evidence-rules.md`、`references/research-rules.md`
- 改能力匹配门槛 → `references/capability-matching.md` + `knowledge/company-profile.md`
- 设计背景 → `docs/superpowers/specs/`、`docs/superpowers/plans/`（实现时以现网契约与测试为准）

## 硬约束（违反即错误）

1. **单一入口**：不要拆成多个可调用 Skill。
2. **不推测补全**：缺失、冲突、不可读一律保留并降级，不静默选边。
3. **证据**：搜索摘要不是事实；循环转载只计一个来源；仅 `已由一手来源确认` / `已交叉验证` 可支撑正式确定事实。
4. **公司基线**：无有效条目 ID、过期或缺失时，`company_match` → `待内部确认`，`strategy.recommendation` → `Insufficient Information`。
5. **双报告**：正式版必须按披露白名单**独立生成**，禁止「删减内部版」。
6. **不产出**：法律意见、完整标书、未授权正式报价、中标后项目管理文档。
7. **不入库**：真实客户招标原件、密钥、客户正文证据粘贴进 `knowledge/`。

## 字段与定位契约

归一化对象与 provenance 以 `references/project-profiling.md`、`references/material-classification.md` 及测试中的 token 为准。常见格式定位：

- XLSX：`path` / `sheet` / `cell_or_range`
- DOCX：`path` / `heading` / `table_row`（不适用时显式 `null`）
- PDF：`path` / `page` / `region`（不得用降级文本行号冒充页码）
- OCR：`path` / `page` / `bbox` / `ocr_confidence`

跨文件接口使用契约中的**精确字段名**；不要发明同义字段。

## 修改工作流（TDD）

1. 先改/加 `tests/` 中会失败的断言或夹具。
2. 跑测试，确认失败原因符合预期。
3. 用最小 diff 改 `references/` 或 `SKILL.md` / `knowledge/`。
4. 再跑测试至全绿，并跑包校验 CLI。

```bash
PYTHONPATH=tests python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 tests/check_skill_package.py .
```

完成标准：上述两条均成功；`check_skill_package.py` 输出 `skill package valid`。

## 编辑风格

- 最小改动：只动当前任务相关文件；不顺手重构相邻规则。
- 中文写规则与说明；代码标识符、字段名、命令保持英文原样。
- 新增 reference 时同步：`SKILL.md` 规则索引、`tests/check_skill_package.py` 的 `REQUIRED_FILES`、单元测试期望。
- 更新样例时保持 `examples/sample-input.md` 与 `examples/sample-report.md` 一致，并覆盖关键质量门槛场景。

## 输出目录约定

分析运行产物写入 `outputs/<项目简称>-<日期>/`（见 `references/report-template.md`）。仓库内通常不提交真实运行产物；若添加演示输出，必须为虚构内容。
