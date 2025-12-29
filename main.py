import requests
import re
import pandas as pd

# Items are considered pickupable objects
category_name = "Pickupable_Objects"
wiki_url = "https://tibia.fandom.com"
api_url = f"{wiki_url}/api.php"

params = {
    "action": "query",
    "generator": "categorymembers",
    "gcmtitle": f"Category:{category_name}",
    "prop": "revisions",
    "rvprop": "content",
    "rvslots": "*",
    "gcmlimit": "max"
}

# Keep requesting pages until 'continue' is not found
def query(request):
    request['action'] = 'query'
    request['format'] = 'json'
    last_continue = {}
    while True:
        # Clone original request
        req = request.copy()
        # Modify it with the values returned in the 'continue' section of the last result
        req.update(last_continue)
        # Call API
        result = requests.get(api_url, params=req).json()
        if 'error' in result:
            raise Exception(result['error'])
        if 'warnings' in result:
            print(result['warnings'])
        if 'query' in result:
            yield result['query']
        if 'continue' not in result:
            break
        last_continue = result['continue']

items_pages_json = {}

for result in query(params):
    for page in result['pages']:
        if 'revisions' in result['pages'][page]:
            # Extract only the infobox data
            items_pages_json[page] = result['pages'][page]['revisions'][0]['slots']['main']['*']

# If a new tag is created, it must be added here
supported_tags = [
    'name', 'article', 'actualname', 'plural', 'itemid', 'objectclass', 'primarytype', 'slot', 'implemented', 'immobile',
    'walkable', 'pickupable', 'levelrequired', 'vocrequired', 'imbueslots', 'upgradeclass', 'attrib', 'armor', 'weight', 'stackable',
    'marketable', 'droppedby', 'value', 'npcvalue', 'npcprice', 'buyfrom', 'sellto', 'notes', 'history', 'defense',
    'holdsliquid', 'usable', 'status', 'sounds', 'flavortext', 'duration', 'attack', 'npcvaluerook', 'npcpricerook', 'hands',
    'weapontype', 'enchantable', 'secondarytype', 'volume', 'consumable', 'regenseconds', 'defensemod', 'hangable', 'range', 'atk_mod',
    'hit_mod', 'blockspath', 'writable', 'writechars', 'fansite', 'words', 'lightradius', 'lightcolor', 'mlrequired', 'storevalue',
    'damagetype', 'imbuements', 'tertiarytype', 'rewritable', 'pricecurrency', 'wrappable', 'manaleech_ch', 'manaleech_am', 'crithit_ch', 'critextra_dmg',
    'hpleech_ch', 'hpleech_am', 'resist', 'ice_attack', 'augments', 'death_attack', 'fire_attack', 'earth_attack', 'manacost', 'damagerange',
    'energy_attack', 'elementalbond', 'charges', 'destructible', 'location', 'mantra', 'notes2', 'enchanted', 'rotatable',
]

# Parsing the infobox
items_info_dict = {}
for page in items_pages_json:
    items_info_dict[page] = {}
    
    # Find every supported tag
    matches = []
    for match in re.finditer("|".join(["\n\\| " + tag + " = " for tag in supported_tags]), re.sub(" {2,}", " ", items_pages_json[page])):
        matches.append([match.group()[3:-3], match.start(), match.end()])
    # Smooth ending
    matches.append(['end', -3, -1])
    
    # Extracting values
    for i in range(len(matches)-1):
        key = matches[i][0]
        start_of_value = matches[i][2]
        end_of_value = matches[i+1][1]
        value = re.sub(" {2,}", " ", items_pages_json[page])[start_of_value:end_of_value]
        items_info_dict[page][key] = value

    for tag in supported_tags:
        if tag not in items_info_dict[page]:
            items_info_dict[page][tag] = '-'

items_info_df = pd.DataFrame.from_dict(items_info_dict, orient='index').reset_index(drop=True)

# Droppedby column starts with 'DroppedBy{{' and ends with '}}'
items_info_df['droppedby'] = items_info_df['droppedby'].str[13:-2].str.replace("|", " | ")
for col in items_info_df.columns:
    items_info_df[col] = items_info_df[col].replace("", "-")
    items_info_df[col] = items_info_df[col].replace("--", "-")
    items_info_df[col] = items_info_df[col].str.replace('\n', '\\n')
    items_info_df[col] = items_info_df[col].str.replace('\t', '\\t')

items_info_df.to_csv("tibia_wiki_items.csv", index=False)