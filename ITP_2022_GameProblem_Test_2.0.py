import numpy as np
import pandas as pd

class Team():
    def __init__(self, team_name, money_a, money_b, money_c, money_get):
        self.team_name = team_name
        self.money_a = money_a
        self.money_b = money_b
        self.money_c = money_c
        self.money_get = money_get

    def check(self):
        if self.money_a + self.money_b + self.money_c + self.money_get == 3000:
            return 1
        else:
            return 0

def tier_classification(team_investment):
    tier1 = int(len(team_investment) * 0.2)
    tier2 = int(len(team_investment) * 0.7) - tier1
    tier3 = int(len(team_investment) * 0.9) - tier1 - tier2
    tier4 = int(len(team_investment)) - tier1 - tier2 - tier3
    return tier1, tier2, tier3, tier4


def dig_resource_sort(team_list, money, key_word):
    team_investment = dict()
    for i in range(len(team_list)):
        team_investment[team_list[i].team_name] = eval('team_list[i].' + key_word)

    key_flag = []

    for key, val in team_investment.items():
        if val == 0:
            key_flag.append(key)

    for key in key_flag:
        del team_investment[key]

    team_investment = dict(sorted(team_investment.items(), key=lambda x:x[1], reverse=True))

    tier1, tier2, tier3, tier4 = tier_classification(team_investment)

    d = {'team_name':[], key_word:[], 'tier':[]}
    money_sort_frame = pd.DataFrame(data=d)

    i = 0
    for key, val in team_investment.items():

        if i < tier1:
            tier = 'tier1'
        elif i < tier1 + tier2:
            tier = 'tier2'
        elif i < tier1 + tier2 + tier3:
            tier = 'tier3'
        else:
            tier = 'tier4'
        
        tmp = pd.DataFrame({'team_name':[key], key_word:[val], 'tier':[tier]})
        money_sort_frame = money_sort_frame.append(tmp, ignore_index=False)

        i += 1

    money_sort_frame.to_csv(key_word + '_distribution.csv', index=False)

    tier1_money = (money * 0.6) / tier1
    tier2_money = (money * 0.35) / tier2
    tier3_money = (money * 0.04) / tier3
    tier4_money = (money * 0.01) / tier4

    i = 0

    for key, val in team_investment.items():
        if i < tier1:
            team_get[key] = team_get[key] + tier1_money
        elif i < tier1 + tier2:
            team_get[key] = team_get[key] + tier2_money
        elif i < tier1 + tier2 + tier3:
            team_get[key] = team_get[key] + tier3_money
        else:
            team_get[key] = team_get[key] + tier4_money

        i += 1

if __name__ == "__main__":
    team_money_distribution = pd.read_csv("./data.csv")

    team_list = []
    read_check_flag = 0

    for index, row in team_money_distribution.iterrows():
        team_tmp = Team(row["team_name"], row["money_a"], row["money_b"], row["money_c"], row["remain"])
        if not team_tmp.check():
            print(f"Someone's investment plan have problems, in row {index+2}")
            read_check_flag = 1
        team_list.append(team_tmp)
    
    if read_check_flag:
        exit(0)

    team_get = dict()

    for i in range(len(team_list)):
        team_get[team_list[i].team_name] = float(team_list[i].money_get)

    dig_resource_sort(team_list, 50000, 'money_a')
    dig_resource_sort(team_list, 100000, 'money_b')
    dig_resource_sort(team_list, 200000, 'money_c')

    team_get = dict(sorted(team_get.items(), key=lambda x:x[1], reverse=True))

    team_get = pd.DataFrame.from_dict(team_get, orient='index')

    team_get.to_csv('./result.csv', header=False)

    

    