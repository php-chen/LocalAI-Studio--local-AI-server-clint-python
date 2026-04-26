import requests
import json
import time
from config import Config

def get_comfyui_url(endpoint):
    """构建ComfyUI API URL"""
    url = f"{Config.COMFYUI_BASE_URL}/{endpoint.lstrip('/')}"
    print(f"ComfyUI URL: {url}")
    return url

def make_comfyui_request(method, endpoint, **kwargs):
    """发送请求到ComfyUI，带有重试机制"""
    url = get_comfyui_url(endpoint)
    max_retries = 3
    retry_delay = 1

    for attempt in range(max_retries):
        try:
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            if response.status_code == 500:
                if attempt < max_retries - 1:
                    print(f"Attempt {attempt + 1} failed, retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
            raise e
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1} failed, retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2
                continue
            raise e

def create_production_record(base_url, queue_id, work_id, status):
    """创建生产记录"""
    print(f"\n正在创建生产记录...")
    print(f"queue_id: {queue_id}, work_id: {work_id}, status: {status}")

    production_data = {
        "queue_id": str(queue_id),
        "work_id": work_id,
        "status": status
    }

    try:
        production_response = requests.post(
            f"{base_url}/production/create",
            json=production_data
        )

        if production_response.status_code == 200:
            production_result = production_response.json()
            print("生产记录创建成功")
            try:
                print(f"创建结果: {json.dumps(production_result, ensure_ascii=False)}")
            except UnicodeEncodeError:
                print("创建结果: (Unicode编码错误，跳过打印)")
            return True, production_result
        else:
            print(f"生产记录创建失败: {production_response.status_code}")
            print(f"响应内容: {production_response.text}")
            return False, None
    except Exception as e:
        print(f"创建生产记录时出错: {str(e)}")
        return False, None

