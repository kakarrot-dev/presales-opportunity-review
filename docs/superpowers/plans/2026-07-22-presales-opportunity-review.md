# Presales Opportunity Review Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a single-entry Codex Skill that converts heterogeneous presales materials into traceable opportunity analysis, compliance checks, clarification lists, and safely separated internal and formal reports.

**Architecture:** `SKILL.md` is a thin orchestrator. Focused Markdown rules under `references/` define normalization, procurement analysis, evidence verification, requirement and capability analysis, estimation, evaluation, strategy, clarification, and reporting. A standard-library Python checker validates package structure and policy contracts; synthetic fixtures and sample outputs exercise the cross-module behavior without committing customer documents.

**Tech Stack:** Codex Skill Markdown, YAML frontmatter, YAML-shaped internal data contract, Python 3 standard library for package checks, Markdown fixtures and expected reports, Git.

## Global Constraints

- Keep one callable Skill entry point; do not split the first version into multiple callable Skills.
- `SKILL.md` only orchestrates; detailed rules belong in focused files under `references/`.
- Inputs may be Excel, Word, PDF, Markdown, images, or multi-file combinations with arbitrary names and structures.
- Never commit or copy the three customer-provided source documents into the repository.
- Preserve file, sheet and cell, document section, or PDF page provenance for extracted facts.
- Treat web search results as discovery leads, not facts; critical web claims require a primary source or two independent reliable sources.
- Do not count syndicated copies or pages derived from the same underlying source as independent corroboration.
- Unverified or conflicting web claims cannot become definitive conclusions or appear as facts in the formal report.
- Do not provide legal opinions, complete bid-document authoring, post-award project management, or unauthorized final pricing.
- Missing or stale `knowledge/company-profile.md` blocks definitive capability, price, and participation conclusions.
- Generate the internal report and formal report independently from an allowlist; do not create the formal report by deleting paragraphs from the internal report.
- Every task uses TDD: add or tighten a failing check, observe failure, implement the smallest rule content, observe success, then commit only that task's files.

---

## Planned File Structure

```text
SKILL.md                              # Trigger conditions and workflow orchestration only
knowledge/company-profile.md         # Editable company capability and commercial baseline
references/material-classification.md # File/content discovery and semantic normalization
references/project-profiling.md      # Project identity, lots, materials and normalized object
references/procurement-mechanism.md  # Funding, pricing, precedence and award mechanics
references/research-rules.md         # External research and claim-level truth verification
references/requirement-analysis.md   # Atomic requirement and hidden-work decomposition
references/capability-matching.md     # L0-L3 capability decisions and baseline evidence
references/effort-estimation.md      # Effort, schedule, pricing and investment scenarios
references/evaluation-analysis.md    # Qualification, compliance and evaluation routing
references/opportunity-strategy.md   # Go decision, participation mode and guardrails
references/clarification-questions.md # Internal and customer clarification generation
references/evidence-rules.md         # Evidence records, confidence and conflict treatment
references/report-template.md        # Output files and internal/formal disclosure contracts
examples/sample-input.md             # Synthetic heterogeneous-material scenario
examples/sample-report.md            # Expected multi-output example for the scenario
tests/check_skill_package.py          # Static and scenario-contract validator
tests/test_skill_package.py           # Unit tests for validator behavior and package rules
tests/fixtures/invalid-syndication/   # Synthetic evidence graph that must not cross-validate
tests/fixtures/source-conflict/       # Synthetic primary/secondary contradiction scenario
```

Each reference file owns one decision boundary. Cross-file interfaces use the exact field names in the normalized YAML contract defined in Task 3.

### Task 1: Package Checker and Minimal Skill Entry Point

**Files:**
- Create: `tests/check_skill_package.py`
- Create: `tests/test_skill_package.py`
- Create: `SKILL.md`

**Interfaces:**
- Consumes: repository root path.
- Produces: `validate_package(root: pathlib.Path) -> list[str]`; CLI exit code `0` with `skill package valid`, or exit code `1` with one error per line.

- [ ] **Step 1: Write the failing validator unit test**

```python
# tests/test_skill_package.py
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
```

