---
name: Finloop 资讯API调用技能
description: 当需要调用Finloop资讯相关接口时，请参考此规范。包括财经早餐、资讯列表、AI热闻、股票行情。
---

## 指令
  
1. **必须直接使用 HTTP 请求调用接口**：使用curl 直接调用接口
2. **接口基础域名**：`https://aiapi-sit.finloopg.com`
4. **请求头**：`Content-Type: application/json`
5. **响应格式**：接口返回的数据结构为 `{ code: 200, data: {...} }`，需要从响应中提取 `data` 字段
6. **错误处理**：需要检查响应状态码和错误信息，进行适当的错误处理

## 场景预设

### 场景1：用户询问"给我十条资讯"或"给我十条XX方面的资讯"

**触发条件：**
当用户询问"给我十条资讯"、"给我十条新闻"、"给我十条XX方面的资讯"等类似问题时。

**传参调用：**
- **接口**：POST `https://aiapi-sit.finloopg.com/flp-news-api/v1/news-agent/informationList`
- **请求头**：`Content-Type: application/json`
- **请求体参数**：
  - `category`: 新闻分类（string），如果用户未指定分类或只问"给我十条资讯"，使用 `'discover'`；如果用户明确指定分类，根据分类关键词映射到对应的分类值
  - `page_size`: 每页加载条数（number），例如：`10`

**示例请求体：**
```json
{
  "category": "discover",
  "page_size": 10
}
```

---

### 场景2：用户询问"今日的AI热闻"

**触发条件：**
当用户询问"今日的AI热闻"或类似问题时（如"今天的AI热点"、"AI热门新闻"等）。

**传参调用：**

1. **第一步：查询AI热闻列表**
   - **接口**：GET `https://aiapi-sit.finloopg.com/flp-news-api/v1/news-agent/banner/list`
   - **请求头**：`Content-Type: application/json`（可能需要 Cookie 认证 `sl-session`）
   - **请求参数**：无需请求体参数

2. **第二步：查询AI热闻详情**
   - **接口**：POST `https://aiapi-sit.finloopg.com/flp-news-api/v1/news-agent/bannerDetail`
   - **请求头**：`Content-Type: application/json`
   - **请求体参数**：
     - `id`: XCF资讯ID（string，来自第一步返回的 `banner_list` 中每个AI热闻的 `xcf_id` 字段）
   - **重要**：必须从第一步的列表中提取所有 `xcf_id`，然后分别调用详情接口获取每个AI热闻的完整详情

**示例请求体（详情接口）：**
```json
{
  "id": "21640"
}
```

---

### 场景3：用户询问"财经早餐"、"港股午盘"、"港股收盘"

**触发条件：**
当用户询问"财经早餐"、"港股午盘"、"港股收盘"、"今天的财经早餐"、"今日财经早餐"、"收盘汇"等类似问题时。

**传参调用：**
- **接口**：POST `https://aiapi-sit.finloopg.com/flp-news-api/v1/news-agent/financeBreakfast`
- **请求头**：`Content-Type: application/json`
- **请求体参数**：无需请求体参数
- **说明**：此接口会根据当前时间自动返回对应时段的内容（早晨返回财经早餐，中午返回港股午盘，收盘时段返回港股收盘），无需在请求中指定时间或类型

---

### 场景4：用户询问"今天AI的十条资讯"、"今天XX的N条资讯"

**触发条件：**
当用户询问"今天AI的十条资讯"、"今天AI的10条资讯"、"今天RWA的二十条资讯"、"今天宏观的5条资讯"、"今天XX的N条资讯"等类似问题时。

**传参调用：**
- **接口**：POST `https://aiapi-sit.finloopg.com/flp-news-api/v1/news-agent/informationList`
- **请求头**：`Content-Type: application/json`
- **请求体参数**：
  - `category`: 新闻分类（string），根据用户询问中的分类关键词映射到对应的分类值，如果未指定分类，默认使用 `'discover'`
  - `page_size`: 每页加载条数（number），根据用户询问中的数量关键词解析为数字，如果未指定数量，默认使用 `10`

**示例请求体：**
```json
{
  "category": "ai",
  "page_size": 10
}
```

---

### 场景5：用户询问"搜索XXX的资讯"、"查找XXX相关资讯"

