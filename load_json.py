
#!/usr/bin/env python3

import json



with open('mydata.json') as f:
    team = json.load(f)

    print(team['tux'])
    print(team['tux']['health'])
    print(team['tux']['level'])

    print(team['beastie'])
    print(team['beastie']['health'])
    print(team['beastie']['level'])