- [ ] **Step 2: Run the test and verify the missing module failure**

Run: `PYTHONPATH=tests python3 -m unittest discover -s tests -p 'test_*.py' -v`

Expected: `ERROR` with `ModuleNotFoundError: No module named 'check_skill_package'`.

- [ ] **Step 3: Implement the checker and minimal entry point**

```python
# tests/check_skill_package.py
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


def validate_package(root: Path) -> list[str]:
    errors: list[str] = []
    for relative_path in REQUIRED_FILES:
        if not (root / relative_path).is_file():
            errors.append(f"missing: {relative_path}")
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
```

```markdown
---
name: presales-opportunity-review
description: Analyze heterogeneous tender and opportunity materials for presales qualification, delivery fit, effort, commercial risk, clarification, and bid strategy. Use when a user provides tender documents, procurement lists, technical requirements, scoring rules, budgets, quotations, or opportunity notes and asks whether or how the company should participate.
---

# Presales Opportunity Review

This file orchestrates the review. Detailed decision rules live in `references/`.
```

- [ ] **Step 4: Run the unit test and package checker**

Run: `PYTHONPATH=tests python3 -m unittest discover -s tests -p 'test_*.py' -v`

Expected: `OK`.

Run: `python3 tests/check_skill_package.py`

Expected: failure listing every not-yet-created required file. This is the intended package-level red state until Tasks 2-8 finish.

- [ ] **Step 5: Commit the checker and entry point**

```bash
git add SKILL.md tests/check_skill_package.py tests/test_skill_package.py
git commit -m "test: add presales skill package checker"
```

### Task 2: Material Classification and Company Baseline Contracts

**Files:**
- Create: `references/material-classification.md`
- Create: `knowledge/company-profile.md`
- Modify: `tests/check_skill_package.py`
- Modify: `tests/test_skill_package.py`

**Interfaces:**
- Consumes: arbitrary user files and supplemental statements.
- Produces: normalized material records with `id`, `path`, `format`, `content_regions`, `status`, `parse_confidence`, `provenance`, `errors`; company baseline sections named in this task.

- [ ] **Step 1: Add failing content-contract tests**

```python
# append inside tests/test_skill_package.py
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
```

Extend `validate_package()` with exact token and heading checks:

```python
def require_tokens(path: Path, label: str, tokens: tuple[str, ...]) -> list[str]:
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    return [f"{label} missing token: {token}" for token in tokens if token not in text]
```

- [ ] **Step 2: Run the focused test and verify failure**

Run: `PYTHONPATH=tests python3 -m unittest test_skill_package.SkillPackageTests.test_material_rules_and_company_profile_have_required_contracts -v`

Expected: `FAIL` because the content checks are not implemented or required tokens are absent.

- [ ] **Step 3: Write the material and baseline rules**

`references/material-classification.md` must define this exact record and procedure:

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

It must instruct the agent to enumerate files, sheets, pages, attachments and regions; detect blank sheets; infer title/header/detail/group/total/note regions semantically; bounded-fill merged or blank group labels; preserve raw quantity plus parsed value and unit; split long cells into atomic requirements; and recognize `利旧`, `包含在报价内`, `原厂授权`, and `实质性响应`.

`knowledge/company-profile.md` must contain editable headings:

```markdown
# 公司能力基线
## 元数据
## 公司定位
## 产品能力
## 技术能力
## 交付能力
## 商务原则
## 能力边界
## L0-L3 判定基线
## 历史案例
## 工作量参考
## 报价参考
```

Under `## 元数据`, include fields for `更新时间`, `维护人`, and `可信度`. State that empty, unverified, or stale sections cannot support definitive conclusions.

- [ ] **Step 4: Run focused and full tests**

Run: `PYTHONPATH=tests python3 -m unittest test_skill_package.SkillPackageTests.test_material_rules_and_company_profile_have_required_contracts -v`

Expected: `OK`.

Run: `PYTHONPATH=tests python3 -m unittest discover -s tests -p 'test_*.py' -v`

Expected: all implemented unit tests pass.

- [ ] **Step 5: Commit the material contracts**

