__author__ = 'CJB'

from bs4 import BeautifulSoup
import requests
import html2text
from datetime import datetime
import re

def innerHTML(element):
    return element.decode_contents(formatter="html")

def mathjax_preproc(body, soup):
    scripts = body.find_all("script", {"id": re.compile("^MathJax-Element")})
    for script in scripts:
        # print(script)

        tag = "span"
        arounder = "$"
        if script.has_attr("type") and "mode=display" in script["type"]:
            tag = "p"
            arounder = "$$"

        # div_tag = soup.new_tag("div")
        new_tag = soup.new_tag(tag)
        new_tag.string = "{0}{1}{0}".format(arounder, script.string)
        # div_tag.insert(0, p_tag)
        # print(p_tag)
        script.replace_with(new_tag)
        # print(script.string)
        # script.extract()
        # script.replace_with(script.string)

    # print(body)


def crawl_page(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    contents = soup.find("div", {"class": "font-resize"})
    header = soup.find("header", {"class": "entry-header global-links"})
    body = contents.find("div", {"class": "entry-content"})

    if header is None or body is None:
        return None

    title = header.h1.get_text().strip()
    time = header.time.get_text().strip()
    category = header.p.a.get_text().strip()

    # remove useless nodes
    # print(body.span)
    # body.span.extract()
    body.find("div", {"class": "another_category another_category_color_gray"}).extract()

    mathjax_preproc(body, soup)

    # print(innerHTML(body))
    # print(html2text.html2text(innerHTML(body)))

    return title, time, category, innerHTML(body)

def html2md(html):
    return html2text.html2text(html, bodywidth=0)


def jekyll_header(title, time, category):
    modified_cateogry = {
        "그 외/Tech": "ETC",
        "Web(Front-end)": "Web",
        "Server(Back-end)": "Web",
        "DataScience/Text Mining": "Text Mining",
        "DataScience/Deep Learning": "Deep Learning",
        "DataScience/Bioinformatics": "Bioinformatics"
    }
    if category in modified_cateogry:
        category = modified_cateogry[category]

    tags = [category]
    date = datetime.strptime(time, "%Y.%m.%d %H:%M")
    p = re.compile('[^ㄱ-ㅣ가-힣a-zA-Z0-9()]+')
    filename = date.strftime("%Y-%m-%d") + "-" + p.sub("-", title) + ".md"

    ret = "\n".join(["---", "layout: post", "title: \"{}\"".format(title), \
                    "tags: {}".format(str(tags)), "date: {}".format(str(date)), "---"])

    return filename, ret

if __name__ == "__main__":
    for i in range(1, 140):
        url = "http://khanrc.tistory.com/{}".format(i)
        try:
            title, time, category, body = crawl_page(url)
        except Exception as e:
            print("[Exception, {}] {}".format(i, e))
            continue

        fn, header = jekyll_header(title, time, category)
        markdown = html2md(body)
        tistory_md = "[Tistory 원문보기]({})".format(url)
        if "type=\"math/tex\"" in body:
            print("[{}] mathjax check!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!".format(i))
        # print(body)
        # print(repr(markdown))
        print("[{}] {}".format(i, fn))

        with open("posts/{}".format(fn), "w") as f:
            f.write("{}\n{}\n\n{}\n".format(header, markdown, tistory_md))
