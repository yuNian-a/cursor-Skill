# Finloop 资讯API详细文档

本文档包含所有接口的详细说明、参数、响应结构和使用场景。

## 目录

- [接口详细说明](#接口详细说明)
- [Banner查询自动化流程](#banner查询自动化流程)
- [场景预设](#场景预设)
- [通用注意事项](#通用注意事项)

---

## 接口详细说明

### 1. 首页财经早餐接口

**接口信息：**
- 接口地址：`/flp-news-api/v1/news-agent/financeBreakfast`
- 请求方法：POST
- 完整路径：`https://aiapi-sit.finloopg.com/flp-news-api/v1/news-agent/financeBreakfast`

**参数：**
- 此接口为 POST 请求，请求体参数根据实际业务需求确定

**响应参数：**
- `title`: 标题（string）- 财经早餐或收盘汇
- `keyword`: 财经早餐关键词（Array）- 例如：["加密货币", "产业趋势"]
- `publish_time`: 发布时间（string）
- `summary`: 摘要（string）
- `newsCount`: 过去一天资讯数量（number）
- `sentiment`: 市场情绪（string）- 枚举值
- `title_original`: 原始title（string）
- `tag`: 类型标识（int）- 1:财经早餐，2:收盘汇

**使用说明：**
- 此接口用于获取首页财经早餐或收盘汇信息
- 返回数据包含关键词、摘要、市场情绪等综合信息

---

### 2. 获取收益率最高的20条基金

**接口信息：**
- 接口地址：`/flp-news-api/v1/news-agent/topFundsByReturn`
- 请求方法：GET
- 完整路径：`https://aiapi-sit.finloopg.com/flp-news-api/v1/news-agent/topFundsByReturn`

**参数：**
- 此接口为 GET 请求，无需请求体参数

**响应参数：**
返回数据为 `data[List]`，列表中的每个对象包含：
- `isin`: ISIN代码（string）- 例如："LU0496367417"
- `name`: 资产名称/公司名称（string）- 例如："BRAND ENGAGEMENT NETWORK"
- `currency`: 币种（string）
- `return_rate`: 最新成交价格（string）- 例如："222.3881"

**使用说明：**
- 此接口返回收益率最高的20条基金数据
- 数据按收益率从高到低排序
- 用于首页展示基金排行榜

---

### 3. 获取收益率最高的20条股票

**接口信息：**
- 接口地址：`/flp-news-api/v1/news-agent/topStocksByReturn`
- 请求方法：GET
- 完整路径：`https://aiapi-sit.finloopg.com/flp-news-api/v1/news-agent/topStocksByReturn`
- 注意：文档中路径可能为 `topFundsByReturn`，实际应为 `topStocksByReturn`，请以实际接口为准

**参数：**
- 此接口为 GET 请求，无需请求体参数

**响应参数：**
返回数据为 `data[List]`，列表中的每个对象包含：
- `ticker`: 资产代码/股票代码（string）- 例如："BNAI.US"
- `name`: 资产名称/公司名称（string）- 例如："BRAND ENGAGEMENT NETWORK"
- `change_rate`: 涨跌幅/回报率（百分比）（string）- 例如："90.3"
- `total_news_yesterday`: 最新成交价格（string）- 例如："16.48"

**使用说明：**
- 此接口返回收益率最高的20条股票数据
- 数据按收益率从高到低排序
- 用于首页展示股票排行榜

---

### 4. 资讯列表接口

**接口信息：**
- 接口地址：`/flp-news-api/v1/news-agent/informationList`
- 请求方法：POST
- 完整路径示例：`https://aiapi-sit.finloopg.com/flp-news-api/v1/news-agent/informationList`

**请求参数：**
- 必填参数：
  - `category`: 新闻分类（string），可选值：`"discover"`, `"subscribe"`, `"ai"`, `"rwa"`, `"macro"`, `"industry"`, `"market"`, `"company"`, `"viewpoint"`, `"fund"`, `"bond"`, `"bill"`, `"stock"`
  - `page_size`: 每页加载条数（number，注意：参数名使用下划线 `page_size`，不是驼峰 `pageSize`）
- 可选参数：
  - `keyword`: 关键词检索（string）
  - `news_id`: 分页游标，最后一条新闻的ID（用于分页加载）
  - `user_id`: 用户ID（string，订阅分类时必填）

**请求说明：**
- 基础调用：POST 请求，请求体包含 `category` 和 `page_size`
- 带分页：在请求体中添加 `news_id` 参数
- 带搜索关键词：在请求体中添加 `keyword` 参数

**响应参数：**
- `information_list`: 资讯列表数组（注意：字段名使用下划线）
- `total`: 总条数（number）- 例如：120
- `hasMore`: 是否存在更多新闻（Boolean）

**informationList 子参数：**
每个资讯对象包含：
- `newId`: 资讯ID（string）- 例如："AICL000001"
- `tags`: 资讯标签（Array）- 例如：["AI 热闻"]
- `title`: 资讯标题（string）
- `summary`: 资讯摘要（string）
- `imgUrl`: 资讯封面图（string）
- `publishTime`: 发布时间（string）
- `wordCount`: 正文字数（number）
- `readTime`: 预计阅读时间（分钟）（number）
- `influence`: 影响力（string）- 枚举值
- `influenceScore`: 影响力得分（string）- 枚举值
- `marketTrends`: 市场趋势列表（List）

**marketTrends 子参数：**
每个市场趋势对象包含：
- `ticker`: 挂钩标的（string）- 例如："AAPL"
- `changeRate`: 标的涨势（string）- 例如："-0.05"

**使用说明：**
- 此接口用于获取指定分类下的资讯列表数据
- 适用于信息流或列表页展示
- 支持关键词检索和分页加载
- 个性化分类需要传入 `user_id` 参数
- 注意：参数名使用下划线 `page_size`，不是驼峰 `pageSize`

---

### 5. Banner列表接口

**接口信息：**
- 接口地址：`/flp-news-api/v1/news-agent/banner/list`
- 请求方法：GET
- 完整路径示例：`https://aiapi-sit.finloopg.com/flp-news-api/v1/news-agent/banner/list`
- 注意：此接口可能需要 Cookie 认证（`sl-session`）

**参数：**
- 此接口为 GET 请求，无需请求体参数

**请求说明：**
- 此接口为 GET 请求，无需请求体参数
- 需要在请求头中携带 Cookie 认证信息（如 `sl-session`）

**返回数据：**
- `banner_list`: Banner列表数组，每个Banner包含：
  - `news_id`: 新闻ID
  - `xcf_id`: XCF资讯ID
  - `tag`: 标签数组
  - `title`: 标题
  - `summary`: 摘要
  - `img_url`: 图片URL（可能为null）

---

### 6. Banner详情接口

**接口信息：**
- 接口地址：`/flp-news-api/v1/news-agent/bannerDetail`
- 请求方法：POST
- 完整路径示例：`https://aiapi-sit.finloopg.com/flp-news-api/v1/news-agent/bannerDetail`

**参数：**
- 必填参数：
  - `id`: XCF资讯ID（来自banner的 `xcf_id` 字段），类型为字符串

**请求说明：**
- POST 请求，请求体包含 `id` 字段（XCF资讯ID，来自banner的 `xcf_id` 字段）
- 请求体格式：`{ "id": "21640" }`

**返回数据：**
- 返回 `XcfDetail` 类型的数据，包含Banner的详细信息

---

## Banner查询自动化流程

**重要：当需要查询Banner详情时，必须使用此自动化流程。**

### 自动化流程说明

当调用Banner查询时，系统会自动执行以下步骤：

1. **自动查询Banner列表**
   - 调用 GET `/flp-news-api/v1/news-agent/banner/list` 获取所有Banner
   
2. **自动提取所有xcf_id**
   - 从返回的 `banner_list` 中提取所有的 `xcf_id`
   - 通常返回3个Banner，每个Banner都有一个 `xcf_id`
   
3. **自动批量查询详情**
   - 使用提取的所有 `xcf_id`，分别调用 POST `/flp-news-api/v1/news-agent/bannerDetail` 接口
   - 获取每个Banner的完整详情信息

### 执行步骤说明

1. **步骤1：获取Banner列表**
   - 调用 GET `/flp-news-api/v1/news-agent/banner/list` 接口
   - 从响应的 `data.banner_list` 中获取所有Banner

2. **步骤2：提取所有xcf_id**
   - 遍历 `banner_list`，提取每个Banner的 `xcf_id` 字段
   - 过滤掉为 null 或 undefined 的 `xcf_id`

3. **步骤3：批量查询详情**
   - 对每个 `xcf_id`，直接使用 HTTP POST 请求调用 `/flp-news-api/v1/news-agent/bannerDetail` 接口
   - 请求体格式：`{ "id": "xcf_id值" }`
   - 建议使用并行请求提高效率
   - 如果某个详情查询失败，记录错误但继续处理其他Banner
   - **注意**：必须直接使用 HTTP 请求，不要创建封装函数

### 执行规则

**必须遵循以下规则：**
1. 查询Banner详情时，必须先查询Banner列表
2. 必须提取列表中的所有 `xcf_id`（不能只查询部分）
3. 必须使用所有提取的 `xcf_id` 分别调用详情接口
4. 如果某个详情查询失败，应该记录错误但继续处理其他Banner
5. 建议使用并行请求以提高效率

---

## 场景预设

### 场景1：用户询问"给我十条资讯"或"给我十条XX方面的资讯"

**触发条件：**
当用户询问"给我十条资讯"、"给我十条新闻"、"给我十条XX方面的资讯"等类似问题时，必须执行以下流程。

**分类映射规则：**
- 如果用户未指定分类或只问"给我十条资讯"，使用 `category: 'discover'`（发现分类）
- 如果用户明确指定分类，按以下映射：
  - "AI方面的资讯"、"AI资讯"、"人工智能资讯" → `category: 'ai'`
  - "RWA方面的资讯"、"RWA资讯" → `category: 'rwa'`
  - "宏观方面的资讯"、"宏观资讯" → `category: 'macro'`
  - "行业方面的资讯"、"行业资讯" → `category: 'industry'`
  - "市场方面的资讯"、"市场资讯" → `category: 'market'`
  - "公司方面的资讯"、"公司资讯" → `category: 'company'`
  - "观点方面的资讯"、"观点资讯" → `category: 'viewpoint'`
  - "基金方面的资讯"、"基金资讯" → `category: 'fund'`
  - "债券方面的资讯"、"债券资讯" → `category: 'bond'`
  - "票据方面的资讯"、"票据资讯" → `category: 'bill'`
  - "股票方面的资讯"、"股票资讯" → `category: 'stock'`

**执行流程：**

1. **确定分类**
   - 根据用户询问内容，确定对应的 `category` 参数
   - 如果未指定分类，默认使用 `'discover'`

2. **查询资讯列表**
   - 调用 POST `/flp-news-api/v1/news-agent/informationList` 接口
   - 请求体参数：`category` 为确定的分类，`page_size: 10`
   - 返回10条对应分类的资讯

**重要提示：**
- ✅ 当用户询问"给我十条资讯"时，默认查询 `discover` 分类
- ✅ 当用户询问"给我十条XX方面的资讯"时，根据XX映射到对应的分类
- ✅ 必须使用资讯列表接口 `/flp-news-api/v1/news-agent/informationList`，不是Banner接口
- ✅ `page_size` 参数名使用下划线，不是驼峰命名
- ❌ 不要使用Banner相关接口，这是资讯列表查询场景

---

### 场景2：用户询问"今日的AI热闻"

**触发条件：**
当用户询问"今日的AI热闻"或类似问题时（如"今天的AI热点"、"AI热门新闻"等），必须执行以下流程。

**执行流程：**

1. **查询Banner列表**
   - 调用 GET `/flp-news-api/v1/news-agent/banner/list` 获取所有Banner
   - Banner列表通常包含今日最热门的AI相关资讯

2. **查询Banner详情**
   - 从Banner列表中提取所有 `xcf_id`
   - 使用所有 `xcf_id` 分别调用 POST `/flp-news-api/v1/news-agent/bannerDetail` 获取每个Banner的完整详情
   - 请求体格式：`{ "id": "xcf_id值" }`
   - 必须查询所有Banner的详情，不能只查询部分

**重要提示：**
- ✅ 当用户询问"今日的AI热闻"时，必须执行完整的Banner查询流程
- ✅ 必须先查询Banner列表，再查询详情
- ✅ 必须查询所有Banner的详情，不能遗漏
- ❌ 不能直接查询资讯列表接口，必须使用Banner相关接口

---

### 场景3：用户询问"财经早餐"、"港股午盘"、"港股收盘"

**触发条件：**
当用户询问以下任何问题时，必须调用财经早餐接口：
- "财经早餐"
- "港股午盘"
- "港股收盘"
- "今天的财经早餐"
- "今日财经早餐"
- "收盘汇"
- 其他类似的财经早餐、午盘、收盘相关询问

**重要说明：**
- **财经早餐、港股午盘、港股收盘都代表调用同一个接口**：`/flp-news-api/v1/news-agent/financeBreakfast`
- 接口返回的 `tag` 字段会标识类型：1表示财经早餐，2表示收盘汇，3表示港股午盘等
- 接口返回的 `title` 字段会显示具体标题（如"财经早餐"、"港股午盘"、"港股收盘"等）

**执行流程：**

1. **调用财经早餐接口**
   - 调用 POST `/flp-news-api/v1/news-agent/financeBreakfast` 接口
   - 请求体参数根据实际业务需求确定
   - 返回数据包含标题、关键词、摘要、市场情绪等信息

**重要提示：**
- ✅ 无论用户问"财经早餐"、"港股午盘"还是"港股收盘"，都调用同一个接口
- ✅ 接口会根据时间自动返回对应类型的内容（财经早餐、午盘、收盘等）
- ✅ 返回的 `tag` 字段标识内容类型，`title` 字段显示具体标题
- ✅ 返回数据包含关键词、摘要、市场情绪等综合信息

---

### 场景4：用户询问"收益率最高的基金"、"基金排行榜"

**触发条件：**
当用户询问以下任何问题时，必须调用基金排行接口：
- "收益率最高的基金"
- "基金排行榜"
- "基金排行"
- "收益最好的基金"
- "基金收益率排行"
- 其他类似的基金排行相关询问

**执行流程：**

1. **调用基金排行接口**
   - 调用 GET `/flp-news-api/v1/news-agent/topFundsByReturn` 接口
   - 此接口为 GET 请求，无需请求体参数
   - 返回收益率最高的20条基金数据

**重要提示：**
- ✅ 返回数据按收益率从高到低排序
- ✅ 每个基金包含：ISIN代码、资产名称、币种、收益率等信息
- ✅ 用于首页展示基金排行榜

---

### 场景5：用户询问"收益率最高的股票"、"股票排行榜"

**触发条件：**
当用户询问以下任何问题时，必须调用股票排行接口：
- "收益率最高的股票"
- "股票排行榜"
- "股票排行"
- "收益最好的股票"
- "股票收益率排行"
- 其他类似的股票排行相关询问

**执行流程：**

1. **调用股票排行接口**
   - 调用 GET `/flp-news-api/v1/news-agent/topStocksByReturn` 接口
   - 此接口为 GET 请求，无需请求体参数
   - 返回收益率最高的20条股票数据

**重要提示：**
- ✅ 返回数据按收益率从高到低排序
- ✅ 每个股票包含：股票代码、公司名称、涨跌幅、最新成交价格等信息
- ✅ 用于首页展示股票排行榜

---

### 场景6：用户询问"今天AI的十条资讯"、"今天XX的N条资讯"

**触发条件：**
当用户询问以下任何问题时，必须调用资讯列表接口，并指定分类和数量：
- "今天AI的十条资讯"
- "今天AI的10条资讯"
- "今天RWA的二十条资讯"
- "今天宏观的5条资讯"
- "今天XX的N条资讯"（XX为分类，N为数量）
- "给我今天AI的十条新闻"
- "今天XX方面的N条资讯"
- 其他类似的指定分类和数量的询问

**执行流程：**

1. **解析用户需求**
   - 提取分类关键词（如"AI"、"RWA"、"宏观"等），映射到对应的 `category` 参数
   - 提取数量关键词（如"十条"、"10条"、"二十条"、"20条"等），转换为数字作为 `page_size` 参数
   - 如果未指定分类，默认使用 `category: 'discover'`
   - 如果未指定数量，默认使用 `page_size: 10`

2. **调用资讯列表接口**
   - 调用 POST `/flp-news-api/v1/news-agent/informationList` 接口
   - 请求体参数：
     - `category`: 根据用户询问确定的分类（如 'ai'、'rwa'、'macro' 等）
     - `page_size`: 根据用户询问确定的数量（如 10、20、5 等）

**分类映射规则：**
- "AI"、"人工智能" → `category: 'ai'`
- "RWA" → `category: 'rwa'`
- "宏观" → `category: 'macro'`
- "行业" → `category: 'industry'`
- "市场" → `category: 'market'`
- "公司" → `category: 'company'`
- "观点" → `category: 'viewpoint'`
- "基金" → `category: 'fund'`
- "债券" → `category: 'bond'`
- "票据" → `category: 'bill'`
- "股票" → `category: 'stock'`

**数量解析规则：**
- "一条"、"1条" → `page_size: 1`
- "五条"、"5条" → `page_size: 5`
- "十条"、"10条" → `page_size: 10`
- "二十条"、"20条" → `page_size: 20`
- 以此类推

**重要提示：**
- ✅ 必须正确解析分类和数量参数
- ✅ 如果用户未指定分类，使用 `category: 'discover'`
- ✅ 如果用户未指定数量，使用 `page_size: 10`
- ✅ 必须使用资讯列表接口，参数名使用下划线 `page_size`

---

### 场景7：用户询问"搜索XXX的资讯"、"查找XXX相关资讯"

**触发条件：**
当用户询问以下任何问题时，必须调用资讯列表接口，并使用关键词搜索：
- "搜索XXX的资讯"
- "查找XXX相关资讯"
- "搜索XXX"
- "查找XXX"
- "XXX相关的资讯"
- "关于XXX的资讯"
- "XXX的新闻"
- 其他类似的搜索关键词相关询问

**执行流程：**

1. **提取搜索关键词**
   - 从用户询问中提取搜索关键词（如"股票"、"AI"、"市场"等）
   - 关键词作为 `keyword` 参数

2. **确定分类（可选）**
   - 如果用户同时指定了分类（如"搜索AI相关的股票资讯"），使用对应的 `category` 参数
   - 如果用户未指定分类，可以不传 `category` 参数，或使用 `category: 'discover'`

3. **调用资讯列表接口**
   - 调用 POST `/flp-news-api/v1/news-agent/informationList` 接口
   - 请求体参数：
     - `keyword`: 搜索关键词（必填）
     - `category`: 分类（可选，如果用户指定了分类）
     - `page_size`: 每页数量（可选，默认10）

**重要提示：**
- ✅ 必须提取用户询问中的关键词作为 `keyword` 参数
- ✅ 如果用户同时指定了分类，需要同时传入 `category` 和 `keyword` 参数
- ✅ 搜索功能支持跨分类搜索，如果不指定分类，会在所有分类中搜索
- ✅ 必须使用资讯列表接口，参数名使用下划线 `page_size`

---

### 场景8：用户询问"给我更多资讯"、"下一页资讯"

**触发条件：**
当用户询问以下任何问题时，必须调用资讯列表接口，并使用分页参数：
- "给我更多资讯"
- "下一页资讯"
- "加载更多"
- "继续加载"
- "更多XX资讯"（XX为分类）
- 其他类似的分页加载相关询问

**执行流程：**

1. **确定分页参数**
   - 需要获取上一次查询返回的最后一条资讯的ID作为 `news_id` 参数
   - 如果用户指定了分类，使用对应的 `category` 参数
   - 如果用户未指定分类，使用 `category: 'discover'`
   - `page_size` 参数保持与上一次查询一致，或使用默认值 10

2. **调用资讯列表接口**
   - 调用 POST `/flp-news-api/v1/news-agent/informationList` 接口
   - 请求体参数：
     - `category`: 分类（如果用户指定了分类）
     - `page_size`: 每页数量（与上一次查询保持一致）
     - `news_id`: 上一次查询返回的最后一条资讯的ID（用于分页）

**重要提示：**
- ✅ 分页查询必须使用 `news_id` 参数，传入上一次查询的最后一条资讯ID
- ✅ `page_size` 参数应该与上一次查询保持一致
- ✅ 如果用户指定了分类，需要同时传入 `category` 参数
- ✅ 必须使用资讯列表接口，参数名使用下划线 `page_size`
- ⚠️ 注意：需要保存上一次查询的结果，以便获取最后一条资讯的ID

---

## 通用注意事项

1. **必须直接使用 HTTP 请求**：
   - ✅ 直接使用 fetch、axios、curl 或其他 HTTP 客户端调用接口
   - ❌ **禁止创建任何封装函数或 JS/TS 文件**
   - ❌ **禁止创建 `api/news.ts`、`utils/api.js` 等封装文件**
   - ❌ **禁止使用 `import` 或 `require` 引入封装函数**
   - 所有接口调用必须在调用处直接使用 HTTP 请求

2. **参数命名规范**：注意接口参数命名可能使用驼峰命名（如 `pageSize`）或下划线命名（如 `page_size`），请根据实际接口文档确定。资讯列表接口使用下划线 `page_size`

3. **错误处理**：检查 HTTP 状态码和响应体中的错误信息，进行适当的错误处理

4. **认证信息**：部分接口（如Banner列表）可能需要 Cookie 认证，确保在请求时携带 `sl-session` Cookie

5. **接口路径**：使用完整的接口路径，包括基础域名和接口路径

6. **响应处理**：接口返回格式为 `{ code: 200, data: {...} }`，需要检查 `code` 字段判断请求是否成功，并从 `data` 字段获取实际数据

7. **Banner查询自动化**：查询Banner详情时必须使用自动化流程，先查列表再查详情

