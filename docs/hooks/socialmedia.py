from textwrap import dedent
import urllib.parse
import re

x_intent = "https://x.com/intent/tweet"
fb_sharer = "https://www.facebook.com/sharer/sharer.php"
wa_sharer = "https://api.whatsapp.com/send"
li_sharer = "https://www.linkedin.com/shareArticle"
include = re.compile(r"blog/[1-9].*")

def on_page_markdown(markdown, **kwargs):
    page = kwargs['page']
    config = kwargs['config']
    if not include.match(page.url):
        return markdown

    page_url = config.site_url + page.url
    page_title = urllib.parse.quote(page.title + '\n')

    return markdown + dedent(f"""
    [Share on :simple-x:]({x_intent}?text={page_title}&url={page_url}){{ .md-button }}
    [Share on :simple-facebook:]({fb_sharer}?u={page_url}){{ .md-button }}
    [Share on :simple-whatsapp:]({wa_sharer}?text={page_title}%20{page_url}){{ .md-button }}
    [Share on :simple-linkedin:]({li_sharer}?mini=true&url={page_url}&title={page_title}){{ .md-button }}
    """)