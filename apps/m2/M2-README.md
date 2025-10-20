# Milestone-2

Jump to:
- [Part 1](#part-1)
- [Part 2](#part-2)
- [Part 3](#part-3)

## Part 1

Jump to:
- [task2](#task2)
- [task3](#task3)
- [task4](#task4)

### task2
> Print out all the hyperlinks (a tags).

This task is accomplished by parsing the BeautifulSoup tree using the strainer '''SoupStrainer("a")'''

To run task2, run the following command from the command line, substituting in the appropriate file name:

```python task2.py <input_html_or_xml_file>```

For example, I ran the following command, targeting large_sample_file_2.html (here, I provided the full path to the 
file used in milestone-1, so as to reduce copying):

```python task2.py "C:\Users\19493\Desktop\UCI\SWE262P-SWStyles\SWE262PProject\Milestone-1\sample_files\large_sample_file_2.html"```

The output should appear similar to:
```html
(bs4) C:\Users\19493\Desktop\UCI\SWE262P-SWStyles\SWE262PProject\beautifulsoup\apps\m2>python task2.py "C:\Users\19493\Desktop\UCI\SWE262P-SWStyles\SWE262PProject\Milestone-1\sample_files\large_sample_file_2.html"
<a class="mw-jump-link" href="#bodyContent">Jump to content</a>
<a accesskey="z" href="/wiki/Main_Page" title="Visit the main page [z]"><span>Main page</span></a>
<a href="/wiki/Wikipedia:Contents" title="Guides to browsing Wikipedia"><span>Contents</span></a>
<a href="/wiki/Portal:Current_events" title="Articles related to current events"><span>Current events</span></a>
<a accesskey="x" href="/wiki/Special:Random" title="Visit a randomly selected article [x]"><span>Random article</span></a>
<a href="/wiki/Wikipedia:About" title="Learn about Wikipedia and how it works"><span>About Wikipedia</span></a>
<a href="//en.wikipedia.org/wiki/Wikipedia:Contact_us" title="How to contact Wikipedia"><span>Contact us</span></a>
<a href="/wiki/Help:Contents" title="Guidance on how to use and edit Wikipedia"><span>Help</span></a>
<a href="/wiki/Help:Introduction" title="Learn how to edit Wikipedia"><span>Learn to edit</span></a>
<a href="/wiki/Wikipedia:Community_portal" title="The hub for editors"><span>Community portal</span></a>
<a accesskey="r" href="/wiki/Special:RecentChanges" title="A list of recent changes to Wikipedia [r]"><span>Recent changes</span></a>
<a href="/wiki/Wikipedia:File_upload_wizard" title="Add images or other media for use on Wikipedia"><span>Upload file</span></a>
<a href="/wiki/Special:SpecialPages"><span>Special pages</span></a>
<a class="mw-logo" href="/wiki/Main_Page">
...
```

### task3
> Print out all the tags in the document.

Since we are interested in all tags in the document, there is not really anything to filter out (other than text, 
comments, et cetera). Therefore, we can accomplish this by simply straining for anything that has a name, using the
strainer ```SoupStrainer(name=True)```. 

Since there are many tags in the large documents we will target, I simplified the output to only print the tag name, using
```tag.name```. See Milestone-1 for more info.

To run task3, run the following command from the command line, substituting in the appropriate file name:

```python task3.py <input_html_or_xml_file>```

For example, I ran the following command, targeting large_sample_file_2.html (here, I provided the full path to the 
file used in milestone-1, so as to reduce copying):

```python task3.py "C:\Users\19493\Desktop\UCI\SWE262P-SWStyles\SWE262PProject\Milestone-1\sample_files\large_sample_file_2.html"```

The output should appear similar to:
```html
(bs4) C:\Users\19493\Desktop\UCI\SWE262P-SWStyles\SWE262PProject\beautifulsoup\apps\m2>python task3.py "C:\Users\19493\Desktop\UCI\SWE262P-SWStyles\SWE262PProject\Milestone-1\sample_files\large_sample_file_2.html"
html
head
meta
title
script
script
link
script
meta
link
meta
meta
meta
meta
...
```

### task4

> Print out all the tags that have an id attribute. (this should be done with a single API call)

This task is achieved similarly to the previous tasks, but with the strainer defined as  
```SoupStrainer(attrs={"id": True})```. Since tags with ids may contain large subtrees, I simplified the output to 
only print the tag name and id in the form ```"Tag '<tag.name>' has id '<tag.id>'"```. See Milestone-1 for more info.

To run task4, run the following command from the command line, substituting in the appropriate file name:

```python task4.py <input_html_or_xml_file>```

For example, I ran the following command, targeting large_sample_file_2.html (here, I provided the full path to the 
file used in milestone-1, so as to reduce copying):

```python task4.py "C:\Users\19493\Desktop\UCI\SWE262P-SWStyles\SWE262PProject\Milestone-1\sample_files\large_sample_file_2.html"```

The output should appear similar to:
```
(bs4) C:\Users\19493\Desktop\UCI\SWE262P-SWStyles\SWE262PProject\beautifulsoup\apps\m2>python task4.py "C:\Users\19493\Desktop\UCI\SWE262P-SWStyles\SWE262PProject\Milestone-1\sample_files\large_sample_file_2.html"
Tag 'div' has id 'vector-main-menu-dropdown'
Tag 'div' has id 'p-search'
Tag 'div' has id 'p-vector-user-menu-preferences'
Tag 'div' has id 'p-vector-user-menu-userpage'
Tag 'div' has id 'vector-appearance-dropdown'
Tag 'div' has id 'p-vector-user-menu-notifications'
Tag 'div' has id 'p-vector-user-menu-overflow'
Tag 'div' has id 'vector-user-links-dropdown'
Tag 'div' has id 'siteNotice'
Tag 'div' has id 'mw-navigation'
Tag 'nav' has id 'mw-panel-toc'
Tag 'main' has id 'content'
Tag 'footer' has id 'footer'
Tag 'div' has id 'vector-sticky-header'
Tag 'div' has id 'p-dock-bottom'
```

## Part 2

Included here are all of the API Calls, along with their corresponding files, locations, and starting line numbers.
I also included some additional non-API calls that I felt were interesting to note, such as attrs={} typing.

| API Call/<br/>Other interesting things |      File       |               Location                | Line Number |
|:--------------------------------------:|:---------------:|:-------------------------------------:|:-----------:|
|        BeautifulSoup(f, parser)        | bs4/__init__.py |  bs4.__init__.BeautifulSoup.__init__  |     209     |
|              *.prettify()              | bs4/element.py  |       bs4.element.Tag.prettify        |    2601     |
|              *.find_all()              | bs4/element.py  |       bs4.element.Tag.find_all        |    2715     |
|                tag.name                | bs4/element.py  |       bs4.element.Tag.__init__        |    1648     |
|                attrs={}                | bs4/_typing.py  |   bs4._typing._StrainableAttributes   |     188     |
|            *.find_parent()             | bs4/element.py  |  bs4.element.PageElement.find_parent  |     992     |
|              *.get_text()              | bs4/element.py  |   bs4.element.PageElement.get_text    |     524     |
|              *.new_tag()               | bs4/__init__.py |  bs4.__init__.BeautifulSoup.new_tag   |     682     |
|          *.decode_contents()           | bs4/element.py  |    bs4.element.Tag.decode_contents    |    2619     |
|               *.append()               | bs4/element.py  |        bs4.element.Tag.append         |    2046     |
|            *.replace_with()            | bs4/element.py  | bs4.element.PageElement.replace_with  |     552     |
|                *.get()                 | bs4/element.py  |          bs4.element.Tag.get          |    2160     |
|                *.find()                | bs4/element.py  |         bs4.element.Tag.find          |    2684     |
|            *.next_siblings             | bs4/element.py  | bs4.element.PageElement.next_siblings |    1162     |
|             SoupStrainer()             | bs4/filter.py   |   bs4.filter.SoupStrainer.__init__    |     345     |


## Part 3