import os
import pandas as pd


class FileTool:

    def read_file(self, path):

        if not os.path.exists(path):
            return {"success": False, "error": "File not found"}

        if path.endswith(".csv"):
            df = pd.read_csv(path)
            return {
                "success": True,
                "preview": df.head().to_string(),
                "columns": list(df.columns)
            }

        else:
            with open(path, "r") as f:
                return {
                    "success": True,
                    "content": f.read()[:2000]
                }

    def write_file(self, path, content):

        with open(path, "w") as f:
            f.write(content)

        return {"success": True}