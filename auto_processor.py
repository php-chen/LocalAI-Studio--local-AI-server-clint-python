import requests
import json
import time
import os
from pathlib import Path

class ComfyUIConfig:
    """ComfyUI配置"""
    COMFYUI_BASE_URL = "http://127.0.0.1:6401"

class APIConfig:
    """API服务器配置"""
    API_BASE_URL = "http://localhost:5000"

class ComfyUIClient:
    """ComfyUI客户端"""

    @staticmethod
    def get_url(endpoint):
        url = f"{ComfyUIConfig.COMFYUI_BASE_URL}/{endpoint.lstrip('/')}"
        return url

    @staticmethod
    def make_request(method, endpoint, **kwargs):
        """发送请求到ComfyUI"""
        url = ComfyUIClient.get_url(endpoint)
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

    @staticmethod
    def submit_workflow(workflow_data):
        """提交工作流到ComfyUI"""
        client_id = f"api-{int(time.time())}"
        prompt_url = ComfyUIClient.get_url('/prompt')

        print(f"Submitting workflow to ComfyUI at: {prompt_url}")

        response = ComfyUIClient.make_request('POST', '/prompt', json={
            "prompt": workflow_data,
            "client_id": client_id
        })

        if response.status_code == 200:
            return response.json()
        return None

    @staticmethod
    def get_history(prompt_id):
        """获取任务历史"""
        try:
            response = ComfyUIClient.make_request('GET', f'/history/{prompt_id}')
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None

class QueueService:
    """队列服务"""

    @staticmethod
    def get_public_list():
        """获取公开队列列表"""
        print("\n正在请求队列列表...")
        try:
            response = requests.post(
                f"{APIConfig.API_BASE_URL}/queue/public/list",
                json={}
            )
            if response.status_code == 200:
                data = response.json()
                print(f"队列列表请求成功")
                return data.get("data", {}).get("list", [])
        except Exception as e:
            print(f"请求队列列表失败: {str(e)}")
        return []

    @staticmethod
    def get_public_detail(work_id):
        """获取公开队列详情"""
        print(f"正在请求作品详情 (work_id: {work_id})...")
        try:
            response = requests.post(
                f"{APIConfig.API_BASE_URL}/queue/public/detail",
                json={"work_id": work_id}
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"请求详情失败: {str(e)}")
        return None

class ProductionService:
    """生产服务"""

    @staticmethod
    def create(queue_id, work_id, status):
        """创建生产记录"""
        print(f"\n正在创建生产记录... queue_id: {queue_id}, status: {status}")
        try:
            response = requests.post(
                f"{APIConfig.API_BASE_URL}/production/create",
                json={
                    "queue_id": str(queue_id),
                    "work_id": work_id,
                    "status": status
                }
            )
            if response.status_code == 200:
                result = response.json()
                print(f"生产记录创建成功")
                return result
            else:
                print(f"生产记录创建失败: {response.status_code}")
        except Exception as e:
            print(f"创建生产记录时出错: {str(e)}")
        return None

    @staticmethod
    def get_public_list(status):
        """获取公开生产列表"""
        print(f"\n正在查询生产状态列表，状态: {status}")
        try:
            response = requests.post(
                f"{APIConfig.API_BASE_URL}/production/public/list",
                json={"status": status}
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"查询生产列表失败: {str(e)}")
        return None

    @staticmethod
    def get_public_detail(queue_id):
        """获取公开生产详情"""
        print(f"\n正在查询生产详情，queue_id: {queue_id}")
        try:
            response = requests.post(
                f"{APIConfig.API_BASE_URL}/production/public/detail",
                json={"queue_id": queue_id}
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"查询详情失败: {str(e)}")
        return None

    @staticmethod
    def upload(work_id, queue_id, file_path):
        """上传文件"""
        print(f"\n正在上传文件... work_id: {work_id}, queue_id: {queue_id}")
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                data = {'work_id': work_id, 'queue_id': queue_id}
                response = requests.post(
                    f"{APIConfig.API_BASE_URL}/production/upload",
                    files=files,
                    data=data
                )
            if response.status_code == 200:
                result = response.json()
                print(f"上传成功: {result}")
                return True, result
            else:
                print(f"上传失败: {response.status_code}")
        except Exception as e:
            print(f"上传时出错: {str(e)}")
        return False, None

