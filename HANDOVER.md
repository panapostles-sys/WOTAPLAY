# WOTAPLAYER — 项目交接文档

## 项目信息
- **版本**: 1.3.0 (versionCode 16)
- **构建 APK**: `WOTAPLAYER-v1.3.0.apk`
- **项目路径**: `D:\ai_tools\WORKPLACE1\WOTAPLAYER`

## 构建方式
```bash
cd /d/ai_tools/WORKPLACE1/WOTAPLAYER
export ANDROID_HOME=/d/android-sdk
./gradlew assembleDebug
# APK 输出: app/build/outputs/apk/debug/app-debug.apk
# 复制到桌面: cp app/build/outputs/apk/debug/app-debug.apk /c/Users/ASUS/Desktop/WOTAPLAYER-v1.3.0.apk
```

## 依赖版本 (2026-07 更新)
| 组件 | 版本 | 说明 |
|------|------|------|
| compileSdk / targetSdk | 36 | Android 14+ |
| minSdk | 26 | Android 8.0 |
| Kotlin | 1.9.24 | |
| Compose BOM | 2025.02.00 | |
| Compose Compiler | 1.5.14 | 配套 Kotlin 1.9.24 |
| Media3 (ExoPlayer) | 1.2.0 | 双播放器 |
| Media3 Session | 1.2.0 | 听视频后台播放 |
| AGP | 8.2.0 | |

## 项目结构

```
app/
├── build.gradle.kts                          # compileSdk 34, minSdk 26, Media3 1.2.0, Media3 Session, Compose BOM 2024.06.00
└── src/main/
    ├── AndroidManifest.xml                    # 权限: READ/WRITE_EXTERNAL_STORAGE, READ_MEDIA_VIDEO, FOREGROUND_SERVICE, POST_NOTIFICATIONS, RECORD_AUDIO
    ├── res/
    │   ├── values/{strings,themes,colors}.xml
    │   ├── drawable/ic_launcher_foreground.xml
    │   └── mipmap-anydpi-v26/{ic_launcher,ic_launcher_round}.xml
    └── java/com/wotaplayer/
        ├── AudioKeepAliveService.kt           # 前台 Service，听视频后台播放通知
        ├── MainActivity.kt                    # 主入口, 权限申请, 页面导航 (list/player/split_player)
        ├── model/VideoFile.kt                 # 数据类: id, uri, name, duration, size, dateAdded, folder, isStarred
        ├── viewmodel/PlayerViewModel.kt       # 核心逻辑: 双播放器, 视频列表, A-B Loop, 分屏, 检索, 文件夹, 听视频
        └── ui/
            ├── theme/Theme.kt                 # 深/浅色双主题，DARK/LIGHT/SYSTEM 模式，iOS 色板 (#0A84FF primary, #000000/#F2F2F7 背景)
            └── screens/
                ├── VideoListScreen.kt         # 视频列表: 2列网格, 缩略图, 星标, ModalBottomSheet, 搜索, 文件夹, 自定义拖动滑条(像素级连续thumb), 液态玻璃设置菜单(点击图标切换)
                └── PlayerScreen.kt            # 播放器: 横屏/竖屏, 分屏双TextureView, 双播放器控制, 半透控制栏, ColorMatrix色彩校正, 三模式播放循环, 听视频频谱+波形可视化, 滚动播放列表(适配浅色模式), 倍速栏底部弹出动画
```

## 已实现功能

| 功能 | 文件 | 说明 |
|------|------|------|
| 读取本地视频 (MediaStore) | PlayerViewModel.kt | 查询 MediaStore.Video.Media，按 DATE_ADDED DESC 排序 |
| 视频列表 (2列 LazyVerticalGrid) | VideoListScreen.kt | 使用 key = uri，支持搜索+文件夹过滤 |
| 封面缩略图 (MediaMetadataRetriever) | VideoListScreen.kt | 取视频 20% 位置帧代替第一帧，避免黑屏；20% 处寻帧比 loadThumbnail 更清晰 |
| 刷新按钮 | VideoListScreen.kt | 重新查询 MediaStore |
| 星标收藏 (SharedPreferences 持久化) | PlayerViewModel.kt | 存为 Set\<String\> key "starred_ids" |
| 重命名 | PlayerViewModel.kt / VideoListScreen.kt | API 30+ 用 MediaStore.createWriteRequest 弹窗授权 |
| 删除确认 | PlayerViewModel.kt / VideoListScreen.kt | API 30+ 用 MediaStore.createDeleteRequest 弹窗授权 |
| 横屏全屏播放 | PlayerScreen.kt | ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE，可在设置中切换为竖屏 |
| TextureView 视频渲染 | PlayerScreen.kt | 自定义 VideoTextureView，自适应比例 fit center，一次性绑定防跳帧 |
| 镜像翻转 (scaleX = -1) | PlayerScreen.kt | View 级 scaleX，每个 slot 独立 |
| 上一帧/下一帧 (33ms) | PlayerViewModel.kt | seekTo ±33ms |
| 0.25/0.5/0.75/1.0 倍速 | PlayerViewModel.kt | ExoPlayer.setPlaybackSpeed，每个 slot 独立 |
| 沉浸模式 (隐藏导航栏) | PlayerScreen.kt | SYSTEM_UI_FLAG + IMMERSIVE_STICKY |
| 控制栏自动隐藏 (4s) | PlayerScreen.kt | LaunchedEffect + delay(4000) |
| 回到顶部 | VideoListScreen.kt | 滚动后顶栏显示 ⬆ 按钮，点击平滑回到列表顶部 |
| "create by 汐槿 v1.2.8" | VideoListScreen.kt | TopAppBar 标题区 subtitle，含版本号 |
| **听视频（音频后台播放）** | PlayerViewModel.kt / PlayerScreen.kt / AudioKeepAliveService.kt | 播放时切换到音频模式，视频隐藏只保留频谱+波形可视化；通知栏媒体控制+后台播放；返回列表不停止（退出听模式才停止）；音频焦点处理
| **A-B 段落循环** | PlayerViewModel.kt / PlayerScreen.kt | 播放中标记 A/B 点，开启循环后播放到 B 点自动跳回 A，每个 slot 独立 |
| **视频检索** | VideoListScreen.kt | 顶部搜索栏，按文件名实时过滤（contains 忽略大小写） |
| **文件夹分类** | PlayerViewModel.kt / VideoListScreen.kt | 查询 RELATIVE_PATH/\_DATA 提取文件夹，FilterChip 切换筛选 |
| **分屏双视频播放** | PlayerViewModel.kt / PlayerScreen.kt / VideoListScreen.kt / MainActivity.kt | 两个 ExoPlayer 实例 + 两个 TextureView 左右分屏，独立控制 |
| **返回键与系统返回键绑定** | PlayerScreen.kt | BackHandler 拦截系统返回键，分屏模式先退出分屏再返回列表 |
| **播放时屏幕常亮** | PlayerScreen.kt | FLAG_KEEP_SCREEN_ON 进入播放器时开启，退出时清除 |
| **双指缩放+拖动** | PlayerViewModel.kt / PlayerScreen.kt | pinch-to-zoom (0.5x-5x)，放大/缩小后可单指拖动画面 |
| **时间轴标记标签** | PlayerViewModel.kt / PlayerScreen.kt | 可自定义标签名的打点标记，按时间排序，点击跳转，选中后删除；标记持久化到 SharedPreferences |
| **自定义收藏夹** | PlayerViewModel.kt / VideoListScreen.kt | 可新建/删除收藏夹，视频菜单添加/移除到收藏夹，FilterChip 切换筛选；JSON 持久化到 SharedPreferences |
| **iOS 风格 UI + 双主题** | Theme.kt / VideoListScreen.kt / PlayerScreen.kt | 深色/浅色双背景可切换（DARK/LIGHT/SYSTEM），iOS 蓝 #0A84FF，扁平卡片，ModalBottomSheet 菜单。浅色模式顶部栏+播放列表加黑色细边框 |
| **视频分享** | VideoListScreen.kt | 三点菜单 → Share → Intent.ACTION_SEND 分享视频 URI |
| **右侧拖动滑条** | VideoListScreen.kt | 20dp 触摸区，11dp 视觉轨道，自定义 detectDragGestures + dispatchRawDelta 像素级丝滑滚动；拖拽时 thumb 独立计算 1:1 跟手，非拖拽时 firstVisibleItemScrollOffset 行级插值连续更新 |