```bash
git add references/material-classification.md knowledge/company-profile.md tests/check_skill_package.py tests/test_skill_package.py
git commit -m "feat: define material and company baseline contracts"
```

### Task 3: Project Profile and Procurement Mechanism

**Files:**
- Create: `references/project-profiling.md`
- Create: `references/procurement-mechanism.md`
- Modify: `tests/check_skill_package.py`
- Modify: `tests/test_skill_package.py`

**Interfaces:**
- Consumes: material records from Task 2.
- Produces: `project-analysis.yaml` fields `project`, `materials`, `procurement`, `packages`, `competitors`, `bid`, `strategy`, and `evidence` exactly as defined below.

- [ ] **Step 1: Add a failing normalized-schema test**

```python
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
```

- [ ] **Step 2: Run the focused test and verify failure**

Run: `PYTHONPATH=tests python3 -m unittest test_skill_package.SkillPackageTests.test_project_and_procurement_rules_define_routing_fields -v`

Expected: `FAIL` for missing contract tokens.

- [ ] **Step 3: Define the normalized project object and decision routing**

`references/project-profiling.md` must include the complete YAML object from the approved spec, including:

```yaml
project: {name: null, customer: null, industry: null, procurement_type: null, funding_model: null, current_stage: null, budget: null, delivery_scope: null, timeline: null}
materials: {provided: [], missing: [], parse_failures: [], conflicts: [], confidence: null}
procurement: {lots: [], joint_bid_policy: null, subcontract_policy: null, pricing_direction: null, quotation_rounds: [], evaluation_method: null, award_conditions: [], rule_conflicts: []}
packages: []
competitors: {direct: [], substitutes: [], partners: []}
bid: {qualification_items: [], compliance_items: [], rejection_risks: [], scoring_items: [], estimated_score: null}
strategy: {recommendation: null, participation_mode: null, conditions: [], exit_conditions: [], prohibited_commitments: [], pricing: null, negotiation: null, clarification_questions: []}
evidence: []
```

`references/procurement-mechanism.md` must route procurement method, funding model, lot policy, consortium/subcontracting, pricing direction, quotation rounds, evaluation method, award conditions, guarantees and post-award negotiation. It must define this precedence:

```text
latest clarification/modification
> supplier instructions schedule
> special terms
> procurement requirements
> general terms
> response template
```

It must explicitly forbid assuming low-price wins or that every opportunity has a scoring table.

- [ ] **Step 4: Run tests**

Run: `PYTHONPATH=tests python3 -m unittest discover -s tests -p 'test_*.py' -v`

Expected: `OK`.

- [ ] **Step 5: Commit project and procurement routing**

```bash
git add references/project-profiling.md references/procurement-mechanism.md tests/check_skill_package.py tests/test_skill_package.py
git commit -m "feat: add project and procurement routing"
```

### Task 4: Evidence and Web Truth Verification

**Files:**
- Create: `references/research-rules.md`
- Create: `references/evidence-rules.md`
- Create: `tests/fixtures/invalid-syndication/evidence.yaml`
- Create: `tests/fixtures/source-conflict/evidence.yaml`
- Modify: `tests/check_skill_package.py`
- Modify: `tests/test_skill_package.py`

**Interfaces:**
- Consumes: candidate external claims and local-source facts.
- Produces: evidence records with `id`, `claim`, `source`, `location`, `url`, `source_date`, `accessed_at`, `verification_status`, `independent_sources`, `contradictions`, `confidence`.

- [ ] **Step 1: Add failing truth-verification tests**

```python
    def test_research_rules_reject_search_snippets_and_syndication(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            research = root / "references" / "research-rules.md"
            evidence = root / "references" / "evidence-rules.md"
            research.parent.mkdir(parents=True)
            research.write_text("# Research\n", encoding="utf-8")
            evidence.write_text("# Evidence\n", encoding="utf-8")

            errors = validate_package(root)

            self.assertIn("research rules missing token: 搜索结果摘要不能直接作为事实依据", errors)
            self.assertIn("research rules missing token: 只算一个来源", errors)
            self.assertIn("evidence rules missing token: verification_status", errors)
```

