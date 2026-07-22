# 输出与双报告模板

以完整的 `project-analysis.yaml`、证据核验状态和策略决策为唯一分析输入。在 `outputs/<项目简称>-<日期>/` 下生成以下七个 Markdown 文件及一个结构化分析文件：

- `00-material-index.md`
- `01-opportunity-review-internal.md`
- `02-opportunity-review-formal.md`
- `03-clarification-internal.md`
- `04-clarification-customer.md`
- `05-response-compliance-matrix.md`
- `06-evidence-register.md`
- `project-analysis.yaml`

所有结论必须追溯到材料、公司基线、已核验的 `evidence` 或明确的待确认事项；不得将缺失信息补写为事实。

## 01-opportunity-review-internal.md

内部报告包含以下固定章节：

- 决策摘要
- 参与建议
- 项目与采购包拆解
- 能力匹配
- 资格和废标风险
- 评审路径
- 隐藏工作量
- 人天和报价区间
- 商业模式和资金风险
- 竞品生态
- 投标及谈判策略
- 禁止承诺
- 退出条件
- 内部待确认事项
- 行动时间表
- 证据说明

## 02-opportunity-review-formal.md

正式报告包含以下固定章节：

- 项目理解
- 建设目标
- 需求和采购包分析
- 建议技术与实施边界
- 关键依赖
- 工作量和周期
- 风险及前置条件
- 正式澄清事项
- 服务与验收关注点
- 结论和后续建议

## 正式报告白名单

`02-opportunity-review-formal.md`、`04-clarification-customer.md` 和对甲方交付的响应片段只能使用披露白名单中的允许项。

### 正式版允许项

- 采购材料直接支持的项目事实
- 已核验的能力与证据
- 明确标注的方案边界
- 正式澄清问题
- 风险及前置条件
- 经批准的工作量和周期表述
- 已批准的结论和后续建议

正式版必须从披露白名单独立生成，不得通过对内部版删减或删除敏感段落生成。

正式版严禁包含以下内容：

### 正式版严禁项

- 内部底价
- 能力弱项
- 竞品策略
- 未经验证的主张
- 仅供内部审批的条件
- 原始推理笔记

无法进入白名单的内容只保留在内部报告或内部待确认清单中。

## 05-response-compliance-matrix.md

### 字段

- 要求
- 类型
- 原文位置
- 响应材料
- 当前状态
- 后果
- 责任人

### 要求类型

- 主体与信用资格
- 人员和案例证明
- 保证金
- 有效期
- 时间节点
- 签章装订
- 报价
- 技术响应
- 原厂证明
- 接口
- 安全
- 交付
- 验收
- 联合体
- 分包
- 关联关系限制

`当前状态` 必须区分直接满足、配置满足、合作满足、不建议承诺和待确认；不得将待确认或无法验证事项标为已满足。

## 06-evidence-register.md

### 字段

- `id`
- `claim`
- `source`
- `location`
- `url`
- `source_date`
- `accessed_at`
- `verification_status`
- `independent_sources`
- `contradictions`
- `confidence`

来自用户材料的证据在 `location` 保存 `source_fact_id`，并回溯 `project-analysis.yaml` 的 `materials.source_facts[].provenance`。XLSX、DOCX、PDF 与图片/OCR 分别保持自己的定位字段，不得将自由文本行号伪装为 PDF 页码。

### verification_status

- 已由一手来源确认
- 已交叉验证
- 单一来源待验证
- 来源冲突
- 无法验证

单一来源待验证、来源冲突和无法验证不得写成正式报告的确定性事实。
