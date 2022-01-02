import requests as requests
from lxml.html import fromstring

from constants import diccioMoji, userAgent


def appendPrimary(img_list, rune_list):
    for img in img_list:
        primary = img.get("alt")
        rune_list.append(f"{getMoji(primary)} {primary}")


def appendSecondary(img_list, rune_list):
    for img in img_list:
        secondary = img.get("alt")
        rune_list.append(f"{getMoji(secondary)} {secondary}")


def appendTertiary(img_list3, rune_list):
    for img in img_list3:
        tertiary = tertiary_correction(img.get("alt"))
        rune_list.append(f"- {tertiary}")


def tertiary_correction(tertiary):
    if tertiary == "OFFENSE":
        tertiary = "Amarillas o Violeta, vos fijate"
    elif tertiary == "FLEX":
        tertiary = "Roja o Lila, como te convenga"
    else:
        tertiary = "La Verde maestro"
    return tertiary


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
        rune_list.append("----------------Primary:------------------")

        appendPrimary(img_list, rune_list)

        rune_list.append("\n----------------Secondary:----------------")

        img_selector2 = '.ChampionKeystoneRune-1>tr:first-child .perk-page:nth-child(3) .perk-page__item--active>div>img'
        img_list2 = doc.cssselect(img_selector2)

        appendSecondary(img_list2, rune_list)

        rune_list.append("\n----------------Tertiary:--------------------")

        img_selector3 = '.ChampionKeystoneRune-1>tr:first-child .fragment__detail img.active'
        img_list3 = doc.cssselect(img_selector3)

        appendTertiary(img_list3, rune_list)

        return "\n".join(rune_list)