## 架构要点

### 导航架构
- **页面切换**: `MainActivity` 中 `screen` 状态为 `"list"` / `"player"` / `"split_player"`，用 `Box` + `if` 条件控制页面显示
- **滚动位置保持**: `VideoListScreen` **始终在组合树中不销毁**（播放器页面覆盖在上面而非替换），返回列表时 `LazyGridState` 保持原样，滚动位置不变
- **列表 → 播放**: 点击视频 → `screen = "player"` → PlayerScreen 覆盖在列表上方，返回时 `screen = "list"` → PlayerScreen 移出组合树 → `DisposableEffect` 触发 `releasePlayer`
- **列表 → 分屏**: Split 选两个视频 → `screen = "split_player"` → 同上

### 分屏双视频播放
- **SlotState 数据类**: 将单份播放状态抽象为 `SlotState(uri, isPlaying, currentPosition, duration, playbackSpeed, isMirrored, loopPointA/B, loopEnabled, zoomLevel, offsetX/Y, markers)`，每个 slot 持有自己的一份
- **双播放器**: `playerA` / `playerB` 两个独立的 ExoPlayer 实例，各带独立的 Player.Listener
- **activeSide**: `SplitSide.A` / `SplitSide.B` 枚举表示当前控制目标，通过顶部 Side A/B 芯片切换；控制栏所有操作（进度、倍速、镜像、A-B Loop）均作用于 active 侧
- **音频**: 分屏模式下一时间只能一个视频出声，通过 `activeSide` 确定；底部有 Play/Pause All 按钮一键同步两侧
- **surface 一次性绑定**: `VideoTextureView.surfaceBound` 标志位 + `update` 块判断，确保只绑一次，`showControls` 切换等重组不再触发 `setVideoSurface()`，避免跳帧
- **进度追踪**: `LaunchedEffect(Unit)` 持续运行，不以 isPlaying 为 key，避免播放/暂停重启协程导致状态混淆
- **进入分屏**: 列表 → 视频 `⋮` → Split → 蓝色横幅提示选择第二个视频 → 点击第二个视频 → `split_player` 页面
- **退出分屏**: 返回键 → `exitSplitMode()` → 释放 playerB + 重置 slotB 状态

### 播放器
- 使用裸 **TextureView** + ExoPlayer.setVideoSurface(Surface)，而非 PlayerView
- 自定义 `VideoTextureView` 在 `onMeasure` 中做视频比例适配（fit center），`onMeasure` 末尾调用 `applyScale()` 确保旋转暂停时不拉伸
- 镜像通过 View 级 `scaleX = -1f` 实现（TextureView 直接变换，不走 Compose graphicsLayer 离屏缓冲区，避免色彩降级）
- 进入播放器强制横屏（可在设置中切换竖屏），退出恢复 `UNSPECIFIED`
- 控制栏背景: 液态玻璃效果 `drawBackdrop + blur(4f.dp.toPx()) + lens(16f.dp.toPx(), 32f.dp.toPx())`，底色 `surfaceBg.copy(alpha=0.5f)`
- 倍速选择栏: 液态玻璃面板，底部弹出动画（`slideInVertically/slideOutVertically` + `Alignment.BottomCenter`），`padding(bottom=64.dp)` 固定底部定位
- 返回按钮: `CircleShape` 圆形背景

### 视频列表
- 排序: **isStarred DESC → dateAdded DESC**
- 布局: **2列 LazyVerticalGrid** (GridCells.Fixed(2))，间距 10dp
- 卡片: 扁平设计，无阴影(elevation=0dp)，`#1C1C1E` 背景
- 封面: 120dp 高，优先使用 `MediaStore.Video.Thumbnails.getThumbnail(MINI_KIND)`（系统缓存，极快），失败时回退 `MediaMetadataRetriever` 取 20% 时间点帧并 1/4 降采样
- 星标: 右上角（`Alignment.TopEnd`），24dp
- info 区: Column 布局，文件名在上，时长在下（Apple Photos 风格）
- 缩略图在 `LaunchedEffect(video.id)` 中异步加载
- **搜索过滤**: `videoList.filter { name.contains(searchQuery, ignoreCase = true) }`，实时响应
- **文件夹过滤**: 查询 `MediaStore.Video.Media.RELATIVE_PATH` (API 30+) 或 `_DATA` 退栈提取路径，FilterChip 单选切换。文件夹列表从加载结果中 `distinct().sorted()` 生成
- **滚动位置保持**: MainActivity 用 `Box` 让 VideoListScreen 始终保持在组合树中，播放器覆盖在上面，返回列表时 LazyGridState 不丢失，滚动位置不变
- **回到顶部**: 监听 `LazyGridState.firstVisibleItemIndex > 0` 时顶栏显示 `KeyboardDoubleArrowUp` 图标按钮，点击 `animateScrollToItem(0)` 平滑滚动回顶部
- **右侧滚动条**: 自定义 `detectDragGestures`，20dp 宽触摸区，11dp 宽浅色轨道条 + 比例滑块（11dp 宽，0.6 alpha）
  - **拇指位置**: 拖动时由 `dragFraction` 独立驱动（手指 1:1 跟手），非拖动时用 `firstVisibleItemIndex + firstVisibleItemScrollOffset` + 行级处理（Grid 2列）实现像素级连续位置计算，不跳格
  - **拖动滚动**: `dispatchRawDelta(dragAmount * scale)` 跳过协程直接在帧管线中写入偏移量，拖拽开始时固定比例因子
  - **顶部 padding**: `chipsHeightDp + 10.dp` 顶部削减不紧贴 grid 层
