# Milestone-3

Jump to:
- [Implementation](#implementation)
- [Tests](#tests)
- [task7](#task7)
- [Technical Brief](#technical-brief)

## Implementation

The implementation of this feature was pretty straight forward. I reused the initialize function from the previous 
milestone, such that SoupReplacer accepts the following arguments (defaults provided):
```SoupReplacer(og_tag=None, alt_tag=None, name_xformer=None, attrs_xformer=None, xformer=None)```. As such, I made 
some minor adjustments to the defaults and use of og_tag and alt_tag to accommodate the extra arguments, while preserving 
their functionality

Unlike with the og_tag/alt_tag logic, which was implemented within BeautifulSoup.handle_starttag, I chose to implement 
the logic within the SoupReplacer class by creating methods ```name_xform```, ```attrs_xform```, and ```xform```.
Each method accepts a tag as an argument, and applies the corresponding function to that tag if defined. For 
```name_xform``` and ```attrs_xform```, the name and attributes, respectively, are returned, while for ```xform```, 
nothing is returned, as the tag is modified in-place.

Within the BeautifulSoup.handle_starttag method, the methods described above are called in order (if the replacer 
is passed in) as so:
```
if self.replacer:
    tag.name = self.replacer.name_xform(tag)
    tag.attrs = self.replacer.attrs_xform(tag)
    self.replacer.xform(tag)
```

As such, the replacer is applied to the tag during parsing. Important to note is that the effects of one xform may impact 
effects of the subsequent ones. For example, if name_xform changes all p tags to b, then xform will not see any p tags 
and will not change them.

## Tests

For this milestone, I added the following 6 tests (18 test cases total) to test_replacer.py:

|              Test               | Tests Attribute |                                         Description                                         | 
|:-------------------------------:|:---------------:|:-------------------------------------------------------------------------------------------:|
|        test_name_xformer        |  name_xformer   | Replaces b tags with blockquote tags to confirm name_xformer replacer works with basic HTML |
| test_name_xformer_nestled_tags  |  name_xformer   |       Parametrized test which verifies name_xformer replacer works with nestled tags        |
|       test_attrs_xformer        |  attrs_xformer  |           Replaces attrs to confirm attrs_xformer replacer works with basic HTML            |
| test_attrs_xformer_nestled_tags |  attrs_xformer  |       Parametrized test which verifies attrs_xformer replacer works with nestled tags       |
|          test_xformer           |     xformer     |     Switches tags and removes classes to verify xformer replacer works with basic HTML      |
|   test_xformer_nestled_tags     |     xformer     |            Parametrized test which verifies xformer replacer works with nestled tags        |

As expected, all test cases (including test cases from Milestone 2) pass:
```html
============================= test session starts =============================
collecting ... collected 26 items

bs4/tests/test_replacer.py::TestReplacer::test_default_replacer PASSED   [  3%]
bs4/tests/test_replacer.py::TestReplacer::test_nestled_tags[<b>Some Text</b>-<blockquote>Some Text</blockquote>] PASSED [  7%]
bs4/tests/test_replacer.py::TestReplacer::test_nestled_tags[<b><b>Some Text</b></b>-<blockquote><blockquote>Some Text</blockquote></blockquote>] PASSED [ 11%]
...
bs4/tests/test_replacer.py::TestReplacer::test_xformer_nestled_tags[<p>Some Text</p>-<b>Some Text</b>] PASSED [ 92%]
bs4/tests/test_replacer.py::TestReplacer::test_xformer_nestled_tags[<p class="some_class">Some Text</p>-<b>Some Text</b>] PASSED [ 96%]
bs4/tests/test_replacer.py::TestReplacer::test_xformer_nestled_tags[<p class="some_class"><b class="some_class">Some Text</b></p>-<b><p>Some Text</p></b>] PASSED [100%]

============================= 26 passed in 0.34s ==============================
```

## task7

I implemented task7 by defining the following replacer ```replacer = SoupReplacer(xformer=add_test_class_to_p)```, using 
the method:
```
def add_test_class_to_p(tag):
    # Add a "test" class to all <p> tags
    if tag.name == "p":
        classes = tag.attrs.get("class", [])
        classes.append("test")
        tag.attrs["class"] = classes
```

To run task7, run the following command from the command line, substituting in the appropriate file name:

```python task7.py <input_html_or_xml_file> <output_file>```

For example, I ran the following command, targeting small_sample_file_3.html (here, I provided the full paths to the 
files used in milestone-1, so as to reduce copying):

```python task7.py "C:\Users\19493\Desktop\UCI\SWE262P-SWStyles\SWE262PProject\Milestone-1\sample_files\small_sample_file_3.html" "C:\Users\19493\Desktop\UCI\SWE262P-SWStyles\SWE262PProject\Milestone-1\output_files\small_sample_file_3.html"```

We see that, for the <p> tags from the input file:
```html
...
<p class="test">In this example, we have created a header, two columns/boxes and a footer. On smaller screens, the columns will stack on top of each other.</p>
<p>Resize the browser window to see the responsive effect (you will learn more about this in our next chapter - HTML Responsive.)</p>
...
    <p class="class1 class2">London is the capital city of England. It is the most populous city in the  United Kingdom, with a metropolitan area of over 13 million inhabitants.</p>
    <p class="">Standing on the River Thames, London has been a major settlement for two millennia, its history going back to its founding by the Romans, who named it Londinium.</p>
...
  <p>Footer</p>
...
```

The class 'test' is added:
```html
...
  <p class="test test">
   In this example, we have created a header, two columns/boxes and a footer. On smaller screens, the columns will stack on top of each other.
  </p>
  <p class="test">
   Resize the browser window to see the responsive effect (you will learn more about this in our next chapter - HTML Responsive.)
  </p>
...
    <p class="class1 class2 test">
     London is the capital city of England. It is the most populous city in the  United Kingdom, with a metropolitan area of over 13 million inhabitants.
    </p>
    <p class="test">
     Standing on the River Thames, London has been a major settlement for two millennia, its history going back to its founding by the Romans, who named it Londinium.
    </p>
...
   <p class="test">
    Footer
   </p>
```


## Technical Brief

This is a technical brief for extending the functionality of SoupReplacer from its implemetation in milestone-2 to
its implementation in milestone-3.

### Milestone 2

Current milestone-2 implementation accepts two parameters, og_tag and alt_tag, and directly substitutes each tag 
instance of og_tag with alt_tag while parsing. 

While this functionality is simple, intuitive, and requires a minimal learning curve, it is very limited. Its usage is 
restricted to a single tag name replacement, and does not support multiple tag name replacements, tag attribute 
replacement, multi-attribute replacements, tag attribute deletion or addition, or more complex tag manipulation on parsing.

### Milestone 3

To address the limitations on milestone-2, I propose extending the functionality of soup replacer with the following 
parameters: name_xformer, attrs_xformer, and xformer. 

These parameters will be defined as functions which accept the 
current tag when parsing as an argument and affect change in real time to that tag. The name_xformer parameter will apply the given 
function to the tag's name and return the modified name, while the attrs_xformer parameter will apply the function to 
the tag's attrs and return the modified attrs. The xformer function will not return anything, but rather apply the given 
function to the given tag object.

This approach will give users full control over tag manipulation on parsing, allowing for multiple tag name replacements, 
tag attribute replacements, multi-attribute replacements, tag attribute deletion or addition, and more complex tag manipulation on parsing. 

Additionally, by extending and not replacing the og_tag and alt_tag functionality, this approach will remain backwards 
compatible with usages of the implementation used in milestone-2.
