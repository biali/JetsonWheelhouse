import subprocess
import tempfile
import unittest
from pathlib import Path


class BuildSimpleIndexTests(unittest.TestCase):
    def test_generates_root_and_package_pages(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            packages_dir = base / "packages"
            simple_dir = base / "simple"
            packages_dir.mkdir()

            wheel = "my_pkg-1.0.0-py3-none-any.whl"
            (packages_dir / wheel).write_text("placeholder", encoding="utf-8")

            result = subprocess.run(
                [
                    "python3",
                    "scripts/build_simple_index.py",
                    "--packages-dir",
                    str(packages_dir),
                    "--simple-dir",
                    str(simple_dir),
                ],
                cwd=Path(__file__).resolve().parents[1],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((simple_dir / "index.html").exists())
            self.assertTrue((simple_dir / "my-pkg" / "index.html").exists())


if __name__ == "__main__":
    unittest.main()