- **三点菜单**: **ModalBottomSheet** (iOS 动作表单) + Android 12+ `RenderEffect` 高斯模糊。包含: Star/Unstar, Rename, Split, Share, Create Playlist, Add to playlist(折叠≤2→Show all), Delete。播放列表超过 2 个时折叠，点击 "Show All" 展开

### 作用域存储 (Scoped Storage)
- **Android 11+ (API 30+)**: 删除/重命名必须先调用 `MediaStore.createDeleteRequest` / `MediaStore.createWriteRequest` 获取 `PendingIntent`，通过 `ActivityResultContracts.StartIntentSenderForResult` 发起系统弹窗，用户允许后才执行实际 `ContentResolver.delete/update`
- **Android 10 及以下**: 直接执行 `ContentResolver.delete/update`
- 流程: UI 调 `requestRename/requestDelete` → ViewModel 判断 API 版本 → 需要授权则设 `pendingStorageAction` → VideoListScreen 观察到后启动 `IntentSender` → 回调 `onStorageActionResult(success)` → 成功则执行实际操作

### A-B 段落循环
- 状态: `loopPointA` / `loopPointB` / `loopEnabled` — 每个 SlotState 中各自维护
- 操作: 播放中按 "A" 标记起点、"B" 标记终点（B 必须在 A 之后）、"Loop" 开关循环
- 实现: 在 `onProgressUpdate()` 中检测 `当前 >= loopPointB && loopEnabled` 时 `player.seekTo(loopPointA)`
- 控件位于播放器控制栏第二行，循环启用时顶部会显示绿色 "A-B" 指示器（#34C759 iOS 绿）
- 调用 `initPlayer()` 时自动清空 A/B 点和循环状态

## UI 主题 (Apple iOS 风格) — 双主题

| 角色 | 深色模式 | 浅色模式 | 说明 |
|------|----------|----------|------|
| 背景 background | `#000000` | `#F2F2F7` | 真黑 / 浅灰 |
| 表面 surface | `#1C1C1E` | `#FFFFFF` | 卡片/弹窗背景 |
| 表面变体 surfaceVariant | `#2C2C2E` | `#E5E5EA` | 未选中控件底色 |
| 强调色 primary | `#0A84FF` | `#0A84FF` | iOS 蓝 |
| 成功色 tertiary | `#34C759` | `#34C759` | iOS 绿，A-B Loop |
| 主文字 onSurface | `#F2F2F7` | `#1C1C1E` | 主文字色 |
| 辅助文字 onSurfaceVariant | `#8E8E93` | `#8E8E93` | iOS 二级文本 |
| 分隔线 outline | `#38383A` | `#C6C6C8` | 分割线 |
| 红色 destructive | `#FF453A` | `#FF453A` | iOS 红，删除操作 |

### 图标风格
- 优先使用 `Icons.Outlined.*` 系列（更纤细的线条风格）
- 保持 Filled 的仅有: Star（显眼标识）、Pause/PlayArrow（核心控制）

## 已知待优化

### 1. 缩略图加载
- **文件**: `VideoListScreen.kt` (LaunchedEffect 内 MediaMetadataRetriever)
- **建议**: 使用 Coil 库加载缩略图，自带内存/磁盘缓存和异步加载
- **接入**: 添加 `implementation("io.coil-kt:coil-compose:2.6.0")` 依赖，替换 LaunchedEffect 为 `AsyncImage`

### 2. 分屏模式下音频
- 目前通过 `activeSide` 纯 UI 指示哪边走音频，exoplayer 实际所有实例都会输出
- **建议**: 通过 `ExoPlayer.setVolume()` 将非 active 侧的音量置 0

## 已修复问题 (2026-06-23)

### 1. 侧边滚动条
- **问题**: 滚动条占用视频区域、未实现滑块指示、拖动不跟手
- **修复**: 
  - `LazyVerticalGrid` `contentPadding(end = 28.dp)` 预留空间，不再遮挡视频卡片
  - 新增比例滑块：高度按 `visibleItems / totalItems` 计算，位置按 `firstVisibleItemIndex / (totalItems - visibleItems)` 计算，8dp 宽
  - 使用 `detectDragGestures` + `change.consume()` 确保手势正确消费
  - 轨道由 3dp → 8dp 加宽，触摸区初始 28dp→40dp→20dp（最终调整为 20dp 触摸区 + 网格 end=20dp 不重叠）

### 2. 底部三点菜单磨砂玻璃效果
- **问题**: 需要高斯模糊而非单纯半透，且不覆盖全屏
- **修复**: 
  - 使用 Android 12+ `RenderEffect.createBlurEffect(25f)` 全屏模糊 + `scrimColor(alpha=0.55f)` 深色遮罩，非菜单区域模糊不可见
  - `containerColor(alpha=0.68f)` 菜单区域透出模糊内容，真正玻璃质感
  - `DisposableEffect` + `onDispose` 确保退出清除模糊效果
  - 添加 `DisposableEffect` 处理异常防止崩溃

### 3. 播放触屏反馈
- **问题**: 触碰视频画面有 Material ripple 颗粒反馈
- **修复**: `clickable(onClick)` → `pointerInput + detectTapGestures`，消除 ripple

### 4. 播放器布局
- **问题**: 进度条遮挡标签、控制栏区域过大
- **修复**: 
  - 标签（markers）移至进度条上方，`Spacer(4.dp)` 隔开
  - 进度条 `padding(top=4.dp)` 下移
  - Column 内边距 `vertical = 2.dp`，控制栏间距 1dp，整体紧凑

### 5. 封面缩略图加速
- **问题**: `MediaMetadataRetriever` 加载过慢
- **修复**: 优先使用 `MediaStore.Video.Thumbnails.getThumbnail(MINI_KIND)`（系统缓存，毫秒级），失败时回退 `MediaMetadataRetriever` 20% 帧 + 1/4 降采样

### 6. 底部菜单折叠
- **问题**: 播放列表过多时占满屏幕
- **修复**: 默认只显示前 2 个播放列表，超过时显示 "Show All (n)" 蓝色按钮点击展开/收起

## 已修复问题 (2026-06-23 v2)

