# 公司能力基线

## 元数据

- 状态：空模板，尚无可引用条目

## 可引用条目结构

实际数据保存在 `company_profile.entries`；当前保持空数组。新增条目时必须逐项填写稳定字段，不得以章节级更新时间或可信度代替条目级信息。

```yaml
company_profile:
  entries: []
company_profile_entry:
  id: null
  statement: null
  scope: null
  evidence: []
  updated_at: null
  owner: null
  confidence: null
  status: null
  review_due: null
```

- `id`：稳定且唯一的条目 ID；内容更新不得复用其他事实的 ID。
- `statement`：可引用的能力、边界、案例、工作量或商务基线陈述。
- `scope`：适用的产品、版本、行业、区域、交付方式及排除项。
- `evidence`：内部批准记录、验收材料或其他可核验依据的引用；不得写入客户文件正文。
- `updated_at`：条目最后核验日期，使用 `YYYY-MM-DD`。
- `owner`：对条目准确性和复核负责的角色或人员。
- `confidence`：仅使用 `high`、`medium` 或 `low`。
- `status`：仅使用 `verified`、`pending`、`retired`。
- `review_due`：最晚复核日期，使用 `YYYY-MM-DD`。

空白、未经核验或已过期的章节不得支持确定性结论；仅可作为待澄清信息，并明确其限制。整个文件或公司基线缺失时，不得给出确定性的能力匹配、报价和参与建议；应先标记为待补充或待澄清。

## 公司定位

待维护。

## 产品能力

待维护。

## 技术能力

待维护。

## 交付能力

待维护。

## 商务原则

待维护。

## 能力边界

待维护。

## L0-L3 判定基线

待维护。

## 历史案例

待维护。

## 工作量参考

待维护。

## 报价参考

待维护。
