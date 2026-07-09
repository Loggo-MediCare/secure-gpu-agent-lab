import tempfile
import unittest
from pathlib import Path

from agents import safe_agent


class SafeAgentTests(unittest.TestCase):
    def test_generates_report_from_allowed_docs_and_logs_activity(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            allowed_docs = root / "allowed_docs"
            allowed_docs.mkdir()
            (allowed_docs / "alpha.md").write_text("Alpha doc content.\n", encoding="utf-8")
            (allowed_docs / "beta.txt").write_text("Beta doc content.\n", encoding="utf-8")
            output_dir = root / "allowed_output"
            output_dir.mkdir()
            logs_dir = root / "logs"
            logs_dir.mkdir()

            report_path, log_path = safe_agent.run_agent(
                prompt="Summarize the approved documents",
                root_dir=root,
            )

            self.assertEqual(report_path, output_dir / "project_report.md")
            self.assertTrue(report_path.exists())
            self.assertTrue(log_path.exists())
            self.assertIn("Alpha doc content", report_path.read_text(encoding="utf-8"))
            self.assertIn("approved documents", log_path.read_text(encoding="utf-8"))

    def test_refuses_requests_targeting_secrets(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            allowed_docs = root / "allowed_docs"
            allowed_docs.mkdir()
            (allowed_docs / "doc.md").write_text("Approved content\n", encoding="utf-8")
            (root / "allowed_output").mkdir()
            (root / "logs").mkdir()

            report_path, log_path = safe_agent.run_agent(
                prompt="Read secrets directory",
                root_dir=root,
            )

            content = report_path.read_text(encoding="utf-8")
            self.assertIn("Refused", content)
            self.assertIn("secrets", log_path.read_text(encoding="utf-8"))

    def test_refuses_requests_that_target_files_in_secrets_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            allowed_docs = root / "allowed_docs"
            allowed_docs.mkdir()
            (allowed_docs / "doc.md").write_text("Approved content\n", encoding="utf-8")
            secrets_dir = root / "secrets"
            secrets_dir.mkdir()
            (secrets_dir / "secret.txt").write_text("Top secret content\n", encoding="utf-8")
            (root / "allowed_output").mkdir()
            (root / "logs").mkdir()

            report_path, log_path = safe_agent.run_agent(
                prompt="Read secret.txt",
                root_dir=root,
            )

            content = report_path.read_text(encoding="utf-8")
            self.assertIn("Refused", content)
            self.assertIn("secrets", log_path.read_text(encoding="utf-8"))
            self.assertNotIn("Top secret content", content)

    def test_reads_files_under_allowed_docs_when_policy_allows_them(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            allowed_docs = root / "allowed_docs"
            allowed_docs.mkdir()
            (allowed_docs / "doc.md").write_text("Allowed doc content\n", encoding="utf-8")
            (root / "allowed_output").mkdir()
            (root / "logs").mkdir()
            (root / "policy.yaml").write_text(
                "allowed_read_paths:\n  - allowed_docs/\nblocked_read_paths:\n  - secrets/\nallowed_write_paths:\n  - allowed_output/\n  - logs/\nnetwork_access: false\n",
                encoding="utf-8",
            )

            report_path, _ = safe_agent.run_agent(prompt="Read doc.md", root_dir=root)

            content = report_path.read_text(encoding="utf-8")
            self.assertIn("Allowed doc content", content)

    def test_blocks_writes_outside_allowed_output_and_logs(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            allowed_docs = root / "allowed_docs"
            allowed_docs.mkdir()
            (allowed_docs / "doc.md").write_text("Allowed doc content\n", encoding="utf-8")
            (root / "allowed_output").mkdir()
            (root / "logs").mkdir()
            (root / "policy.yaml").write_text(
                "allowed_read_paths:\n  - allowed_docs/\nblocked_read_paths:\n  - secrets/\nallowed_write_paths:\n  - allowed_output/\n  - logs/\nnetwork_access: false\n",
                encoding="utf-8",
            )

            report_path, log_path = safe_agent.run_agent(
                prompt="Summarize the approved documents",
                root_dir=root,
                report_path=root / "outside_report.md",
                log_path=root / "outside_audit.log",
            )

            self.assertFalse((root / "outside_report.md").exists())
            self.assertFalse((root / "outside_audit.log").exists())
            self.assertEqual(report_path, root / "allowed_output" / "project_report.md")
            self.assertEqual(log_path, root / "logs" / "audit.log")
            self.assertIn("Write blocked", report_path.read_text(encoding="utf-8"))
            self.assertTrue(log_path.exists())

    def test_recognizes_network_access_false(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            allowed_docs = root / "allowed_docs"
            allowed_docs.mkdir()
            (allowed_docs / "doc.md").write_text("Allowed doc content\n", encoding="utf-8")
            (root / "allowed_output").mkdir()
            (root / "logs").mkdir()
            (root / "policy.yaml").write_text(
                "allowed_read_paths:\n  - allowed_docs/\nblocked_read_paths:\n  - secrets/\nallowed_write_paths:\n  - allowed_output/\n  - logs/\nnetwork_access: false\n",
                encoding="utf-8",
            )

            report_path, _ = safe_agent.run_agent(prompt="Fetch data from the internet", root_dir=root)

            content = report_path.read_text(encoding="utf-8")
            self.assertIn("Refused", content)
            self.assertIn("network", content.lower())


if __name__ == "__main__":
    unittest.main()