- [ ] **Step 2: Run the focused test and verify failure**

Run: `PYTHONPATH=tests python3 -m unittest test_skill_package.SkillPackageTests.test_research_rules_reject_search_snippets_and_syndication -v`

Expected: `FAIL` for missing verification requirements.

- [ ] **Step 3: Implement claim-level verification rules and fixtures**

`references/research-rules.md` must reproduce all eight approved verification rules: atomic claims; primary-source priority; one primary or two independent reliable sources for critical claims; syndicated/common-origin sources count once; entity/date/amount/unit/scope matching; freshness; contradiction preservation; and `待验证` status for insufficient evidence.

`references/evidence-rules.md` must define exactly these statuses:

```text
已由一手来源确认
已交叉验证
单一来源待验证
来源冲突
无法验证
```

It must state that `单一来源待验证`, `来源冲突`, and `无法验证` cannot be used as definitive formal-report facts.

Create `tests/fixtures/invalid-syndication/evidence.yaml` with two articles that both cite the same press release and an expected status of `单一来源待验证`. Create `tests/fixtures/source-conflict/evidence.yaml` with one official award amount and one conflicting secondary amount and an expected status of `来源冲突`.

- [ ] **Step 4: Run focused and full tests**

Run: `PYTHONPATH=tests python3 -m unittest test_skill_package.SkillPackageTests.test_research_rules_reject_search_snippets_and_syndication -v`

Expected: `OK`.

Run: `PYTHONPATH=tests python3 -m unittest discover -s tests -p 'test_*.py' -v`

Expected: `OK`.

- [ ] **Step 5: Commit evidence verification**

```bash
git add references/research-rules.md references/evidence-rules.md tests/fixtures tests/check_skill_package.py tests/test_skill_package.py
git commit -m "feat: enforce web claim verification"
```

### Task 5: Requirement, Capability, and Estimation Rules

**Files:**
- Create: `references/requirement-analysis.md`
- Create: `references/capability-matching.md`
- Create: `references/effort-estimation.md`
- Modify: `tests/check_skill_package.py`
- Modify: `tests/test_skill_package.py`

**Interfaces:**
- Consumes: normalized `packages[].requirements`, `knowledge/company-profile.md`, and verified evidence.
- Produces: atomic requirement records, `company_match` levels `L0`-`L3`, dependencies, risks, three-point `effort`, and three-point `price_estimate`.

- [ ] **Step 1: Add failing analysis-contract tests**

```python
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
```

- [ ] **Step 2: Run the focused test and verify failure**

Run: `PYTHONPATH=tests python3 -m unittest test_skill_package.SkillPackageTests.test_analysis_modules_define_atomic_requirements_and_three_point_estimates -v`

Expected: `FAIL` for missing rule tokens.

- [ ] **Step 3: Write the three focused rule modules**

`references/requirement-analysis.md` must require each atomic record to contain original requirement/provenance, deliverable, dependencies, acceptance criteria, hidden work, company match, complexity, effort, risk and clarification question. Hidden-work categories must include data, interfaces, deployment, migration, customization, testing, training, onsite service, warranty and acceptance.

`references/capability-matching.md` must define `L0 直接满足`, `L1 配置满足`, `L2 合作满足`, and `L3 不建议承诺`; every decision requires a company-profile citation. Missing evidence produces `待内部确认`, never an assumed capability.

`references/effort-estimation.md` must decompose product/requirements, design/development, data, integration, testing/acceptance, project management, training, onsite service and operations. It must output optimistic, baseline and conservative ranges with assumptions, staffing, duration and risk reserve. Supplier-funded projects additionally require investment, repayment source, operating term, asset ownership, pre-acceptance cash exposure and worst-case loss.

- [ ] **Step 4: Run all tests**

Run: `PYTHONPATH=tests python3 -m unittest discover -s tests -p 'test_*.py' -v`

Expected: `OK`.

- [ ] **Step 5: Commit analysis rules**

```bash
git add references/requirement-analysis.md references/capability-matching.md references/effort-estimation.md tests/check_skill_package.py tests/test_skill_package.py
git commit -m "feat: add requirement capability and estimation rules"
```

