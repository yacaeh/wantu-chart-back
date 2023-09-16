import wikipediaapi
wiki = wikipediaapi.Wikipedia('Wantu (yacaeh@gmail.com)','ko')
import re

query = "우마게임"
page_py = wiki.page(query)

if page_py.exists() == True:
    print("Page - Title: %s" % page_py.title)
    print("Page - Summary: %s" % page_py.summary)
    print("Page - Text: %s" % page_py.text)
    # print("Page - Categories: %s" % page_py.categories)
    # print("Page - Links: %s" % page_py.links)
    print("Page - Sections: %s" % page_py.sections)
    # print("Page - Images: %s" % page_py.images)
    # print("Page - References: %s" % page_py.references)
    # print("Page - Backlinks: %s" % page_py.backlinks)
    # print("Page - Parent: %s" % page_py.parent)

else:
    print("No page found.")