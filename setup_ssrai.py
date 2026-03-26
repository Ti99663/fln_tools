#!/usr/bin/env python
"""
SSRAI 配置助手
帮助用户快速配置 SSRAI API 相关参数
"""

import os
import sys

def setup_ssrai_config():
    """交互式配置 SSRAI"""
    print("\n" + "="*60)
    print("🔧 SSRAI (GPT-4o) 配置助手")
    print("="*60)
    
    print("\n📋 请按照以下步骤配置 SSRAI:\n")
    
    # 获取 API 端点
    print("1️⃣  SSRAI API 端点")
    print("   提示: 通常格式为 https://api.example.com/v1 或类似")
    api_endpoint = input("   请输入 API 端点 URL: ").strip()
    
    if not api_endpoint:
        print("❌ API 端点不能为空!")
        return False
    
    # 获取 API Key
    print("\n2️⃣  SSRAI API Key")
    print("   提示: 从你的公司 SSRAI 平台获取")
    api_key = input("   请输入 API Key: ").strip()
    
    if not api_key:
        print("❌ API Key 不能为空!")
        return False
    
    # 获取模型名称
    print("\n3️⃣  模型选择")
    print("   常见选项: gpt-4o, gpt-4-turbo, gpt-3.5-turbo 等")
    model = input("   请输入模型名称 (默认: gpt-4o): ").strip() or "gpt-4o"
    
    # 保存到 .env 文件
    env_file = ".env"
    
    # 读取现有配置
    config = {}
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    
    # 更新 SSRAI 配置
    config['SSRAI_API_ENDPOINT'] = api_endpoint
    config['SSRAI_API_KEY'] = api_key
    config['SSRAI_MODEL'] = model
    
    # 写入 .env 文件
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write("# ============ SSRAI 配置 ============\n")
        f.write(f"SSRAI_API_ENDPOINT={config['SSRAI_API_ENDPOINT']}\n")
        f.write(f"SSRAI_API_KEY={config['SSRAI_API_KEY']}\n")
        f.write(f"SSRAI_MODEL={config['SSRAI_MODEL']}\n")
        f.write("\n# ============ 其他配置 ============\n")
        for key, value in config.items():
            if key not in ['SSRAI_API_ENDPOINT', 'SSRAI_API_KEY', 'SSRAI_MODEL']:
                f.write(f"{key}={value}\n")
    
    # 验证配置
    print("\n" + "="*60)
    print("✅ SSRAI 配置已保存!")
    print("="*60)
    print(f"\n配置信息:")
    print(f"  API 端点: {api_endpoint}")
    print(f"  模型: {model}")
    print(f"  配置文件: .env")
    
    print("\n🚀 接下来的步骤:")
    print("  1. 激活虚拟环境: & apitest\\Scripts\\Activate.ps1")
    print("  2. 运行 POC:     python run_poc.py")
    print("  3. 选择选项 4 使用 SSRAI")
    
    return True

def test_ssrai_connection():
    """测试 SSRAI 连接"""
    print("\n" + "="*60)
    print("🧪 测试 SSRAI 连接")
    print("="*60)
    
    api_endpoint = os.getenv('SSRAI_API_ENDPOINT')
    api_key = os.getenv('SSRAI_API_KEY')
    model = os.getenv('SSRAI_MODEL', 'gpt-4o')
    
    if not api_endpoint or not api_key:
        print("❌ 请先运行配置助手设置 SSRAI 参数")
        return False
    
    print(f"\n测试配置:")
    print(f"  端点: {api_endpoint}")
    print(f"  模型: {model}")
    
    try:
        import requests
        
        print("\n正在测试连接...")
        response = requests.post(
            f"{api_endpoint}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 50
            },
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ SSRAI 连接成功!")
            print(f"   响应: {response.json()['choices'][0]['message']['content'][:100]}")
            return True
        else:
            print(f"❌ SSRAI API 返回错误: {response.status_code}")
            print(f"   详情: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ 连接失败: {str(e)}")
        return False

def main():
    """主函数"""
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            test_ssrai_connection()
        else:
            print("用法: python setup_ssrai.py [test]")
    else:
        # 检查现有配置
        if os.path.exists('.env') and os.getenv('SSRAI_API_ENDPOINT'):
            print("\n📋 检测到现有 SSRAI 配置:")
            print(f"  端点: {os.getenv('SSRAI_API_ENDPOINT')}")
            print(f"  模型: {os.getenv('SSRAI_MODEL', 'gpt-4o')}")
            
            choice = input("\n是否要重新配置? (y/n): ").strip().lower()
            if choice != 'y':
                print("\n💡 提示: 运行 python setup_ssrai.py test 来测试连接")
                return
        
        # 运行配置
        if setup_ssrai_config():
            print("\n💡 提示: 运行 python setup_ssrai.py test 来测试连接")
        else:
            print("❌ 配置失败")
            sys.exit(1)

if __name__ == "__main__":
    main()
