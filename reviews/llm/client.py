import os
import json

from huggingface_hub import InferenceClient

from .prompts import SYSTEM_PROMPT
from .parser import parse_llm_response


class LLMClient:

    def __init__(self):
        self.client = InferenceClient(
            token=os.getenv("HF_TOKEN")
        )

    def build_review_input(self, repository, pr_title, files):

        prompt = f"""
Repository:
{repository}

Title:
{pr_title}

Changed Files:
"""

        for file in files:
            prompt += f"""
Filename:
{file['filename']}

Status:
{file['status']}

Diff:
{file['patch']}
"""

        return prompt

    def review_code(self, repository, pr_title, files):

        user_prompt = self.build_review_input(
            repository,
            pr_title,
            files
        )

        response = self.client.chat_completion(
            model="Qwen/Qwen2.5-Coder-7B-Instruct",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            max_tokens=1000,
        )

        raw_output = response.choices[0].message.content

        # print(repr(raw_output))

        return parse_llm_response(raw_output)