class WorkflowExecutor:
    """工作流执行器"""

    @staticmethod
    def find_and_replace_text_node(workflow_data, new_text):
        """查找并替换文本节点"""
        text_nodes = {}

        if not isinstance(workflow_data, dict):
            return None

        for node_id, node_data in workflow_data.items():
            if not isinstance(node_data, dict):
                continue

            if node_data.get('class_type') in ['Text Multiline', 'CLIPTextEncode']:
                # 检查widgets_values
                if 'widgets_values' in node_data and node_data['widgets_values']:
                    if node_data['widgets_values'][0] == "ChangeThisContent":
                        text_nodes[node_id] = node_data
                # 检查inputs中的text
                elif 'inputs' in node_data and 'text' in node_data['inputs']:
                    if node_data['inputs']['text'] == "ChangeThisContent":
                        text_nodes[node_id] = node_data

        if text_nodes:
            text_node_id = next(iter(text_nodes))
            text_node = text_nodes[text_node_id]

            if 'widgets_values' in text_node and text_node['widgets_values']:
                text_node['widgets_values'][0] = new_text
            elif 'inputs' in text_node and 'text' in text_node['inputs']:
                text_node['inputs']['text'] = new_text

            print(f"已更新文本节点 {text_node_id} 的内容为: {new_text}")
            return workflow_data

        return None

    @staticmethod
    def execute_from_detail(detail_data):
        """从详情数据执行工作流"""
        if not detail_data or not detail_data.get("data"):
            return None

        creation = detail_data["data"].get("creation")
        models = detail_data["data"].get("models")

        if not creation or not models:
            return None

        content = creation.get("content")
        work_id = creation.get("creation_id")

        if not content:
            return None

        print(f"\n正在执行任务: {content}")

        for model in models:
            workflow_name = model.get("workflow")
            config_info = model.get("config_info")

            if not workflow_name or not config_info:
                continue

            try:
                workflow_data = json.loads(config_info)
                updated_workflow = WorkflowExecutor.find_and_replace_text_node(workflow_data, content)

                if updated_workflow:
                    result = ComfyUIClient.submit_workflow(updated_workflow)
                    if result:
                        prompt_id = result.get('prompt_id')
                        print(f"任务已提交，prompt_id: {prompt_id}")
                        return {
                            "prompt_id": prompt_id,
                            "work_id": work_id,
                            "content": content
                        }
            except json.JSONDecodeError as e:
                print(f"解析配置信息失败: {str(e)}")
            except Exception as e:
                print(f"处理工作流时出错: {str(e)}")

        return None

class FileService:
    """文件服务"""

    IMAGE_DIR = Path(__file__).parent / "image"

    @staticmethod
    def find_file(filename):
        """查找文件"""
        image_path = FileService.IMAGE_DIR / filename
        if image_path.exists():
            return str(image_path)

        video_path = FileService.IMAGE_DIR / "video" / filename
        if video_path.exists():
            return str(video_path)

        return None

class TaskProcessor:
    """任务处理器"""

    @staticmethod
    def process_pending_queue():
        """处理待制造的队列"""
        print("\n" + "="*50)
        print("步骤1: 处理待制造的队列")
        print("="*50)

        queue_list = QueueService.get_public_list()
        if not queue_list:
            print("没有待处理的队列")
            return

        print(f"找到 {len(queue_list)} 个待处理的队列")

        for item in queue_list:
            work_id = item.get("work_id")
            if not work_id:
                continue

            detail = QueueService.get_public_detail(work_id)
            if not detail:
                continue

            result = WorkflowExecutor.execute_from_detail(detail)
            if result and result.get("prompt_id"):
                ProductionService.create(
                    result["prompt_id"],
                    result["work_id"],
                    "PRODUCING"
                )

    @staticmethod
    def check_production_completion():
        """检查生产完成情况"""
        print("\n" + "="*50)
        print("步骤2: 检查生产完成情况")
        print("="*50)

        production_list = ProductionService.get_public_list("PRODUCING")
        if not production_list or not production_list.get("data"):
            print("没有生产中的任务")
            return

        items = production_list["data"].get("list", [])
        if not items:
            print("没有生产中的任务")
            return

        print(f"找到 {len(items)} 个生产中的任务")

        for item in items:
            queue_id = item.get("queue_id")
            work_id = item.get("work_id")

            if not queue_id:
                continue

            # 查询详情
            detail = ProductionService.get_public_detail(queue_id)
            if not detail or not detail.get("data"):
                continue

            # 查询ComfyUI任务状态
            history = ComfyUIClient.get_history(queue_id)
            if not history or queue_id not in history:
                continue

            task_history = history[queue_id]
            outputs = task_history.get('outputs', {})

            if not outputs:
                continue

            print(f"任务 {queue_id} 已完成，找到输出")

            # 处理输出文件
            for node_id, node_output in outputs.items():
                if 'images' not in node_output:
                    continue

                for img in node_output['images']:
                    filename = img.get('filename')
                    if not filename:
                        continue

                    file_path = FileService.find_file(filename)
                    if file_path:
                        success, result = ProductionService.upload(work_id, queue_id, file_path)
                        if success:
                            print(f"文件上传成功")

def run_cycle():
    """执行一次循环"""
    print("\n" + "#"*60)
    print(f"开始执行循环 - {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("#"*60)

    TaskProcessor.process_pending_queue()
    TaskProcessor.check_production_completion()

    print("\n" + "#"*60)
    print(f"循环执行完成 - {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("#"*60)

def main():
    """主函数"""
    print("="*60)
    print("ComfyUI 任务处理脚本")
    print("="*60)
    print(f"API服务器: {APIConfig.API_BASE_URL}")
    print(f"ComfyUI服务器: {ComfyUIConfig.COMFYUI_BASE_URL}")
    print(f"图片目录: {FileService.IMAGE_DIR}")
    print("="*60)

    cycle_interval = 10  # 循环间隔（秒）

    while True:
        try:
            run_cycle()
            print(f"\n等待 {cycle_interval} 秒后执行下一次循环...\n")
            time.sleep(cycle_interval)
        except KeyboardInterrupt:
            print("\n\n脚本被用户中断，退出...")
            break
        except Exception as e:
            print(f"\n执行循环时出错: {str(e)}")
            print(f"等待 {cycle_interval} 秒后重试...\n")
            time.sleep(cycle_interval)

if __name__ == "__main__":
    main()