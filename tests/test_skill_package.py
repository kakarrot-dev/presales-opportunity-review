import tempfile
import unittest
from pathlib import Path

from check_skill_package import validate_package


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

    def test_project_schema_and_procurement_precedence_are_complete(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            profiling = root / "references" / "project-profiling.md"
            mechanism = root / "references" / "procurement-mechanism.md"
            profiling.parent.mkdir(parents=True)
            profiling.write_text(
                "\n".join(
                    (
                        "project: {name: null, customer: null, industry: null, procurement_type: null, funding_model: null, current_stage: null, budget: null, delivery_scope: null, timeline: null}",
                        "materials: {provided: [], missing: [], confidence: null}",
                        "procurement: {lots: [], joint_bid_policy: null, subcontract_policy: null, pricing_direction: null, quotation_rounds: [], evaluation_method: null, award_conditions: []}",
                        "packages: []",
                        "competitors: {direct: [], substitutes: [], partners: []}",
                        "bid: {qualification_items: [], compliance_items: [], rejection_risks: [], scoring_items: [], estimated_score: null}",
                        "strategy: {recommendation: null, participation_mode: null, conditions: [], exit_conditions: [], pricing: null, negotiation: null, clarification_questions: []}",
                        "evidence: []",
                    )
                ),
                encoding="utf-8",
            )
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

            self.assertIn("project schema missing token: parse_failures", errors)
            self.assertIn("project schema missing token: rule_conflicts", errors)
            self.assertIn(
                "project schema missing token: prohibited_commitments", errors
            )
            self.assertIn("procurement rules invalid precedence order", errors)
