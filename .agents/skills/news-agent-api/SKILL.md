---
name: 资讯Agent API调用技能
description: 当需要调用资讯Agent相关接口时，请参考此规范。包括资讯列表、Banner列表、Banner详情等接口。
---

## 指令
1. 所有接口调用必须使用项目中的封装函数（位于 `frontend/src/api/news.ts`）。
2. 接口域名：开发环境使用代理，生产环境使用 `VITE_FLPAI_API_KEY` 环境变量
3. 请求头：`Content-Type: application/json`
4. 接口返回的数据结构为 `{ code: 200, data: {...} }`，函数会自动提取 `data` 字段
5. 错误处理：函数会抛出错误，需要在外层使用 try-catch 处理

## 接口列表

### 1. 资讯列表接口

**接口信息：**
- 函数：`getInformationList`
- 接口地址：`/flp-news-api/v1/news-agent/informationList`
- 请求方法：POST

**参数：**
- 必填参数：
  - `category`: 新闻分类，类型为 `NewsCategory`，可选值：`"discover"`, `"subscribe"`, `"ai"`, `"rwa"`, `"macro"`, `"industry"`, `"market"`, `"company"`, `"viewpoint"`, `"fund"`, `"bond"`, `"bill"`, `"stock"`
  - `page_size`: 每页加载条数（注意：参数名使用下划线 `page_size`，不是驼峰 `pageSize`）
- 可选参数：
  - `keyword`: 关键词检索
  - `news_id`: 分页游标，最后一条新闻的ID（用于分页加载）
  - `user_id`: 用户ID（订阅分类时必填）

**使用示例：**
```typescript
import { getInformationList } from '@/api/news';

// 基础调用
const params = {
  category: 'discover',
  page_size: 10
};
const response = await getInformationList(params);

// 带分页
const params = {
  category: 'discover',
  page_size: 20,
  news_id: 'last_news_id_here'
};
const response = await getInformationList(params);

// 带搜索关键词
const params = {
  category: 'discover',
  page_size: 10,
  keyword: '股票'
};
const response = await getInformationList(params);
```

**返回数据：**
- `information_list`: 资讯列表数组
- 其他字段见 `NewsListResponse` 类型定义

---

### 2. Banner列表接口

**接口信息：**
- 函数：`getBannerListNew`（新接口）或 `getBannerList`（旧接口）
- 接口地址：`/flp-news-api/v1/news-agent/banner/list`
- 请求方法：GET
- 注意：此接口可能需要 Cookie 认证（`sl-session`）

**参数：**
- 此接口为 GET 请求，无需请求体参数

**使用示例：**
```typescript
import { getBannerListNew } from '@/api/news';

// 获取Banner列表
const response = await getBannerListNew();

// 在组件中使用
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

**返回数据：**
- `banner_list`: Banner列表数组，每个Banner包含：
  - `news_id`: 新闻ID
  - `xcf_id`: XCF资讯ID
  - `tag`: 标签数组
  - `title`: 标题
  - `summary`: 摘要
  - `img_url`: 图片URL（可能为null）

---

### 3. Banner详情接口

**接口信息：**
- 函数：`getXcfDetail`
- 接口地址：`/flp-news-api/v1/news-agent/bannerDetail`
- 请求方法：POST

**参数：**
- 必填参数：
  - `id`: XCF资讯ID（来自banner的 `xcf_id` 字段），类型为字符串

**使用示例：**
```typescript
import { getXcfDetail } from '@/api/news';

// 基础调用
const xcfId = '21640';
const response = await getXcfDetail(xcfId);

// 从Banner列表获取详情
import { getBannerListNew, getXcfDetail } from '@/api/news';

const banners = await getBannerListNew();
if (banners.banner_list && banners.banner_list.length > 0) {
  const firstBanner = banners.banner_list[0];
  if (firstBanner.xcf_id) {
    const detail = await getXcfDetail(firstBanner.xcf_id.toString());
    console.log('Banner详情:', detail);
  }
}
```

**返回数据：**
- 返回 `XcfDetail` 类型的数据，包含Banner的详细信息

---

---

## 4. Banner查询自动化流程（内置操作）

**重要：当需要查询Banner详情时，必须使用此自动化流程。**

### 自动化流程说明

当调用Banner查询时，系统会自动执行以下步骤：

1. **自动查询Banner列表**
   - 调用 `getBannerListNew()` 获取所有Banner
   
2. **自动提取所有xcf_id**
   - 从返回的 `banner_list` 中提取所有的 `xcf_id`
   - 通常返回3个Banner，每个Banner都有一个 `xcf_id`
   
3. **自动批量查询详情**
   - 使用提取的所有 `xcf_id`，分别调用 `getXcfDetail()` 接口
   - 获取每个Banner的完整详情信息

### 使用示例

```typescript
import { getBannerListNew, getXcfDetail } from '@/api/news';

