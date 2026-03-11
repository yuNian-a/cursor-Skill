# 发布指南

## 发布到 npm

### 1. 准备工作

确保你已经：
- 注册了 npm 账号 (https://www.npmjs.com/signup)
- 登录了 npm (`npm login`)
- 更新了 `package.json` 中的版本号

### 2. 发布步骤

#### 方法一：使用发布脚本（推荐）

```bash
# Windows (Git Bash)
bash scripts/publish.sh

# Linux/Mac
chmod +x scripts/publish.sh
./scripts/publish.sh
```

#### 方法二：手动发布

```bash
# 1. 检查包内容
npm pack --dry-run

# 2. 发布 (scoped package 需要 --access public)
npm publish --access public
```

### 3. 发布后使用

发布成功后，其他用户可以通过以下方式安装你的 skills：

```bash
# 列出所有可用的 skills
npx @mierhaosi3/cursor-skills list

# 安装指定的 skill
npx @mierhaosi3/cursor-skills install news-agent-api
```

### 4. 更新版本

当你更新了 skills 内容后：

1. 更新 `package.json` 中的版本号
2. 更新对应 skill 的 `skill-manifest.json` 中的版本号
3. 重新发布：`npm publish`

### 5. 注意事项

- 确保 `.npmignore` 文件正确配置，避免发布不必要的文件
- 发布前测试安装流程：`npm pack` 然后解压测试
- 如果包名已被占用，需要修改 `package.json` 中的 `name` 字段

