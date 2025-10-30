class SoupReplacer:

    def __init__(self, og_tag=None, alt_tag=None, name_xformer=None, attrs_xformer=None, xformer=None):
        self.og_tag = og_tag.strip().lower() if og_tag else None
        self.alt_tag = alt_tag.strip().lower() if alt_tag else None
        self.name_xformer = name_xformer
        self.attrs_xformer = attrs_xformer
        self.xformer = xformer

    def name_xform(self, tag):
        return self.name_xformer(tag) if self.name_xformer else tag.name

    def attrs_xform(self, tag):
        return self.attrs_xformer(tag) if self.attrs_xformer else tag.attrs

    def xform(self, tag):
        if self.xformer:
            self.xformer(tag)
