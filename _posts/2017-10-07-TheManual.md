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

### man2html
- There are two different fundamental man2html programs, both from around the early/mid 90s. One is a C program that is quite fast and does not rely on groff/troff, but has 'quirky internals'. The other is a Perl script that reads already formatted (by groff/troff/nroff) manpages and outputs them to pretty good HTML.
- [This Unix stackexchange post has several very good posts on the topic](https://unix.stackexchange.com/questions/246888/how-do-i-convert-linux-man-pages-to-html-without-using-groff)
- [A very good post by Thomas Dickey on the changes he made to Perl man2html](http://invisible-island.net/scripts/man2html.html)
- [The page for VH-man2html, one of the original enhancements to C man2html](http://users.actrix.gen.nz/michael/vhman2html.html)


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

### pypub initial
- The tutorial is 5 lines of code! The abstractions in pypub make starting much easier.
- Its output did not have the inclusion of all the "\n" characters. Pypub does say that its HTML/XHTML import functions try to sanitize the input, so I assume the newline characters are being sanitized out.
- The main formatting problem is that the options sections (-D, -e, -A, etc with descriptions) was completely mangled into one paragraph. In ebooklib's version of the Apache docs the options displayed fine (except for all the '\n's that are in the whole document)



