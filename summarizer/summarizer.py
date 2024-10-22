import logging
from openai import AzureOpenAI

SYSTEM = "system"
USER = "user"

SYSTEM_PROMPT = """
あなたは要約に特化したエキスパートです。以下の文章を要約してください。
"""

class ContentSummarizer:
    def __init__(self, api_key: str, endpoint: str, deployment_name: str):
        self.api_type = "azure"
        self.aoai_api_key = api_key
        self.aoai_api_endpoint = endpoint
        self.aoai_api_version = "2024-05-01-preview"
        self.deployment_name = deployment_name or "gpt-4o-mini"   
        self.aoai_client = AzureOpenAI(
            azure_endpoint=self.aoai_api_endpoint,
            api_key=self.aoai_api_key,
            api_version=self.aoai_api_version,
        )
    
    def summarize(self, text: str) -> str:
        try:
            response = self.aoai_client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {
                        "role": SYSTEM,
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": USER,
                        "content": text,
                    }
                ]
            )
            summary_text = response.choices[0].message.content
            logging.debug(f'生成された文章: {summary_text}')
            logging.info('要約の生成に成功しました。')
            return summary_text
        except Exception as e:
            logging.error('要約の生成に失敗しました。')
            logging.error(e)
            raise