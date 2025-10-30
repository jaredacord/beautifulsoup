import pytest
import re
import warnings

from bs4 import SoupReplacer
from bs4.tests import SoupTest


class TestReplacer(SoupTest):

    html_basic = """<!DOCTYPE html>
                    <html>
                    <head><title>Page Title</title></head>
                    <body>
                    <h1>Some Header</h1>
                    <p><b>Bold Paragraph 1</b></p>
                    <p>Unbold Paragraph</p>
                    <p><b>Bold Paragraph 2</b></p>
                    <p><blockquote>Blockquote Paragraph</blockquote></p>
                    </body>
                    </html>"""

    def test_default_replacer(self):
        """
        Default sanity check test, to confirm that the replacer works with basic HTML
        """

        # Define replacer to replace <b> tags with <blockquote> tags
        replacer = SoupReplacer("b", "blockquote")

        # Confirm parsing without the replacer works
        soup = self.soup(self.html_basic)

        assert soup.find(string="Bold Paragraph 1").parent.name == "b"
        assert soup.find(string="Unbold Paragraph").parent.name == "p"
        assert soup.find(string="Bold Paragraph 2").parent.name == "b"
        assert soup.find(string="Blockquote Paragraph").parent.name == "blockquote"

        # Confirm parsing with the replacer works
        soup = self.soup(self.html_basic, replacer=replacer)

        assert soup.find(string="Bold Paragraph 1").parent.name == "blockquote"
        assert soup.find(string="Unbold Paragraph").parent.name == "p"
        assert soup.find(string="Bold Paragraph 2").parent.name == "blockquote"
        assert soup.find(string="Blockquote Paragraph").parent.name == "blockquote"

    @pytest.mark.parametrize(
        "input_markup,expected_output_markup",
        [
            ("<b>Some Text</b>", "<blockquote>Some Text</blockquote>"),
            ("<b><b>Some Text</b></b>", "<blockquote><blockquote>Some Text</blockquote></blockquote>"),
            ("<b><b><b>Some Text</b></b></b>", "<blockquote><blockquote><blockquote>Some Text</blockquote></blockquote></blockquote>"),
            ("<title><p><b>Some Text</b></p></title>", "<title><p><blockquote>Some Text</blockquote></p></title>"),
            ("<title><b><p>Some Text</p></b></title>", "<title><blockquote><p>Some Text</p></blockquote></title>"),
            ("<b><title><p>Some Text</p></title></b>", "<blockquote><title><p>Some Text</p></title></blockquote>"),
            ("<b><title><b>Some Text</b></title></b>", "<blockquote><title><blockquote>Some Text</blockquote></title></blockquote>"),
        ],
    )
    def test_nestled_tags(self, input_markup, expected_output_markup):
        """
        Test to confirm the replacer works with nested tags
        """

        replacer = SoupReplacer("b", "blockquote")
        assert self.soup(input_markup, replacer=replacer).decode() == expected_output_markup

    def test_name_xformer(self):
        """
        Confirm replacer with parameter name_xformer works with basic HTML
        """

        # define replacer to replace <b> tags with <blockquote> tags
        replacer = SoupReplacer(name_xformer=lambda tag: "blockquote" if tag.name == "b" else tag.name)

        # Confirm parsing without the replacer works
        soup = self.soup(self.html_basic)

        assert soup.find(string="Bold Paragraph 1").parent.name == "b"
        assert soup.find(string="Unbold Paragraph").parent.name == "p"
        assert soup.find(string="Bold Paragraph 2").parent.name == "b"
        assert soup.find(string="Blockquote Paragraph").parent.name == "blockquote"

        # Confirm parsing with the replacer works
        soup = self.soup(self.html_basic, replacer=replacer)

        assert soup.find(string="Bold Paragraph 1").parent.name == "blockquote"
        assert soup.find(string="Unbold Paragraph").parent.name == "p"
        assert soup.find(string="Bold Paragraph 2").parent.name == "blockquote"
        assert soup.find(string="Blockquote Paragraph").parent.name == "blockquote"

    @pytest.mark.parametrize(
        "input_markup,expected_output_markup",
        [
            ("<p>Some Text</p>", "<h2>Some Text</h2>"),
            ("<p><p>Some Text</p></p>", "<h2><h2>Some Text</h2></h2>"),
            ("<p><p><p>Some Text</p></p></p>", "<h2><h2><h2>Some Text</h2></h2></h2>"),
            ("<title><p><b>Some Text</b></p></title>", "<title><h2><b>Some Text</b></h2></title>"),
            ("<title><b><p>Some Text</p></b></title>", "<title><b><h2>Some Text</h2></b></title>"),
            ("<b><h2><p>Some Text</p></h2></b>", "<b><h2><h2>Some Text</h2></h2></b>"),
            ("<p><title><p>Some Text</p></title></p>", "<h2><title><h2>Some Text</h2></title></h2>"),
        ],
    )
    def test_name_xformer_nestled_tags(self, input_markup, expected_output_markup):
        """
        Confirm replacer with parameter name_xformer works with nested tags
        """

        # define replacer to replace <p> tags with <h2> tags
        replacer = SoupReplacer(name_xformer=lambda tag: "h2" if tag.name == "p" else tag.name)
        assert self.soup(input_markup, replacer=replacer).decode() == expected_output_markup

    def test_attrs_xformer(self):
        """
        Confirm replacer with parameter attrs_xformer works with basic HTML
        """

        # define replacer to set the attr to 'class="some_class" style="color: blue; font-size: 18px;"'
        replacer = SoupReplacer(attrs_xformer=
                                lambda tag: {"class":"some_class",  "style":"color: blue; font-size: 18px;"}
                                if tag.name == "p" else tag.attr)

        # Confirm parsing without the replacer works
        soup = self.soup(self.html_basic)

        for tag in soup.find_all('p'):
            assert tag.get('class') is None
            assert tag.get('style') is None

        # Confirm parsing with the replacer works
        soup = self.soup(self.html_basic, replacer=replacer)

        for tag in soup.find_all('p'):
            assert tag.get('class') == "some_class"
            assert tag.get('style') == "color: blue; font-size: 18px;"

    @pytest.mark.parametrize(
        "input_markup,expected_output_markup",
        [
            ('<p>Some Text</p>', '<p class="some_class" style="color: blue">Some Text</p>'),
            ('<p class="some_other_class">Some Text</p>', '<p class="some_class" style="color: blue">Some Text</p>'),
            ('<p><p>Some Text</p></p>', '<p class="some_class" style="color: blue"><p class="some_class" style="color: blue">Some Text</p></p>'),
            ('<title><p><b>Some Text</b></p></title>', '<title><p class="some_class" style="color: blue"><b>Some Text</b></p></title>'),
            ('<title><b><p>Some Text</p></b></title>', '<title><b><p class="some_class" style="color: blue">Some Text</p></b></title>'),

        ],
    )
    def test_attrs_xformer_nestled_tags(self, input_markup, expected_output_markup):
        """
        Confirm replacer with parameter attrs_xformer works with nested tags
        """

        replacer = SoupReplacer(attrs_xformer=
                                lambda tag: {"class": "some_class", "style": "color: blue"}
                                if tag.name == "p" else tag.attr)

        assert self.soup(input_markup, replacer=replacer).decode() == expected_output_markup

    def test_xformer(self):
        """
        Confirm replacer with parameter xformer works with basic HTML
        """

        # define replacer to switch <b> tags with <p> tags, and <p> tags with <b> tags
        def switch_tags(tag):
            if tag.name == "b":
                tag.name = "p"
            elif tag.name == "p":
                tag.name = "b"

        replacer = SoupReplacer(xformer=switch_tags)

        # Confirm parsing without the replacer works
        soup = self.soup(self.html_basic)

        assert soup.find(string="Bold Paragraph 1").parent.name == "b"
        assert soup.find(string="Unbold Paragraph").parent.name == "p"
        assert soup.find(string="Bold Paragraph 2").parent.name == "b"
        assert soup.find(string="Blockquote Paragraph").parent.name == "blockquote"

        # Confirm parsing with the replacer works
        soup = self.soup(self.html_basic, replacer=replacer)

        assert soup.find(string="Bold Paragraph 1").parent.name == "p"
        assert soup.find(string="Bold Paragraph 1").parent.parent.name == "b"
        assert soup.find(string="Unbold Paragraph").parent.name == "b"
        assert soup.find(string="Bold Paragraph 2").parent.name == "p"
        assert soup.find(string="Bold Paragraph 2").parent.parent.name == "b"
        assert soup.find(string="Blockquote Paragraph").parent.name == "blockquote"
        assert soup.find(string="Blockquote Paragraph").parent.parent.name == "b"

    @pytest.mark.parametrize(
        "input_markup,expected_output_markup",
        [
            ('<p>Some Text</p>', '<b>Some Text</b>'),
            ('<p class="some_class">Some Text</p>', '<b>Some Text</b>'),
            ('<p class="some_class"><b class="some_class">Some Text</b></p>', '<b><p>Some Text</p></b>'),
        ]
    )
    def test_xformer_nestled_tags(self, input_markup, expected_output_markup):
        """
        Confirm replacer with parameter xformer works with nested tags
        """

        # define replacer to remove class attribute, switch <b> tags with <p> tags, and <p> tags with <b> tags
        def switch_tags_remove_attrs(tag):
            if tag.name == "b":
                tag.name = "p"
            elif tag.name == "p":
                tag.name = "b"
            if "class" in tag.attrs:
                del tag.attrs["class"]

        replacer = SoupReplacer(xformer=switch_tags_remove_attrs)

        assert self.soup(input_markup, replacer=replacer).decode() == expected_output_markup