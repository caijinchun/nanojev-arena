# NanoJev Arena · 贪吃蛇大乱斗 + 百人求生

**和 AI 打一架:你用方向键操纵金色蛇,四条 NanoJev AI 蛇同场抢食。**

这是 [NanoJev](https://github.com/TianyuCodings/NanoJev)([Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev) 的开源迷你复刻,0.6B 参数)的本地游戏演示。模型不生成任何文字——一次前向直接输出所有候选动作的完整概率分布,蛇头上悬浮的概率条就是它"此刻的想法"。

![arena](assets/arena.png)

## 两个玩法

| 页面 | 玩法 |
|---|---|
| `snake.html` | **贪吃蛇大乱斗**:1v4 人机对战。代码规划器排除必死方向并筛出候选,NanoJev 在候选间按分布选择;撞墙撞身即死,尸体化作食物。`↑↓←→`/`WASD` 移动,`P` 暂停,`R` 重开 |
| `swarm.html` | **百人求生**:最多 100 个 agent 各自只有 5×5 局部视野,每拍一次批量前向指挥全场;红绿热力图实时可视化模型对每个格子的"恐惧"。鼠标可现场画墙,看概率场重排 |
| `intro.html` | 视频用竖屏动画卡片(1080×1920,URL 参数 `scene`/`dur` 控制场景与时长) |

## 快速开始(Windows)

需要:NVIDIA 显卡(显存 ≥6GB)+ Python 3.10+ + Git。

```powershell
git clone https://github.com/<YOU>/nanojev-arena.git
cd nanojev-arena
python install.py
```

`install.py` 会自动:克隆上游 NanoJev 仓库 → 建虚拟环境装依赖(torch CUDA 版需代理或镜像,见脚本内说明)→ 从 HuggingFace 下载两个已训练 checkpoint(默认走 hf-mirror 镜像,国内可用)→ 把本仓库的游戏页面拷入上游 `web/` 目录。

装完启动:

```powershell
cd NanoJev
.venv\Scripts\activate
python scripts/serve_decisions.py --checkpoint-dir checkpoints/games_gold/variants/games_gold_seed17 --web-root web --port 8766 --precision fp32
```

打开 **http://127.0.0.1:8766/snake.html** 开打。百人求生换用 `local_atomic` checkpoint 与 8765 端口,命令同上。

> 无 NVIDIA 显卡?上游仓库的纯浏览器回放(`side-by-side.html` 等)不需要模型,任何机器都能看。

## 它是怎么工作的

混合决策,**代码与模型各司其职**:

1. **代码规划器**(每帧,0ms):排除反向/撞墙/撞身方向 → BFS 找到食物的静态最短路 → 筛出 2–4 个候选动作;
2. **NanoJev**(批量,~0.2s/4 蛇):收到一个 choice 问题,一次前向输出候选的完整概率分布,取 argmax;模型响应到达前由规划器代管,所以 AI 永远不会因为"没想好"而撞墙;
3. 提问格式与上游训练数据严格一致(`evaluate_composed_snake.py` 的 composed 协议),模型判别力实测:目标方向 97.5% 压倒性概率。

## 致谢与协议

- 游戏页面、安装脚本:本仓库,MIT License
- 模型与训练管线:[TianyuCodings/NanoJev](https://github.com/TianyuCodings/NanoJev)(MIT)· 概念源自 [Jev / Typesafe](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
- checkpoint 权重:[C-Tianyu/NanoJev @ HuggingFace](https://huggingface.co/C-Tianyu/NanoJev)(`games_gold_seed17`、`local_atomic_seed17`)
