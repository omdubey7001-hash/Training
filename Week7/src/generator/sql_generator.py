# src/generator/sql_generator.py

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import re

MODEL_NAME = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"


class SQLGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto"
        )

    def _extract_sql(self, text: str) -> str:
        """
        Robust SQL extractor:
        - Removes explanations / OUTPUT text
        - Extracts first valid SELECT statement
        """

        # Remove everything before SQL:
        if "SQL:" in text:
            text = text.split("SQL:", 1)[1]

        # Regex to capture SELECT ... ;
        match = re.search(
            r"(SELECT\s+.*?;)",
            text,
            re.IGNORECASE | re.DOTALL
        )

        if not match:
            raise ValueError("❌ No valid SQL found in LLM output")

        sql = match.group(1).strip()
        return sql

    def generate(self, question: str, schema: str) -> str:
        """
        Convert natural language → SQL
        """

        prompt = f"""
You are an expert SQL generator.

DATABASE SCHEMA:
{schema}

STRICT RULES:
- Output ONLY a valid SQL query
- Start with SELECT
- Do NOT explain anything
- Do NOT add words like OUTPUT, RESULT, NOTE
- Use table and column names exactly from schema
- End the query with ;

QUESTION:
{question}

SQL:
"""

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            output = self.model.generate(
                **inputs,
                max_new_tokens=150,
                do_sample=False
            )

        decoded = self.tokenizer.decode(output[0], skip_special_tokens=True)

        sql = self._extract_sql(decoded)
        return sql
