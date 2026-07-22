import tempfile
import unittest
from pathlib import Path

from check_skill_package import validate_package


PROJECT_SCHEMA = """```yaml
project:
  name: null
  customer: null
  industry: null
  procurement_type: null
  funding_model: null
  current_stage: null
  budget: null
  delivery_scope: null
  timeline: null
materials:
  provided: []
  missing: []
  parse_failures: []
  conflicts: []
  confidence: null
procurement:
  lots: []
  joint_bid_policy: null
  subcontract_policy: null
  pricing_direction: null
  quotation_rounds: []
  evaluation_method: null
  award_conditions: []
  rule_conflicts: []
packages: []
competitors:
  direct: []
  substitutes: []
  partners: []
bid:
  qualification_items: []
  compliance_items: []
  rejection_risks: []
  scoring_items: []
  estimated_score: null
strategy:
  recommendation: null
  participation_mode: null
  conditions: []
  exit_conditions: []
  prohibited_commitments: []
  pricing: null
  negotiation: null
  clarification_questions: []
evidence: []
```"""

EVIDENCE_FIELDS = {
    "id",
    "claim",
    "source",
    "location",
    "url",
    "source_date",
    "accessed_at",
    "verification_status",
    "independent_sources",
    "contradictions",
    "confidence",
}


def fixture_records(path: Path) -> tuple[list[dict[str, str | list[str]]], str]:
    records: list[dict[str, str | list[str]]] = []
    current: dict[str, str | list[str]] | None = None
    expected_status = ""
    list_key: str | None = None

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("  - id:"):
            current = {"id": line.split(":", 1)[1].strip().strip('"')}
            records.append(current)
            list_key = None
        elif current is not None and line.startswith("    ") and ":" in line:
            key, value = line.strip().split(":", 1)
            if key in current:
                raise ValueError(f"duplicate fixture field: {key}")
            current[key] = [] if value.strip() in ("", "[]") else value.strip().strip('"')
            list_key = key if not value.strip() else None
        elif current is not None and list_key and line.startswith("      - "):
            values = current[list_key]
            assert isinstance(values, list)
            values.append(line.removeprefix("      - ").strip().strip('"'))
        elif line.startswith("expected_status:"):
            expected_status = line.split(":", 1)[1].strip().strip('"')

    return records, expected_status


