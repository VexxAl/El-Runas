import re

import requests as requests
from lxml.html import fromstring

from constants import diccioMoji, userAgent


def appendPrimary(img_list, rune_list, doc):
    PrimarySelector = '.ChampionKeystoneRune-1>tr:first-child .perk-page:first-child .perk-page__row:first-child img'
    Primary_imgurl = doc.cssselect(PrimarySelector)[0].get("src")
    Primary_imgName = re.search(r".*/(.*)\.png", Primary_imgurl).group(1)
    rune_list.append(f"----------------Primary:{getMoji(Primary_imgName)}------------------")
    for img in img_list:
        primary = img.get("alt")
        rune_list.append(f"{getMoji(primary)} {primary}")


def appendSecondary(img_list, rune_list, doc):
    SecondarySelector = '.ChampionKeystoneRune-1>tr:first-child .perk-page:nth-child(3) .perk-page__row:first-child img'
    Secondary_imgurl = doc.cssselect(SecondarySelector)[0].get("src")
    Secondary_imgName = re.search(r".*/(.*)\.png", Secondary_imgurl).group(1)
    rune_list.append(f"\n----------------Secondary:{getMoji(Secondary_imgName)}----------------")
    for img in img_list:
        secondary = img.get("alt")
        rune_list.append(f"{getMoji(secondary)} {secondary}")


def getMoji(runeMoji):
    return diccioMoji.get(runeMoji, " ")


def get_rune(champ_name, line):
    result = requests.get(f'https://op.gg/champion/{champ_name}/statistics/{line}/build',
                          cookies={'customLocale': 'en'}, headers={
            'user-agent': userAgent})
    doc = fromstring(result.content)
    rune_list = []

    img_selector1 = '.ChampionKeystoneRune-1>tr:first-child .perk-page:first-child .perk-page__item--active>div>img'
    img_list = doc.cssselect(img_selector1)

    if len(img_list) > 0:
        appendPrimary(img_list, rune_list, doc)

        img_selector2 = '.ChampionKeystoneRune-1>tr:first-child .perk-page:nth-child(3) .perk-page__item--active>div>img'
        img_list2 = doc.cssselect(img_selector2)

        appendSecondary(img_list2, rune_list, doc)

        return "\n".join(rune_list)