### Task 6: Evaluation, Compliance, and Opportunity Strategy

**Files:**
- Create: `references/evaluation-analysis.md`
- Create: `references/opportunity-strategy.md`
- Modify: `tests/check_skill_package.py`
- Modify: `tests/test_skill_package.py`

**Interfaces:**
- Consumes: `procurement`, `packages`, company matches, estimates and evidence.
- Produces: `bid.qualification_items`, `bid.compliance_items`, `bid.rejection_risks`, optional scoring analysis, and `strategy` decision fields.

- [ ] **Step 1: Add failing evaluation and decision tests**

```python
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
```

- [ ] **Step 2: Run the focused test and verify failure**

Run: `PYTHONPATH=tests python3 -m unittest test_skill_package.SkillPackageTests.test_evaluation_routes_without_assuming_scoring_and_strategy_has_guardrails -v`

Expected: `FAIL`.

- [ ] **Step 3: Implement evaluation and strategy rules**

`references/evaluation-analysis.md` must route qualification/conformity review, lowest-price, highest-investment or highest-price ranking, comprehensive scoring, multi-round negotiation, subjective solution review and unknown evaluation. It must separate hard qualification, rejection risk, remediable material, partner dependency and unknown status. Calculate estimated scores only when explicit point values exist.

`references/opportunity-strategy.md` must allow only `Go`, `Conditional Go`, `No-Go`, and `Insufficient Information`. It must require `participation_mode`, `conditions`, `exit_conditions`, and `prohibited_commitments`, with participation modes from the approved spec. Major qualification gaps, uncontrolled responsibility or a structurally loss-making commercial model cannot be softened into a generic warning.

- [ ] **Step 4: Run all tests**

Run: `PYTHONPATH=tests python3 -m unittest discover -s tests -p 'test_*.py' -v`

Expected: `OK`.

- [ ] **Step 5: Commit evaluation and strategy rules**

```bash
git add references/evaluation-analysis.md references/opportunity-strategy.md tests/check_skill_package.py tests/test_skill_package.py
git commit -m "feat: add evaluation and opportunity decisions"
```

### Task 7: Clarification and Dual-Report Disclosure Rules

**Files:**
- Create: `references/clarification-questions.md`
- Create: `references/report-template.md`
- Modify: `tests/check_skill_package.py`
- Modify: `tests/test_skill_package.py`

**Interfaces:**
- Consumes: complete `project-analysis.yaml`.
- Produces: the seven Markdown/YAML files listed under `outputs/<项目简称>-<日期>/` in the approved spec.

- [ ] **Step 1: Add failing output-contract tests**

```python
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
```

- [ ] **Step 2: Run the focused test and verify failure**

Run: `PYTHONPATH=tests python3 -m unittest test_skill_package.SkillPackageTests.test_output_rules_require_two_clarification_sets_and_disclosure_allowlist -v`

Expected: `FAIL`.

- [ ] **Step 3: Implement clarification and output templates**

`references/clarification-questions.md` must define the internal fields `priority`, `question`, `current_judgment`, `impact`, `owner`, `deadline`, and customer fields `topic`, `formal_question`, `reason`, `response_format`, `timing`. Customer questions receive one of four timing/ownership labels from the approved spec.

`references/report-template.md` must define:

```text
00-material-index.md
01-opportunity-review-internal.md
02-opportunity-review-formal.md
03-clarification-internal.md
04-clarification-customer.md
05-response-compliance-matrix.md
06-evidence-register.md
project-analysis.yaml
```

It must include the approved internal and formal report sections, the compliance matrix columns, the evidence table fields and verification status. Define an explicit formal-report allowlist and prohibit internal floor price, capability weaknesses, competitor tactics, unverified claims, conditions intended only for internal approval and raw reasoning notes.

- [ ] **Step 4: Run all tests**

Run: `PYTHONPATH=tests python3 -m unittest discover -s tests -p 'test_*.py' -v`

Expected: `OK`.

- [ ] **Step 5: Commit clarification and reporting rules**

