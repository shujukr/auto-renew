# 自动续期服务器

使用 GitHub Actions 自动执行服务器续期任务。

## 设置步骤

1. Fork 或创建此仓库
2. 进入 设置 → 安全 → 机密和变量 → 操作
3. 添加以下机密（Secrets）：
   - `RENEW_URL`: 续期页面的完整 URL
   - `COOKIES`: 登录后的 Cookie 字符串（推荐方式）
   
   **或者使用用户名密码**（备用方式）：
   - `USERNAME`: 登录用户名
   - `PASSWORD`: 登录密码

4. 启用 GitHub Actions（操作标签页）

## 获取 Cookie 的方法

1. 用 Chrome 登录网站
2. 按 F12 → 应用程序 → Cookie → 选择网站
3. 复制所有 Cookie 为格式：`name1=value1; name2=value2`
4. 粘贴到 COOKIES 机密中

## 手动触发

进入 操作 → Auto Renew Server → 运行工作流

## 查看结果

- 执行日志：操作标签页查看每次运行的详细日志
- 截图：每次运行后会上传截图，保存30天
