import argparse
import os
import yaml
import logging

from dotenv import load_dotenv

from crawler.crawler import WebCrawler
from differ.differ import ContentDiffer
from summarizer.summarizer import ContentSummarizer
from utils.logger import get_logger

load_dotenv()

# ログ設定
def setup_logging(log_level=logging.INFO):
    logger = get_logger(level=log_level)
    return logger

# クロール対象URLリストの読み込み
def load_config():
    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config

# ファイルの存在確認
def ensure_directories():
    os.makedirs('data/previous', exist_ok=True)
    os.makedirs('data/current', exist_ok=True)

def main():
    # --debugでデバッグモード
    parser = argparse.ArgumentParser(description="Web Crawler")
    parser.add_argument('--debug', action='store_true', help='Debug mode')
    args = parser.parse_args()

    log_level = logging.DEBUG if args.debug else logging.INFO
    logger = setup_logging(log_level)
    config = load_config()
    ensure_directories()

    urls = config.get('urls', [])

    aoai_api_endpoint = os.getenv('AZURE_OPENAI_API_ENDPOINT')
    aoai_api_key = os.getenv('AZURE_OPENAI_API_KEY')
    deployment_name = "gpt-4o-mini"

    crawler = WebCrawler()
    summarizer = ContentSummarizer(api_key=aoai_api_key, endpoint=aoai_api_endpoint, deployment_name=deployment_name)
    summarizer.deployment_name = deployment_name

    for url in urls:
        logger.info(f"{url}のクロールを開始します")
        
        filename = url.replace('https://', '').replace('http://', '').replace('/', '_').replace(':', '_')
        prev_path = f'data/previous/{filename}.txt'
        current_path = f'data/current/{filename}.txt'

        # 前回のコンテンツがあれば、取得
        if os.path.exists(prev_path):
            with open(prev_path, 'r', encoding='utf-8') as f:
                prev_content = f.read()
        else:
            prev_content = ''

        try:
            html = crawler.fetch_content(url)
            current_content = crawler.parse_content(html)
        except Exception as e:
            logger.error(f"{url}のクロールに失敗しました。")
            logger.error(e)
            continue
        
        with open(current_path, 'w', encoding='utf-8') as f:
            f.write(current_content)
        
        # 差分チェック
        differ = ContentDiffer(prev_content, current_content)
        if differ.has_changes():
            diff_text = differ.get_diff()

            # 要約
            try:
                pass
                summary = summarizer.summarize(diff_text)
                logging.info(f"{url}の要約: {summary}")
            except Exception as e:
                logger.error(f"{url}の要約に失敗しました。")
                logger.error(e)
                raise
        else:
            logger.info(f"{url}に変更はありません。")

        # 前回のコンテンツを更新
        with open(prev_path, 'w', encoding='utf-8') as f:
            f.write(current_content)

if __name__ == '__main__':
    main()