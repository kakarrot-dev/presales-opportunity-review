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

REQUIREMENT_ANALYSIS_TOKENS = (
    "原始要求和出处",
    "交付物",
    "依赖",
    "验收",
    "隐含工作",
    "能力匹配",
    "复杂度",
    "工作量",
    "风险",
    "澄清",
    "数据",
    "接口",
    "部署",
    "迁移",
    "定制",
    "测试",
    "培训",
    "现场服务",
    "质保",
)

CAPABILITY_MATCHING_TOKENS = (
    "L0 直接满足",
    "L1 配置满足",
    "L2 合作满足",
    "L3 不建议承诺",
    "待内部确认",
)

EFFORT_ESTIMATION_TOKENS = (
    "乐观",
    "未经用户/公司授权不得生成最终或正式报价",
    "投资",
    "还款来源",
    "运营期限",
    "资产归属",
    "验收前现金暴露",
    "最坏情景损失",
)

CAPABILITY_LEVEL_DEFINITIONS = {
    "L0 直接满足": "现有产品、技术或交付能力可在约定范围内直接满足",
    "L1 配置满足": "通过标准配置、参数设置或既有模板可满足",
    "L2 合作满足": "需要已识别合作方、外部产品或外部服务",
    "L3 不建议承诺": "不具备、存在不可接受边界，或关键依赖不可控",
}

THREE_POINT_ESTIMATE_TOKENS = (
    "乐观",
    "基准",
    "保守",
    "假设",
    "人数",
    "周期",
    "风险储备",
)

ATOMIC_REQUIREMENT_TOKENS = (
    "原始要求和出处", "交付物", "依赖", "验收", "隐含工作", "能力匹配",
    "复杂度", "工作量", "风险", "澄清", "数据", "接口",
)
HIDDEN_WORK_TOKENS = ("数据", "接口", "部署", "迁移", "定制", "测试", "培训", "现场服务", "质保", "验收")

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


def markdown_section(text: str, heading: str) -> str:
    _, marker, remainder = text.partition(heading)
    if not marker:
        return ""
    return remainder.partition("\n## ")[0]


def require_requirement_sections(path: Path) -> list[str]:
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    sections = (("原子需求记录", ATOMIC_REQUIREMENT_TOKENS), ("隐性工作清单", HIDDEN_WORK_TOKENS))
    return [
        f"requirement rules missing {heading} token: {token}"
        for heading, tokens in sections
        for token in tokens
        if token not in markdown_section(text, f"## {heading}")
    ]


def require_capability_definitions(path: Path) -> list[str]:
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    errors = [
        f"capability rules invalid definition: {level}"
        for level, definition in CAPABILITY_LEVEL_DEFINITIONS.items()
        if f"`{level}`：{definition}" not in text
    ]
    required_relationships = (
        "`company_match` 必须引用 `knowledge/company-profile.md`",
        "公司基线为空白、过期、无法定位，或没有覆盖该能力时，输出 `待内部确认`",
    )
    if any(relationship not in text for relationship in required_relationships):
        errors.append("capability rules missing evidence fallback relationship")
    return errors


def require_estimation_section_tokens(path: Path, heading: str) -> list[str]:
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    _, marker, remainder = text.partition(heading)
    if not marker:
        section = ""
    else:
        section, _, _ = remainder.partition("\n## ")
    return [
        f"effort rules missing {heading} token: {token}"
        for token in THREE_POINT_ESTIMATE_TOKENS
        if token not in section
    ]


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
    errors: list[str] = []
    if actual_path_counts.get("evidence", 0) > 1:
        errors.append("evidence rules duplicate root: evidence")
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
    errors.extend(
        f"evidence rules missing field: {field}"
        for field in sorted(expected_fields - actual_fields)
    )
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
    errors.extend(
        require_tokens(
            root / "references" / "requirement-analysis.md",
            "requirement rules",
            REQUIREMENT_ANALYSIS_TOKENS,
        )
    )
    errors.extend(require_requirement_sections(root / "references" / "requirement-analysis.md"))
    errors.extend(
        require_tokens(
            root / "references" / "capability-matching.md",
            "capability rules",
            CAPABILITY_MATCHING_TOKENS,
        )
    )
    errors.extend(require_capability_definitions(root / "references" / "capability-matching.md"))
    errors.extend(
        require_tokens(
            root / "references" / "effort-estimation.md",
            "effort rules",
            EFFORT_ESTIMATION_TOKENS,
        )
    )
    errors.extend(
        require_estimation_section_tokens(
            root / "references" / "effort-estimation.md", "## 三点工作量"
        )
    )
    errors.extend(
        require_estimation_section_tokens(
            root / "references" / "effort-estimation.md", "## 三点报价"
        )
    )
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