def main():
    # 基础URL
    base_url = "http://localhost:5000"

    # 1. 请求队列列表
    print("正在请求队列列表...")
    list_response = requests.post(f"{base_url}/queue/public/list")

    if list_response.status_code == 200:
        list_data = list_response.json()
        print("队列列表请求成功")

        # 检查是否有数据
        if list_data.get("data") and list_data["data"].get("list"):
            # 获取第一条信息
            first_item = list_data["data"]["list"][0]
            print(f"第一条队列信息: {json.dumps(first_item, ensure_ascii=False)}")

            # 2. 请求详情信息
            work_id = first_item.get("work_id")
            if work_id:
                print(f"正在请求作品详情 (work_id: {work_id})...")
                detail_response = requests.post(
                    f"{base_url}/queue/public/detail",
                    json={"work_id": work_id}
                )

                if detail_response.status_code == 200:
                    detail_data = detail_response.json()
                    print("作品详情请求成功")
                    # 处理Unicode编码问题
                    try:
                        print(f"详情信息: {json.dumps(detail_data, ensure_ascii=False)}")
                    except UnicodeEncodeError:
                        print("详情信息: (Unicode编码错误，跳过打印)")

                    # 3. 直接请求ComfyUI执行任务
                    if detail_data.get("data"):
                        creation = detail_data["data"].get("creation")
                        models = detail_data["data"].get("models")

                        if creation and models:
                            content = creation.get("content")
                            creation_id = creation.get("creation_id")

                            if content:
                                print(f"\n正在直接执行任务: {content}")

                                # 从模型信息中获取工作流配置
                                for model in models:
                                    if model.get("workflow"):
                                        workflow_name = model.get("workflow")
                                        config_info = model.get("config_info")

                                        if config_info:
                                            try:
                                                # 解析工作流配置
                                                workflow_data = json.loads(config_info)

                                                # 查找并更新文本节点
                                                text_nodes = {}

                                                # 检查workflow_data的结构
                                                if isinstance(workflow_data, dict):
                                                    # 遍历所有节点
                                                    for node_id, node_data in workflow_data.items():
                                                        # 检查node_data是否为字典
                                                        if isinstance(node_data, dict):
                                                            # 检查节点类型
                                                            if node_data.get('class_type') in ['Text Multiline', 'CLIPTextEncode']:
                                                                # 检查节点值是否为"ChangeThisContent"
                                                                if 'widgets_values' in node_data and node_data['widgets_values']:
                                                                    if node_data['widgets_values'][0] == "ChangeThisContent":
                                                                        text_nodes[node_id] = node_data
                                                                # 或者检查inputs中的text值
                                                                elif 'inputs' in node_data and 'text' in node_data['inputs']:
                                                                    if node_data['inputs']['text'] == "ChangeThisContent":
                                                                        text_nodes[node_id] = node_data
                                                        else:
                                                            print(f"节点 {node_id} 不是字典类型: {type(node_data)}")
                                                else:
                                                    print(f"workflow_data 不是字典类型: {type(workflow_data)}")

                                                if text_nodes:
                                                    # 使用找到的第一个文本节点
                                                    text_node_id = next(iter(text_nodes))
                                                    text_node = text_nodes[text_node_id]

                                                    # 更新文本节点的内容
                                                    if 'widgets_values' in text_node and text_node['widgets_values']:
                                                        text_node['widgets_values'][0] = content
                                                        print(f"已更新文本节点 {text_node_id} 的widgets_values为: {content}")
                                                    elif 'inputs' in text_node and 'text' in text_node['inputs']:
                                                        text_node['inputs']['text'] = content
                                                        print(f"已更新文本节点 {text_node_id} 的inputs.text为: {content}")

                                                    # 提交工作流到ComfyUI
                                                    client_id = f"direct-api-{int(time.time())}"
                                                    prompt_url = get_comfyui_url('/prompt')
                                                    print(f"\nSubmitting workflow to ComfyUI at: {prompt_url}")

                                                    # 打印最终的工作流数据
                                                    print("\n=== Final Workflow JSON ===")
                                                    print(json.dumps(workflow_data, indent=2, ensure_ascii=False))
                                                    print("=== End of Workflow JSON ===\n")

                                                    prompt_response = make_comfyui_request('POST', '/prompt', json={
                                                        "prompt": workflow_data,
                                                        "client_id": client_id
                                                    })

                                                    print(f"Prompt Response Status: {prompt_response.status_code}")
                                                    print(f"Prompt Response Content: {prompt_response.text}")

                                                    if prompt_response.status_code == 200:
                                                        prompt_data = prompt_response.json()
                                                        print("任务执行请求成功")
                                                        print(f"执行结果: {json.dumps(prompt_data, ensure_ascii=False)}")

                                                        # 获取prompt_id
                                                        prompt_id = prompt_data.get('prompt_id')
                                                        if prompt_id:
                                                            print(f"\n任务已提交，prompt_id: {prompt_id}")

                                                            # 任务提交后立即创建生产记录，状态为PRODUCING
                                                            print("\n任务已提交，创建生产记录，状态为PRODUCING")
                                                            create_production_record(
                                                                base_url,
                                                                prompt_id,
                                                                work_id,
                                                                "PRODUCING"
                                                            )

                                                            # 等待任务执行
                                                            print(f"\n正在查询任务状态...")
                                                            time.sleep(5)  # 等待5秒后查询

                                                            status_response = make_comfyui_request('GET', f'/history/{prompt_id}')
                                                            if status_response.status_code == 200:
                                                                status_data = status_response.json()
                                                                print("任务状态查询成功")
                                                                print(f"状态信息: {json.dumps(status_data, ensure_ascii=False)}")

                                                                # 检查任务是否完成
                                                                if status_data and prompt_id in status_data:
                                                                    outputs = status_data[prompt_id].get('outputs', {})
                                                                    if outputs:
                                                                        print("\n任务已完成")
                                                                    else:
                                                                        print("\n任务仍在处理中")
                                                            else:
                                                                print(f"任务状态查询失败: {status_response.status_code}")
                                                    else:
                                                        print(f"任务执行请求失败: {prompt_response.status_code}")
                                                        print(f"响应内容: {prompt_response.text}")
                                                else:
                                                    print("工作流中没有找到值为'ChangeThisContent'的文本节点")
                                            except json.JSONDecodeError as e:
                                                print(f"解析配置信息失败: {str(e)}")
                                            except Exception as e:
                                                print(f"处理工作流时出错: {str(e)}")
                                else:
                                    print("模型信息中没有workflow字段")
                            else:
                                print("作品详情中没有content字段")
                        else:
                            print("作品详情中缺少creation或models字段")
                    else:
                        print("作品详情中没有data字段")
                else:
                    print(f"详情请求失败: {detail_response.status_code}")
                    print(f"响应内容: {detail_response.text}")
            else:
                print("第一条队列信息中没有work_id")
        else:
            print("队列列表为空")
    else:
        print(f"队列列表请求失败: {list_response.status_code}")
        print(f"响应内容: {list_response.text}")

if __name__ == "__main__":
    main()