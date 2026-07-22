# 采购机制路由

从材料中识别 `procurement_type`（如公开招标、邀请招标、竞争性谈判、询比/比选、单一来源）和 `funding_model`（财政预算、自筹、融资、专项资金或未知）。采购类型仅用于决定应核查的程序和文件，不能替代文件中明示的规则。

## 规则优先级

同一事项存在冲突时，以更高优先级为准，并将原始冲突写入 `procurement.rule_conflicts`：

```text
latest clarification/modification
> supplier instructions schedule
> special terms
> procurement requirements
> general terms
> response template
```

其中 `supplier instructions schedule` 对应采购文件中的“供应商须知前附表”。未能判断版本或发布日期时，不自行裁决，转为澄清问题。

## 路由字段

- `lots`：按标段/包件拆分范围、预算、交付地点、资格、报价口径与独立授标规则；未明确时保留空列表而非默认单一标段。
- `joint_bid_policy`：记录联合体是否允许、牵头方/成员资格、责任分配、份额和授权要求；未授权不得建议联合投标。
- `subcontract_policy`：记录分包是否允许、可分包范围、比例、审批和责任；禁止分包或未明确时，不将分包写入承诺。
- `pricing_direction`：记录总价/单价/费率、含税与币种、最高限价、暂估量、调价、价格分及报价响应方式。不得假定低价中标。
- `quotation_rounds`：记录一次性报价、二次/多轮报价、谈判报价、澄清和截止时间；没有明示轮次时不虚构轮次。
- `evaluation_method`：记录最低评标价法、综合评分法、资格后审等实际方法和评分表。不得假定每个机会都有评分表。
- `award_conditions`：记录授标前提、资格复核、保证金、履约保证、签约、验收及资金落实条件。

## 保证与授标后谈判

逐项核查投标保证金、履约保证金、保函格式、金额/比例、有效期、递交方式、退还/没收条件，并列入 `bid.compliance_items` 或 `bid.rejection_risks`。对于 `post-award negotiation`，仅在文件明确允许时记录可谈事项、边界与审批条件；不得把中标后谈判当作可改变报价、范围、资格或实质条款的默认机制。

## 决策边界

资金来源决定回款、付款节点、资金落实和担保风险的核查重点；它不自动决定报价或参与结论。缺少采购方式、标段、评审、条款或保证要求时，输出澄清问题和条件，不做确定性参与、报价或中标判断。