### 1. 封面缩略图加速（v2）
- **问题**: 来回滚动时缩略图重复加载，列表卡顿
- **修复**: 在 `VideoListScreen.kt` 添加**会话级 LRU 内存缓存**（`LinkedHashMap`，上限 64 张），`LaunchedEffect` 先查缓存命中直接返回，避免重复查询 MediaStore / MediaMetadataRetriever

### 2. 右侧滚动条跟手性
- **问题**: 拖动不跟手
- **修复**: 触摸区 **28dp → 40dp**；拖动逻辑改为**增量模式**（`lastDragY` 追踪，~8px/item 灵敏度），替代原始的位置比例跳转；轨道/滑块保持原始 8dp 视觉样式

### 3. 磨砂玻璃过渡卡顿
- **问题**: 关闭 ModalBottomSheet 时背景从模糊→清晰的 `setRenderEffect(null)` 触发过快，导致突变卡顿
- **修复**: `DisposableEffect` → 两个 `LaunchedEffect`：打开即时模糊，关闭**延迟 300ms** 再清除模糊，等菜单收起动画完成后再恢复清晰

### 4. 标签图例置于最顶层
- **问题**: tag（Time markers）被底部控制栏遮挡
- **修复**: 将 markers 渲染放到 Box 子级**最后位置**（controls 之后），由 Compose Z-order（后绘制在上）确保始终最上层不被遮挡

### 5. 白色发光进度条
- **问题**: Material Slider 高度大、颜色不匹配播放器风格
- **修复**: 用自定义 `GlowProgressBar`（`Canvas` 绘制）替代：
  - 轨道降至 2dp 高，纯白色活跃轨道
  - 多层递减 alpha（0.18→0.12→0.06）模拟发光效果
  - 滑块改为**水平胶囊形圆角矩形**（12dp × 6dp）代替圆形
  - 支持 `detectDragGestures` 拖动 + `detectTapGestures` 点击

### 6. 标签随控制栏联动动画
- **问题**: 标签与底部控制栏分离，隐藏控制栏时标签残留
- **修复**: 将 Time markers 嵌入 `AnimatedVisibility` 控制的 Column 内部，与进度条/控制按钮同一容器，随 `slideInVertically/slideOutVertically` 一起从下至上浮现、从上至下退出

### 7. 缩略图加载提速
- **问题**: `createScaledBitmap` 使用 bilinear filter 增加耗时
- **修复**: `filter=false` 跳过双线性插值；`OPTION_CLOSEST` 代替 `OPTION_CLOSEST_SYNC` 减少关键帧查找；会话级 LRU 缓存避免重复解码

### 8. 滚动条位置比例跟随 + 靠右对齐
- **问题**: 增量模式滚动速度不跟随手速；列表未铺满屏幕
- **修复**: 
  - 滚动条改回**位置比例模式**，手指位置直接映射列表位置
  - 触摸区 40dp，`padding(end=0.dp)` 紧贴右边缘
  - 网格 `contentPadding(end = 28.dp)` → `0.dp`，视频列表横向铺满屏幕

### 9. 磨砂玻璃平滑动画
- **问题**: 关闭底部菜单时模糊→清晰突变
- **修复**: 用 `animateFloatAsState`（tween 200ms）驱动模糊半径 25f↔0f 渐变，`LaunchedEffect` 实时更新 `decorView.setRenderEffect`，实现实时模糊过渡；`LaunchedEffect` 移至 `if (showBottomSheet)` 外确保卸载时仍能清除模糊

### 10. 标签样式紧凑化
- **问题**: 标签背景过高，与进度条间距过大
- **修复**: 圆角缩至 4dp/1dp，`heightIn(max=14.dp)` 限制行高，lineHeight 9sp；标签订位 Row `vertical=1dp`，进度条 Column `vertical=1dp`，间隔缩至 2dp，整体控制栏布局更紧凑

## 已修复问题 (2026-06-23 v3 — v1.2.5)

### 1. 主界面全屏铺满
- **问题**: 视频列表左侧未铺满、右侧滚动条与视频重叠、文件夹/播放列表未铺满
- **修复**: `VideoListScreen.kt` 网格 `contentPadding(start = 12.dp → 0.dp)`；网格 `contentPadding(end = 40.dp → 20.dp)` 为滚动条预留空间；文件夹/播放列表 `LazyRow` 的 `padding(end = 0.dp)` 铺满右边缘

### 2. 播放界面标签太小/图标太小
- **问题**: 控制栏文字标签、图标过小难以辨认
- **修复**: time markers 字体 7sp→11sp；时间文字 11sp→14sp；倍速 10sp→12sp；A/B/L 按钮 10sp→13sp；清除/图钉/循环图标 14dp→18dp；镜像/帧按钮增大

### 3. 视频色彩发灰（TextureView gamma 校正）
- **问题**: TextureView 将视频帧作为 sRGB 纹理渲染，跳过系统色彩引擎，导致饱和度/对比度下降
- **修复**: `VideoTextureView` 添加 `isOpaque() = true` 避免预乘 alpha 降级；View 级 `scaleX/scaleY`（不走 Compose `graphicsLayer` 离屏缓冲区）；硬件层 `ColorMatrix` 轻度校正（contrast 1.08x + saturation 1.05x）

### 4. 进度条刚进入时无法拖动
- **问题**: `pointerInput(Unit)` 在首次 composition 时捕获了 `duration=0` 的闭包，之后不重启
- **修复**: 新增 `seekToRatio()` 方法实时从 `ExoPlayer` 获取 `duration`，解除闭包捕获依赖

### 5. A-B 循环指示器位置
- **问题**: 分屏模式下指示器在左上角与返回按钮重叠
- **修复**: 顶部控件 `Box` 添加 `fillMaxSize()`，A-B 标签通过 `TopEnd` 对齐到右上角

### 6. 镜像功能失效
- **问题**: SurfaceView 是独立硬件层，`scaleX = -1` 无效
- **修复**: 回退到 `TextureView`，View 级 `scaleX = -1`（不经 Compose graphicsLayer）

## 已修复问题 (2026-06-23 v4 — v1.2.6)

### 1. 播放模式切换按钮
- **功能**: 新增播放模式循环按钮（列表循环 / 单视频循环 / 随机播放），位于"下一帧"与"0.25x"之间
- **实现**: `PlayerViewModel.PlayMode` 枚举（PLAYLIST_LOOP / SINGLE_LOOP / SHUFFLE），`togglePlayMode()` 循环切换，分别显示 Repeat / RepeatOne / Shuffle 图标
- **图标颜色**: 非列表循环模式时高亮为 iOS 蓝

