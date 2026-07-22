from __future__ import annotations

import sys
import re
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

PROJECT_SCHEMA_PATHS = (
    "project",
    "project.name", "project.customer", "project.industry", "project.procurement_type",
    "project.funding_model", "project.current_stage", "project.budget",
    "project.delivery_scope", "project.timeline",
    "materials", "materials.provided", "materials.missing", "materials.parse_failures",
    "materials.conflicts", "materials.confidence",
    "procurement", "procurement.lots", "procurement.joint_bid_policy",
    "procurement.subcontract_policy", "procurement.pricing_direction",
    "procurement.quotation_rounds", "procurement.evaluation_method",
    "procurement.award_conditions", "procurement.rule_conflicts",
    "packages",
    "competitors", "competitors.direct", "competitors.substitutes", "competitors.partners",
    "bid", "bid.qualification_items", "bid.compliance_items", "bid.rejection_risks",
    "bid.scoring_items", "bid.estimated_score",
    "strategy", "strategy.recommendation", "strategy.participation_mode",
    "strategy.conditions", "strategy.exit_conditions", "strategy.prohibited_commitments",
    "strategy.pricing", "strategy.negotiation", "strategy.clarification_questions",
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

RESEARCH_RULE_TOKENS = (
    "搜索结果摘要不能直接作为事实依据",
    "原子主张",
    "优先使用一手来源",
    "一个一手来源，或两个相互独立的可靠来源",
    "只算一个来源",
    "实体、日期、金额、单位和适用范围必须逐项匹配",
    "来源新鲜度",
    "保留矛盾证据",
    "待验证",
    "单一或低质量来源标记为单一来源待验证",
    "无法取得可核验来源标记为无法验证",
    "不得产生裸待验证状态",
)

EVIDENCE_RULE_TOKENS = (
    "verification_status",
    "不能作为正式报告的确定性事实",
)

EVIDENCE_FIELDS = (
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
)

VERIFICATION_STATUSES = (
    "已由一手来源确认",
    "已交叉验证",
    "单一来源待验证",
    "来源冲突",
    "无法验证",
)

VERIFICATION_STATUS_MARKER = "`verification_status` 只能使用以下状态："

YAML_FENCE = re.compile(r"```yaml\s*\n(?P<body>.*?)```", re.DOTALL)
YAML_MAPPING_LINE = re.compile(
    r"^(?P<indent>[ ]*)(?P<key>[A-Za-z_][A-Za-z0-9_-]*):(?P<value>.*)$"
)
FLOW_MAPPING_KEY = re.compile(r"(?:^|,)\s*([A-Za-z_][A-Za-z0-9_-]*)\s*:")


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


def yaml_mapping_paths(path: Path) -> dict[str, int] | None:
    """Parse constrained schema paths while retaining duplicate-key counts."""
    match = YAML_FENCE.search(path.read_text(encoding="utf-8"))
    if match is None:
        return None

    paths: dict[str, int] = {}

    def add_path(key_path: tuple[str, ...]) -> None:
        schema_path = ".".join(key_path)
        paths[schema_path] = paths.get(schema_path, 0) + 1

    parents: list[tuple[int, tuple[str, ...]]] = []
    for line in match.group("body").splitlines():
        mapping = YAML_MAPPING_LINE.match(line)
        if mapping is None:
            continue
        indent = len(mapping.group("indent"))
        while parents and indent <= parents[-1][0]:
            parents.pop()
        parent_path = parents[-1][1] if parents else ()
        key_path = parent_path + (mapping.group("key"),)
        add_path(key_path)
        value = mapping.group("value").strip()
        if value.startswith("{"):
            for flow_key in FLOW_MAPPING_KEY.findall(value[1:]):
                add_path(key_path + (flow_key,))
        elif not value:
            parents.append((indent, key_path))
    return paths


def require_project_schema(path: Path) -> list[str]:
    if not path.is_file():
        return []
    actual_path_counts = yaml_mapping_paths(path)
    if actual_path_counts is None:
        return ["project schema missing YAML fenced block"]
    actual_paths = set(actual_path_counts)
    expected_paths = set(PROJECT_SCHEMA_PATHS)
    errors = [
        f"project schema missing path: {schema_path}"
        for schema_path in sorted(expected_paths - actual_paths)
    ]
    errors.extend(
        f"project schema unexpected path: {schema_path}"
        for schema_path in sorted(actual_paths - expected_paths)
    )
    return errors


def verification_statuses(path: Path) -> list[str] | None:
    text = path.read_text(encoding="utf-8")
    _, marker, remainder = text.partition(VERIFICATION_STATUS_MARKER)
    if not marker:
        return None

    statuses: list[str] = []
    started = False
    for line in remainder.splitlines():
        if line.startswith("- "):
            statuses.append(line[2:].strip())
            started = True
        elif started and line.strip():
            break
    return statuses


def require_evidence_contract(path: Path) -> list[str]:
    if not path.is_file():
        return []
    actual_path_counts = yaml_mapping_paths(path)
    if actual_path_counts is None:
        return ["evidence rules missing YAML fenced block"]
    actual_paths = set(actual_path_counts)

    expected_paths = {"evidence"} | {f"evidence.{field}" for field in EVIDENCE_FIELDS}
    record_paths = {
        schema_path
        for schema_path in actual_paths
        if schema_path == "evidence" or schema_path.startswith("evidence.")
    }
    actual_fields = {
        schema_path.removeprefix("evidence.")
        for schema_path in record_paths
        if schema_path != "evidence"
    }
    expected_fields = set(EVIDENCE_FIELDS)
    errors = [
        f"evidence rules missing field: {field}"
        for field in sorted(expected_fields - actual_fields)
    ]
    errors.extend(
        f"evidence rules unexpected field: {field}"
        for field in sorted(actual_fields - expected_fields)
    )
    errors.extend(
        f"evidence rules duplicate field: {schema_path.removeprefix('evidence.')}"
        for schema_path, count in sorted(actual_path_counts.items())
        if schema_path.startswith("evidence.") and count > 1
    )
    errors.extend(
        f"evidence rules unexpected path: {schema_path}"
        for schema_path in sorted(actual_paths - expected_paths)
        if not schema_path.startswith("evidence.")
    )

    statuses = verification_statuses(path)
    if statuses is None or set(statuses) != set(VERIFICATION_STATUSES) or len(statuses) != len(VERIFICATION_STATUSES):
        errors.append("evidence rules invalid verification statuses")
    return errors


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
    errors.extend(require_project_schema(root / "references" / "project-profiling.md"))
    errors.extend(
        require_tokens(
            root / "references" / "procurement-mechanism.md",
            "procurement rules",
            PROCUREMENT_MECHANISM_TOKENS,
        )
    )
    errors.extend(require_precedence(root / "references" / "procurement-mechanism.md"))
    errors.extend(
        require_tokens(
            root / "references" / "research-rules.md",
            "research rules",
            RESEARCH_RULE_TOKENS,
        )
    )
    errors.extend(
        require_tokens(
            root / "references" / "evidence-rules.md",
            "evidence rules",
            EVIDENCE_RULE_TOKENS,
        )
    )
    errors.extend(require_evidence_contract(root / "references" / "evidence-rules.md"))
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
