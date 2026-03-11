---
name: Finloop 资讯API调用技能
description: 当需要调用Finloop资讯相关接口时，请参考此规范。包括财经早餐、基金排行、股票排行、资讯列表、Banner列表、Banner详情等接口。
---

## 指令

1. **必须直接使用 HTTP 请求调用接口**：使用 fetch、axios、curl 或其他 HTTP 客户端直接调用接口，禁止创建任何封装函数或 JS/TS 文件
2. **禁止创建封装函数**：不要创建任何 `.js`、`.ts` 文件来封装接口调用，必须直接使用 HTTP 请求
3. **接口基础域名**：`https://aiapi-sit.finloopg.com`（开发环境）或根据实际环境配置
4. **请求头**：`Content-Type: application/json`
5. **响应格式**：接口返回的数据结构为 `{ code: 200, data: {...} }`，需要从响应中提取 `data` 字段
6. **错误处理**：需要检查响应状态码和错误信息，进行适当的错误处理

## 接口列表

### 1. 首页财经早餐接口
- **接口地址**：`/flp-news-api/v1/news-agent/financeBreakfast`
- **请求方法**：POST
- **完整路径**：`https://aiapi-sit.finloopg.com/flp-news-api/v1/news-agent/financeBreakfast`
- **详细文档**：见 `references/REFERENCE.md`

### 2. 获取收益率最高的20条基金
- **接口地址**：`/flp-news-api/v1/news-agent/topFundsByReturn`
- **请求方法**：GET
- **完整路径**：`https://aiapi-sit.finloopg.com/flp-news-api/v1/news-agent/topFundsByReturn`
- **详细文档**：见 `references/REFERENCE.md`

### 3. 获取收益率最高的20条股票
- **接口地址**：`/flp-news-api/v1/news-agent/topStocksByReturn`
- **请求方法**：GET
- **完整路径**：`https://aiapi-sit.finloopg.com/flp-news-api/v1/news-agent/topStocksByReturn`
- **详细文档**：见 `references/REFERENCE.md`

### 4. 资讯列表接口
- **接口地址**：`/flp-news-api/v1/news-agent/informationList`
- **请求方法**：POST
- **完整路径**：`https://aiapi-sit.finloopg.com/flp-news-api/v1/news-agent/informationList`
- **详细文档**：见 `references/REFERENCE.md`

### 5. Banner列表接口
- **接口地址**：`/flp-news-api/v1/news-agent/banner/list`
- **请求方法**：GET
- **完整路径**：`https://aiapi-sit.finloopg.com/flp-news-api/v1/news-agent/banner/list`
- **详细文档**：见 `references/REFERENCE.md`

### 6. Banner详情接口
- **接口地址**：`/flp-news-api/v1/news-agent/bannerDetail`
- **请求方法**：POST
- **完整路径**：`https://aiapi-sit.finloopg.com/flp-news-api/v1/news-agent/bannerDetail`
- **详细文档**：见 `references/REFERENCE.md`

## 快速使用

### 调用示例

**获取财经早餐**
- 请求方法：POST
- 请求URL：`https://aiapi-sit.finloopg.com/flp-news-api/v1/news-agent/financeBreakfast`
- 请求头：`Content-Type: application/json`
- 请求体：根据实际业务需求确定

### 场景预设

- **场景1**：用户询问"给我十条资讯" → 调用资讯列表接口，`category: 'discover'`, `page_size: 10`
- **场景2**：用户询问"今日的AI热闻" → 调用Banner列表接口，然后查询所有Banner详情
- **场景3**：用户询问"财经早餐"、"港股午盘"、"港股收盘" → 调用财经早餐接口
- **场景4**：用户询问"收益率最高的基金"、"基金排行榜" → 调用基金排行接口
- **场景5**：用户询问"收益率最高的股票"、"股票排行榜" → 调用股票排行接口
- **场景6**：用户询问"今天AI的十条资讯"、"今天XX的N条资讯" → 调用资讯列表接口，指定分类和数量
- **场景7**：用户询问"搜索XXX的资讯"、"查找XXX相关资讯" → 调用资讯列表接口，使用关键词搜索
- **场景8**：用户询问"给我更多资讯"、"下一页资讯" → 调用资讯列表接口，使用分页参数

详细场景说明见 `references/REFERENCE.md`

## 重要规则

1. **必须直接使用 HTTP 请求**，禁止创建封装函数或 JS/TS 文件
2. **参数命名**：资讯列表接口使用下划线 `page_size`，不是驼峰 `pageSize`
3. **响应处理**：检查 `code` 字段，从 `data` 字段获取实际数据
4. **Banner查询**：查询详情时必须先查列表，再批量查询详情

## 相关文档

- **详细接口文档**：`references/REFERENCE.md` - 包含完整的参数说明、响应结构、使用场景
- **测试脚本**：`scripts/` - 包含接口测试脚本
- **配置模板**：`assets/` - 包含请求配置模板
