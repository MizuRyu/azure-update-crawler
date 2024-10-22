import difflib
import logging

class ContentDiffer:
    def __init__(self, old_content: str, new_content: str):
        self.old_content = old_content.splitlines()
        self.new_content = new_content.splitlines()
        self.diff = None
        logging.debug('=== # start コンテンツの比較 ===')

    def compare(self):
        differ = difflib.Differ()
        self.diff = list(differ.compare(self.old_content, self.new_content))
        logging.debug(f'差分: {self.diff}')
        logging.info('コンテンツの比較が完了しました。')
    
    def has_changes(self):
        if self.diff is None:
            self.compare()
        changes = [line for line in self.diff if line.startswith('+ ') or line.startswith('- ')]
        logging.debug(f'変更行: {changes}')
        return len(changes) > 0
    
    def get_diff(self):
        if self.diff is None:
            self.compare()
        diff_text = '\n'.join([line for line in self.diff if line.startswith('+ ') or line.startswith('- ')])
        logging.debug(f'変更差分: {diff_text}')
        logging.info('差分の取得が完了しました。')
        logging.debug('=== # end コンテンツの比較 ===')
        return diff_text