// 自动化流程：查询所有Banner及其详情
async function getAllBannerDetails() {
  try {
    // 步骤1: 获取Banner列表
    const bannerListResponse = await getBannerListNew();
    
    if (!bannerListResponse.banner_list || bannerListResponse.banner_list.length === 0) {
      console.log('没有可用的Banner');
      return [];
    }
    
    // 步骤2: 提取所有xcf_id
    const xcfIds = bannerListResponse.banner_list
      .map(banner => banner.xcf_id)
      .filter(id => id != null);
    
    console.log(`找到 ${xcfIds.length} 个Banner，xcf_id:`, xcfIds);
    
    // 步骤3: 批量查询详情
    const detailPromises = xcfIds.map(xcfId => 
      getXcfDetail(xcfId.toString())
        .then(detail => ({ xcfId, detail }))
        .catch(error => {
          console.error(`获取Banner ${xcfId} 详情失败:`, error);
          return { xcfId, detail: null, error };
        })
    );
    
    const details = await Promise.all(detailPromises);
    
    return details;
  } catch (error) {
    console.error('获取Banner列表失败:', error);
    throw error;
  }
}

// 使用
const allDetails = await getAllBannerDetails();
allDetails.forEach(({ xcfId, detail }) => {
  if (detail) {
    console.log(`Banner ${xcfId} 详情:`, detail.title);
  }
});
```

### 在组件中使用

```typescript
import { ref, onMounted } from 'vue';
import { getBannerListNew, getXcfDetail } from '@/api/news';

const bannerDetails = ref([]);

onMounted(async () => {
  try {
    // 1. 获取Banner列表
    const banners = await getBannerListNew();
    
    if (banners.banner_list && banners.banner_list.length > 0) {
      // 2. 提取所有xcf_id并查询详情
      const details = await Promise.all(
        banners.banner_list.map(async (banner) => {
          if (banner.xcf_id) {
            try {
              const detail = await getXcfDetail(banner.xcf_id.toString());
              return {
                ...banner,
                detail
              };
            } catch (error) {
              console.error(`获取Banner ${banner.xcf_id} 详情失败:`, error);
              return { ...banner, detail: null };
            }
          }
          return { ...banner, detail: null };
        })
      );
      
      bannerDetails.value = details;
    }
  } catch (error) {
    console.error('获取Banner详情失败:', error);
  }
});
```

### 执行规则

**必须遵循以下规则：**
1. 查询Banner详情时，必须先查询Banner列表
2. 必须提取列表中的所有 `xcf_id`（不能只查询部分）
3. 必须使用所有提取的 `xcf_id` 分别调用详情接口
4. 如果某个详情查询失败，应该记录错误但继续处理其他Banner
5. 建议使用 `Promise.all()` 并行查询以提高效率

---

## 5. 场景预设

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
   - 调用 `getInformationList()` 接口
   - 参数设置：`category` 为确定的分类，`page_size: 10`
   - 返回10条对应分类的资讯

**实现示例：**

```typescript
import { getInformationList } from '@/api/news';

async function getNewsList(category: string = 'discover', pageSize: number = 10) {
  try {
    const response = await getInformationList({
      category: category,
      page_size: pageSize
    });
    
    if (!response.information_list || response.information_list.length === 0) {
      return {
        message: `暂无${category}分类的资讯`,
        newsList: []
      };
    }
    
    return {
      message: `找到 ${response.information_list.length} 条${category}分类的资讯`,
      newsList: response.information_list
    };
  } catch (error) {
    console.error('获取资讯列表失败:', error);
    throw error;
  }
}

// 使用示例
// 用户问"给我十条资讯" -> getNewsList('discover', 10)
// 用户问"给我十条AI方面的资讯" -> getNewsList('ai', 10)
```

**重要提示：**
- ✅ 当用户询问"给我十条资讯"时，默认查询 `discover` 分类
- ✅ 当用户询问"给我十条XX方面的资讯"时，根据XX映射到对应的分类
- ✅ 必须使用 `getInformationList()` 接口，不是Banner接口
- ✅ `page_size` 参数名使用下划线，不是驼峰命名
- ❌ 不要使用Banner相关接口，这是资讯列表查询场景

---

### 场景2：用户询问"今日的AI热闻"

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

## 通用注意事项

1. **不要直接使用 fetch 调用接口**，必须使用封装好的函数
2. **参数命名规范**：使用下划线命名（如 `page_size`），不是驼峰命名（如 `pageSize`）
3. **错误处理**：所有函数会抛出错误，需要在外层使用 try-catch 处理
4. **Cookie 认证**：部分接口（如Banner列表）可能需要 Cookie 认证，确保在请求时携带 `sl-session` Cookie
5. **类型安全**：使用 TypeScript 类型定义，确保类型安全
6. **Banner查询自动化**：查询Banner详情时必须使用自动化流程，先查列表再查详情

## 相关参考文档

详细的使用说明和示例请参考 `references/` 目录下的文档。
自动化脚本请参考 `scripts/` 目录下的 `get-all-banner-details.py`。

