import numpy as np
import pandas as pd

class Team():
    def __init__(self, team_name, money_a, money_b, money_c):
        self.team_name = team_name
        self.money_a = money_a
        self.money_b = money_b
        self.money_c = money_c
        self.money_get = 0

    def check(self):
        if self.money_a + self.money_b + self.money_c == 3000:
            return 1
        else:
            return 0

def dig_resource_sort(team_investment, money):
    team_get = np.zeros(len(team_investment))
    index_sorted = sorted(range(len(team_investment)), key=lambda k: team_investment[k], reverse=True)
    tier1 = int(len(team_investment) * 0.2)
    tier2 = int(len(team_investment) * 0.7) - tier1
    tier3 = int(len(team_investment) * 0.9) - tier1 - tier2
    tier4 = int(len(team_investment)) - tier1 - tier2 - tier3

    tier1_money = (money * 0.6) / tier1
    tier2_money = (money * 0.35) / tier2
    tier3_money = (money * 0.04) / tier3
    tier4_money = (money * 0.01) / tier4

    i = 0

    for j in range(tier1):
        team_get[index_sorted[i + j]] = tier1_money
    i += tier1

    for j in range(tier2):
        team_get[index_sorted[i + j]] = tier2_money
    i += tier2

    for j in range(tier3):
        team_get[index_sorted[i + j]] = tier3_money
    i += tier3

    for j in range(tier4):
        team_get[index_sorted[i + j]] = tier4_money

    return team_get

if __name__ == "__main__":
    team_money_distribution = pd.read_csv("./test.csv")

    team_list = []
    read_check_flag = 0

    for index, row in team_money_distribution.iterrows():
        team_tmp = Team(row["team_name"], row["money_a"], row["money_b"], row["money_c"])
        if not team_tmp.check():
            print(f"Someone's investment plan have problems, in row {index+2}")
            read_check_flag = 1
        team_list.append(team_tmp)
    
    if read_check_flag:
        exit(0)

    team_money_a = []
    team_money_b = []
    team_money_c = []

    for i in team_list:
        team_money_a.append(i.money_a)
        team_money_b.append(i.money_b)
        team_money_c.append(i.money_c)

    team_get_a = dig_resource_sort(team_money_a, 50000)
    team_get_b = dig_resource_sort(team_money_b, 100000)
    team_get_c = dig_resource_sort(team_money_c, 200000)

    for i in range(len(team_list)):
        team_list[i].money_get += (team_get_a[i] + team_get_b[i] + team_get_c[i])

    d = {'team_name':[], 'money_get':[]}
    result_frame = pd.DataFrame(data=d)

    for i in range(len(team_list)):
        tmp = pd.DataFrame({'team_name':[team_list[i].team_name], 'money_get':[team_list[i].money_get]})
        result_frame = result_frame.append(tmp, ignore_index = True)

    print(result_frame)

    result_frame.to_csv('./result.csv')



    

    