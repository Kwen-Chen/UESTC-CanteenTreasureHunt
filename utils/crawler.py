import time

import requests
import re
from bs4 import BeautifulSoup
import json
import tqdm


def get_page_links(args):
    # 读取 cookie
    with open(args.cookie_file, 'r') as f:
        cookie = f.read().strip()

    headers = {
        'cookie': cookie,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    url = """https://bbs.uestc.edu.cn/forum.php?mod=collection&action=view&ctid=374&page={page}"""
    # 获取 link 列表
    save_dict = {}

    for i in range(2):
        response = requests.get(url.format(page=i), headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        # 读取 div class 是 bm_c
        for div in soup.find_all('div', class_='bm_c'):
            for a in div.find_all('a', class_='xst'):
                save_dict[a['title']] = a['href']

    # save to file, json 格式规范化，并且保存中文
    with open(args.page_link_file, 'w', encoding='utf-8') as f:
        json.dump(save_dict, f, ensure_ascii=False, indent=4)

    print('save to link.json')

    return save_dict


def get_page_content(args, page_links: dict):
    # 读取 cookie
    with open(args.cookie_file, 'r') as f:
        cookie = f.read().strip()

    headers = {
        'cookie': cookie,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Connection': 'close'
    }

    # 获取 link 列表
    save_dict = {}
    save_dict_list = []
    # for title, link in page_links.items():
    for title, link in tqdm.tqdm(page_links.items()):
        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. 读取作者主要内容
        content = soup.find('td', class_='t_f')
        main_content = get_content(content)

        # 2. 读取第一页所有的评论
        comments = []
        contents = soup.find_all('td', class_='t_f')[1:]
        for content in contents:
            if content is None:
                continue
            comments.append(get_content(content))

        # 3. 查看是否有后期回复
        is_replay = False
        h1 = soup.find('h1', class_='ts')
        # 如果底下有 a 标签
        if h1.find('a') and h1.find('a').text == '[已回复]':
            is_replay = True

        save_dict = {'title': title, 'main_content': main_content, 'comments': comments, 'is_replay': is_replay}
        save_dict_list.append(save_dict)

        # save
        with open(args.page_detail_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(save_dict, ensure_ascii=False) + '\n')

        time.sleep(1)

    return save_dict_list

def get_content(content):
    text = content.text
    # 寻找 ignore_js_op 标签内的 text
    ignore_texts = content.find_all('ignore_js_op')
    for ignore_text in ignore_texts:
        text = text.replace(ignore_text.text, '')
    main_content = re.sub(r'\s+', ' ', text)
    return main_content