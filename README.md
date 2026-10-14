# 🎧 English Listening Practice (國一每日英聽與閱讀練習站)

專為**台灣國中七年級（國一）**學生設計的零摩擦力每日英語聽讀、1200 單字字卡與 5 日拆解測驗網站，並內建**備課老師 AI 出題中心**與 **GitHub Actions 自動教材生成**。

## ✨ 核心特色

### 1. 學生端：極低摩擦力學習體驗
- **免註冊、打開即用**：使用瀏覽器 `localStorage` 自動紀錄學習進度、收藏單字與錯題本。
- **點句即讀 + 盲聽訓練**：除了整篇朗讀與三段語速（`0.75x` / `0.88x` / `1.0x`），**點擊文章中任何一句話即可單句重複發音**；還可一鍵切換「🙈 盲聽模式」先練耳力再看文字。
- **自動對應星期幾（Day 1 ~ Day 5）**：週一打開自動顯示 Day 1（聽力大意）、週二 Day 2（聽音辨字）、週三 Day 3（核心文法）、週四 Day 4（細節英聽）、週五 Day 5（綜合挑戰）。
- **智慧錯題重測系統（答對 2 次才畢業）**：答錯題目自動進入錯題本，學生可在錯題本內**直接重新作答**，連續答對 2 次（⭐⭐）才會從錯題本消除。

### 2. 備課者端：零摩擦力教材準備與自動推薦
- **內建「🧑‍🏫 備課中心」**：內建國一上下學期推薦主題與核心文法池，支援填入 Gemini API Key 瀏覽器一鍵出題，或複製結構化 Prompt。
- **免後端「專屬分享連結」**：老師生成新教材後，點擊「🔗 產生學生分享連結」，即可透過 URL Hash 將整週教材直接傳給學生（Line 群組 / Google Classroom）。
- **GitHub Actions 每週自動生成教材**：只要在 GitHub Repo 的 `Settings -> Secrets and variables -> Actions` 新增 `GEMINI_API_KEY`，系統每週日晚上會自動生成下一週的國一教材並更新 GitHub Pages！

## 🚀 部署至 GitHub Pages (`0xImwhatIm/english-listening-practice`)

1. 解壓縮本專案並開啟終端機：
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```
2. 前往 `https://github.com/0xImwhatIm/english-listening-practice/settings/pages`，在 **Build and deployment** 選擇 **GitHub Actions**（或 `Deploy from a branch` -> `main` / `/ (root)`）。
3. 網站將發布於：`https://0ximwhatim.github.io/english-listening-practice/`
