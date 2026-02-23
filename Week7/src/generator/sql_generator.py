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

        match = re.search(
            r"(SELECT\s+.*?)(;|$)",
            text,
            re.IGNORECASE | re.DOTALL
        )

        if not match:
            print("\nDEBUG LLM OUTPUT:\n", text)
            raise ValueError("No valid SQL found in LLM output")

        sql = match.group(1).strip()
        if not sql.endswith(";"):
            sql += ";"

        return sql


    def generate(self, question: str, schema: str) -> str:
        """
        Convert natural language → SQL
        """

        prompt = f"""
<|system|>
You generate SQL queries only.

<|user|>
DATABASE SCHEMA:
{schema}

Rules:
- Output ONLY SQL
- Start with SELECT
- End with ;
- No explanation

Question:
{question}

<|assistant|>
"""


        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            output = self.model.generate(
                **inputs,
                max_new_tokens=120,
                temperature=0.2,
                top_p=0.9,
                repetition_penalty=1.2,
                do_sample=True,
                eos_token_id=self.tokenizer.eos_token_id
            )


        gen_tokens = output[0][inputs["input_ids"].shape[1]:]
        decoded = self.tokenizer.decode(gen_tokens, skip_special_tokens=True)

        sql = self._extract_sql(decoded)
        return sql
