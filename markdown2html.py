#!/usr/bin/python3
"""markdown2html.py - A quick & dirty Markdown > HTML compiler"""

import hashlib
import re
from sys import argv
from sys import exit

if __name__ == "__main__":

    if (len(argv) < 3):
        exit("Usage: ./markdown2html.py README.md README.html")

    if type(argv[1]) is str:
        try:
            with open(argv[1], "r") as fp:
                html = fp.readlines()
        except IOError:
            exit("Missing {:s}".format(argv[1]))

    # Flags for multi-line elements
    ulFlag = False
    olFlag = False
    pFlag = False

    # Main loop
    for i in range(len(html)):

        # Headings
        if html[i].strip().startswith("#"):
            lvl = html[i].split(" ")[0].count("#")
            content = html[i].split(" ", 1)[1].strip()
            if lvl <= 6:
                html[i] = "<h{0}>{1}</h{0}>\n".format(lvl, content)

        # Unordered lists
        if html[i].strip().startswith("- "):
            content = html[i].split(" ", 1)[1].strip()
            if not ulFlag:
                if pFlag:
                    html[i] = "</p>\n<ul>\n<li>{:s}</li>\n".format(content)
                else:
                    html[i] = "<ul>\n<li>{:s}</li>\n".format(content)
            else:
                html[i] = "<li>{:s}</li>\n".format(content)

            ulFlag = True

            if i + 1 >= len(html) or not html[i + 1].strip().startswith("- "):
                html[i] += "</ul>\n"
                ulFlag = False

        # Ordered lists
        if html[i].strip().startswith("* "):
            content = html[i].split(" ", 1)[1].strip()
            if not olFlag:
                if pFlag:
                    html[i] = "</p>\n<ol>\n<li>{:s}</li>\n".format(content)
                    pFlag = False
                else:
                    html[i] = "<ol>\n<li>{:s}</li>\n".format(content)
            else:
                html[i] = "<li>{:s}</li>\n".format(content)

            olFlag = True

            if i + 1 >= len(html) or not html[i + 1].strip().startswith("* "):
                html[i] += "</ol>\n"
                olFlag = False

        # Paragraphs
        if not html[i].strip().startswith("<")\
                and not re.match(r'\s', html[i]):
            content = html[i].strip()
            if not pFlag:
                html[i] = "<p>\n" + html[i]
            else:
                html[i - 1] = html[i - 1].strip() + "<br />\n"

            pFlag = True

            if i + 1 >= len(html) or re.match(r'\s', html[i + 1]):
                html[i] = html[i].strip() + "\n</p>\n"
                pFlag = False

        # Bold text
        if "**" in html[i]:
            for j in range(int(html[i].count("**") / 2)):
                boldStart = html[i].index("**")
                boldStop = html[i].index("**", boldStart + 2)
                boldText = html[i][boldStart + 2:boldStop]
                html[i] = html[i].replace(
                    "**{:s}**".format(boldText), "<b>{:s}</b>".format(boldText))

        # Emphasis
        if "__" in html[i]:
            for j in range(int(html[i].count("__") / 2)):
                emStart = html[i].index("__")
                emStop = html[i].index("__", emStart + 2)
                emText = html[i][emStart + 2:emStop]
                html[i] = html[i].replace("__{:s}__".format(
                    emText), "<em>{:s}</em>".format(emText))

        # Hash to MD5
        if "[[" in html[i] and "]]" in html[i]:
            for j in range(int(html[i].count("[["))):
                md5Start = html[i].index("[[")
                md5Stop = html[i].index("]]")
                md5Text = html[i][md5Start + 2:md5Stop]
                md5Hash = hashlib.md5(md5Text.encode())
                html[i] = html[i].replace("[[{:s}]]".format(md5Text),
                                          str(md5Hash.hexdigest()))

        # Strip the letter c (lower + upper)
        if "((" in html[i] and "))" in html[i]:
            for j in range(int(html[i].count("(("))):
                cStart = html[i].index("((")
                cStop = html[i].index("))")
                cText = html[i][cStart + 2:cStop]
                cLessText = re.sub(r"[cC]", "", cText)
                html[i] = html[i].replace("(({:s}))".format(cText), cLessText)

    # Write final result to html file
    with open(argv[2], "w") as output:
        output.writelines(html)


