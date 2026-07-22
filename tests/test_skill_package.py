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
