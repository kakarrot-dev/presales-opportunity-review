# Material classification

将每份用户提供的异构材料及补充说明标准化为独立记录。先枚举文件、工作表、页面、附件和内容区域；再记录可解析范围、来源和异常，不把推测当作原始事实。

```yaml
material:
  id: M001
  path: original user-provided path or attachment name
  format: xlsx|docx|pdf|markdown|image|other
  content_regions: []
  status: parsed|partial|unreadable|empty
  parse_confidence: high|medium|low
  provenance: []
  errors: []
```

## 分类与提取规则

1. 枚举每个文件、工作表、页面、附件和识别出的区域；空白工作表必须单独标记，不得默认为无效材料。
2. 按语义识别标题、表头、明细、分组、合计和备注区域，而不是只依赖固定行列位置。
3. 合并单元格或空白分组标签仅可在紧邻且语义连续的范围内有限回填；无法确认时保留为空并记录错误或不确定性。
4. 保留原始数量文本，同时提取可计算的数值和单位，避免将原始表达改写为单一数值。
5. 将长单元格拆分为可单独判断的原子需求，并保留其原始区域和出处。
6. 显式识别并保留 `利旧`、`包含在报价内`、`原厂授权`、`实质性响应` 等采购与响应约束，不将其降级为普通备注。
