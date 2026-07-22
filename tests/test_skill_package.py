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
