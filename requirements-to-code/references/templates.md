# 代码模板

本文档包含 requirements-to-code 工作流中使用的代码模板。SKILL.md 各阶段会引用此文件的具体模板。

---

## 目录

1. [HTML 原型模板](#html-原型模板)
2. [index.html 导航枢纽模板](#indexhtml-导航枢纽模板)
3. [数据获取 Hook 模板](#数据获取-hook-模板)
4. [组件单元测试模板](#组件单元测试模板)
5. [Hook 单元测试模板](#hook-单元测试模板)
6. [E2E 测试模板](#e2e-测试模板)

---

## HTML 原型模板

每个原型的骨架结构，包含内联 CSS/JS 和状态切换器：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[页面标题] — Prototype</title>
  <style>
    /* ===== Design Tokens ===== */
    /* ===== Base Styles ===== */
    /* ===== Component Styles ===== */
    /* ===== State Styles ===== */
    /* ===== Responsive ===== */
  </style>
</head>
<body>
  <div class="state-switcher" style="position:fixed;bottom:16px;right:16px;z-index:9999;
              background:rgba(0,0,0,0.8);color:#fff;padding:8px 12px;border-radius:8px;
              font-size:12px;display:flex;gap:6px;flex-wrap:wrap;">
    <button onclick="setState('loading')">加载中</button>
    <button onclick="setState('empty')">空数据</button>
    <button onclick="setState('error')">出错</button>
    <button onclick="setState('normal')">正常</button>
  </div>
  <div id="state-loading"><!-- 骨架屏 --></div>
  <div id="state-empty"><!-- 空状态 + CTA --></div>
  <div id="state-error"><!-- 错误 + 重试 --></div>
  <div id="state-normal"><!-- 正常页面 --></div>
  <script>
    function setState(s) {
      ['loading','empty','error','normal'].forEach(st =>
        document.getElementById('state-'+st).style.display = st===s ? '' : 'none'
      );
    }
    setState('normal');
  </script>
</body>
</html>
```

### 原型生成规则

1. **自包含** — CSS/JS 全内联，浏览器打开即运行
2. **状态全覆盖** — loading/empty/error/normal + 边界状态，通过浮动状态切换器切换
3. **真实感数据** — "Acme 集团"、"¥1,234.56"、"订单 #3847 — 已发货"
4. **交互可感知** — 按钮有反馈、表单有验证、弹窗可开关
5. **设计系统化** — 一致调色板、字体层级、间距尺度
6. **响应式** — 375px / 768px / 1280px+
7. **先结构后视觉** — 第一遍搭建布局骨架+覆盖状态+实现交互；第二遍叠加设计系统

---

## index.html 导航枢纽模板

原型不应是一堆孤立的 HTML 文件。生成一个 `specs/prototypes/index.html` 作为导航枢纽，用户打开它就能浏览整个系统：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>原型导航 — [项目名称]</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; display: flex; height: 100vh; }
    nav {
      width: 240px; background: #1e293b; color: #e2e8f0; padding: 20px 0;
      display: flex; flex-direction: column; overflow-y: auto;
    }
    nav h2 { padding: 0 20px 16px; font-size: 14px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; }
    nav a {
      display: block; padding: 10px 20px; color: #cbd5e1; text-decoration: none;
      font-size: 14px; border-left: 3px solid transparent; transition: all 0.15s;
    }
    nav a:hover { background: #334155; color: #fff; }
    nav a.active { background: #334155; color: #60a5fa; border-left-color: #60a5fa; font-weight: 600; }
    main { flex: 1; display: flex; flex-direction: column; }
    main iframe { flex: 1; border: none; width: 100%; }
    .page-count { padding: 8px 20px; font-size: 12px; color: #64748b; border-top: 1px solid #334155; margin-top: auto; }
  </style>
</head>
<body>
  <nav>
    <h2>页面列表</h2>
    <a href="orders.html" target="preview-frame" onclick="setActive(this)">/orders — 订单列表</a>
    <a href="orders-detail.html" target="preview-frame" onclick="setActive(this)">/orders/:id — 订单详情</a>
    <a href="users.html" target="preview-frame" onclick="setActive(this)">/users — 用户管理</a>
    <a href="dashboard.html" target="preview-frame" onclick="setActive(this)">/dashboard — 数据仪表盘</a>
    <div class="page-count">共 4 个页面</div>
  </nav>
  <main>
    <iframe name="preview-frame" src="orders.html" onload="syncActive(this.src)"></iframe>
  </main>
  <script>
    function setActive(el) {
      document.querySelectorAll('nav a').forEach(a => a.classList.remove('active'));
      el.classList.add('active');
    }
    function syncActive(src) {
      const filename = src.split('/').pop();
      document.querySelectorAll('nav a').forEach(a => {
        a.classList.toggle('active', a.getAttribute('href') === filename);
      });
    }
  </script>
</body>
</html>
```

### 导航枢纽规则

1. **左侧/顶部列出所有页面** — 名称和路由来自 `specs/routes.json`
2. **默认加载第一个页面** — iframe 预加载，用户无需点击
3. **点击导航切换页面** — 用 iframe 或直接跳转（iframe 便于在导航栏上下文中查看）
4. **高亮当前页** — active 状态在导航上可见
5. **显示页面总数** — 底部计数
6. **每个页面可独立打开** — iframe src 指向的文件本身就是自包含的
7. **导航标签使用人类可读名称** — 如"订单列表"而非"orders.html"

---

## 数据获取 Hook 模板

```typescript
function useData<T>(fetcher: () => Promise<T>) {
  const [state, setState] = useState<{
    data: T | null; loading: boolean; error: string | null;
  }>({ data: null, loading: true, error: null });

  const refetch = useCallback(async () => {
    setState(prev => ({ ...prev, loading: true, error: null }));
    try {
      const data = await fetcher();
      setState({ data, loading: false, error: null });
    } catch (e) {
      setState(prev => ({
        ...prev, loading: false,
        error: e instanceof Error ? e.message : '请求失败',
      }));
    }
  }, [fetcher]);

  useEffect(() => { refetch(); }, [refetch]);
  return { ...state, refetch };
}
```

### 使用规则

- 每个数据获取需求封装为一个独立 hook
- 必须覆盖 loading → data → error 三种路径
- 支持 `refetch` 用于重试和刷新

---

## 组件单元测试模板

```typescript
// src/__tests__/components/OrderTable.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { OrderTable } from '@/components/shared/OrderTable';
import { createOrderList } from '@/mocks/data';

describe('OrderTable', () => {
  const defaultProps = {
    orders: createOrderList(5),
    onRowClick: vi.fn(),
    onSort: vi.fn(),
    loading: false,
  };

  // === 正常 ===
  it('renders all orders when data is provided', () => {
    render(<OrderTable {...defaultProps} />);
    expect(screen.getAllByRole('row')).toHaveLength(6); // header + 5
  });

  it('calls onRowClick with order id when a row is clicked', () => {
    render(<OrderTable {...defaultProps} />);
    fireEvent.click(screen.getAllByRole('row')[1]);
    expect(defaultProps.onRowClick).toHaveBeenCalledWith('1');
  });

  // === Loading ===
  it('shows skeleton when loading', () => {
    render(<OrderTable {...defaultProps} loading={true} />);
    expect(screen.getByTestId('table-skeleton')).toBeInTheDocument();
  });

  // === Empty ===
  it('shows empty state with CTA when data is empty', () => {
    render(<OrderTable {...defaultProps} orders={[]} />);
    expect(screen.getByText(/还没有订单/)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /创建/ })).toBeInTheDocument();
  });

  // === 交互 ===
  it('calls onSort when column header is clicked', () => {
    render(<OrderTable {...defaultProps} />);
    fireEvent.click(screen.getByText('金额'));
    expect(defaultProps.onSort).toHaveBeenCalledWith('total', 'asc');
  });

  // === 无障碍 ===
  it('has accessible row click targets', () => {
    render(<OrderTable {...defaultProps} />);
    screen.getAllByRole('row').forEach(row => {
      expect(row).toHaveAttribute('tabindex', '0');
    });
  });
});
```

### 组件测试规则

- 每个组件覆盖四种状态（loading/empty/error/normal）至少各 1 个测试
- 每个用户交互（点击、输入、提交）至少 1 个测试
- 共享组件必须有完整单测
- 测试数据使用阶段 5 的 Mock 工厂函数

---

## Hook 单元测试模板

```typescript
// src/__tests__/hooks/useOrders.test.ts
import { renderHook, waitFor } from '@testing-library/react';
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';
import { useOrders } from '@/hooks/useOrders';
import { createOrderList } from '@/mocks/data';

const server = setupServer();
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('useOrders', () => {
  it('returns data on successful fetch', async () => {
    const mockData = createOrderList(5);
    server.use(http.get('/api/orders', () =>
      HttpResponse.json({ data: mockData, total: 5, page: 1 })
    ));
    const { result } = renderHook(() => useOrders({ page: 1 }));
    expect(result.current.loading).toBe(true);
    await waitFor(() => {
      expect(result.current.loading).toBe(false);
      expect(result.current.data).toEqual(mockData);
    });
  });

  it('returns error on failed fetch', async () => {
    server.use(http.get('/api/orders', () =>
      HttpResponse.json({ error: 'Server Error' }, { status: 500 })
    ));
    const { result } = renderHook(() => useOrders({ page: 1 }));
    await waitFor(() => {
      expect(result.current.loading).toBe(false);
      expect(result.current.error).not.toBeNull();
    });
  });

  it('returns empty array when no data', async () => {
    server.use(http.get('/api/orders', () =>
      HttpResponse.json({ data: [], total: 0, page: 1 })
    ));
    const { result } = renderHook(() => useOrders({ page: 1 }));
    await waitFor(() => {
      expect(result.current.data).toEqual([]);
    });
  });

  it('refetches when params change', async () => {
    const { result, rerender } = renderHook(
      ({ page }) => useOrders({ page }),
      { initialProps: { page: 1 } }
    );
    await waitFor(() => expect(result.current.loading).toBe(false));
    rerender({ page: 2 });
    expect(result.current.loading).toBe(true);
  });
});
```

### Hook 测试规则

- 每个数据 hook 必须有 loading → data → error 三态测试
- 使用 MSW 拦截网络请求，不走真实网络
- 测试参数变化时的重取行为

---

## E2E 测试模板

```typescript
// e2e/orders-flow.spec.ts
import { test, expect } from '@playwright/test';

test.describe('订单管理流程', () => {
  test('完整流程：列表 → 筛选 → 详情 → 返回', async ({ page }) => {
    await page.goto('/orders');
    await expect(page.getByTestId('table-skeleton')).not.toBeVisible();
    await expect(page.getByRole('row')).toHaveCount(11);

    await page.getByLabel('状态').selectOption('shipped');
    await page.getByRole('button', { name: '筛选' }).click();
    await expect(page.getByRole('row')).toHaveCount(6);

    await page.getByRole('row').nth(1).click();
    await expect(page).toHaveURL(/\/orders\/\d+/);

    await page.getByRole('link', { name: '订单管理' }).click();
    await expect(page).toHaveURL('/orders');
  });

  test('空数据流程', async ({ page }) => {
    await page.goto('/orders?mock=empty');
    await expect(page.getByText(/还没有订单/)).toBeVisible();
  });

  test('错误恢复流程', async ({ page }) => {
    await page.goto('/orders?mock=error');
    await expect(page.getByText(/加载失败/)).toBeVisible();
    await page.getByRole('button', { name: '重试' }).click();
    await expect(page.getByText(/加载失败/)).not.toBeVisible();
  });
});
```

### E2E 测试规则

- 只覆盖 P0 关键用户流程，不做全量回归
- 每个流程至少覆盖 2 个页面间的跳转
- 使用 `testid` 定位元素
- URL 参数切换 mock 场景（`?mock=empty`、`?mock=error`）
