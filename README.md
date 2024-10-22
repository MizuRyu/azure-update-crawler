## Azure Update Info Crawler

### 対象WEB URL
今後更新予定。
- Azure Updates<br>
  https://azure.microsoft.com/ja-jp/updates/

### SetUp
`.env`を作成し、以下を記述。<br>
`AZURE_OPENAI_API_ENDPOINT` <br>
`AZURE_OPENAI_API_KEY`

### ローカル実行 (Windows)
`python -m venv venv` <br>

`pip install -r requirements.txt` <br>

`source venv/Scripts/activate` <br>

`python main.py --debug` <br>

>--debug
  logLevelをDEBUGに設定（実行ログの確認）

