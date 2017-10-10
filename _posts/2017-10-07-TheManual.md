---
layout: post
title: "Making an EPUB eBook with All the Man Pages"
date: 2017-10-07
---

I've often been working on something, sometimes without an internet connection, and wished I could have the man pages available on my ereader. We have the technology, so why not?

## 0: So... how?

I figure to make this work we need to get all the manpages in a format appropriate for an ebook, and then write the code that will take those pages and insert them into an eBook (while building a table of contents of what it inserts).

The man pages are quite easy to find. Run `apropos ".*"` and you will get all the pages on your system.
Using `man -w` we can get the file location of all these manpages. 

Further along the pipeline we need a way of making an epub. I chose Python to do this as it is easy to use and has [good](http://ebooklib.readthedocs.io/en/latest/) [library](https://pythonism.wordpress.com/2013/11/08/making-ebooks-with-python/) [support](https://github.com/wcember/pypub)


## 1: Converting the man pages

with `man -P` the pager man uses can be changed to something like cat that will spit out the man page in plaintext. 

There are a [lot of ways](https://stackoverflow.com/questions/13433903/convert-all-linux-man-pages-to-text-html-or-markdown) [of converting man pages](https://unix.stackexchange.com/questions/246888/how-do-i-convert-linux-man-pages-to-html-without-using-groff) [to other formats](https://stackoverflow.com/questions/12768894/how-to-obtain-man-page-contents-in-python). These are the ones I've encountered so far:
- Use man2html perl script or variants (see notes on this)
- Use man2html C program or variants
- Extract the compressed manpage, send it to groff with -Thtml or -Tlatin1
- use man with -Hfirefox (This seems to be a newer option, and leverages groff)
- Use [man-to-github-pages](https://github.com/vbem/man-to-github-pages)
- Use cat as the pager to man (`man -P cat`)
- Cheat: Scrape the man pages already online on linux.die.net or man7.org/linux/man-pages/
- Use the mandoc utility from BSD (which seems exactly right for this purpose, but is actually too NEW for my version of Ubuntu, as its first inclusion was in 17.04)

### man2html
- There are two different fundamental man2html programs, both from around the early/mid 90s. One is a C program that is quite fast and does not rely on groff/troff, but has 'quirky internals'. The other is a Perl script that reads already formatted (by groff/troff/nroff) manpages and outputs them to pretty good HTML.
- [This Unix stackexchange post has several very good posts on the topic](https://unix.stackexchange.com/questions/246888/how-do-i-convert-linux-man-pages-to-html-without-using-groff)
- [A very good post by Thomas Dickey on the changes he made to Perl man2html](http://invisible-island.net/scripts/man2html.html)
- [The page for VH-man2html, one of the original enhancements to C man2html](http://users.actrix.gen.nz/michael/vhman2html.html)

### mandoc
- Installing the .deb for mandoc from 17.04 worked fine on my 16.04.3 LTS system


## 2: The EPUB format
- An epub file is essentially a ZIP archive of XHTML content with XML metadata. It supports all sorts of cool things like images, scripts, sound and video (in EPUB version 3)
- [This post from IBM developerWorks is a good overview of generating an EPUB for developers]
- [This post from OpticalAuthoring has good and simple descriptions of all the key parts of the EPUB](https://www.opticalauthoring.com/inside-the-epub-format-the-basics/)
- [This post on epubsecrets describes the EPUB standard and organization](http://epubsecrets.com/epub-the-language-of-ebooks-a-primer.php)

So we need XHTML or at least to pretend our format is XHTML. I thought this would be an issue given that the converters stop at HTML, but in the early 2000s many websites wanted to move from HTML to XHTML so [there are good converters like 'tidy' available](https://www.princexml.com/forum/topic/8/using-html-tidy-to-convert-html-to-xhtml). [People report that even on HTML that is already close to XHTML to tool can still do a good job of tidying it up](https://www.linuxquestions.org/questions/linux-software-2/html-to-xhtml-conversion-275038/).


## 3: Making an EPUB in Python
From a quick search two Python EPUB libraries came up:
- [ebooklib, which allows you control over all the bits of the epub](http://ebooklib.readthedocs.io/en/latest/)
- [pypub, which abstracts the various bits of the epub into generic functions](https://github.com/wcember/pypub)
- Both come with tutorials on how to get started. From what I can see in their docs, pypub does not support making sections (which could be very useful given we have 8000+ man pages in 9 sections) while ebooklib does.

Given the large number of pages, we definitely want a table of contents with hyperlinks to each man page. This means it makes sense to put each man page as its own chapter. Optimally, each chapter is in a section of the eBook corresponding to the section in the manual.


## 4: Testing
At this stage what we want to do is not tremendously complicated, so it is easy to test both epub libraries.
### ebooklib initial
- The tutorial was easy to setup but expanding beyond it posed difficulties. Adding a second chapter in the same manner as the first resulted in that chapter being opened in a web browser (from within the ebook). Using ebooklib will require some understanding of both the epub I want to generate and the workings of ebooklib.
- Using my test files (html and xhtml pages for Apache and Animate man pages), ebooklib's output had the odd inclusion of a lot of "\n" characters.
- Replacing \n and ', ' with nothing resulted in a much cleaner document with a tolerable amount of formatting oddities

### pypub initial
- The tutorial is 5 lines of code! The abstractions in pypub make starting much easier.
- Its output did not have the inclusion of all the "\n" characters. Pypub does say that its HTML/XHTML import functions try to sanitize the input, so I assume the newline characters are being sanitized out.
- The main formatting problem is that the options sections (-D, -e, -A, etc with descriptions) was completely mangled into one paragraph. In ebooklib's version of the Apache docs the options displayed fine (except for all the '\n's and a few other weird instances of punctuation)

### Picking a format
After a few tests with various HTML sources and ebook viewers I got some decent output by taking the output of mandoc and making a chapter out of with pypub. It is not perfect but is quite readable. 
So, the next step is to ramp up to doing that 8849 times.


## 5: Generation scripts
In not too much time I had scripts for generating all the HTML man pages, and then making an EPUB out of them.
I kept the generation to a Bash script as all the commands were terminal commands and minimal text processing was required at that point. Once all the man pages have been generated as HTML or XHTML, the Python script can be run and will take every manpage and create a chapter in the EPUB for it.

The bash script:

    # have to clobber the field seperator or else the loop splits up the parameters
    oldifs=$IFS; 
    IFS=$(echo -en "\n\b");
    # Have to call apropos with --long option to avoid name truncation
    echo "Converting man pages to (X)HTML..."
    for page in `apropos ".*" -l | cut -f "1,2" -d " " `; do
        # strip out the parenthesis around the section number
        page="${page//(}"; 
        page="${page//)}";
	    # swap the location of the name and section
        pagename=`echo $page | cut -d " " -f 1`;
        pagesection=`echo $page | cut -d " " -f 2`;
        page=$pagesection" "$pagename;
        # Get the location of the manpage then send it to mandoc
	    # Unclobber the IFS so man can work
	    IFS=$oldifs;
	    #echo $page
	    pagelocation=`man -w $page`;
	    mandoc -Thtml $pagelocation | tidy -asxhtml 1>"All_ManPages_HTML/$page.html" 2>/dev/null;
	    IFS=$(echo -en "\n\b");
    done
    echo "Done!"

    IFS=$OLDIFS

The Python script:

    import pypub

    class HTML_Sources(object):
	    def __init__(self, directory, extensions=["html", "xhtml"]):
		    # pages will be stored in list as {[str]name: [str]content}
		    self.HTML_Filenames = {}
		    self.HTML_Pages = {}
		    self._GetFilenames(directory, extensions)
		    self._GetPages()
	
	    # Go into the provided directory and get all the files with the right extensions
	    def _GetFilenames(self, directory, extensions):
		    from os import listdir
		    from os.path import isfile, join
		    print("Directory: " + directory)
		    directoryContents = [f for f in listdir(directory) if isfile(join(directory, f))]
		    self.HTML_Filenames = { name:join(directory, name) for name in directoryContents if name.split('.')[::-1][0] in extensions }
		    #print(self.HTML_Filenames)
	
	    # Take the list of filenames and read their content into the list of dicts
	    def _GetPages(self):
		    for filename in self.HTML_Filenames:
			    #print filename
			    self.HTML_Pages[ filename.split('.')[0] ] = "".join(open( self.HTML_Filenames[filename] ).readlines())
		    #print(self.HTML_Pages)
		    print("%d pages loaded"%len(self.HTML_Pages))


    class TheManual(object):
	    def __init__(self, verbose=True):
		    # Gets us a sources object with all the filenames and their content
		    self.Sources = HTML_Sources("All_ManPages_HTML")
		
		    # Set up the objects for the book
		    self.Book_EPUB = pypub.Epub("The Manual v1")
		
		    # Make the ebook
		    self.create_epub()

		
	    def create_epub(self):
		    Book_Chapters = []
		    Sorted_HTML_Pages = self.Sources.HTML_Pages.keys()
		    Sorted_HTML_Pages.sort()
		    for manpage in Sorted_HTML_Pages:
			    Title = manpage
			    Content = self.Sources.HTML_Pages[Title].replace("\\n", "").replace("', '", " ")#.replace("['", '').replace("']", '')
			    Book_Chapter = pypub.create_chapter_from_string(Content, title=Title)
			    self.Book_EPUB.add_chapter(Book_Chapter)
			
			    currentIndex = Sorted_HTML_Pages.index(manpage)
			    if( currentIndex % 100 == 0 ):
				    print("Done upto chapter: %d" %currentIndex )
		
		    self.Book_EPUB.create_epub("")
		    print("Book created!")
		
	
    TheManual()


The bash script takes about 1 minute to run, and the Python script about 7 minutes (with 8600 manpages to add as chapters). The process appears to be CPU-bound on an i5-5200U with a good SSD.

## 6: The Manual (v1)
The total size of all the HTML pages is about 107MB and the size of the eBook is 27MB so the .ZIP compression definitely makes a difference. As might be expected from an eBook with 100+MB of text, it takes a little while to load. Global searches through ALL the manpages are not instant but fast enough.

("The Manual v1.epub" can be downloaded here)[https://github.com/SuperThunder/SuperThunder.github.io/blob/master/content/Man2eBook/The%20Manual%20v1.epub]

There are some improvements that come immediately to mind:
- The option of which sections should be written to the eBook (for example, only using everyday sections like 1,4,5,6, and 7)
- Creating sections within the eBook for each manual section, under which each page is a chapter
- Make the actual pages look better - the man style formatting means the section headers (NAME, SYNOPSIS, DESCRIPTION, etc) are quite massive compared to the page name and text

### First set of changes
- Sort the pages alphabetically. The os.listdir module in Python does not perform any sorting, so the man pages were massively out of order
- Implement the per-section control of which pages should be included. The biggest advantage of this is the potential smaller file size being more manageable for eBook readers.
- Fix the bug that was causing every page to be encapsulated in [' '] (a result of using str() and not "".join() )

A few more improvements come to mind
- Profile the code to see if there are any obvious bottlenecks. The runtime is a little steep.
- Create command line options so it can be used with options without having to go in and change the code
- Allow for a list of which pages to use from the directory. This also allows for later features of making tailored manual ebook (most used pages, most useful for sysadmin, etc)