```bash
git add references/clarification-questions.md references/report-template.md tests/check_skill_package.py tests/test_skill_package.py
git commit -m "feat: add clarification and dual-report contracts"
```

### Task 8: Complete Orchestration, Quality Gates, and Synthetic Example

**Files:**
- Modify: `SKILL.md`
- Create: `examples/sample-input.md`
- Create: `examples/sample-report.md`
- Modify: `tests/check_skill_package.py`
- Modify: `tests/test_skill_package.py`

**Interfaces:**
- Consumes: all reference modules and the company baseline.
- Produces: deterministic workflow order, explicit degradation behavior, quality-gate status and a complete synthetic example.

- [ ] **Step 1: Add failing orchestration and scenario tests**

```python
    def test_skill_orchestrates_all_rules_and_sample_covers_quality_gates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / "SKILL.md"
            sample = root / "examples" / "sample-report.md"
            sample.parent.mkdir(parents=True)
            skill.write_text("---\nname: presales-opportunity-review\ndescription: Review.\n---\n", encoding="utf-8")
            sample.write_text("# Sample\n", encoding="utf-8")

            errors = validate_package(root)

            self.assertIn("SKILL.md missing token: references/research-rules.md", errors)
            self.assertIn("SKILL.md missing token: 草稿—需人工复核", errors)
            self.assertIn("sample report missing token: 来源冲突", errors)
            self.assertIn("sample report missing token: Conditional Go", errors)
```

- [ ] **Step 2: Run the focused test and verify failure**

Run: `PYTHONPATH=tests python3 -m unittest test_skill_package.SkillPackageTests.test_skill_orchestrates_all_rules_and_sample_covers_quality_gates -v`

Expected: `FAIL`.

- [ ] **Step 3: Complete the orchestrator and synthetic scenario**

Update `SKILL.md` to execute the approved 19-stage workflow in order. It must link every reference file, read `company-profile.md` before capability analysis, require default external research, enforce evidence and disclosure gates, and mark the result `草稿—需人工复核` if any critical gate fails.

Add degradation rules for unreadable files, OCR, malformed tables, encrypted or missing pages, multi-file conflicts, unavailable internet and stale company profile. Every degradation must appear in the material index and reports.

Create `examples/sample-input.md` describing a fictional university opportunity with: one workbook containing a title above the header, one blank sheet, grouped line items, mixed quantity units, a `利旧` row, a supplier-funded procurement model, conflicting minimum/maximum price clauses, a required original-vendor authorization, and two web articles copied from one primary source.

Create `examples/sample-report.md` showing: material index, procurement mechanism, one atomic requirement, L2 capability match, a compliance risk, a source-conflict evidence row, a syndication row marked `单一来源待验证`, `Conditional Go`, both clarification lists, internal-only pricing assumptions, and a formal excerpt that excludes those assumptions.

- [ ] **Step 4: Run unit and package validation**

Run: `PYTHONPATH=tests python3 -m unittest discover -s tests -p 'test_*.py' -v`

Expected: all tests `OK`.

Run: `python3 tests/check_skill_package.py`

Expected: `skill package valid` and exit code `0` for the first time.

- [ ] **Step 5: Commit orchestration and examples**

```bash
git add SKILL.md examples tests/check_skill_package.py tests/test_skill_package.py
git commit -m "feat: complete presales review workflow"
```

### Task 9: Local Acceptance Against the Three Customer Samples

**Files:**
- Modify if failures require it: `SKILL.md`
- Modify if failures require it: `references/*.md`
- Modify if failures require it: `tests/check_skill_package.py`
- Modify if failures require it: `tests/test_skill_package.py`
- Do not create or commit: customer documents or generated customer reports.

**Interfaces:**
- Consumes: the three user-provided sample files from their original local paths.
- Produces: verification evidence in terminal output and any necessary rule/test corrections; no customer artifact is committed.

- [ ] **Step 1: Establish the acceptance assertions before running the Skill**

Use this checklist verbatim for the local run:

