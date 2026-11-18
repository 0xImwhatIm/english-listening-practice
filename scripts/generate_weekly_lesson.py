import os
import json
import datetime
import urllib.request
import urllib.error

API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
if not API_KEY:
    raise RuntimeError("❌ 找不到 GEMINI_API_KEY！請確認 GitHub Secrets 設定。")

LESSONS_FILE = "lessons.json"

if os.path.exists(LESSONS_FILE):
    with open(LESSONS_FILE, "r", encoding="utf-8") as f:
        lessons = json.load(f)
else:
    lessons = []

existing_titles = [l.get("title", "") for l in lessons[:15]]
week_num = len(lessons) + 1
today_str = datetime.date.today().isoformat()

prompt = f"""你是一位台灣國中英語科專業教材編寫老師。請幫「國中七年級（國一）」學生設計一週的全新英聽與閱讀練習教材。
請避開以下已出過的標題：{', '.join(existing_titles)}
請從台灣國中生熟悉的生活情境（如：校園運動會、社團活動、夜市美食、搭捷運與公車、超商購物、週末河濱騎單車、段考準備、家庭旅遊、寵物與動物收容所等）挑選一個新鮮有趣的故事主題，並搭配一個國一核心文法（如：現在進行式、過去簡單式、頻率副詞、可數與不可數名詞、助動詞 can/may、未來式、祈使句等）。
程度規範：使用台灣教育部國中小基礎 1200 單字，英文短文約 85~115 字（約 5~7 句），具故事性與少年感。

請嚴格只輸出一段合法的 JSON 物件，格式如下：
{{
  "id": "week-{week_num}-{today_str}",
  "weekLabel": "Week {week_num} • [填入核心文法與主題簡稱]",
  "date": "{today_str}",
  "title": "[英文標題]",
  "articleZh": "[符合台灣國中生語感的繁體中文全文翻譯]",
  "grammarFocus": "[核心文法說明]",
  "article": "[85~115字的英文短文]",
  "vocabulary": [
    {{"word": "單字1", "kk": "[KK音標]", "pos": "詞性", "zh": "繁體中文解釋", "sentence": "包含該單字的簡單例句"}}
  ],
  "exercises": [
    {{"id": "w{week_num}-d1", "day": 1, "type": "Day 1｜聽力與大意理解", "isListening": true, "audioPrompt": "從文章擷取的關鍵句供朗讀", "q": "英文問題?", "options": ["選項A", "選項B", "選項C"], "answer": 0, "explanation": "繁體中文詳解"}},
    {{"id": "w{week_num}-d2", "day": 2, "type": "Day 2｜單字聽辨與填空", "isListening": true, "audioPrompt": "完整句子音檔", "q": "挖空句子 ______", "options": ["單字A", "單字B", "單字C"], "answer": 1, "explanation": "繁體中文詳解"}},
    {{"id": "w{week_num}-d3", "day": 3, "type": "Day 3｜核心文法檢測", "isListening": false, "audioPrompt": "", "q": "文法題目", "options": ["選項A", "選項B", "選項C"], "answer": 2, "explanation": "繁體中文詳解"}},
    {{"id": "w{week_num}-d4", "day": 4, "type": "Day 4｜細節聽力問答", "isListening": true, "audioPrompt": "文章細節句子", "q": "細節問題?", "options": ["選項A", "選項B", "選項C"], "answer": 0, "explanation": "繁體中文詳解"}},
    {{"id": "w{week_num}-d5", "day": 5, "type": "Day 5｜全週綜合挑戰", "isListening": false, "audioPrompt": "", "q": "綜合理解問題?", "options": ["選項A", "選項B", "選項C"], "answer": 1, "explanation": "繁體中文詳解"}}
  ]
}}
（注意：vocabulary 請提供 6 個核心單字）"""

# 優先使用錯誤訊息指定的 gemini-3.8-flash，並自動動態查詢帳號可用 Flash 模型作為保底
candidate_models = ["gemini-3.8-flash", "gemini-3.0-flash", "gemini-2.5-flash"]
try:
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
    with urllib.request.urlopen(list_url, timeout=20) as resp:
        m_data = json.loads(resp.read().decode("utf-8"))
        for m in m_data.get("models", []):
            name = m.get("name", "").replace("models/", "")
            methods = m.get("supportedGenerationMethods", [])
            if "flash" in name and "generateContent" in methods and name not in candidate_models:
                candidate_models.append(name)
except Exception as e:
    print(f"⚠️ 查詢可用模型清單略過: {e}")

raw_text = None
last_err = None

for model_name in candidate_models:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json"}
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            res_data = json.loads(resp.read().decode("utf-8"))
            raw_text = res_data["candidates"][0]["content"]["parts"][0]["text"]
            print(f"✅ 使用模型 {model_name} 呼叫成功")
            break
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="ignore")
        print(f"⚠️ 模型 {model_name} 失敗 (HTTP {e.code}): {err_body}")
        last_err = e

if not raw_text:
    raise RuntimeError(f"所有 Gemini 模型皆呼叫失敗: {last_err}")

cleaned = raw_text.replace("```json", "").replace("```", "").strip()
new_lesson = json.loads(cleaned)
lessons.insert(0, new_lesson)

with open(LESSONS_FILE, "w", encoding="utf-8") as f:
    json.dump(lessons, f, ensure_ascii=False, indent=2)

print(f"🎉 成功生成最新教材：{new_lesson.get('weekLabel')} - {new_lesson.get('title')}")