### 2. 播放完成后自动切换/循环/随机
- **问题**: 视频播放完就停止，未能按模式继续播放
- **修复**: `handlePlaybackEnded()` 在 Player.Listener 的 `STATE_ENDED` 中触发：
  - **列表循环**: 查找当前视频在 playlist 中的位置，播放下一个（末尾回到第一个）
  - **单视频循环**: `seekTo(0) + play()`
  - **随机播放**: 从 playlist 中随机选一个非当前视频播放
- `currentPlaylistVideos()` 复用现有过滤逻辑（搜索+文件夹+收藏夹）

### 3. 播放列表侧边栏
- **功能**: 播放模式按钮右侧新增列表按钮（PlaylistPlay 图标），单击后在播放画面右侧显示当前 playlist 的视频文件名列表
- **实现**: 200dp 宽半透明深色面板覆盖在视频右侧，使用 `LazyColumn` 滚动显示，当前播放的视频文件名高亮为 iOS 蓝
- 侧边栏通过 `viewModel.showPlaylistPanel` 控制显示/隐藏
- 5 秒无操作自动退出；点击空白画面也可退出
- 切换视频时自动滚动到该视频在列表中的位置

### 4. 返回列表自动滚动到上次播放位置
- **功能**: 从播放器返回列表时，自动滚动到上次播放的视频位置
- **实现**: `PlayerViewModel.lastPlayedUri` 在退出时保存最后播放的 URI，`VideoListScreen` 通过 `LaunchedEffect` 观察该值并 `animateScrollToItem`

### 5. 上/下一视频按钮
- **功能**: 播放控制栏新增 `SkipPrevious` / `SkipNext` 按钮，在帧切换按钮外侧（36dp 小按钮 vs 帧切换 48dp），通过图标+尺寸双重区分
- **行为**:
  - **无模式/列表循环**: 顺序上/下一视频（末尾回到开头/开头回到末尾）
  - **单循环**: 上下都是当前视频
  - **随机**: 从 playlist 中随机选一个（非当前）

## 已修复问题 (2026-06-23 v5 — v1.2.7)

### 1. 默认播放模式改为无循环
- **问题**: 视频播放完应停止而不是自动切下一首
- **修复**: `PlayMode` 新增 `NONE` 枚举值作为默认值；点击切换顺序改为 NONE → SINGLE_LOOP → PLAYLIST_LOOP → SHUFFLE → NONE

### 2. 设置菜单（自动续播 + 横竖屏切换）
- **功能**: 主界面顶栏新增设置齿轮图标，点击弹出 `DropdownMenu`，内含：
  - `Auto-resume` 开关：控制退出播放后是否保存位置，下次进入自动续播
  - `Landscape mode` 开关：控制播放界面为横屏（默认）或竖屏，设置后调用 `Activity.requestedOrientation(SENSOR_LANDSCAPE/PORTRAIT)`
- 两项设置均持久化到 SharedPreferences

### 3. 上/下一视频按钮
- **功能**: 播放控制栏新增 `SkipPrevious` / `SkipNext` 按钮（36dp），位于帧切换按钮（48dp）外侧
- **行为**（根据当前 `PlayMode`）：
  - **无模式 / 列表循环**: 顺序上/下一视频（末尾回开头）
  - **单循环**: 上下都是当前视频
  - **随机**: 从 playlist 中随机选一个非当前视频

## 已修复问题 (2026-06-23 v6 — v1.2.8)

### 1. 标记标签 × 按钮行为修复
- **问题**: 标签右侧 × 按钮在未选中时也出现，且点击一次性清除所有标记
- **修复**: × 按钮仅当选中标签（`selectedMarkerIndex != null`）时出现，点击后仅删除选中标签（`removeTimeMarker(index)`），删除后自动清除选中状态

### 2. 自定义标签名称
- **问题**: 无法手动输入标签名，添加标签直接使用自动生成名
- **修复**: 点击图钉按钮弹出 `AlertDialog` + `OutlinedTextField`，输入自定义名称点 Add 确认，留空使用默认名

### 3. 设置菜单磨砂玻璃
- **问题**: 设置 DropdownMenu 无半透明效果
- **修复**: 下拉菜单背景改为 `Color(0xFF1C1C1E).copy(alpha = 0.72f)` 半透明

### 4. 倍速选择器半透明 + 跟随控制栏动画
- **问题**: 倍速下拉无半透明效果，且未跟随下边栏一同退去
- **修复**: `DropdownMenu` 背景半透明；`showSpeedPicker` 状态提升到 PlayerScreen 顶层共享，控制栏隐藏时下拉自动收起

### 5. 三点菜单背景模糊退出卡顿修复
- **问题**: 关闭 ModalBottomSheet 退出时模糊→清晰有明显卡顿
- **修复**: 移除 `blurTarget < 0.5f` 阈值判断，改为 `blurTarget > 0f` 时始终应用模糊半径，模糊值通过 `animateFloatAsState` tween(200ms) 实时渐变到 0

### 6. 控制栏操作时自动隐藏优化
- **问题**: 操作控制栏时老是自己退出
- **修复**: 新增 `controlInteractionKey` 计数器，所有按钮点击/进度条拖动/画面点击显示控制栏时都会触发 `onControlInteraction()`，每次交互重置 4s 倒计时

### 7. 镜像功能修复
- **问题**: 镜像功能失灵（mirror toggle 无效果）
- **修复**: 移除 `AndroidView` 的 `graphicsLayer { scaleX = ... }`，只保留 `update` 块中 View 级 `tv.scaleX/tv.scaleY` 变换，避免 Compose graphicsLayer 离屏缓冲区与 View 级变换双重覆盖导致 scale 混乱

### 8. Marker 标签行水平滚动
- **问题**: Time marker 过多时直接溢出屏幕裁剪不可见
- **修复**: 标签行改为 `horizontalScroll(rememberScrollState())` 支持水平滚动；`LaunchedEffect` 监听滚动偏移自动触发 `onControlInteraction()` 重置 4s 自动隐藏倒计时

