import logging
import json

from openai import AzureOpenAI

SYSTEM = "system"
USER = "user"

SYSTEM_PROMPT = """
あなたの役割は、Azureの更新情報を日本語で端的に要約し、それに関連するワークロードを出力することです。
入力として与えられるJSON形式のデータから、指定された形式で出力を行ってください。出力は次の[要件]に基づく必要があります。

# 要件
- 必ず日本語で回答してください。
- 各アップデート内容に関連するワークロード（Infra / App / Data / AI）を特定し、出力してください。
- 以下の構造で出力してください：
"date": アップデートの日付（yyyy/mm/dd形式）
"category": 関連するワークロード（Infra / App / Data / AI）
"title": アップデートのタイトル
"url": アップデートのURL
"status": 機能のリリース状況
"description": アップデートの説明
- ワークロードの分類
Infra: インフラストラクチャー関連のアップデート（例: VM、ネットワーク、セキュリティ）
App: アプリケーション関連のアップデート（例: アプリ開発、API、ユーザーインターフェース）
Data: データ管理やストレージ関連のアップデート（例: データベース、バックアップ、データ分析）
AI: AIや機械学習に関連するアップデート（例: AIモデル、MLツール）
- 出力フォーマット（例）
以下の形式に従って出力を行ってください：
[  {    "date": "yyyy/mm/dd",    "category": "string",    "title": "string",    "url": "string",      "description": "string"  }]
- 複数のオブジェクトが含まれる場合、それらを一つの配列としてオブジェクトを返してください。

# Example
入力例
[  {    "date": "Oct 17",    "title": "Generally Available: ED25519 SSH key support for Linux VMs",    "url": "https://azure.microsoft.com/en-us/updates/v2/linux-sssh-ed25519",      "description": "We are excited to offer Azure customers highly secure and faster ED25519 SSH keys support for Linux Virtual Machines (VMs) in Azure."  }]
出力例
[  {    "date": "2023/10/17",    "category": "Infra",    "title": "一般提供開始: Linux VM向けED25519 SSHキーのサポート",    "url": "https://azure.microsoft.com/en-us/updates/v2/linux-sssh-ed25519",      "description": "Azureのお客様向けに、Linux仮想マシンでのよりセキュアで高速なED25519 SSHキーのサポートが提供されます。"  }]
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
    
    def summarize(self, data) -> str:
        logging.info(f'== 要約の生成を開始します ==')
        try:
            # JSON形式のデータをテキストに変換
            text = json.dumps(data, ensure_ascii=False)
            logging.debug(f'変換されたテキスト: {text}')
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

        finally:
            logging.info('== 要約の生成が完了しました ==')