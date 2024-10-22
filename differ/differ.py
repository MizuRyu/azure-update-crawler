import difflib
import logging

class ContentDiffer:
    def __init__(self, old_content: list, new_content: str):
        self.old_content = old_content
        self.new_content = new_content
        self.diff = None
        logging.debug('=== # start コンテンツの比較 ===')

    def compare(self):
        # 新規記事を抽出
        old_urls = {item['url'] for item in self.old_content}
        new_articles = [item for item in self.new_content if item['url'] not in old_urls]
        self.diff = new_articles
        logging.debug(f'新規記事(差分): {new_articles}')
        logging.info('コンテンツの比較が完了しました。')
    
    def has_changes(self):
        if self.diff is None:
            self.compare()
        return len(self.diff) > 0
    
    def get_diff(self):
        if self.diff is None:
            self.compare()
        logging.info('差分の取得が完了しました。')
        logging.debug('=== # end コンテンツの比較 ===')
        return self.diff