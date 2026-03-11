import subprocess
import tempfile
import os


class CodeExecutor:

    def run_python(self, code: str):

        try:

            with tempfile.NamedTemporaryFile(
                suffix=".py",
                delete=False
            ) as tmp:

                tmp.write(code.encode())
                tmp_path = tmp.name

            result = subprocess.run(
                ["python", tmp_path],
                capture_output=True,
                text=True,
                timeout=20
            )

            os.unlink(tmp_path)

            return {
                "success": True,
                "stdout": result.stdout,
                "stderr": result.stderr
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
