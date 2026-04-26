import requests
import json
import time
import os
from pathlib import Path

def get_comfyui_url(endpoint, base_url="http://127.0.0.1:6401"):
    """构建ComfyUI API URL"""
    url = f"{base_url}/{endpoint.lstrip('/')}"
    return url

def query_production_list(base_url, status="PRODUCING"):
    """查询生产状态列表"""
    print(f"\n正在查询生产状态列表，状态: {status}")

    try:
        response = requests.post(
            f"{base_url}/production/public/list",
            json={"status": status}
        )

        if response.status_code == 200:
            result = response.json()
            print(f"查询成功: {json.dumps(result, ensure_ascii=False)}")
            return result
        else:
            print(f"查询失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            return None
    except Exception as e:
        print(f"查询时出错: {str(e)}")
        return None

def query_production_detail(base_url, queue_id):
    """查询生产详情"""
    print(f"\n正在查询生产详情，queue_id: {queue_id}")

    try:
        response = requests.post(
            f"{base_url}/production/public/detail",
            json={"queue_id": queue_id}
        )

        if response.status_code == 200:
            result = response.json()
            print(f"查询成功")
            return result
        else:
            print(f"查询失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"查询时出错: {str(e)}")
        return None

def check_comfyui_task(comfyui_base_url, prompt_id):
    """查询ComfyUI任务状态"""
    print(f"\n正在查询ComfyUI任务状态，prompt_id: {prompt_id}")

    try:
        url = get_comfyui_url(f'/history/{prompt_id}', comfyui_base_url)
        response = requests.get(url)

        if response.status_code == 200:
            result = response.json()
            print(f"查询成功")
            return result
        else:
            print(f"查询失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"查询时出错: {str(e)}")
        return None

def find_image_file(image_dir, filename):
    """在Image目录中查找文件"""
    print(f"\n正在查找文件: {filename} 在目录: {image_dir}")

    image_path = Path(image_dir) / filename
    if image_path.exists():
        print(f"找到文件: {image_path}")
        return str(image_path)

    video_path = Path(image_dir) / "video" / filename
    if video_path.exists():
        print(f"找到文件: {video_path}")
        return str(video_path)

    print(f"未找到文件: {filename}")
    return None

def upload_file(base_url, work_id, queue_id, file_path):
    """上传文件到服务器"""
    print(f"\n正在上传文件...")
    print(f"work_id: {work_id}, queue_id: {queue_id}, file_path: {file_path}")

    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {
                'work_id': work_id,
                'queue_id': queue_id
            }
            response = requests.post(
                f"{base_url}/production/upload",
                files=files,
                data=data
            )

        if response.status_code == 200:
            result = response.json()
            print(f"上传成功: {json.dumps(result, ensure_ascii=False)}")
            return True, result
        else:
            print(f"上传失败: {response.status_code}")
            print(f"响应内容: {response.text}")
            return False, None
    except Exception as e:
        print(f"上传时出错: {str(e)}")
        return False, None

def main():
    # API服务器地址
    api_base_url = "http://localhost:5000"
    # ComfyUI服务器地址
    comfyui_base_url = "http://127.0.0.1:6401"
    # Image目录
    image_dir = Path(__file__).parent / "image"

    # 1. 查询生产状态为PRODUCING的列表
    production_list = query_production_list(api_base_url, "PRODUCING")

    if not production_list or not production_list.get("data") or not production_list["data"].get("list"):
        print("没有找到生产中的任务")
        return

    # 2. 获取前5个任务
    items = production_list["data"]["list"][:5]
    print(f"\n获取到 {len(items)} 个生产中的任务")

    for i, item in enumerate(items):
        print(f"\n{'='*50}")
        print(f"处理第 {i+1} 个任务")

        queue_id = item.get("queue_id")
        work_id = item.get("work_id")

        if not queue_id:
            print("任务中没有queue_id，跳过")
            continue

        # 3. 查询详情
        detail = query_production_detail(api_base_url, queue_id)
        if not detail or not detail.get("data"):
            print("查询详情失败，跳过")
            continue

        detail_data = detail["data"]
        print(f"任务详情: queue_id={queue_id}, work_id={work_id}, status={detail_data.get('status')}")

        # 4. 用queue_id去ComfyUI查询任务状态
        history = check_comfyui_task(comfyui_base_url, queue_id)

        if not history or queue_id not in history:
            print("ComfyUI中没有找到该任务的历史记录")
            continue

        task_history = history[queue_id]
        outputs = task_history.get('outputs', {})

        if not outputs:
            print("任务尚未完成，没有输出")
            continue

        print(f"任务已完成，找到输出: {json.dumps(outputs, ensure_ascii=False)}")

        # 5. 从outputs中提取文件名
        for node_id, node_output in outputs.items():
            if 'images' in node_output:
                for img in node_output['images']:
                    filename = img.get('filename')
                    if filename:
                        # 6. 查找文件
                        file_path = find_image_file(image_dir, filename)
                        if file_path:
                            # 7. 上传文件
                            success, result = upload_file(api_base_url, work_id, queue_id, file_path)
                            if success:
                                print(f"文件上传成功")
                            else:
                                print(f"文件上传失败")

if __name__ == "__main__":
    main()