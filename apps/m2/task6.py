import sys
from pathlib import Path

from bs4 import BeautifulSoup, SoupReplacer


def task6():
    # Usage: python task6.py <input_html_or_xml_file> <output_file>
    # E.g., python task6.py "C:\Users\19493\Desktop\UCI\SWE262P-SWStyles\SWE262PProject\Milestone-1\sample_files\small_sample_file_2.html" "C:\Users\19493\Desktop\UCI\SWE262P-SWStyles\SWE262PProject\Milestone-1\output_files\small_sample_file_2.html"

    # Check if arguments are provided
    if len(sys.argv) != 3:
        print("Usage: python task6.py <input_html_or_xml_file> <output_file>")
        sys.exit(1)

    # Grab input and output files from args
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Determine which parser to use
    parser = "xml" if input_file.lower().endswith(".xml") else "html.parser"

    # Define the replacer
    b_to_blockquote = SoupReplacer("b", "blockquote")

    # Parse the input file using the strainer
    with open(input_file, "r", encoding="utf-8", errors="replace") as f:
        soup_tree = BeautifulSoup(f, parser, replacer=b_to_blockquote)

    # Prettify the output
    prettified_output_string = soup_tree.prettify()

    # Write the prettified output to the output file, creating directories if needed
    output_file = Path(output_file)
    output_file.parent.mkdir(exist_ok=True, parents=True)
    output_file.write_text(prettified_output_string)

if __name__ == "__main__":
    task6()