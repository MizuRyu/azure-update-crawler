import requests
from bs4 import BeautifulSoup
import logging

class WebCrawler:
    def __init__(self, headers=None, timeout=10):
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (compatible, WebCrawler/1.0)'
        }
        self.timeout = timeout

    def fetch_content(self, url: str) -> str:
        try:
            logging.info(f'{url}のフェッチを開始します')
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            logging.debug(f'フェッチ: HTTPステータスコード: {response.status_code}')
            logging.debug(f'フェッチ: レスポンス: {response.text}')
            logging.info(f'{url}のフェッチに成功しました。')
            return response.text
        except requests.exceptions.RequestException as e:
            logging.error(f'{url}のフェッチに失敗しました。')
            logging.error(e)
            raise

    def parse_content(self, content: str):
        try:
            logging.info('HTMLのパースを開始します')
            soup = BeautifulSoup(content, 'html.parser')
            text = soup.get_text(separator='\n', strip=True)
            logging.info('HTMLのパースに成功しました。')
            return text
        except Exception as e:
            logging.error('HTMLのパースに失敗しました。')
            logging.error(e)
            raise
