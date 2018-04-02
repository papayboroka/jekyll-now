# -*- coding: utf-8 -*-
import requests
import codecs
from collections import OrderedDict

API_KEY = "xxxxxxx"
USER_ID = "xxxxxxx"
COLLECTION_ID = "xxxxxxx"

base_url = "https://api.zotero.org/users/%s/collections/%s/items?format=json&include=bib&sort=date"
def get_zotero_api_req(url):
    return requests.get(
            url % (USER_ID, COLLECTION_ID),
            headers={
                "Zotero-API-Version": "3",
                "Zotero-API-Key": API_KEY
            })


def get_bibs_by_year_from_json(req):
    req_dict = req.json()
    
    year_bib_dict = OrderedDict()
    for item in req_dict:
        year = item["meta"].get(u"parsedDate")
        
        bib = "".join(item["bib"].splitlines())
        if year is not None:
            if year_bib_dict.get(year) is None:
                year_bib_dict[year] = []
            
            year_bib_dict[year] += [bib]

    content = ""
    for year, bibs in year_bib_dict.items():
        content += "## %s\n" % year
        content += "\n".join(["- %s" % item for item in bibs])
        content += "\n\n"
        
    return content

template_content = """---
layout: page
title: Publications
permalink: /publications/
---
%s
""" % (
         get_bibs_by_year_from_json(get_zotero_api_req(base_url))                 
        )

codecs.open("publications.md", "w", "UTF8").write(
        template_content
        )