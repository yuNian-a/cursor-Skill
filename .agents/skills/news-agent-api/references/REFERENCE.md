# 资讯Agent API 参考文档

## 概述

本文档提供资讯Agent API的详细使用说明，包括所有接口的参数、返回值和使用示例。

## 目录

- [资讯列表接口](#资讯列表接口)
- [Banner列表接口](#banner列表接口)
- [Banner详情接口](#banner详情接口)
- [完整使用流程](#完整使用流程)

---

## 资讯列表接口

### 接口信息

- **函数名**：`getInformationList`
- **文件位置**：`frontend/src/api/news.ts`
- **接口地址**：`/flp-news-api/v1/news-agent/informationList`
- **请求方法**：POST

### 参数说明

#### 必填参数

- **category** (string): 新闻分类
  - 可选值：`"discover"`, `"subscribe"`, `"ai"`, `"rwa"`, `"macro"`, `"industry"`, `"market"`, `"company"`, `"viewpoint"`, `"fund"`, `"bond"`, `"bill"`, `"stock"`
  - 说明：`"subscribe"` 分类需要提供 `user_id` 参数

- **page_size** (number): 每页加载条数
  - 注意：参数名使用下划线 `page_size`，不是驼峰 `pageSize`

#### 可选参数

- **keyword** (string): 关键词检索
- **news_id** (string): 分页游标，最后一条新闻的ID（用于分页加载）
- **user_id** (string): 用户ID（订阅分类时必填）

### 使用示例

#### 基础调用
```typescript
import { getInformationList } from '@/api/news';

const params = {
  category: 'discover',
  page_size: 10
};

const response = await getInformationList(params);
```

#### 带分页的调用
```typescript
const params = {
  category: 'discover',
  page_size: 20,
  news_id: 'last_news_id_here'
};

const response = await getInformationList(params);
```

#### 带搜索关键词的调用
```typescript
const params = {
  category: 'discover',
  page_size: 10,
  keyword: '股票'
};

const response = await getInformationList(params);
```

#### 订阅分类调用（需要用户ID）
```typescript
const params = {
  category: 'subscribe',
  page_size: 10,
  user_id: 'user_id_here'
};

const response = await getInformationList(params);
```

### 返回数据格式

接口返回 `NewsListResponse` 类型的数据，包含：
- `information_list`: 资讯列表数组
- 其他字段见 `NewsListResponse` 类型定义

---

## Banner列表接口

### 接口信息

- **函数名**：`getBannerListNew`（新接口）或 `getBannerList`（旧接口）
- **文件位置**：`frontend/src/api/news.ts`
- **接口地址**：`/flp-news-api/v1/news-agent/banner/list`
- **请求方法**：GET
- **认证**：可能需要 Cookie 认证（`sl-session`）

### 参数说明

此接口为 GET 请求，无需请求体参数。

### 使用示例

#### 基础调用
```typescript
import { getBannerListNew } from '@/api/news';

const response = await getBannerListNew();
```

#### 在组件中使用
```typescript
import { ref, onMounted } from 'vue';
import { getBannerListNew } from '@/api/news';
import type { BannerListResponse } from '@/types/news';

const bannerList = ref<BannerListResponse | null>(null);

onMounted(async () => {
  try {
    const response = await getBannerListNew();
    bannerList.value = response;
  } catch (error) {
    console.error('获取Banner列表失败:', error);
  }
});
```

### 返回数据格式

接口返回 `BannerListResponse` 类型的数据，包含：
- `banner_list`: Banner列表数组，每个Banner包含：
  - `news_id`: 新闻ID
  - `xcf_id`: XCF资讯ID
  - `tag`: 标签数组
  - `title`: 标题
  - `summary`: 摘要
  - `img_url`: 图片URL（可能为null）

### 返回数据示例

```json
{
  "banner_list": [
    {
      "news_id": "17131313",
      "xcf_id": 27814,
      "tag": ["AI热闻"],
      "title": "诺亚控股39万美元回购17万股,传递信心",
      "summary": "诺亚控股(06686)披露，3月9日在公开市场回购17.065万股...",
      "img_url": null
    }
  ]
}
```

---

## Banner详情接口

### 接口信息

- **函数名**：`getXcfDetail`
- **文件位置**：`frontend/src/api/news.ts`
- **接口地址**：`/flp-news-api/v1/news-agent/bannerDetail`
- **请求方法**：POST

### 参数说明

#### 必填参数

- **id** (string): XCF资讯ID（来自banner的 `xcf_id` 字段）

### 使用示例

#### 基础调用
```typescript
import { getXcfDetail } from '@/api/news';

const xcfId = '21640';
const response = await getXcfDetail(xcfId);
```

#### 在组件中使用
```typescript
import { ref } from 'vue';
import { getXcfDetail } from '@/api/news';
import type { XcfDetail } from '@/types/news';

const bannerDetail = ref<XcfDetail | null>(null);

const loadBannerDetail = async (xcfId: string) => {
  try {
    const response = await getXcfDetail(xcfId);
    bannerDetail.value = response;
  } catch (error) {
    console.error('获取Banner详情失败:', error);
  }
};

// 使用示例：从banner列表点击后获取详情
const handleBannerClick = (banner: BannerItem) => {
  if (banner.xcf_id) {
    loadBannerDetail(banner.xcf_id.toString());
  }
};
```

#### 从Banner列表获取详情
```typescript
import { getBannerListNew, getXcfDetail } from '@/api/news';

// 先获取Banner列表
const banners = await getBannerListNew();

// 获取第一个Banner的详情
if (banners.banner_list && banners.banner_list.length > 0) {
  const firstBanner = banners.banner_list[0];
  if (firstBanner.xcf_id) {
    const detail = await getXcfDetail(firstBanner.xcf_id.toString());
    console.log('Banner详情:', detail);
  }
}
```

### 返回数据格式

接口返回 `XcfDetail` 类型的数据，包含Banner的详细信息。

### 请求示例

```json
{
  "id": "21640"
}
```

---

## Banner查询自动化流程

### 概述

当需要查询Banner详情时，必须使用自动化流程：
1. 先查询Banner列表
2. 提取所有xcf_id
3. 分别查询每个Banner的详情

### 自动化流程实现

#### TypeScript实现

```typescript
import { getBannerListNew, getXcfDetail } from '@/api/news';

async function getAllBannerDetails() {
  try {
    // 步骤1: 获取Banner列表
    const bannerListResponse = await getBannerListNew();
    
    if (!bannerListResponse.banner_list || bannerListResponse.banner_list.length === 0) {
      return [];
    }
    
    // 步骤2: 提取所有xcf_id
    const xcfIds = bannerListResponse.banner_list
      .map(banner => banner.xcf_id)
      .filter(id => id != null);
    
    // 步骤3: 批量查询详情（并行）
    const detailPromises = xcfIds.map(xcfId => 
      getXcfDetail(xcfId.toString())
        .then(detail => ({ xcfId, detail, success: true }))
        .catch(error => ({ xcfId, detail: null, error, success: false }))
    );
    
    const results = await Promise.all(detailPromises);
    return results;
  } catch (error) {
    console.error('获取Banner详情失败:', error);
    throw error;
  }
}
```

#### Python实现

使用提供的自动化脚本：

```bash
python scripts/get-all-banner-details.py
```

脚本会自动执行：
1. 查询Banner列表
2. 提取所有xcf_id
3. 批量查询详情
4. 输出结果摘要并保存到JSON文件

### 执行规则

**必须遵循：**
- ✅ 先查询列表，再查询详情
- ✅ 提取所有xcf_id，不能遗漏
- ✅ 使用所有xcf_id分别查询详情
- ✅ 处理查询失败的情况，继续处理其他Banner
- ✅ 使用并行查询提高效率

**禁止：**
- ❌ 直接查询详情而不先查列表
- ❌ 只查询部分Banner的详情
- ❌ 忽略查询失败的情况

---

## 完整使用流程

### 场景预设：用户询问"今日的AI热闻"

**触发条件：**
当用户询问"今日的AI热闻"或类似问题时（如"今天的AI热点"、"AI热门新闻"等），必须执行以下流程。

**执行流程：**

1. **查询Banner列表**
   - 调用 `getBannerListNew()` 获取所有Banner
   - Banner列表通常包含今日最热门的AI相关资讯

2. **查询Banner详情**
   - 从Banner列表中提取所有 `xcf_id`
   - 使用所有 `xcf_id` 分别调用 `getXcfDetail()` 获取每个Banner的完整详情
   - 必须查询所有Banner的详情，不能只查询部分

**实现示例：**

```typescript
import { getBannerListNew, getXcfDetail } from '@/api/news';

async function getTodayAIHotNews() {
  try {
    // 步骤1: 获取Banner列表（今日AI热闻）
    const bannerListResponse = await getBannerListNew();
    
    if (!bannerListResponse.banner_list || bannerListResponse.banner_list.length === 0) {
      return {
        message: '暂无今日AI热闻',
        banners: []
      };
    }
    
    // 步骤2: 提取所有xcf_id
    const xcfIds = bannerListResponse.banner_list
      .map(banner => banner.xcf_id)
      .filter(id => id != null);
    
    // 步骤3: 批量查询所有Banner详情
    const detailPromises = xcfIds.map(xcfId => 
      getXcfDetail(xcfId.toString())
        .then(detail => ({ xcfId, detail, success: true }))
        .catch(error => ({ xcfId, detail: null, error, success: false }))
    );
    
    const details = await Promise.all(detailPromises);
    
    return {
      message: `找到 ${details.length} 条今日AI热闻`,
      banners: bannerListResponse.banner_list,
      details: details
    };
  } catch (error) {
    console.error('获取今日AI热闻失败:', error);
    throw error;
  }
}
```

**重要提示：**
- ✅ 当用户询问"今日的AI热闻"时，必须执行完整的Banner查询流程
- ✅ 必须先查询Banner列表，再查询详情
- ✅ 必须查询所有Banner的详情，不能遗漏
- ❌ 不能直接查询资讯列表接口，必须使用Banner相关接口

---

### 场景：加载新闻页面

```typescript
import { ref, onMounted } from 'vue';
import { 
  getBannerListNew, 
  getInformationList, 
  getXcfDetail 
} from '@/api/news';
import type { 
  BannerListResponse, 
  NewsListResponse, 
  XcfDetail 
} from '@/types/news';

const bannerList = ref<BannerListResponse | null>(null);
const newsList = ref<NewsListResponse | null>(null);
const bannerDetail = ref<XcfDetail | null>(null);

onMounted(async () => {
  try {
    // 1. 加载Banner列表
    const banners = await getBannerListNew();
    bannerList.value = banners;

    // 2. 加载资讯列表
    const news = await getInformationList({
      category: 'discover',
      page_size: 20
    });
    newsList.value = news;

    // 3. 如果用户点击Banner，加载详情
    // handleBannerClick 函数中调用
  } catch (error) {
    console.error('加载数据失败:', error);
  }
});

const handleBannerClick = async (banner: BannerItem) => {
  if (banner.xcf_id) {
    try {
      const detail = await getXcfDetail(banner.xcf_id.toString());
      bannerDetail.value = detail;
    } catch (error) {
      console.error('获取Banner详情失败:', error);
    }
  }
};
```

---

## 注意事项

1. **不要直接使用 fetch 调用接口**，必须使用封装好的函数
2. **参数命名规范**：使用下划线命名（如 `page_size`），不是驼峰命名（如 `pageSize`）
3. **错误处理**：所有函数会抛出错误，需要在外层使用 try-catch 处理
4. **Cookie 认证**：Banner列表接口可能需要 Cookie 认证，确保在请求时携带 `sl-session` Cookie
5. **类型安全**：使用 TypeScript 类型定义，确保类型安全
6. **接口返回格式**：所有接口返回的数据结构为 `{ code: 200, data: {...} }`，函数会自动提取 `data` 字段
7. **xcf_id 转换**：从Banner列表获取详情时，需要将 `xcf_id` 转换为字符串

