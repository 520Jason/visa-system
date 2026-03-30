"""
🛂 签证系统 - GitHub 自动上传脚本
使用方法：
1. 获取 GitHub Token: https://github.com/settings/tokens
2. 运行：python upload_to_github.py 你的用户名 你的Token 仓库名
"""

import os
import sys
import requests
import base64
from pathlib import Path

# GitHub API 配置
GITHUB_API = "https://api.github.com"

def get_token():
    """获取 GitHub Token"""
    print("=" * 50)
    print("🔑 获取 GitHub Token 步骤：")
    print("=" * 50)
    print("1. 访问：https://github.com/settings/tokens")
    print("2. 点击 'Generate new token (classic)'")
    print("3. 填写 Note: visa-system")
    print("4. 勾选 scopes: repo, workflow")
    print("5. 点击 'Generate token'")
    print("6. 复制生成的 token（只显示一次！）")
    print("=" * 50)
    return input("请输入你的 GitHub Token: ").strip()

def create_repo(username, token, repo_name, description="签证办理系统 - Python FastAPI"):
    """创建 GitHub 仓库"""
    url = f"{GITHUB_API}/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": repo_name,
        "description": description,
        "private": False,
        "auto_init": True
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 201:
        print(f"✅ 仓库创建成功：{username}/{repo_name}")
        return True
    elif response.status_code == 422:
        print(f"⚠️  仓库已存在：{username}/{repo_name}")
        return True
    else:
        print(f"❌ 创建失败：{response.status_code}")
        print(response.json())
        return False

def upload_file(username, token, repo_name, file_path, commit_message="Upload file"):
    """上传单个文件到 GitHub"""
    # 读取文件内容
    with open(file_path, 'rb') as f:
        content = f.read()
    
    # Base64 编码
    content_base64 = base64.b64encode(content).decode('utf-8')
    
    # GitHub 上的路径（相对于项目根目录）
    github_path = file_path.replace('visa-project\\', '').replace('visa-project/', '')
    
    url = f"{GITHUB_API}/repos/{username}/{repo_name}/contents/{github_path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    # 检查文件是否已存在
    check_response = requests.get(url, headers=headers)
    
    if check_response.status_code == 200:
        # 文件存在，需要更新
        sha = check_response.json().get('sha')
        data = {
            "message": f"Update {github_path}",
            "content": content_base64,
            "sha": sha
        }
        response = requests.put(url, json=data, headers=headers)
    else:
        # 文件不存在，创建新文件
        data = {
            "message": commit_message,
            "content": content_base64
        }
        response = requests.put(url, json=data, headers=headers)
    
    if response.status_code in [200, 201]:
        print(f"  ✅ {github_path}")
        return True
    else:
        print(f"  ❌ {github_path}: {response.status_code}")
        return False

def upload_project(username, token, repo_name):
    """上传整个项目"""
    project_dir = Path("visa-project")
    
    if not project_dir.exists():
        print(f"❌ 项目目录不存在：{project_dir}")
        return False
    
    print(f"\n📁 开始上传项目到 {username}/{repo_name}...")
    print("=" * 50)
    
    # 需要上传的文件
    files_to_upload = []
    
    # 遍历项目目录
    for root, dirs, files in os.walk(project_dir):
        # 跳过不需要的目录
        dirs[:] = [d for d in dirs if d not in ['__pycache__', 'node_modules', '.git', 'uploads', '.idea', '.vscode']]
        
        for file in files:
            # 跳过不需要的文件
            if file.endswith(('.pyc', '.pyo', '.log', '.db', '.sqlite')):
                continue
            if file == '.env':
                continue
            
            file_path = Path(root) / file
            files_to_upload.append(file_path)
    
    # 上传文件
    success_count = 0
    for file_path in files_to_upload:
        if upload_file(username, token, repo_name, str(file_path)):
            success_count += 1
    
    print("=" * 50)
    print(f"✅ 上传完成：{success_count}/{len(files_to_upload)} 个文件")
    print(f"\n🌐 访问你的仓库：https://github.com/{username}/{repo_name}")
    
    return True

def main():
    print("\n" + "=" * 50)
    print("🛂 签证系统 - GitHub 自动上传工具")
    print("=" * 50 + "\n")
    
    # 获取用户信息
    if len(sys.argv) >= 4:
        username = sys.argv[1]
        token = sys.argv[2]
        repo_name = sys.argv[3]
    else:
        username = input("请输入你的 GitHub 用户名: ").strip()
        token = get_token()
        repo_name = input("请输入仓库名 (默认: visa-system): ").strip() or "visa-system"
    
    print(f"\n📋 配置信息：")
    print(f"  用户名：{username}")
    print(f"  仓库名：{repo_name}")
    print(f"  项目目录：visa-project/")
    print()
    
    # 创建仓库
    if not create_repo(username, token, repo_name):
        return
    
    # 上传项目
    upload_project(username, token, repo_name)

if __name__ == "__main__":
    try:
        import requests
        main()
    except ImportError:
        print("❌ 缺少依赖：requests")
        print("请运行：pip install requests")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  用户取消操作")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        sys.exit(1)