## 项目纪要
- Starred IDs 存储在 SharedPreferences key `"starred_ids"` (Set\<String\>)
- Android SDK 位置: `D:\android-sdk\` (commandline-tools 手动安装)
- 无 gradle wrapper jar，已有 gradlew 脚本
- 主题色: **#0A84FF** (iOS 蓝) — 从 #4FC3F7 迁移过来
- A-B Loop 状态不持久化，退出播放页时自动清除
- 分屏模式不持久化，返回列表自动退出
- 横竖屏设置持久化到 SharedPreferences（key `landscape_player`），进入播放界面时读取该设置决定横屏/竖屏
- 图标三点菜单已改为 ModalBottomSheet（替代 DropdownMenu）
- 播放模式状态（无/单循环/列表循环/随机）不持久化，进入播放页时重置为无循环
- 列表栏默认关闭，进入播放页时重置为关闭
- 视频播放位置持久化到 SharedPreferences（key `resume_pos_${uri}`），下次进入自动续播（>5s 时），可通过设置菜单关闭
- 返回列表时自动滚动到最后播放的视频位置
- 自动续播（Auto-resume）默认开启，可在主界面顶栏齿轮菜单中关闭，设置持久化到 SharedPreferences
- 横竖屏模式（Landscape mode）默认横屏，可在主界面顶栏齿轮菜单中切换，设置持久化到 SharedPreferences

## 已修复问题 (2026-06-24 — v1.2.8)

### 1. 听视频（音频后台播放）
- **功能**: 播放器中点击耳机图标切换到听视频模式
- **实现**:
  - `AudioKeepAliveService.kt`: 前台 Service，显示通知栏媒体控制（播放/暂停/上一首/下一首/关闭），支持后台播放
  - `PlayerViewModel.toggleListenMode()`: 切换听模式，请求音频焦点、创建 MediaSession、启动 ForegroundService
  - `PlayerViewModel.releasePlayer()`: 听模式下不释放 playerA，保持后台播放
  - `CombinedVisualizerEffect()`: 单个 Visualizer 同时获取 FFT 频谱 + 波形数据
- **频谱可视化**: 32 根白色方柱，dB 刻度（-40dB 映射），从底部向上生长，无声音时全黑
- **波形可视化**: 白色平滑曲线，中心线上下对称（仅保留下半部分），门限 0.5，振幅 1.2x
- **音频焦点**: 来电暂停/恢复，音频焦点丢失自动退出听模式
- **通知**: RECORD_AUDIO 权限（API 29+ 用于 Visualizer）
- **退出**: 返回列表时自动退出听模式并停止播放

### 2. 版本号 1.2.7 → 1.2.8

### 1. 竖屏分屏改为上下排列
- **问题**: 横屏和竖屏分屏都是左右排列（Row），竖屏画面过窄
- **修复**: `PlayerScreen.kt` 分屏 `Row` 外包 `if (landscape)` 条件，横屏保持 `Row`（左右），竖屏用 `Column`（上下），分隔线也相应改为水平

### 2. 主界面顶栏标题布局修正
- **问题**: "WOTAPLAYER" 和 "create by 汐槿" 上下重叠，且与图标未对齐
- **修复**: `VideoListScreen.kt` TopAppBar title 中的 `Column` 改用 `fillMaxSize()` + `Arrangement.SpaceBetween`，"WOTAPLAYER" 在 `Box` 中 `Alignment.Center` 居中，"create by 汐槿" 紧贴底部，不再重叠

### 3. 设置菜单半透明 + 布局优化
- **问题**: 设置 DropdownMenu 无半透明效果；开关与文字距离过近
- **修复**: 外层包裹 `MaterialTheme` + `colorScheme.copy(surface = ...alpha)` 实现真实半透明；文字与 Switch 间插入 `Spacer(12.dp)`

### 4. 倍速选择器半透明化
- **问题**: 倍速 `DropdownMenu` 未实现半透明效果
- **修复**: 同样包裹 `MaterialTheme` + `colorScheme.copy(surface = ...)` 实现半透明背景

### 5. 下边栏空白区域触摸重置自动隐藏计时
- **问题**: 点击下边栏空白区域（非按钮区域）不会重置 4s 自动隐藏倒计时
- **修复**: `PlayerScreen.kt` 底部 Column 添加 `pointerInput + detectTapGestures`，整个下边栏区域触摸都会重置计时

### 6. 横/竖屏开关逻辑调整
- **问题**: 横竖屏设置概念与用户预期相反
- **修复**: ViewModel 改为 `portraitMode`（默认 false=横屏），设置菜单标签改为"横/竖屏"，开关关闭=横屏，开启=竖屏；PlayerScreen 中 `requestedOrientation` 和分屏布局均按 `!portraitMode` 判断

### 7. 设置菜单和倍速选择器颜色统一
- **问题**: 设置菜单和倍速选择器因 MaterialTheme elevation 叠加 primary 色导致偏蓝，且半透明未生效
- **修复**: 统一使用 `MaterialTheme` 包裹 + `surface = Color(0xFF1C1C1E).copy(alpha = 0.88f)` + `surfaceTint = Color(0xFF1C1C1E).copy(alpha = 0f)` 禁用 elevation 染色，实现与右侧播放列表面板一致的颜色（#1C1C1E）和半透明

## 已修复问题 (v1.2.9 → v1.2.11)

### 1. 色彩校正参数调整
- **调整**: 对比度 1.0x、亮度偏移 -12、饱和度 1.1x

### 2. 触控手势合并
- **问题**: 双击区域和双指缩放互相抢占事件
- **修复**: 三个独立的 Box overlay 合并为单个 Box，用 `detectTapGestures`（双击/单击）+ `detectTransformGestures`（缩放/拖动）共存

### 3. 初始全屏拉伸 Bug
- **问题**: 刚进入播放器时画面经常从拉伸全屏再跳到正常比例
- **修复**: `VideoTextureView.onMeasure` 在 `videoWidth/videoHeight` 未知时默认 16:9 比例，等待视频尺寸加载后自动调整为正确比例

### 4. 浅色/深色双主题系统
- **新增**: `Theme.kt` 添加 `LightColorPalette`（iOS 浅色系），`ThemeMode` 枚举（DARK/LIGHT/SYSTEM）
- **实现**: `PlayerViewModel` 持久化主题模式到 SharedPreferences，`MainActivity` 读取并传参给 `WotaPlayerTheme`
- **VideoListScreen**: 所有硬编码 `#1C1C1E` / `#000000` / `#FFFFFF` / `#2C2C2E` / `#8E8E93` 等替换为 `MaterialTheme.colorScheme.*`
- **顶部栏分隔线**: 浅色模式显示黑色细线（`HorizontalDivider` 1dp, alpha 0.12），深色模式隐藏
- **播放列表面板**: 浅色模式添加 0.5dp 黑色细边框（`Modifier.border`）

### 5. 图标黑白配色
- **`ic_launcher_foreground.xml`**: 白色三角图标（#FFFFFF）
- **`colors.xml`**: `ic_launcher_background` = #000000（黑底）

### 6. 播放模式切换顺序
- **问题**: 播完停止（NONE）→ 单循环 → 列表循环 → 随机 → NONE
- **改为**: NONE → 列表循环 → 单循环 → 随机 → NONE

### 7. 缩放退出重置
- **修复**: `savePlaybackPosition()` 退出时重置两个 slot 的 `zoomLevel=1f`、`offsetX/Y=0f`

### 8. 顶部标题布局
- **调整**: 左侧图标 `top=27.dp`，"WOTAPLAYER" 前加 `Spacer(7.dp)` 一起下移 7dp，"create by" 位置不变
- **版本号**: UI 显示 v1.2.11（延续自 v1.2.10）

