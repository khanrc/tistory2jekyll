__author__ = 'CJB'

import os
import re

path = "/Users/CJB/Blog/khanrc.github.io/_posts"

def rearrange(contents):
    ## tags rearrange
    modified_cateogry = {
        "그 외/Tech": "ETC",
        "Web(Front-end)": "Web",
        "Server(Back-end)": "Web",
        "DataScience/Text Mining": "Text Mining",
        "DataScience/Deep Learning": "Deep Learning",
        "DataScience/Bioinformatics": "Bioinformatics",
        "Apps": "Test"
    }

    prog = re.compile("---.*?---", re.DOTALL)
    head = prog.findall(contents)[0]
    tags_line = re.findall("(tags.+?)\n", head)[0]
    tags = re.findall("'(.*?)'", tags_line)

    arranged_tags = []
    for tag in tags:
        if tag in modified_cateogry:
            arranged_tags.append(modified_cateogry[tag])
        else:
            arranged_tags.append(tag)

    contents = re.sub(r"(tags.+?)\n", "tags: {}\n".format(str(arranged_tags)), contents, count=1)

    ## mathjax rearrange
    contents = re.sub(r"^(\$.+?\$)$", r"<div>\1</div>", contents, flags = re.VERBOSE | re.MULTILINE)

    return contents

if __name__ == "__main__":
    for fn in os.listdir(path):
        print(fn)
        filepath = os.path.join(path, fn)

        if fn.startswith(".") or not os.path.isfile(filepath):
            continue
        with open(filepath, "r") as f:
            after = rearrange(f.read())
        with open(filepath, "w") as f:
            f.write(after)