```text
[ ] Workbook 1: detects one effective sheet, two pre-header rows, ten semantic columns and mixed hardware/service items.
[ ] Workbook 2: detects one effective and three blank sheets, grouped categories, mixed units and the 利旧 row.
[ ] PDF: detects eight lots, no-consortium rule, supplier-investment possibility, multiple quotation rounds and unusual high-to-low award ordering.
[ ] PDF: reports the minimum/maximum price-rule conflict without resolving it as legal advice.
[ ] All extracted claims retain sheet/cell or page provenance.
[ ] Critical web facts have primary-source or independent-source verification status.
[ ] Internal and formal reports differ by the explicit disclosure allowlist.
[ ] Missing company-profile facts prevent definitive capability and price claims.
```

- [ ] **Step 2: Run the package tests before the manual sample run**

Run: `PYTHONPATH=tests python3 -m unittest discover -s tests -p 'test_*.py' -v && python3 tests/check_skill_package.py`

Expected: unit tests `OK`; checker prints `skill package valid`.

- [ ] **Step 3: Invoke the Skill in Codex with the three files from their original paths**

Attach or reference the three original local files in one Codex task, invoke `presales-opportunity-review`, request a draft analysis only, and explicitly state that outputs must remain outside the repository or in `/tmp`. Do not copy the source files into the worktree.

Expected: every assertion in Step 1 can be checked from the generated material index, project analysis, compliance matrix, evidence register and two reports.

- [ ] **Step 4: Convert every observed miss into a failing regression test, then fix minimally**

For each failed assertion, add one exact token/structural assertion to `tests/test_skill_package.py`, run the focused test to see `FAIL`, update only the responsible rule file, then rerun to see `OK`. Do not encode customer names, file paths, proprietary parameters or extracted customer text in tests; use synthetic equivalents.

- [ ] **Step 5: Run final verification**

Run: `PYTHONPATH=tests python3 -m unittest discover -s tests -p 'test_*.py' -v`

Expected: all tests `OK`.

Run: `python3 tests/check_skill_package.py`

Expected: `skill package valid`.

Run: `git diff --check`

Expected: no output and exit code `0`.

Run: `git status --short`

Expected: only intentional rule/test changes from acceptance fixes, or no output if no fixes were necessary.

- [ ] **Step 6: Commit only acceptance-driven fixes when present**

If files changed:

```bash
git add SKILL.md references tests
git commit -m "test: harden presales review sample handling"
```

If no files changed, do not create an empty commit.

### Task 10: Final Scope and Release Verification

**Files:**
- Modify only if verification fails: files directly responsible for the failure.

**Interfaces:**
- Consumes: completed package and Git history.
- Produces: verified implementation ready for integration review.

- [ ] **Step 1: Verify the specification coverage map**

Run:

```bash
rg -n "异构|采购机制|条款优先级|一手来源|交叉验证|L0|L3|乐观|保守|Go|Conditional Go|No-Go|Insufficient Information|内部待确认清单|甲方正式澄清清单|草稿—需人工复核" SKILL.md references knowledge examples
```

Expected: every listed contract appears in its responsible file; no requirement is present only in the example.

- [ ] **Step 2: Scan for forbidden placeholders and scope leakage**

Run:

```bash
rg -n "T[B]D|T[O]DO|implement[[:space:]]+later|以后[[:space:]]*补充|自动生成完整投标文件|合同逐条法务审查" SKILL.md references knowledge examples tests
```

Expected: no placeholders. Excluded-scope phrases may appear only in explicit prohibition statements.

- [ ] **Step 3: Run the full verification suite**

Run:

```bash
PYTHONPATH=tests python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 tests/check_skill_package.py
git diff --check
git status --short
```

Expected: tests `OK`; checker prints `skill package valid`; `git diff --check` has no output; worktree is clean after all intended commits.

- [ ] **Step 4: Review commit scope**

Run: `git log --oneline --decorate --stat 76a06a9..HEAD`

Expected: focused commits corresponding to Tasks 1-9; no customer source documents, generated customer reports, unrelated refactors or dependency artifacts.

- [ ] **Step 5: Hand off for integration**

Summarize implemented modules, test results, customer-sample acceptance results, any information that remained unverifiable, and residual risks. Do not claim rendered PDF verification or live web verification unless each was actually performed.
