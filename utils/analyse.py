import matplotlib.pyplot as plt


def analyse(args, data_list):
    # 1. 统计 location 的数量
    # location_analyse(data_list)
    # 2. 统计 mess 的数量
    # mess_analyse(data_list)
    # 3. 统计 is_follow_up 的数量
    follow_up_analyse(data_list)



def location_analyse(data_list):
    # 1. 统计 location 的数量
    location_dict = {}
    for data in data_list:
        location = data['result']['location']
        if location in location_dict:
            location_dict[location] += 1
        else:
            location_dict[location] = 1

    print('*'*20 + 'location 统计：'+ '*'*20)
    all_sum = 0
    known_sum = 0
    for location, count in location_dict.items():
        all_sum += count
        if location != 'unknown':
            known_sum += count

    print(f'总数：{all_sum}, 有地点的帖子数：{known_sum}, 无地点的帖子数：{all_sum - known_sum}')

    # 根据 count 排序
    location_dict = dict(sorted(location_dict.items(), key=lambda x: x[1], reverse=True))
    for location, count in location_dict.items():
        if location == 'unknown':
            continue
        print(f'{location}: {count}, 占比：{count / known_sum:.2%}')

    # 统计图绘制
    # 添加中文支持
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

    location_dict.pop('unknown')
    labels = list(location_dict.keys())
    sizes = list(location_dict.values())
    # sizes 占比百分之四以下的合并为 其他
    other_sum = 0
    other_index = []
    for i in range(len(sizes)):
        if sizes[i] / known_sum < 0.04:
            other_sum += sizes[i]
            other_index.append(i)

    for i in other_index[::-1]:
        labels.pop(i)
        sizes.pop(i)
    labels.append('其他')
    sizes.append(other_sum)

    explode = [0.1 if location == '清水河-学子餐厅' else 0 for location in labels]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')
    plt.title('location 统计')
    plt.show()

def mess_analyse(data_list):
    # 2. 统计 mess 的数量
    # mess key ['蛋白质类'， '纤维类', '钙硅类', '金属类','其他物质']
    mess_dict = {'蛋白质类': [], '纤维类': [], '钙硅类': [], '金属类': [], '其他物质': []}
    mess_num = {'蛋白质类': 0, '纤维类': 0, '钙硅类': 0, '金属类': 0, '其他物质': 0}

    protein_keywords = ('虫', '蟑螂', '蜘蛛', '苍蝇', '蚊子', '蜜蜂', '蛆', '蜗牛', '蚂蚁', '小强', '蟋蟀')
    fiber_keywords = ('发', '毛', '塑料', '纸', '木', '牌', '线', '证', '布')
    ca_si_keywords = ('石', '玻璃', '壳', '骨', '瓷', '指甲', '碗')
    metal_keywords = ('铁', '钢', '螺丝', '铁丝', '金属')

    for data in data_list:
        mess = data['result']['mess']
        if mess == 'unknown':
            continue
        if any(keyword in mess for keyword in protein_keywords):
            mess_dict['蛋白质类'].append(mess)
            mess_num['蛋白质类'] += 1
        elif any(keyword in mess for keyword in fiber_keywords):
            mess_dict['纤维类'].append(mess)
            mess_num['纤维类'] += 1
        elif any(keyword in mess for keyword in ca_si_keywords):
            mess_dict['钙硅类'].append(mess)
            mess_num['钙硅类'] += 1
        elif any(keyword in mess for keyword in metal_keywords):
            mess_dict['金属类'].append(mess)
            mess_num['金属类'] += 1
        else:
            mess_dict['其他物质'].append(mess)
            mess_num['其他物质'] += 1

    print('\n\n' + '*'*20 + 'mess 统计：'+ '*'*20)

    all_sum = 0

    for mess, count in mess_num.items():
        all_sum += count
    print(f'总数：{all_sum}')

    # 根据 count 排序
    mess_num = dict(sorted(mess_num.items(), key=lambda x: x[1], reverse=True))
    for mess, count in mess_num.items():
        print(f'{mess}: {count}, 占比：{count / all_sum:.2%}')

    # 各类物质统计
    for mess, mess_list in mess_dict.items():
        print(f'\n{mess} 统计：')
        mess_set = set(mess_list)
        print(mess_set)

    # 统计图绘制
    # 添加中文支持
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

    labels = list(mess_num.keys())
    sizes = list(mess_num.values())
    explode = [0.1 if label == '蛋白质类' else 0 for label in labels]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')
    plt.title('mess 统计')
    plt.show()

def follow_up_analyse(data_list):
    is_replay = {'已回复': 0, '未回复': 0}
    for data in data_list:
        if data['is_replay']:
            is_replay['已回复'] += 1
        else:
            is_replay['未回复'] += 1

    print('\n\n' + '*'*20 + 'is_follow_up 统计：'+ '*'*20)

    print(f'总数：{is_replay["已回复"] + is_replay["未回复"]}')
    print(f'已回复：{is_replay["已回复"]}, 未回复：{is_replay["未回复"]}')

    follow_up = []
    follow_up_dict = {'有后续': 0, '无后续': 0}
    for data in data_list:
        if data['result']['is_follow_up'] != '无后续':
            follow_up_dict['有后续'] += 1
            follow_up.append(data['result']['is_follow_up'])
        else:
            follow_up_dict['无后续'] += 1

    print(f'有后续：{follow_up_dict["有后续"]}, 无后续：{follow_up_dict["无后续"]}')

    for follow in follow_up:
        print(follow)