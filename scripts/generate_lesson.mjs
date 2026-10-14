import fs from 'fs';

const apiKey = process.env.GEMINI_API_KEY;
if (!apiKey) {
  console.log('No GEMINI_API_KEY provided, exiting.');
  process.exit(0);
}

const lessons = JSON.parse(fs.readFileSync('./lessons.json', 'utf8'));
const existingTitles = lessons.map(l => l.title).join(', ');

const prompt = `你是一位台灣國中英語科專業教材編寫老師。請幫「國中七年級（國一）」學生設計最新一週的英聽與閱讀練習教材。
過去已經出過的主題有：${existingTitles}。請挑選一個全新的、貼近台灣國一學生生活的有趣主題（例如：校園生活、運動、寵物、科學常識、台灣文化、日常購物等），並搭配一個國一核心文法。
程度規範：使用台灣教育部國中小基礎 1200 單字，短文約 85~115 字。
請只輸出一段合法的 JSON 物件（包含 id, weekLabel, date, title, grammarFocus, article, vocabulary (6個單字), exercises (Day 1~Day 5 共5題)）。`;

async function main() {
  const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      contents: [{ parts: [{ text: prompt }] }],
      generationConfig: { responseMimeType: "application/json" }
    })
  });

  if (!res.ok) {
    throw new Error(`Gemini API failed: ${res.status}`);
  }
  const data = await res.json();
  const raw = data?.candidates?.[0]?.content?.parts?.[0]?.text || '';
  const newLesson = JSON.parse(raw.replace(/```json|```/g, '').trim());
  lessons.unshift(newLesson);
  fs.writeFileSync('./lessons.json', JSON.stringify(lessons, null, 2), 'utf8');
  console.log('Successfully generated new lesson:', newLesson.title);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