**触发条件：**
当用户询问"搜索XXX的资讯"、"查找XXX相关资讯"、"搜索XXX"、"查找XXX"、"XXX相关的资讯"、"关于XXX的资讯"、"XXX的新闻"等类似问题时。

**传参调用：**
- **接口**：POST `https://aiapi-sit.finloopg.com/flp-news-api/v1/news-agent/informationList`
- **请求头**：`Content-Type: application/json`
- **请求体参数**：
  - `keyword`: 搜索关键词（string，必填），从用户询问中提取
  - `category`: 新闻分类（string，可选），如果用户同时指定了分类，使用对应的分类值
  - `page_size`: 每页数量（number，可选），默认 `10`

**示例请求体：**
```json
{
  "keyword": "股票",
  "category": "market",
  "page_size": 10
}
```

---

### 场景6：用户询问"给我更多资讯"、"下一页资讯"

**触发条件：**
当用户询问"给我更多资讯"、"下一页资讯"、"加载更多"、"继续加载"、"更多XX资讯"等类似问题时。

**传参调用：**
- **接口**：POST `https://aiapi-sit.finloopg.com/flp-news-api/v1/news-agent/informationList`
- **请求头**：`Content-Type: application/json`
- **请求体参数**：
  - `category`: 新闻分类（string），如果用户指定了分类，使用对应的分类值；如果未指定，使用 `'discover'`（发现）
  - `page_size`: 每页数量（number），与上一次查询保持一致，或使用默认值 `10`
  - `news_id`: 分页游标（string，必填），上一次查询返回的最后一条资讯的ID

**示例请求体：**
```json
{
  "category": "discover",
  "page_size": 10,
  "news_id": "AICL000001"
}
```

**重要提示：**
- 需要保存上一次查询的结果，以便获取最后一条资讯的ID作为 `news_id` 参数

---

### 场景7：用户询问某只股票的行情

**触发条件：**
当用户询问某只股票的行情时，例如：
- "HSI.HK的行情"
- "恒生指数的行情"
- "BABA.US的股价"
- "苹果股票的行情"
- "AAPL的行情"
- "道琼斯指数的行情"
- "上证指数的行情"
- 其他类似的股票行情查询问题

**传参调用：**
- **接口**：POST `https://papi-sit.finloopg.com/flp-mktdata-hub/v1/stock/quote`
- **请求头**：
  - `Content-Type: application/json`
- **请求体参数**：
  - `tickers`: 股票代码列表（list，必填），每个元素按照"代码.市场"格式，如 `"BABA.US"`、`"HSI.HK"` 等
  - 支持的市场代码：
    - 港股：`.HK`
    - 美股：`.US`
    - A股：`.SZ`（深交所）、`.SH`（上交所）、`.BJ`（北交所）
    - 指数：支持部分指数行情（见下方支持的指数列表）

**示例请求体：**
```json
{
    "tickers": ["HSI.HK"]
}
```

**重要提示：**
- 必须从用户询问中提取股票代码，并转换为"代码.市场"格式
- 如果用户提到股票名称或指数名称，需要依靠 skill 来主动转换为对应的股票代码（ISIN格式）
- 无法提供全面的转换规则或枚举，需要 skill 根据实际情况进行转换
- 输出时必须包含所有返回的字段信息

---

详细接口文档见 `references/REFERENCE.md`

## 重要规则

1. **必须直接使用 HTTP 请求调用接口**：使用curl直接调用接口，禁止创建任何封装函数
2. **参数命名**：资讯列表接口使用下划线 `page_size`，不是驼峰 `pageSize`
3. **响应处理**：检查 `code` 字段，从 `data` 字段获取实际数据
4. **AI热闻查询**：查询详情时必须先查列表，再批量查询详情
5. **财经早餐接口时间逻辑**：接口会根据当前时间自动返回财经早餐、港股午盘或港股收盘，无需指定时间参数
6. **股票行情查询**：查询股票行情时必须包含所有返回的字段信息，如果用户提到股票名称或指数名称，需要依靠 skill 来主动转换为对应的股票代码（ISIN格式）

## 相关文档

- **详细接口文档**：`references/REFERENCE.md` - 包含完整的参数说明、响应结构
