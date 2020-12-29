import gspread


class Gsheet:
    """Google spreadsheet document class"""

    key = '1MJbDJzx8JHVbe9aH--FqkW34eDUczF9WnQvFq9szrzs'  # development
    gc = None

    def __init__(self, key=key):
        self.key = key
        self.gc = gspread.service_account()

    def get_wb(self):
        return self.gc.open_by_key(self.key)
