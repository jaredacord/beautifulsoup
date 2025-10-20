import sys

from bs4 import SoupStrainer, BeautifulSoup


def task4():
    # Usage: python task4.py <input_html_or_xml_file>
    # E.g., python task4.py "C:\Users\19493\Desktop\UCI\SWE262P-SWStyles\SWE262PProject\Milestone-1\sample_files\large_sample_file_2.html"

    # Check if arguments are provided
    if len(sys.argv) != 2:
        print("Usage: python task4.py <input_html_or_xml_file>")
        sys.exit(1)

    # Grab input files from arg
    input_file = sys.argv[1]

    # Determine which parser to use
    parser = "xml" if input_file.lower().endswith(".xml") else "html.parser"

    # Define the strainer
    # See https://beautiful-soup-4.readthedocs.io/en/latest/#parsing-only-part-of-a-document
    only_tags_with_id = SoupStrainer(attrs={"id": True})

    # Parse the input file using the strainer
    with open(input_file, "r", encoding="utf-8", errors="replace") as f:
        soup_tree = BeautifulSoup(f, parser, parse_only=only_tags_with_id)

    # Print the hyperlinks (ie, everything parsed into soup_tree)
    for tag in soup_tree:
        print("Tag '{}' has id '{}'".format(tag.name, tag.get("id")))

if __name__ == "__main__":
    task4()