class SkillPackageTests(unittest.TestCase):
    def test_output_rules_require_two_clarification_sets_and_disclosure_allowlist(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            references = root / "references"
            references.mkdir(parents=True)
            (references / "clarification-questions.md").write_text("# Clarifications\n", encoding="utf-8")
            (references / "report-template.md").write_text("# Reports\n", encoding="utf-8")

            errors = validate_package(root)

            self.assertIn("clarification rules missing token: 内部待确认清单", errors)
            self.assertIn("clarification rules missing token: 甲方正式澄清清单", errors)
            self.assertIn("report rules missing token: 05-response-compliance-matrix.md", errors)
            self.assertIn("report rules missing token: 白名单", errors)

    def test_current_package_has_no_capability_definition_errors(self) -> None:
        root = Path(__file__).resolve().parents[1]

        errors = validate_package(root)

        self.assertNotIn("capability rules invalid definition: L1 配置满足", errors)
        self.assertNotIn("capability rules invalid definition: L3 不建议承诺", errors)

    def test_evaluation_routes_without_assuming_scoring_and_strategy_has_guardrails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            references = root / "references"
            references.mkdir(parents=True)
            (references / "evaluation-analysis.md").write_text("# Evaluation\n", encoding="utf-8")
            (references / "opportunity-strategy.md").write_text("# Strategy\n", encoding="utf-8")

            errors = validate_package(root)

            self.assertIn("evaluation rules missing token: 最高投入或最高报价排序", errors)
            self.assertIn("evaluation rules missing token: 只有存在明确分值时", errors)
            self.assertIn("strategy rules missing token: Insufficient Information", errors)
            self.assertIn("strategy rules missing token: prohibited_commitments", errors)

    def test_requirement_rules_reject_tokens_deleted_only_from_required_sections(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "references" / "requirement-analysis.md"
            target.parent.mkdir(parents=True)
            source = (Path(__file__).resolve().parents[1] / "references" / "requirement-analysis.md").read_text(encoding="utf-8")
            before, heading, remainder = source.partition("## 原子需求记录")
            section, next_heading, after = remainder.partition("## 拆分方法")
            target.write_text(before + heading + section.replace("数据", "已删除") + next_heading + after, encoding="utf-8")

            errors = validate_package(root)

            self.assertIn("requirement rules missing 原子需求记录 token: 数据", errors)

    def test_capability_rules_require_missing_evidence_fallback_relationship(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "references" / "capability-matching.md"
            target.parent.mkdir(parents=True)
            source = (Path(__file__).resolve().parents[1] / "references" / "capability-matching.md").read_text(encoding="utf-8")
            target.write_text(
                source.replace("公司基线为空白、过期、无法定位，或没有覆盖该能力时，输出 `待内部确认`", "公司基线缺少时需要补充"),
                encoding="utf-8",
            )

            errors = validate_package(root)

            self.assertIn("capability rules missing evidence fallback relationship", errors)

    def test_capability_rules_require_missing_profile_citation_fallback_relationship(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "references" / "capability-matching.md"
            target.parent.mkdir(parents=True)
            source = (Path(__file__).resolve().parents[1] / "references" / "capability-matching.md").read_text(encoding="utf-8")
            target.write_text(
                source.replace("任何 L0-L2 结论若缺少公司-profile citation，均降级为 `待内部确认`；", ""),
                encoding="utf-8",
            )

            errors = validate_package(root)

            self.assertIn("capability rules missing evidence fallback relationship", errors)

    def test_analysis_rule_contracts_reject_missing_or_swapped_guards(self) -> None:
        source_root = Path(__file__).resolve().parents[1]
        cases = (
            ("requirement-analysis.md", "requirement rules", "原始要求和出处"),
            ("requirement-analysis.md", "requirement rules", "交付物"),
            ("requirement-analysis.md", "requirement rules", "依赖"),
            ("requirement-analysis.md", "requirement rules", "验收"),
            ("requirement-analysis.md", "requirement rules", "隐含工作"),
            ("requirement-analysis.md", "requirement rules", "能力匹配"),
            ("requirement-analysis.md", "requirement rules", "复杂度"),
            ("requirement-analysis.md", "requirement rules", "工作量"),
            ("requirement-analysis.md", "requirement rules", "风险"),
            ("requirement-analysis.md", "requirement rules", "澄清"),
            ("requirement-analysis.md", "requirement rules", "数据"),
            ("requirement-analysis.md", "requirement rules", "接口"),
            ("requirement-analysis.md", "requirement rules", "部署"),
            ("requirement-analysis.md", "requirement rules", "迁移"),
            ("requirement-analysis.md", "requirement rules", "定制"),
            ("requirement-analysis.md", "requirement rules", "测试"),
            ("requirement-analysis.md", "requirement rules", "培训"),
            ("requirement-analysis.md", "requirement rules", "现场服务"),
            ("requirement-analysis.md", "requirement rules", "质保"),
            ("requirement-analysis.md", "requirement rules", "验收"),
            ("capability-matching.md", "capability rules", "L0 直接满足"),
            ("capability-matching.md", "capability rules", "L1 配置满足"),
            ("capability-matching.md", "capability rules", "L2 合作满足"),
            ("capability-matching.md", "capability rules", "L3 不建议承诺"),
            ("capability-matching.md", "capability rules", "待内部确认"),
            ("effort-estimation.md", "effort rules", "未经用户/公司授权不得生成最终或正式报价"),
            ("effort-estimation.md", "effort rules", "投资"),
            ("effort-estimation.md", "effort rules", "还款来源"),
            ("effort-estimation.md", "effort rules", "运营期限"),
            ("effort-estimation.md", "effort rules", "资产归属"),
            ("effort-estimation.md", "effort rules", "验收前现金暴露"),
            ("effort-estimation.md", "effort rules", "最坏情景损失"),
        )

        for filename, label, token in cases:
            with self.subTest(filename=filename, token=token), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                target = root / "references" / filename
                target.parent.mkdir(parents=True)
                source = source_root / "references" / filename
                target.write_text(
                    source.read_text(encoding="utf-8").replace(token, "已删除"),
                    encoding="utf-8",
                )

                errors = validate_package(root)

                self.assertIn(f"{label} missing token: {token}", errors)

    def test_capability_rules_reject_swapped_level_definition(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "references" / "capability-matching.md"
            target.parent.mkdir(parents=True)
            source = Path(__file__).resolve().parents[1] / "references" / "capability-matching.md"
            target.write_text(
                source.read_text(encoding="utf-8").replace(
                    "现有产品、技术或交付能力可在约定范围内直接满足",
                    "需要已识别合作方、外部产品或外部服务",
                    1,
                ),
                encoding="utf-8",
            )

            errors = validate_package(root)

            self.assertIn("capability rules invalid definition: L0 直接满足", errors)

    def test_estimation_rules_reject_missing_three_point_assumptions(self) -> None:
        source_root = Path(__file__).resolve().parents[1]
        cases = (
            ("## 三点工作量", "乐观"),
            ("## 三点工作量", "基准"),
            ("## 三点工作量", "保守"),
            ("## 三点工作量", "假设"),
            ("## 三点工作量", "人数"),
            ("## 三点工作量", "周期"),
            ("## 三点工作量", "风险储备"),
            ("## 三点报价", "乐观"),
            ("## 三点报价", "基准"),
            ("## 三点报价", "保守"),
            ("## 三点报价", "假设"),
            ("## 三点报价", "人数"),
            ("## 三点报价", "周期"),
            ("## 三点报价", "风险储备"),
        )

        for heading, token in cases:
            with self.subTest(heading=heading, token=token), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                target = root / "references" / "effort-estimation.md"
                target.parent.mkdir(parents=True)
                source = (source_root / "references" / "effort-estimation.md").read_text(encoding="utf-8")
                before, section, after = source.partition(heading)
                section_body, next_heading, remainder = after.partition("## ")
                target.write_text(
                    before + section + section_body.replace(token, "已删除") + next_heading + remainder,
                    encoding="utf-8",
                )

                errors = validate_package(root)

                self.assertIn(f"effort rules missing {heading} token: {token}", errors)

    def test_analysis_modules_define_atomic_requirements_and_three_point_estimates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            references = root / "references"
            references.mkdir(parents=True)
            (references / "requirement-analysis.md").write_text("# Requirements\n", encoding="utf-8")
            (references / "capability-matching.md").write_text("# Capability\n", encoding="utf-8")
            (references / "effort-estimation.md").write_text("# Effort\n", encoding="utf-8")

            errors = validate_package(root)

            self.assertIn("requirement rules missing token: 原始要求和出处", errors)
            self.assertIn("capability rules missing token: L3 不建议承诺", errors)
            self.assertIn("effort rules missing token: 乐观", errors)
            self.assertIn("effort rules missing token: 最坏情景损失", errors)

    def test_minimal_package_requires_all_references(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "SKILL.md").write_text(
                "---\nname: presales-opportunity-review\n"
                "description: Review presales opportunities.\n---\n",
                encoding="utf-8",
            )

            errors = validate_package(root)

            self.assertIn("missing: knowledge/company-profile.md", errors)
            self.assertIn("missing: references/material-classification.md", errors)

    def test_material_rules_and_company_profile_have_required_contracts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            material = root / "references" / "material-classification.md"
            profile = root / "knowledge" / "company-profile.md"
            material.parent.mkdir(parents=True)
            profile.parent.mkdir(parents=True)
            material.write_text("# Material classification\n", encoding="utf-8")
            profile.write_text("# Company profile\n", encoding="utf-8")

            errors = validate_package(root)

            self.assertIn("material rules missing token: parse_confidence", errors)
            self.assertIn("company profile missing heading: ## 能力边界", errors)

    def test_company_profile_requires_missing_baseline_blocking_rule(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            profile = root / "knowledge" / "company-profile.md"
            profile.parent.mkdir(parents=True)
            profile.write_text(
                "\n".join(
                    (
                        "# 公司能力基线",
                        "## 元数据",
                        "## 公司定位",
                        "## 产品能力",
                        "## 技术能力",
                        "## 交付能力",
                        "## 商务原则",
                        "## 能力边界",
                        "## L0-L3 判定基线",
                        "## 历史案例",
                        "## 工作量参考",
                        "## 报价参考",
                    )
                ),
                encoding="utf-8",
            )

            errors = validate_package(root)

            self.assertIn(
                "company profile missing token: "
                "公司基线缺失时，不得给出确定性的能力匹配、报价和参与建议",
                errors,
            )

    def test_project_and_procurement_rules_define_routing_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            profiling = root / "references" / "project-profiling.md"
            mechanism = root / "references" / "procurement-mechanism.md"
            profiling.parent.mkdir(parents=True)
            profiling.write_text("# Project\n", encoding="utf-8")
            mechanism.write_text("# Procurement\n", encoding="utf-8")

            errors = validate_package(root)

            self.assertIn("project rules missing token: funding_model", errors)
            self.assertIn("procurement rules missing token: pricing_direction", errors)
            self.assertIn("procurement rules missing token: 供应商须知前附表", errors)

    def test_project_schema_reports_missing_nested_strategy_pricing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            profiling = root / "references" / "project-profiling.md"
            profiling.parent.mkdir(parents=True)
            profiling.write_text(
                PROJECT_SCHEMA.replace("  pricing: null\n", "", 1),
                encoding="utf-8",
            )

            errors = validate_package(root)

            self.assertIn("project schema missing path: strategy.pricing", errors)

    def test_project_schema_rejects_field_under_wrong_parent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            profiling = root / "references" / "project-profiling.md"
            profiling.parent.mkdir(parents=True)
            profiling.write_text(
                PROJECT_SCHEMA.replace("  pricing: null\n", "").replace(
                    "evidence: []", "pricing: null\nevidence: []"
                ),
                encoding="utf-8",
            )

            errors = validate_package(root)

            self.assertIn("project schema missing path: strategy.pricing", errors)
            self.assertIn("project schema unexpected path: pricing", errors)

    def test_procurement_precedence_rejects_swapped_levels(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            mechanism = root / "references" / "procurement-mechanism.md"
            mechanism.parent.mkdir(parents=True)
            mechanism.write_text(
                "\n".join(
                    (
                        "procurement_type funding_model lots joint_bid_policy subcontract_policy",
                        "pricing_direction quotation_rounds evaluation_method award_conditions",
                        "供应商须知前附表 post-award negotiation",
                        "latest clarification/modification",
                        "> special terms",
                        "> supplier instructions schedule",
                        "> procurement requirements",
                        "> general terms",
                        "> response template",
                    )
                ),
                encoding="utf-8",
            )

            errors = validate_package(root)

            self.assertIn("procurement rules invalid precedence order", errors)

    def test_research_rules_reject_search_snippets_and_syndication(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            research = root / "references" / "research-rules.md"
            evidence = root / "references" / "evidence-rules.md"
            research.parent.mkdir(parents=True)
            research.write_text("# Research\n", encoding="utf-8")
            evidence.write_text("# Evidence\n", encoding="utf-8")

            errors = validate_package(root)

            self.assertIn(
                "research rules missing token: 搜索结果摘要不能直接作为事实依据",
                errors,
            )
            self.assertIn("research rules missing token: 只算一个来源", errors)
            self.assertIn("evidence rules missing token: verification_status", errors)

    def test_evidence_rules_reject_extra_schema_fields_and_statuses(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evidence = root / "references" / "evidence-rules.md"
            evidence.parent.mkdir(parents=True)
            evidence.write_text(
                """```yaml
evidence:
  id: E001
  claim: example
  source: example
  location: example
  url: null
  source_date: null
  accessed_at: null
  verification_status: 单一来源待验证
  independent_sources: []
  contradictions: []
  confidence: low
  source_origin: example
```

`verification_status` 只能使用以下状态：

- 已由一手来源确认
- 已交叉验证
- 单一来源待验证
- 来源冲突
- 无法验证
- 待验证
""",
                encoding="utf-8",
            )

            errors = validate_package(root)

            self.assertIn("evidence rules unexpected field: source_origin", errors)
            self.assertIn("evidence rules invalid verification statuses", errors)

    def test_evidence_rules_reject_fields_outside_the_evidence_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evidence = root / "references" / "evidence-rules.md"
            evidence.parent.mkdir(parents=True)
            evidence.write_text(
                """id claim source location url source_date accessed_at verification_status
independent_sources contradictions confidence

```yaml
evidence: []
```

`verification_status` 只能使用以下状态：

- 已由一手来源确认
- 已交叉验证
- 单一来源待验证
- 来源冲突
- 无法验证
""",
                encoding="utf-8",
            )

            errors = validate_package(root)

            self.assertIn("evidence rules missing field: id", errors)

    def test_evidence_rules_reject_duplicate_record_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evidence = root / "references" / "evidence-rules.md"
            evidence.parent.mkdir(parents=True)
            source = (
                Path(__file__).resolve().parents[1]
                / "references"
                / "evidence-rules.md"
            )
            evidence.write_text(
                source.read_text(encoding="utf-8").replace(
                    "  claim: 可独立核验的主张\n",
                    "  claim: 可独立核验的主张\n  claim: 重复主张\n",
                ),
                encoding="utf-8",
            )

            errors = validate_package(root)

            self.assertIn("evidence rules duplicate field: claim", errors)

    def test_evidence_rules_reject_duplicate_evidence_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            evidence = root / "references" / "evidence-rules.md"
            evidence.parent.mkdir(parents=True)
            source = (
                Path(__file__).resolve().parents[1]
                / "references"
                / "evidence-rules.md"
            )
            evidence.write_text(
                source.read_text(encoding="utf-8").replace(
                    "evidence:\n",
                    "evidence:\nevidence:\n",
                    1,
                ),
                encoding="utf-8",
            )

            errors = validate_package(root)

            self.assertIn("evidence rules duplicate root: evidence", errors)

    def test_research_rules_require_explicit_unverified_status_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            research = root / "references" / "research-rules.md"
            research.parent.mkdir(parents=True)
            research.write_text(
                """搜索结果摘要不能直接作为事实依据
原子主张
优先使用一手来源
一个一手来源，或两个相互独立的可靠来源
只算一个来源
实体、日期、金额、单位和适用范围必须逐项匹配
来源新鲜度
保留矛盾证据
待验证
""",
                encoding="utf-8",
            )

            errors = validate_package(root)

            self.assertIn(
                "research rules missing token: 单一或低质量来源标记为单一来源待验证",
                errors,
            )
            self.assertIn(
                "research rules missing token: 无法取得可核验来源标记为无法验证",
                errors,
            )
            self.assertIn("research rules missing token: 不得产生裸待验证状态", errors)

    def test_evidence_fixtures_match_the_exact_record_contract(self) -> None:
        fixture_root = Path(__file__).parent / "fixtures"
        syndication, syndication_status = fixture_records(
            fixture_root / "invalid-syndication" / "evidence.yaml"
        )
        conflict, conflict_status = fixture_records(
            fixture_root / "source-conflict" / "evidence.yaml"
        )

        self.assertEqual(syndication_status, "单一来源待验证")
        self.assertEqual(len(syndication), 2)
        self.assertEqual({record["verification_status"] for record in syndication}, {syndication_status})
        self.assertTrue(all(set(record) == EVIDENCE_FIELDS for record in syndication))
        self.assertEqual(
            {record["source"] for record in syndication},
            {"示例行业媒体甲", "示例行业媒体乙"},
        )
        self.assertEqual(
            {source for record in syndication for source in record["independent_sources"]},
            {"示例采购方新闻稿"},
        )
        self.assertEqual(
            [record["independent_sources"] for record in syndication],
            [["示例采购方新闻稿"], ["示例采购方新闻稿"]],
        )
        degraded_origins = [record["independent_sources"] for record in syndication]
        degraded_origins[1] = []
        with self.assertRaises(AssertionError):
            self.assertEqual(
                degraded_origins,
                [["示例采购方新闻稿"], ["示例采购方新闻稿"]],
            )
        self.assertEqual(conflict_status, "来源冲突")
        self.assertEqual(len(conflict), 2)
        self.assertEqual({record["verification_status"] for record in conflict}, {conflict_status})
        self.assertTrue(all(set(record) == EVIDENCE_FIELDS for record in conflict))
        self.assertEqual(
            {record["source"] for record in conflict},
            {"示例采购方授标公告", "示例资讯汇总"},
        )
        self.assertEqual(
            {record["claim"] for record in conflict},
            {
                "示例采购方公布的示例项目授标金额为 120 万示例货币单位。",
                "示例采购方公布的示例项目授标金额为 150 万示例货币单位。",
            },
        )
        self.assertTrue(all(record["contradictions"] for record in conflict))

    def test_fixture_parser_rejects_duplicate_record_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "evidence.yaml"
            source = (
                Path(__file__).parent
                / "fixtures"
                / "invalid-syndication"
                / "evidence.yaml"
            )
            path.write_text(
                source.read_text(encoding="utf-8").replace(
                    '    source: "示例行业媒体甲"\n',
                    '    source: "示例行业媒体甲"\n    source: "重复媒体"\n',
                    1,
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "duplicate fixture field: source"):
                fixture_records(path)
