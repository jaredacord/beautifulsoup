class SoupReplacer:

    def __init__(self, og_tag, alt_tag):
        self.og_tag = og_tag.strip().lower()
        self.alt_tag = alt_tag.strip().lower()
