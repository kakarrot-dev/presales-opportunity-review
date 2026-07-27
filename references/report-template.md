# 输出与双报告模板

以完整的 `project-analysis.yaml`、证据核验状态和策略决策为唯一分析输入。在 `outputs/<项目简称>-<日期>/` 下生成以下七个 Markdown 文件、一个结构化分析文件及两份单文件 HTML 报告：

- `00-material-index.md`
- `01-opportunity-review-internal.md`
- `02-opportunity-review-formal.md`
- `03-clarification-internal.md`
- `04-clarification-customer.md`
- `05-response-compliance-matrix.md`
- `06-evidence-register.md`
- `project-analysis.yaml`
- `01-opportunity-review-internal.html`
- `02-opportunity-review-formal.html`

所有结论必须追溯到材料、公司基线、已核验的 `evidence` 或明确的待确认事项；不得将缺失信息补写为事实。

两份 HTML 是对应 Markdown 报告的可阅读、可打印交付面，不是新的事实来源。HTML 必须使用 `templates/opportunity-review-report.html` 的单文件壳层，填充前已完成证据、质量门槛和披露检查的内容；不得由浏览器脚本执行证据筛选、隐藏内部内容或生成正式版。HTML 中的表格、状态、事实引用和结论必须与同名 Markdown 及 `project-analysis.yaml` 一致。

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

`02-opportunity-review-formal.md`、`02-opportunity-review-formal.html`、`04-clarification-customer.md` 和对甲方交付的响应片段只能使用披露白名单中的允许项。

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

## HTML 报告契约

### 生成顺序

1. 从 `project-analysis.yaml` 和证据台账独立组装内部报告内容。
2. 从披露白名单独立组装正式报告内容，不读取内部 HTML 后删除或隐藏节点。
3. 分别将两套内容填入 `templates/opportunity-review-report.html`，生成 `01-opportunity-review-internal.html` 与 `02-opportunity-review-formal.html`。
4. 对两份 HTML 做内容一致性、敏感信息、桌面、375px 和打印预览检查。

### 必填占位符

- `REPORT_VISIBILITY`
- `REPORT_VISIBILITY_LABEL`
- `REPORT_TITLE`
- `REPORT_SUBTITLE`
- `PROJECT_NAME`
- `CUSTOMER_NAME`
- `REPORT_DATE`
- `DELIVERY_STATUS`
- `DECISION_TITLE`
- `DECISION_NOTE`
- `DECISION_STATUS`
- `REPORT_TOC`
- `REPORT_SECTIONS`
- `REPORT_FOOTER`

所有占位符必须完成 HTML 转义；只有由生成器构造并经过允许元素校验的 `REPORT_TOC` 与 `REPORT_SECTIONS` 可以写入 HTML 片段。不得把用户原始文本直接拼接为标签、属性或脚本。

### 视觉与运行边界

- 色彩、字体、间距和圆角映射自 `/Users/kakarrot/Dev/claude-cream/tokens/tokens.json`；仓库模板保存所需值，运行时不得依赖该绝对路径。
- 使用原生 CSS 和少量原生 JavaScript，禁止外部字体、样式、脚本、图片及 CDN，确保离线打开。
- 页面提供跳至正文、明暗主题切换和打印入口；交互不得改变报告事实、证据状态或披露范围。
- 桌面端使用目录与正文布局；窄屏转为单列，表格允许横向滚动。
- 必须提供 `@media print`，打印时移除导航和操作控件，保留状态色与正文层级。
- 必须遵守 `prefers-reduced-motion`，所有按钮保留可见键盘焦点。
- HTML 页脚只说明报告状态和数据边界，不复制参考仓库的品牌、署名或社交链接。

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
