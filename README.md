# Mstic_Island_Auto  
**链游神秘岛自动化脚本**  

## 简介  
Mstic_Island_Auto 是一个专为链游“神秘岛”设计的自动化脚本，旨在通过模拟网络请求完成游戏内特定任务，从而提升游戏效率。  
我就开了1地，后续会更新2地的脚本

---

## 功能特点  
- 自动连接钱包完成任务  
- 支持批量操作  
- 可扩展性强，便于定制  

---

## 安装与配置  

### 环境要求  
- Python 版本：3.8 或以上  
- 依赖库：脚本运行所需依赖请参考 `requirements.txt`  

### 获取 Authorization Key  
1. 登录神秘岛网页端并连接您的钱包。  
2. 按 `F12` 打开开发者工具，选择 **Network** 标签页。  
3. 滑动到底部找到任意请求记录，点击进入详情页。  
4. 定位到 **Headers** 中的 **Authorization** 字段，复制其值。  
5. 将复制的值粘贴到脚本中，赋值给变量 `key`：  
   ```python
   key = "your_authorization_key_here"

  
