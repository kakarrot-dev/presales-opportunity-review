from __future__ import annotations

import sys
from pathlib import Path


REQUIRED_FILES = (
    "SKILL.md",
    "knowledge/company-profile.md",
    "references/material-classification.md",
    "references/project-profiling.md",
    "references/procurement-mechanism.md",
    "references/research-rules.md",
    "references/requirement-analysis.md",
    "references/capability-matching.md",
    "references/effort-estimation.md",
    "references/evaluation-analysis.md",
    "references/opportunity-strategy.md",
    "references/clarification-questions.md",
    "references/evidence-rules.md",
    "references/report-template.md",
    "examples/sample-input.md",
    "examples/sample-report.md",
)

MATERIAL_RECORD_TOKENS = (
    "id",
    "path",
    "format",
    "content_regions",
    "status",
    "parse_confidence",
    "provenance",
    "errors",
)

PROJECT_PROFILING_TOKENS = (
    "project",
    "funding_model",
    "materials",
    "procurement",
    "packages",
    "competitors",
    "bid",
    "strategy",
    "evidence",
)

PROJECT_SCHEMA_TOKENS = (
    "project",
    "name",
    "customer",
    "industry",
    "procurement_type",
    "funding_model",
    "current_stage",
    "budget",
    "delivery_scope",
    "timeline",
    "materials",
    "provided",
    "missing",
    "parse_failures",
    "conflicts",
    "confidence",
    "procurement",
    "lots",
    "joint_bid_policy",
    "subcontract_policy",
    "pricing_direction",
    "quotation_rounds",
    "evaluation_method",
    "award_conditions",
    "rule_conflicts",
    "packages",
    "competitors",
    "direct",
    "substitutes",
    "partners",
    "bid",
    "qualification_items",
    "compliance_items",
    "rejection_risks",
    "scoring_items",
    "estimated_score",
    "strategy",
    "recommendation",
    "participation_mode",
    "conditions",
    "exit_conditions",
    "prohibited_commitments",
    "pricing",
    "negotiation",
    "clarification_questions",
    "evidence",
)

PROCUREMENT_PRECEDENCE = (
    "latest clarification/modification",
    "supplier instructions schedule",
    "special terms",
    "procurement requirements",
    "general terms",
    "response template",
)

PROCUREMENT_MECHANISM_TOKENS = (
    "procurement_type",
    "funding_model",
    "lots",
    "joint_bid_policy",
    "subcontract_policy",
    "pricing_direction",
    "quotation_rounds",
    "evaluation_method",
    "award_conditions",
    "供应商须知前附表",
    "post-award negotiation",
)

COMPANY_PROFILE_HEADINGS = (
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

COMPANY_PROFILE_GUARDRAIL_TOKENS = (
    "公司基线缺失时，不得给出确定性的能力匹配、报价和参与建议",
)


def require_tokens(path: Path, label: str, tokens: tuple[str, ...]) -> list[str]:
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    return [f"{label} missing token: {token}" for token in tokens if token not in text]


def require_headings(path: Path, label: str, headings: tuple[str, ...]) -> list[str]:
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    return [f"{label} missing heading: {heading}" for heading in headings if heading not in text]


def require_precedence(path: Path) -> list[str]:
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    positions = [text.find(token) for token in PROCUREMENT_PRECEDENCE]
    if -1 in positions or positions != sorted(positions):
        return ["procurement rules invalid precedence order"]
    return []


def validate_package(root: Path) -> list[str]:
    errors: list[str] = []
    for relative_path in REQUIRED_FILES:
        if not (root / relative_path).is_file():
            errors.append(f"missing: {relative_path}")
    errors.extend(
        require_tokens(
            root / "references" / "material-classification.md",
            "material rules",
            MATERIAL_RECORD_TOKENS,
        )
    )
    errors.extend(
        require_headings(
            root / "knowledge" / "company-profile.md",
            "company profile",
            COMPANY_PROFILE_HEADINGS,
        )
    )
    errors.extend(
        require_tokens(
            root / "knowledge" / "company-profile.md",
            "company profile",
            COMPANY_PROFILE_GUARDRAIL_TOKENS,
        )
    )
    errors.extend(
        require_tokens(
            root / "references" / "project-profiling.md",
            "project rules",
            PROJECT_PROFILING_TOKENS,
        )
    )
    errors.extend(
        require_tokens(
            root / "references" / "project-profiling.md",
            "project schema",
            PROJECT_SCHEMA_TOKENS,
        )
    )
    errors.extend(
        require_tokens(
            root / "references" / "procurement-mechanism.md",
            "procurement rules",
            PROCUREMENT_MECHANISM_TOKENS,
        )
    )
    errors.extend(require_precedence(root / "references" / "procurement-mechanism.md"))
    return errors


def main() -> int:
    errors = validate_package(Path(__file__).resolve().parents[1])
    if errors:
        print("\n".join(errors))
        return 1
    print("skill package valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