### 9. 右侧滚动条
- **宽度**: 由 12dp → 10dp

## 已修复/新增问题 (v1.2.12 特性)

### 1. 播放界面横竖屏切换按钮
- **功能**: 播放界面左上角返回键右侧新增横竖屏切换按钮（ScreenRotation 图标），点击切换横竖屏，效果与设置菜单同步
- **文件**: `PlayerScreen.kt` (顶部控制栏 Row 中第二个 IconButton)
- **实现**: 调用 `viewModel.togglePortraitMode()`，复用已有的 `portraitMode` SharedPreferences 持久化逻辑
- **布局**: 36dp 圆形半透黑背景，22dp 白色图标，与返回按钮保持 6dp 间距

### 2. 长按 3x 倍速播放
- **功能**: 触摸视频画面时长按触发 3x 倍速播放，松开恢复原速，屏幕顶部显示 "3x 倍速中" 文字指示器
- **文件**:
  - `PlayerViewModel.kt`: `startLongPress3x(side)` / `stopLongPress3x(side)` — 使用 `_savedSpeedBefore3x` Map 保存原速度，`_isLongPress3xSide` StateFlow 跟踪当前长按侧
  - `PlayerScreen.kt`: 通过 `detectTapGestures(onLongPress=...)` 触发启动，`awaitEachGesture + awaitFirstDown + waitForUpOrCancellation` 检测松手触发停止；Text composable 在 `isLongPress3xSide == side` 时显示指示器
- **分屏适配**: 使用 `SplitSide?` 类型追踪，每个 slot 独立显示，长按哪个哪个顶部显示

### 3. 分屏横竖屏切换黑屏 Bug 修复 (关键)
- **问题**: 分屏模式下多次切换横竖屏，有概率黑屏停止播放
- **根因**: 之前使用 `if (isLandscape) { Row(...) } else { Column(...) }` 双分支布局，每次切换整个 if/else 分支的 Composable 树销毁重建，两个 VideoSlot 的 TextureView 和 Surface 被销毁后重建，`onSurfaceTextureAvailable` / `update` / player 引用三者之间存在时序竞态，导致 Surface 无法正确绑定到 ExoPlayer
- **修复方案 (双重保障)**:
  - **布局改造**: 分屏模式下两个 VideoSlot 改为**根 Box 的直接子节点**（不再嵌套 Row/Column 条件分支），只有 Modifier 随横竖屏变化。TextureView 在整个分屏生命周期内始终存活，Surface 不会被 destroy/recreate，彻底消除表面生命周期竞态
  - **Surface 绑定优化**: 移除 `surfaceBound` 标志位守卫，改为无条件重绑策略：
    - `playerRef` 字段直接存储在 `VideoTextureView` 上，`update` 块中同步写入，`onSurfaceTextureAvailable` 中同步读取（消除闭包捕获延迟）
    - `update` 块中只要 `surfaceTexture != null` 就调用 `setVideoSurface()`
    - `onSurfaceTextureAvailable` 中总是通过 `tv.playerRef` 重绑
    - 移除 `onSurfaceTextureDestroyed` 中的解绑操作（避免旧 Surface 销毁晚于新 Surface 绑定的逆向竞态）
- **文件**: `PlayerScreen.kt` VideoSlot 布局及 `VideoTextureView` 类

### 4. 标题布局微调
- **主界面**: 左图标 `top=27dp`，"WOTAPLAYER" 与图标整体下移 7dp，"create by 汐槿" 保持原位置不变
- **文件**: `VideoListScreen.kt` TopAppBar title 部分

### 5. 长按 3x 倍速卡顿修复
- **问题**: 长按触发 3x 倍速时，视频卡顿一下才加速
- **根因**: 之前分屏黑屏修复中，`AndroidView.update` 块**无条件**调用 `p.setVideoSurface(Surface(surface))`，长按改变 playbackSpeed → slotState 变化 → 重组 → update 执行 → 重新绑定 Surface → 视频跳帧卡顿
- **修复**: `update` 块改为只在 **player 实例变更时**（`prev !== p`）才绑定 Surface，首次绑定或切换视频后绑定一次即可；`onSurfaceTextureAvailable` 始终无条件重绑兜底 Surface 重建场景
- **文件**: `PlayerScreen.kt` VideoSlot 的 `AndroidView.update` 块

### 6. 后台通知增加播放模式切换按钮
- **功能**: 听视频模式下，通知栏增加"播完即停/列表循环/单曲循环/随机播放"切换按钮，点击后循环切换模式，效果与播放界面同步
- **实现**:
  - `AudioKeepAliveService.kt`: 新增 `ACTION_TOGGLE_PLAY_MODE` action 和 `EXTRA_PLAY_MODE` extra，通知按钮从 4 个增加到 5 个：上一首 → 播放/暂停 → 下一首 → 模式切换 → 关闭
  - `PlayerViewModel.kt`: `notificationReceiver` 新增 `ACTION_TOGGLE_PLAY_MODE` 分支调用 `togglePlayMode()`，`togglePlayMode()` 结束后自动调用 `updateListenNotification()` 刷新通知
- **通知更新优化**: 首次调用 `startForeground()`，后续用 `notificationManager.notify()` 快速更新，避免重复 `startForeground` 开销
- **图标**: 所有通知按钮改用自定义矢量 drawable（`ic_notif_*.xml`），去除 `android:tint` 属性（Android 通知系统自动为 action 图标着色）
- **模式对应图标**:
  - 播完即停 → PlayCircle（带播放箭头的圆形）
  - 列表循环 → Repeat（循环箭头）
  - 单曲循环 → RepeatOne（循环箭头+小圆点）
  - 随机播放 → Shuffle（交叉箭头）
- **文件**: `AudioKeepAliveService.kt`、`PlayerViewModel.kt`、`build.gradle.kts`（新增 `androidx.media:media:1.6.0` 依赖）

## 已修复/新增问题 (v1.3.0)

### 1. 液态玻璃 (Liquid Glass) UI
- **功能**: 使用 `io.github.kyant0:backdrop:2.0.0` 库实现真正的磨砂玻璃效果
- **文件**: `MainActivity.kt`、`PlayerScreen.kt`、`VideoListScreen.kt`
- **实现**:
  - `MainActivity.kt`: 根 Box 创建 `rememberLayerBackdrop`，通过 `CompositionLocal`（`LocalBackdrop`）传递到子组件
  - 播放器底部控制栏: `drawBackdrop + blur(4f.dp.toPx()) + lens(16f.dp.toPx(), 32f.dp.toPx())` 替代原来的 `Color.Black.copy(alpha=0.4f)` 半透黑
  - 播放列表面板: 相同玻璃效果替代 `Color(0xFF1C1C1E).copy(alpha=0.95f)`
  - 倍速选择栏: 玻璃面板 + `onGloballyPositioned/positionInRoot()` 精确定位在倍速按钮上方
  - 主界面设置菜单: 玻璃面板 + `drawBackdrop`
  - 低 API 回退: API < 31 时自动使用半透明颜色方案
