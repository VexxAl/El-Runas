import re

import requests as requests
from lxml.html import fromstring

from constants import diccioMoji, userAgent


def appendPrimary(img_list, rune_list, doc):
    PrimarySelector = '.rune-tree_mobile .primary-tree .rune-tree_header img'
    Primary_imgurl = doc.cssselect(PrimarySelector)[0].get("src")
    Primary_imgName = re.search(r".*/(.*)\.png", Primary_imgurl).group(1)
    rune_list.append(f"----------------Primary:{get_emoji(Primary_imgName)}------------------")
    for img in img_list:
        primary = img.get("alt").replace("The Keystone ", "").replace('The Rune ', '')
        rune_list.append(f"{get_emoji(primary)} {primary}")


def appendSecondary(img_list, rune_list, doc):
    SecondarySelector = '.secondary-tree .rune-tree_mobile .rune-tree_header img'
    Secondary_imgurl = doc.cssselect(SecondarySelector)[0].get("src")
    Secondary_imgName = re.search(r".*/(.*)\.png", Secondary_imgurl).group(1)
    rune_list.append(f"\n----------------Secondary:{get_emoji(Secondary_imgName)}----------------")
    for img in img_list:
        secondary = img.get("alt").replace("The Keystone ", "").replace('The Rune ', '')
        rune_list.append(f"{get_emoji(secondary)} {secondary}")


def get_emoji(runeMoji):
    return diccioMoji.get(runeMoji, " ")


def get_rune(champ_name):
    result = requests.get(f'https://u.gg/lol/champions/{champ_name}/build',
                          cookies={'customLocale': 'en'}, headers={
            'user-agent': userAgent})
    doc = fromstring(result.content)
    rune_list = []

    img_selector1 = '.rune-tree_mobile .primary-tree .perk-active img'
    img_list = doc.cssselect(img_selector1)

    if len(img_list) > 0:
        appendPrimary(img_list, rune_list, doc)

        img_selector2 = '.secondary-tree .rune-tree_mobile .perk-active img'
        img_list2 = doc.cssselect(img_selector2)

        appendSecondary(img_list2, rune_list, doc)

        return "\n".join(rune_list)
