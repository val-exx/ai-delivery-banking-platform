from __future__ import annotations

import unittest

from agenticops_toolkit.scaffold import module_plan


class ScaffoldPlanTest(unittest.TestCase):
    def test_module_plan_normalizes_name(self) -> None:
        plan = module_plan("Credit_Risk_MLOps")

        self.assertEqual(plan.module_name, "credit-risk-mlops")
        self.assertIn("credit-risk-mlops/README.md", plan.files)

    def test_to_markdown_lists_files(self) -> None:
        plan = module_plan("banking-rag-agent")

        markdown = plan.to_markdown()

        self.assertIn("# Scaffold plan for `banking-rag-agent`", markdown)
        self.assertIn("- `banking-rag-agent/Dockerfile`", markdown)

    def test_empty_module_name_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            module_plan("   ")

    def test_delivery_files_are_included(self) -> None:
        plan = module_plan("credit-risk-mlops")

        self.assertIn("credit-risk-mlops/docker-compose.yml", plan.files)
        self.assertIn("credit-risk-mlops/.github/workflows/ci.yml", plan.files)
        self.assertIn("credit-risk-mlops/docs/interview-notes.md", plan.files)


if __name__ == "__main__":
    unittest.main()

