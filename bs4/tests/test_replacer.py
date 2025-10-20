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
