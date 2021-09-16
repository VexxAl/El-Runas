import requests as requests
from lxml.html import fromstring


def get_rune(champ_name, line):
    result = requests.get(f'https://op.gg/champion/{champ_name}/statistics/{line}', cookies={'customLocale': 'es'})
    doc = fromstring(result.content)
    rune_list = []

    img_list = doc.cssselect(
        '.ChampionKeystoneRune-1>tr:first-child .perk-page:first-child .perk-page__item--active>div>img')

    if len(img_list) > 0:
        rune_list.append("----------------Primarias:------------------")
        
        for img in img_list:
          celeridad = img.get("alt")
          
          if celeridad == "Leyenda: Presteza":
            celeridad = "Leyenda: Celeridad"
            rune_list.append("- " + f"{celeridad}")
          else:
            rune_list.append("-" + f"{celeridad}")
        
        rune_list.append("\n----------------Secundarias:----------------")
        
        for img in doc.cssselect(
                '.ChampionKeystoneRune-1>tr:first-child .perk-page:nth-child(3) .perk-page__item--active>div>img'):
            rune_list.append("- " + img.get("alt"))
        
        rune_list.append("\n----------------Terciarias:--------------------")
        
        for img in doc.cssselect('.ChampionKeystoneRune-1>tr:first-child .fragment__detail img.active'):
            terciarias = img.get("alt")
        
            if terciarias == "OFFENSE":
              terciarias = "Amarillas o Violeta, vos fijate"
            elif terciarias == "FLEX":
                terciarias = "Roja o Lila, como te convenga"
            else:
              terciarias = "La Verde maestro"
              
            rune_list.append("- " + f"{terciarias}")

        return "\n".join(rune_list)
