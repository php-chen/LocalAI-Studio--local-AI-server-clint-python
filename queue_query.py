import requests
import json

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
                    print(f"详情信息: {json.dumps(detail_data, ensure_ascii=False)}")
                    
                    # 3. 根据作品信息执行任务
                    if detail_data.get("data"):
                        creation = detail_data["data"].get("creation")
                        models = detail_data["data"].get("models")
                        
                        if creation:
                            content = creation.get("content")
                            creation_id = creation.get("creation_id")
                            
                            if content:
                                print(f"\n正在执行任务: {content}")
                                # 假设使用文字生成图片工作流
                                workflow_name = "image_z_image_turbo"
                                
                                # 构建请求数据
                                request_data = {
                                    "prompt": content
                                }
                                
                                # 调用工作流执行接口
                                workflow_response = requests.post(
                                    f"{base_url}/api/workflow/{workflow_name}",
                                    json=request_data
                                )
                                
                                if workflow_response.status_code == 200:
                                    workflow_result = workflow_response.json()
                                    print("任务执行请求成功")
                                    print(f"执行结果: {json.dumps(workflow_result, ensure_ascii=False)}")
                                    
                                    # 获取prompt_id
                                    prompt_id = workflow_result.get("prompt_id")
                                    if prompt_id:
                                        print(f"\n任务已提交，prompt_id: {prompt_id}")
                                        # 可以在这里添加任务状态查询逻辑
                                else:
                                    print(f"任务执行请求失败: {workflow_response.status_code}")
                                    print(f"响应内容: {workflow_response.text}")
                            else:
                                print("作品详情中没有content字段")
                        else:
                            print("作品详情中没有creation字段")
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