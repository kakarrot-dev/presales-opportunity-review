# 证据记录与结论边界

每条可用于分析的事实或外部主张均以独立记录保存，避免把搜索线索、客户材料和已核验事实混为一谈。

```yaml
evidence:
  id: E001
  claim: 可独立核验的主张
  source: 来源主体或材料名称
  location: 页码、段落、公告编号或定位说明
  url: null
  source_date: null
  accessed_at: null
  verification_status: 单一来源待验证
  independent_sources: []
  contradictions: []
  confidence: low
```

`verification_status` 只能使用以下状态：

- 已由一手来源确认
- 已交叉验证
- 单一来源待验证
- 来源冲突
- 无法验证

`independent_sources` 只列彼此独立的来源；转引、转载或共同源自同一公告的材料只记录一次。`contradictions` 保留不一致的主张、来源和差异，不能删除较弱的一方来制造一致性。`confidence` 反映证据质量和完整性，不替代 `verification_status`。

单一来源待验证、来源冲突和无法验证不能作为正式报告的确定性事实；它们只能驱动澄清、风险提示或后续核验。只有已由一手来源确认或已交叉验证的记录，才可在符合时效性和适用范围前提下作为正式结论的事实依据。
