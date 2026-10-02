# Xanaka Travel — брендбук

**Главный файл:** [`Xanaka-Travel-Brandbook.pdf`](Xanaka-Travel-Brandbook.pdf) — брендбук и гайдлайны, 49 страниц, A4 горизонтально.

| Папка / файл | Что внутри |
|---|---|
| `assets/logo/` | Логотип в SVG: горизонтальный, вертикальный, знак, утолщённый знак (коричневый и светлый). Временная версия до получения исходника |
| `assets/fonts/` | Playfair Display и Manrope (Google Fonts, лицензия OFL) |
| `PLAN.md`, `01-brand-platform.md`, `02-visual-system.md` | Рабочие материалы: бриф, решения, черновики разделов |
| `review/` | Сравнения, которые показывались при согласовании |
| `src/` | Исходники брендбука: `build_brandbook.py` + `brandbook.css` → PDF; `build_logo.py` → SVG логотипа |

**Пересобрать PDF** (нужен Chromium): `python3 brandbook/src/build_brandbook.py`

**Заменить логотип:** положить новые SVG в `assets/logo/` с теми же именами файлов и пересобрать PDF.
