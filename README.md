# 自动续期服务器

使用 GitHub Actions 自动执行服务器续期任务。

## 设置步骤

1. Fork 或创建此仓库
2. 进入 Settings → Secrets and variables → Actions
3. 添加以下 Secrets：
   - `RENEW_URL`: 续期页面的完整 URL
   - `USERNAME`: 登录用户名（如果需要）
   - `PASSWORD`: 登录密码（如果需要）

4. 启用 GitHub Actions（Actions 标签页）

## 手动触发

进入 Actions → Auto Renew Server → Run workflow

## 查看结果

- 执行日志：Actions 标签页查看每次运行的详细日志
- 截图：每次运行后会上传截图，保存30天