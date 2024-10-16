import argparse
import os
import jsonlines
import yaml

from utils.analyse import analyse
from utils.crawler import *
from utils.generate import basis_prompt, get_api_results


def parse_arguments():
    parser = argparse.ArgumentParser(description='args for persona_gen.py')
    parser.add_argument("--cookie_file", type=str, default="config/cookie.txt")
    parser.add_argument("--page_link_file", type=str, default="output/page_link.json")
    parser.add_argument("--page_detail_file", type=str, default="output/page_detail.jsonl")
    parser.add_argument("--output_path", type=str, default="output/data.jsonl")
    parser.add_argument("--config_path", type=str, default="config/config.yaml")
    parser.add_argument("--log_path", type=str, default="log")
    parser.add_argument("--run", nargs='+', type=str, default=['crawler', 'generate', 'analyse'])

    args = parser.parse_args()
    return args

log_file_name = f'log_{time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())}.txt'

def write_to_log(args, data):
    log_path = os.path.join(args.log_path, log_file_name)
    with open(log_path, 'a') as f:
        f.write(data)
        f.write('\n')

def main():
    args = parse_arguments()
    config = yaml.load(open(args.config_path, 'r'), Loader=yaml.FullLoader)
    output_data = {}
    # 1. 爬虫部分
    if 'crawler' in args.run:
        page_links = get_page_links(args)
        page_details = get_page_content(args, page_links)

    # 2. LLM 生成部分
    if 'generate' in args.run:
        with open(args.page_detail_file, 'r') as f:
            data_dicts = f.readlines()

        for line in tqdm.tqdm(data_dicts):
            data = json.loads(line)
            prompt = basis_prompt.format(dict_data=json.dumps(data, ensure_ascii=False, indent=4))
            response = get_api_results(prompt, config)
            write_to_log(args, response)
            try:
                response_dict = response.split('```json')[1].split('```')[0]
                response_dict = json.loads(response_dict)
                output_data['is_replay'] = data['is_replay']
                output_data['index'] = data_dicts.index(line)
                output_data['result'] = response_dict
                with jsonlines.open(args.output_path, mode='a') as writer:
                    writer.write(output_data)
            except Exception as e:
                write_to_log(args, f'{data_dicts.index(line)} error')
                print(e)

    # 3. 分析部分
    if 'analyse' in args.run:
        with jsonlines.open(args.output_path) as reader:
            data_list = list(reader)
        analyse(args, data_list)

if __name__ == '__main__':
    main()