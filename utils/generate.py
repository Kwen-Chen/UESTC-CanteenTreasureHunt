import openai
from openai import OpenAI

basis_prompt = """
给定一个字典，字典的每条记录包含帖子的标题、主要内容、评论。发帖人为电子科技大学的学生，他们在食堂吃到异物并发帖吐槽，评论也是对食堂的吐槽或阴阳怪气的回复。

[字典内容]
{dict_data}

[分析要求]
请根据帖子内容及评论信息分析并总结以下信息：
1. **事件发生的地点**：用户可能会提到具体餐厅名称或楼层，请识别并输出对应的食堂名称，校区及餐厅名称对照如下：
   - **清水河校区**：
     - 银桦餐厅（包含一楼银桦餐厅、二楼紫荆餐厅、三楼芙蓉餐厅）
     - 学子餐厅（包含一楼学子餐厅、二楼思源餐厅、三楼家园餐厅）
     - 朝阳餐厅（包含朝阳一层、朝阳二层）
     - 西北餐厅（即清真餐厅）
     - 桃园餐厅
     - 科创餐厅
     - 还有商业街、三秦面馆等
   - **沙河校区**：
     - 阳光餐厅
     - 西北美食城
     - 风华餐厅
     - 万友餐厅
     - 桂苑餐厅

   请注意，用户可能简写餐厅名称，或使用餐厅名称+楼层的描述，请识别并输出正确的餐厅名称，例如：
    - 我在学子吃到了一个虫子 -> 清水河-学子餐厅
    - 银桦二层的米饭里有异物 -> 清水河-紫荆餐厅

   如果无法识别具体餐厅，请输出 `unknown`。

2. **吃出的异物**：如果提到“蛋白质”，这里指的是虫类，请做相应转换。**请注意，用户可能没有在帖子内容中提出具体的异物，但在评论中可以推理出提到的异物，则应该输出这个推理得到的异物**。如果未能推出，请输出 `unknown`。

3. **后续**：判断帖子内容或评论中是否提到后续赔偿或处理。没有后续时请输出 `无后续`，有后续时请简单描述后续情况。

[输出格式]
```json
{{
	"location": "<事件发生的地点 （校区-食堂名称）>",
	"mess': "<吃出的异物>",
	"is_follow_up": "<后续赔偿>"
}}
```
下面是你的输出：
"""

def get_api_results(prompt_input, config):
    model = config['args']['api_name']
    key = config['args']['api_key']
    url = config['args']['api_url']
    messages = [{"role": "user", "content": prompt_input}]

    client = OpenAI(
        api_key=key,
        base_url=url
    )

    if config['type'] == 'OpenAI':
        try:
            chat_response = client.chat.completions.create(
                model=model,
                messages=messages,
            )
            return chat_response.choices[0].message.model_dump()['content']
        except Exception as e:
            print(e)
            return []