- **注意**: `vibrancy()` 会导致文字模糊已被移除

### 2. 设置菜单全屏模糊移除
- **问题**: 主界面开设置后整个屏幕多了一层模糊
- **修复**: `VideoListScreen.kt` 第 150 行 `anyOverlayOpen` 只追踪 `showBottomSheet`，不再触发全屏 `RenderEffect`

### 3. 倍速选择栏卡片样式
- **问题**: 倍速选择栏一直是大卡片
- **修复**: 改为 80dp 宽竖条小卡片（与设置菜单类似），文字居中、无标题/分隔线/勾选图标
- **定位**: 通过 `onGloballyPositioned + positionInRoot()` 追踪倍速按钮坐标，`Modifier.offset` 绝对定位在按钮正上方

### 4. PushPin 标记图标颜色
- **问题**: 📌 图标一直是蓝色
- **修复**: 默认白色 `Color.White`，仅当有选中标记时（`selectedMarkerIndex != null`）才显示蓝色 `Color(0xFF0A84FF)`

### 5. 视频旋转时画面拉伸
- **问题**: 暂停状态旋转屏幕，视频画面比例错误（拉伸）
- **根因**: `TextureView.onMeasure` 在旋转后触发，重新计算 `baseScaleX/Y`，但 Compose `update` 块只在新状态驱动时执行，暂停时无状态变化所以 `scaleX/Y` 仍用旧 `baseScale`
- **修复**: `VideoTextureView.onMeasure` 末尾调用 `applyScale()`，确保每次布局后重新应用 transform

### 6. 视频列表间距
- **调整**: `LazyVerticalGrid` `contentPadding` 改为 `start=3.dp, end=17.dp`，列表整体右移 3dp，滚动条位置不变

## 已修复/新增问题 (v1.3.0 — 2026-07-08 session)

### 1. 右侧滚动条彻底改造

**问题**: 滚动条 thumb 按 `firstVisibleItemIndex`（整型索引）间隔跳跃更新，拖动时 `scrollToItem` 协程调度导致"一卡一卡"，非拖动时 thumb 每跨项跳变

**修复**:
- **Thumb 位置**:
  - **拖动时**: 独立 `dragFraction` 状态直接跟踪手指位置，thumb 100% 1:1 跟手，不依赖 grid 布局更新
  - **静止时**: `firstVisibleItemIndex / spanCount + firstVisibleItemScrollOffset / rowHeight` 行级连续插值，每滚动 1px 更新一次
- **拖动滚动**: 拖拽开始固定比例因子，每帧用 `scrollBy(dragAmount * ratio)` 不带延迟
- **拇指高度**: `visibleItems / totalItems` 比例计算，最小 8%
- **轨道尺寸**: 触摸区 20dp，视觉 11dp 宽
- **顶部 offset**: `chipsHeightDp + 10.dp` 顶部削减，不紧贴 grid
- **文件**: `VideoListScreen.kt`

### 2. 浅色模式播放列表面板文字颜色
- **问题**: 右侧播放列表文件名/序号使用 `Color(0xFFF2F2F7)`（白色），浅色模式下白底白字不可见
- **修复**: 改为 `MaterialTheme.colorScheme.onSurface`，跟随主题自动深色/浅色切换
- **文件**: `PlayerScreen.kt:616`

### 3. 设置菜单卡片位置 + 切换
- **问题**: 设置卡片位置过低；点击齿轮图标只能打开不能关闭
- **修复**: `.align(Alignment.TopEnd).padding(top = (-2).dp, end = 8.dp)`（上移 4dp）；`onClick = { showSettings = !showSettings }` 切换开关
- **文件**: `VideoListScreen.kt`

### 4. 倍速选择栏动画
- **问题**: 倍速选择栏使用 `scaleIn/scaleOut` 缩放动画
- **修复**: 改为弹性放缩浮现（`scaleIn/scaleOut` 0.7f → 1.0f，`FastOutSlowInEasing`，`TransformOrigin(0.5f, 1f)` 从底部弹出）+ `fadeIn/fadeOut`，移除下滑动
- **文件**: `PlayerScreen.kt`

### 5. 设置菜单卡片动画
- **问题**: 设置菜单只有硬出现/消失
- **修复**: 添加弹性放缩浮现（`scaleIn/scaleOut` 0.7f → 1.0f，`FastOutSlowInEasing`，`TransformOrigin(1f, 0f)` 从右上角弹出）+ `fadeIn/fadeOut`
- **文件**: `VideoListScreen.kt`

### 6. 随机播放退出发光 Bug
- **问题**: 随机播放退出后 glow 不触发（因为 `playerA ?: return` 早返回跳过设置 `_lastPlayedUri`），且 grid 滚动异常
- **修复**: `savePlaybackPosition()` 移除 `playerA ?: return` 早返回，永远设置 `_lastPlayedUri`
- **文件**: `PlayerViewModel.kt:537-549`

### 7. ViewModel 编译修复
- **问题**: `deletePlaylist` 缺少闭合大括号 + 重复 `setSelectedPlaylist` 导致编译失败
- **修复**: 重构方法体，修复括号平衡
- **文件**: `PlayerViewModel.kt:989-999`

### 8. 设置菜单动画
- **调整**: 卡片位置上移 4dp（`offset(y = (-2).dp)`），点击齿轮图标可关闭；弹性放缩浮现/退出（`FastOutSlowInEasing`，`scaleIn/scaleOut` 0.7f，右上角原点）
- **倍速**: 弹性放缩浮现/退出（`FastOutSlowInEasing`，`scaleIn/scaleOut` 0.7f，底部中心原点）+ `fadeIn/fadeOut`，移除下滑动
- **文件**: `VideoListScreen.kt` / `PlayerScreen.kt`

## 项目结构快照 (项目文件)

| 文件 | 行数 | 作用 |
|------|------|------|
| `VideoListScreen.kt` | ~810 | 视频网格 + 滚动条 + 设置 + 底部弹窗 + 文件夹 |
| `PlayerScreen.kt` | ~1480 | 播放器 + 控制栏 + 分屏 + 倍速 + 频谱 |
| `PlayerViewModel.kt` | ~1000 | 双播放器 + 收藏 + 循环 + 设置持久化 |
| `Theme.kt` | ~100 | 深/浅色主题 |
| `MainActivity.kt` | ~90 | 导航 + 权限 |