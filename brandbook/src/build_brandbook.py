"""Builds the Xanaka Travel brand book: HTML (A4 landscape pages) -> PDF via headless Chromium.

Usage: python3 brandbook/src/build_brandbook.py
Output: brandbook/Xanaka-Travel-Brandbook.pdf
"""
import os, re, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
LOGO = os.path.join(ROOT, 'assets', 'logo')
CHROME = os.environ.get('CHROME', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')


def svg(name, cls='', style=''):
    s = open(os.path.join(LOGO, name + '.svg')).read().strip()
    s = re.sub(r'style="color:[^"]+"', '', s)
    s = re.sub(r'width="[^"]+" height="[^"]+"', f'class="{cls}" style="{style}"', s, count=1)
    return s


H_LOGO = svg('xanaka-logo-horizontal-brown', 'logo')
S_LOGO = svg('xanaka-logo-stacked-brown', 'logo')
MARK = svg('xanaka-mark-brown', 'logo')
MARK_B = svg('xanaka-mark-bold-brown', 'logo')

# Arch outline used for photo crops (same equilateral construction as the mark).
def arch_path(w, h):
    import math
    rise = min(math.sqrt(w * w - (w / 2) ** 2), h * 0.75)
    r = ((w / 2) ** 2 + rise ** 2) / w
    return f"M0 {h} V{rise:.1f} A{r:.1f} {r:.1f} 0 0 1 {w/2:.1f} 0 A{r:.1f} {r:.1f} 0 0 1 {w} {rise:.1f} V{h} Z"


def arch_clip(w, h):
    return f"clip-path:path('{arch_path(w, h)}');width:{w}px;height:{h}px"


CSS = open(os.path.join(HERE, 'brandbook.css')).read()

pages = []
TOC = []


def page(body, section='', cls='', title=None, num=True):
    if title:
        TOC.append((title, len(pages) + 1, section))
    foot = ''
    if num:
        foot = (f'<div class="foot"><span>Xanaka Travel · Brand Book</span>'
                f'<span>{section}</span><span class="pn">{len(pages)+1:02d}</span></div>')
    pages.append(f'<section class="pg {cls}">{body}{foot}</section>')


def head(eyebrow, title, lead=''):
    l = f'<p class="lead">{lead}</p>' if lead else ''
    return f'<div class="eb">{eyebrow}</div><h2>{title}</h2><div class="rule"></div>{l}'


def ph(label='фото', style='', cls=''):
    return f'<div class="ph {cls}" style="{style}"><span>{label}</span></div>'


def part(no, name, items):
    li = ''.join(f'<li>{i}</li>' for i in items)
    page(f'<div class="partno">Part {no}</div><h1 class="parth">{name}</h1>'
         f'<ul class="partlist">{li}</ul><div class="partmark">{MARK}</div>',
         section=name, cls='dark part', title=f'Part {no}. {name}')


# ---------------------------------------------------------------- cover
page(f'''<div class="cover-logo">{S_LOGO}</div>
<div class="cover-t">Brand Book<br><em>&amp; Guidelines</em></div>
<div class="cover-m">Version 1.0 · October 2026 · EN / FR</div>''', cls='cover', num=False)

# ---------------------------------------------------------------- contents (filled later)
pages.append('__TOC__')

# ================================================================ PART I
part('I', 'Brand Strategy', ['Главный принцип', 'История имени', 'Суть бренда и позиционирование',
     'Аудитории и рынки', 'Архитектура бренда', 'Опоры и характер', 'Обещание и путь клиента'])
S = 'Brand Strategy'

page(f'''<div class="big-quote">
<div class="eb">Главный принцип бренда</div>
<p class="q">Xanaka does not sell Uzbekistan as a destination.<br>Xanaka sells <em>the experience of discovering</em> Uzbekistan.</p>
<div class="rule"></div>
<p class="lead">Это правило определяет всё: сайт → Instagram → рекламу → фотографии → тексты → туры → работу гида → сервис.
Если решение не помогает гостю открыть Узбекистан глубже, оно не подходит бренду.</p></div>''', S, title='Главный принцип')

page(f'''<div class="cols2"><div>
{head('История имени', 'Ханака: дом для путника')}
<p>Ханака (узб. <i>xonaqoh</i>) — обитель на караванных путях Центральной Азии. Здесь путника принимали,
кормили и давали ночлег, кем бы он ни был. Самая известная — ханака Надир Диван-беги (1620) в ансамбле
Ляби-Хауз в Бухаре.</p>
<p>Xanaka Travel продолжает эту роль: мы принимающая сторона, у которой гость Узбекистана в надёжных руках
с момента прилёта до вылета.</p>
<p class="small"><b>Произношение:</b> X читается как «кх» — <i>Kha-na-ka</i>. Один раз объясняем в презентации и на сайте.</p>
</div><div>
<div class="quote-box"><div class="eb">EN</div><p class="qs">Our name comes from the khanaqah, the lodges where Silk Road travellers were welcomed,
fed and sheltered. Four centuries later, we still believe <em>every traveller is our guest.</em></p>
<div class="eb">FR</div><p class="qs">Notre nom vient de la khanaqah, ces maisons d’accueil où les voyageurs de la Route de la Soie
trouvaient un repas et un abri. Quatre siècles plus tard, <em>chaque voyageur reste notre hôte.</em></p>
<p class="small">Во французском <i>hôte</i> значит и «хозяин», и «гость»: одним словом сказано, кто мы и как относимся к путешественнику.</p></div>
</div></div>''', S, title='История имени')

page(f'''{head('Brand essence', 'Authentic Uzbekistan, <em>thoughtfully experienced.</em>')}
<div class="cols2"><div>
<div class="kv"><b>Категория</b><span>Inbound travel company / Destination Management Company</span></div>
<div class="kv"><b>Направление</b><span>Узбекистан и Центральная Азия</span></div>
<div class="kv"><b>Core proposition</b><span>We don’t simply show Uzbekistan. We help travellers experience it.</span></div>
<p>Xanaka соединяет международный уровень сервиса с локальной экспертизой.</p>
</div><div>
<div class="nots"><div>Не массовый туризм.</div><div>Не стандартный экскурсионный пакет.</div><div>Не «luxury ради luxury».</div></div>
<p class="em-line">Xanaka = carefully designed journeys through the real Uzbekistan.</p>
</div></div>''', S, title='Суть бренда')

page(f'''{head('Positioning', 'From <em>visiting</em> Uzbekistan to <em>experiencing</em> Uzbekistan')}
<div class="cols2"><div>
<div class="eb">Positioning statement</div>
<p class="qs">Xanaka Travel creates private and small-group journeys through Uzbekistan and Central Asia for curious
international travellers — and for the tour operators who send them — who want to experience the country’s history,
culture, food and people beyond the standard tourist route.</p>
</div><div>
<div class="eb">Отстройка от категории</div>
<p>Большинство DMC в Узбекистане показывают одно и то же: Регистан на закате, купола, «Pearl of the East».
Мы говорим о людях, деталях и надёжности. Узбекская культура видна в нашей арке, цветах изразцов и
орнаменте — без клише.</p>
<p>«Шёлковый путь» используем не больше одного раза на носитель и всегда рядом с конкретикой: город, люди, опыт.</p>
</div></div>''', S, title='Позиционирование')

page(f'''{head('Target audience', 'Два адресата, одна интонация')}
<div class="cols2"><div class="card">
<div class="eb">B2C · путешественники</div><h3>Curious international traveller</h3>
<p><b>Возраст:</b> 35–65+. <b>Языки:</b> английский и французский.</p>
<p><b>Рынки:</b> Франция, Бельгия, Швейцария, Канада (Квебек), Великобритания, США и другие англоязычные рынки.</p>
<p><b>Интересы:</b> история, культура, архитектура, гастрономия, фотография, ремёсла, живые встречи с людьми —
при комфорте, безопасности и хорошей организации.</p>
<p class="em-line">Ищет не самый дорогой тур, а поездку, которая стоит его времени и денег.</p>
</div><div class="card">
<div class="eb">B2B · партнёры</div><h3>Tour operators, agencies, MICE planners</h3>
<p>Зарубежные туроператоры и агентства, тревел-дизайнеры, MICE- и incentive-организаторы.</p>
<p><b>Что им важно:</b> быстрый ответ, один менеджер, понятные нетто-цены, надёжная работа на месте,
гиды с французским и английским, план Б.</p>
<p class="em-line">Им мы продаём уверенность: ваши клиенты — наши гости.</p>
</div></div>''', S, title='Аудитории и рынки')

arch_items = [
    ('XANAKA PRIVATE', 'Private tailor-made journeys', 'Маршрут под одного клиента или семью.'),
    ('XANAKA SMALL GROUP', 'Small group departures', 'Групповые выезды по датам, без автобусов на 50 мест.'),
    ('XANAKA EXPERIENCES', 'Food, crafts &amp; local life', 'Гастро-туры, кухня, ремёсла, вино, фото, семейные дома.'),
    ('XANAKA DISCOVERY', 'Hidden Uzbekistan', 'Малоизвестные места: Нурата, Аральское море, горы, пустыня.'),
    ('XANAKA MICE', 'Meetings, incentives, events', 'Конференции, incentive-поездки, корпоративные программы.'),
    ('XANAKA CENTRAL ASIA', 'Multi-country journeys', 'Узбекистан + Таджикистан, Кыргызстан, Туркменистан.'),
]
cells = ''.join(f'<div class="ba"><div class="ba-n">{a}</div><div class="ba-e">{b}</div><p>{c}</p></div>' for a, b, c in arch_items)
page(f'''{head('Brand architecture', 'Одна марка — шесть направлений', 'Все направления используют один логотип XANAKA. Название направления — текстовая подпись Manrope 600 капителью, не отдельный логотип. Так бизнес растёт без новых брендов.')}
<div class="ba-grid">{cells}</div>''', S, title='Архитектура бренда')

pillars = [('01', 'AUTHENTIC', 'The real Uzbekistan', 'Местные люди, ремёсла, рынки, кухня, семейные традиции, малоизвестные места.'),
           ('02', 'PERSONAL', 'Your journey, your way', 'Не готовый пакет, а путешествие, адаптированное под человека или группу.'),
           ('03', 'EXPERT', 'Local knowledge, international standards', 'Знаем страну изнутри, а сервис и коммуникация — на уровне ожиданий международного клиента.'),
           ('04', 'DISCOVERY', 'Beyond the obvious', 'Самарканд, Бухара и Хива — но не только Регистан, Арк и Ичан-Кала.')]
pc = ''.join(f'<div class="pil"><div class="pil-n">{n}</div><div class="pil-t">{t}</div><div class="pil-e">{e}</div><p>{d}</p></div>' for n, t, e, d in pillars)
page(f'''{head('Brand pillars', 'Четыре опоры бренда')}<div class="pil-grid">{pc}</div>
<p class="em-line" style="margin-top:8mm">There is more to Uzbekistan than the famous landmarks.</p>''', S, title='Опоры бренда')

pers = [('Knowledgeable', 'Мы знаем страну.'), ('Warm', 'Мы гостеприимны.'), ('Curious', 'Нам интересно находить новое.'),
        ('Refined', 'Мы ценим детали.'), ('Authentic', 'Мы не создаём искусственную «экзотику».'), ('Confident', 'Мы не кричим о своей премиальности.')]
notl = ['mass-market tour operator', 'дешёвый туристический агент', '«этно-туризм» в стереотипном понимании',
        'flashy luxury travel', 'overly corporate DMC', 'backpacker hostel brand']
page(f'''{head('Brand personality', 'Опытный хозяин дома')}
<div class="cols2"><div><div class="eb">Мы</div>
{''.join(f'<div class="kv"><b>{a}</b><span>{b}</span></div>' for a,b in pers)}</div>
<div><div class="eb">Мы не выглядим как</div><ul class="x">{''.join(f'<li>{n}</li>' for n in notl)}</ul></div></div>''', S, title='Характер бренда')

page(f'''{head('Brand promise', 'Ваши клиенты — <em>наши гости</em>', 'Vos clients sont nos hôtes. Обещание подкрепляется стандартами сервиса — их соблюдает каждый сотрудник.')}
<div class="std-grid">
<div class="std"><div class="std-n">24 h</div><p>Ответ на любой запрос в течение 24 часов, готовое предложение — до 48 часов.</p></div>
<div class="std"><div class="std-n">1</div><p>Один менеджер на досье — от запроса до вылета гостей.</p></div>
<div class="std"><div class="std-n">24/7</div><p>Поддержка на месте круглосуточно и понятный план Б.</p></div>
<div class="std"><div class="std-n">EN · FR</div><p>Гиды с английским и французским, которых мы сами отбираем и обучаем.</p></div>
<div class="std"><div class="std-n">Net</div><p>Прозрачные цены для партнёров, без скрытых доплат.</p></div>
</div>''', S, title='Обещание бренда')

cj = [('Before the trip', ['Inspire', 'Consult', 'Design', 'Confirm']),
      ('During', ['Welcome', 'Guide', 'Experience', 'Support']),
      ('After', ['Follow-up', 'Memories', 'Referral', 'Community'])]
cjh = ''.join(f'<div class="cj"><div class="eb">{a}</div><div class="cj-row">{"".join(f"<span>{x}</span>" for x in b)}</div></div>' for a, b in cj)
page(f'''{head('Customer experience', 'Мы продаём не тур, а путешествие целиком', 'Бренд проявляется не только в визуале: на каждом шаге гость должен чувствовать одно и то же — заботу хозяина.')}
<div class="cj-wrap">{cjh}</div>
<div class="cols3 small"><p><b>До поездки:</b> быстрый и личный ответ, программа под гостя, ясные условия.</p>
<p><b>В поездке:</b> встреча с табличкой, гид знает имена гостей, связь 24/7, мелочи предусмотрены заранее.</p>
<p><b>После:</b> письмо-благодарность в течение 3 дней, лучшие фото, просьба об отзыве, приглашение вернуться.</p></div>''', S, title='Путь клиента')

# ================================================================ PART II
part('II', 'Visual Identity', ['Логотип', 'Охранное поле и размеры', 'Фоны и запреты', 'Цвет', 'Типографика', 'Графика: арка, линии, орнамент, иконки', 'Фотография'])
S = 'Visual Identity'

page(f'''{head('Logo', 'Логотип и его версии', 'Логотип состоит из знака (стрельчатая арка с диагональю, образующей X) и надписи XANAKA. Используйте только готовые файлы из папки assets/logo.')}
<div class="lv-grid">
<div class="lv"><div class="lv-box">{H_LOGO}</div><b>Горизонтальная</b><span>Сайт, документы, email, визитка</span></div>
<div class="lv"><div class="lv-box">{S_LOGO}</div><b>Вертикальная с подписью</b><span>Обложки, стенд, мерч, квадратные форматы</span></div>
<div class="lv"><div class="lv-box sq">{MARK}</div><b>Знак</b><span>Водяной знак, паттерн, крупные форматы</span></div>
<div class="lv"><div class="lv-box sq">{MARK_B}</div><b>Знак утолщённый</b><span>До 48 px: фавикон, аватар, бейдж, вышивка</span></div>
</div>
<p class="small note">Текущие файлы логотипа — временная версия. После получения исходника файлы заменяются; все правила этого раздела остаются.</p>''', S, title='Логотип')

page(f'''<div class="cols2"><div>
{head('Logo idea', 'Арка и перекрёсток')}
<p><b>Арка</b> — вход в медресе и портал ханаки, где путника встречали как гостя. Она построена как классическая
равносторонняя стрельчатая арка: радиус каждой дуги равен пролёту — канон архитектуры Самарканда и Бухары.</p>
<p><b>Диагональ</b> повторяет правую дугу со сдвигом на половину пролёта и вместе с левой стороной образует X —
первую букву имени и перекрёсток караванных путей.</p>
<p><b>Надпись</b> набрана Playfair Display Bold с разрядкой 0,06 em и переведена в кривые.</p>
</div><div class="construct">{MARK}<div class="c-lab l1">R = пролёт</div><div class="c-lab l2">X</div></div></div>''', S, title='Идея знака')

# clear space: horizontal logo shown at 26mm height; x = cap height = 180/430 of logo height
page(f'''{head('Clear space &amp; minimum size', 'Охранное поле и минимальный размер')}
<div class="cols2"><div>
<div class="cs-wrap"><div class="cs">{H_LOGO}</div></div>
<p>Минимальный отступ от логотипа до любого элемента и края носителя = <b>x</b>, высота буквы X в надписи XANAKA.</p>
</div><div>
<table class="tb"><tr><th>Версия</th><th>Экран</th><th>Печать</th></tr>
<tr><td>Горизонтальная</td><td>120 px</td><td>30 мм</td></tr>
<tr><td>Вертикальная</td><td>80 px</td><td>20 мм</td></tr>
<tr><td>Знак</td><td>48 px</td><td>12 мм</td></tr>
<tr><td>Знак утолщённый</td><td>16 px</td><td>5 мм</td></tr></table>
<p class="small">Размер — по ширине логотипа. Меньше этих значений тонкие линии знака пропадают; для мелких размеров используйте утолщённый знак.</p>
<div class="minis"><div style="width:30mm">{H_LOGO}</div><div style="width:12mm">{MARK}</div><div style="width:5mm">{MARK_B}</div></div>
</div></div>''', S, title='Охранное поле')

page(f'''{head('Backgrounds', 'Логотип на фонах')}
<div class="bg-grid">
<div class="bgc" style="background:var(--ivory);color:var(--brown)">{H_LOGO}<span>Ivory · основной</span></div>
<div class="bgc" style="background:var(--sand);color:var(--brown)">{H_LOGO}<span>Sand</span></div>
<div class="bgc" style="background:var(--brown);color:var(--ivory)">{H_LOGO}<span style="color:var(--ivory)">Brown · светлая версия</span></div>
<div class="bgc phbg" style="color:var(--ivory)">{H_LOGO}<span style="color:var(--ivory)">Фото: спокойная зона, светлая версия</span></div>
<div class="bgc phbg busy" style="color:var(--ivory)"><div class="plate">{H_LOGO}</div><span style="color:var(--ivory)">Пёстрое фото: только с плашкой Brown</span></div>
<div class="bgc" style="background:var(--teal);color:var(--ivory)">{H_LOGO}<span style="color:var(--ivory)">Teal · только для мерча и стенда</span></div>
</div>''', S, title='Фоны')

mis = [('transform:scaleX(1.5)', 'Не растягивать и не сжимать'), ('transform:rotate(-12deg)', 'Не поворачивать'),
       ('color:#C0392B', 'Не перекрашивать вне палитры'), ('filter:drop-shadow(1.2mm 1.2mm 0.8mm rgba(0,0,0,.55))', 'Без теней и эффектов'),
       ('', 'Не делать обводку и не красить в несколько цветов'), ('', 'Не набирать другим шрифтом')]
mc = ''
for st, lab in mis:
    if lab.startswith('Не набирать'):
        inner = '<div class="fake">XANAKA</div>'
    elif lab.startswith('Не делать обводку'):
        inner = f'<div class="twotone">{H_LOGO}</div>'
    else:
        inner = f'<div style="{st}">{H_LOGO}</div>'
    mc += f'<div class="mis"><div class="mis-box">{inner}<div class="cross"></div></div><span>{lab}</span></div>'
page(f'''{head('Misuse', 'Так нельзя')}<div class="mis-grid">{mc}</div>
<p class="small">Также нельзя: менять расстояние между знаком и надписью, переставлять их, ставить логотип на пёстрое фото без плашки.</p>''', S, title='Запреты')

pal = [('Xanaka Brown', '#4A3B30', '74 59 48', '0 20 35 71', 'Логотип, заголовки, текст, тёмные фоны', 'ivory'),
       ('Ivory', '#FAF7EF', '250 247 239', '0 1 4 2', 'Основной фон', 'brown'),
       ('Tile Teal', '#2E7A7B', '46 122 123', '63 1 0 52', 'Кнопки, ссылки, активные элементы', 'ivory'),
       ('Tile Teal Dark', '#235E5F', '35 94 95', '63 1 0 63', 'Наведение и нажатие, текст на бирюзе', 'ivory'),
       ('Sand', '#E6DCCB', '230 220 203', '0 4 12 10', 'Второй фон: блоки, карточки', 'brown'),
       ('Saffron', '#C9973F', '201 151 63', '0 25 69 21', 'Линии, иконки, детали. Не текст на светлом', 'brown')]
pcards = ''.join(f'<div class="sw" style="background:{h};color:var(--{fg})"><div class="sw-n">{n}</div>'
                 f'<div class="sw-v">HEX {h}<br>RGB {r}<br>CMYK {c}</div><div class="sw-u">{u}</div></div>' for n, h, r, c, u, fg in pal)
page(f'''{head('Colour', 'Палитра: изразец, глина, свет')}<div class="sw-grid">{pcards}</div>
<p class="small note">HEX/RGB — эталон для экрана. CMYK — стартовые значения: перед первым тиражом сделать пробную печать и подобрать Pantone по вееру в типографии.</p>''', S, title='Палитра')

contrast = [('Brown на Ivory', '10.0', 'Любой текст', 'var(--brown)', 'var(--ivory)'),
            ('Brown на Sand', '7.9', 'Любой текст', 'var(--brown)', 'var(--sand)'),
            ('Ivory на Brown', '10.0', 'Любой текст', 'var(--ivory)', 'var(--brown)'),
            ('Белый на Teal', '5.0', 'Текст кнопок', '#fff', 'var(--teal)'),
            ('Teal на Ivory', '4.7', 'Ссылки, текст от 14 px', 'var(--teal)', 'var(--ivory)'),
            ('Saffron на Brown', '4.1', 'Капитель от 18 px', 'var(--saffron)', 'var(--brown)'),
            ('Saffron на Ivory', '2.5', 'Нельзя для текста', 'var(--saffron)', 'var(--ivory)')]
crow = ''.join(f'<div class="cr" style="color:{f};background:{b}"><b>Aa</b><span>{n}</span><span>{v} : 1</span><span>{u}</span></div>' for n, v, u, f, b in contrast)
page(f'''{head('Colour use', 'Пропорции и контраст')}
<div class="prop"><div style="flex:60;background:var(--ivory)">Ivory 60%</div><div style="flex:15;background:var(--sand)">Sand 15%</div>
<div style="flex:15;background:var(--brown);color:var(--ivory)">Brown 15%</div><div style="flex:7;background:var(--teal);color:var(--ivory)">Teal 7%</div><div style="flex:3;background:var(--saffron)"></div></div>
<p class="small">Saffron ≈ 3%. Бирюза и шафран — акценты: если бирюзы больше, чем коричневого, носитель теряет характер бренда.</p>
<div class="cr-grid">{crow}</div>
<p class="small">Контраст по WCAG 2.1. Аудитория 35–65+, поэтому основной текст — всегда Brown на Ivory или Sand.</p>''', S, title='Пропорции и контраст')

page(f'''{head('Typography', 'Два шрифта сайта')}
<div class="cols2"><div class="tf">
<div class="tf-big pf">Aa</div><h3 class="pf">Playfair Display</h3>
<p>Заголовки, названия городов, цитаты. Regular 400 и Italic 400.</p>
<div class="pf glyphs">ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>abcdefghijklmnopqrstuvwxyz<br><i>àâçéèêëîïôœùûü « » 0123456789</i></div>
</div><div class="tf">
<div class="tf-big mr">Aa</div><h3 class="mr" style="font-weight:600">Manrope</h3>
<p>Текст, меню, кнопки, программы туров, подписи. Regular 400, Medium 500, SemiBold 600.</p>
<div class="mr glyphs">ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>abcdefghijklmnopqrstuvwxyz<br>àâçéèêëîïôœùûü « » 0123456789</div>
</div></div>
<p class="small">Оба шрифта бесплатные (Google Fonts, лицензия OFL), с полной поддержкой французского. Логотип не набирается шрифтом — только файлы.</p>''', S, title='Шрифты')

page(f'''{head('Type scale', 'Иерархия текста')}
<div class="scale">
<div class="sc"><span class="tag">H1 · Playfair 400 · 56/60 px · печать 32 pt</span><div class="pf" style="font-size:34pt;line-height:1.05">Experience Uzbekistan <em>Differently.</em></div></div>
<div class="sc"><span class="tag">H2 · Playfair 400 · 40/46 px · 22 pt</span><div class="pf" style="font-size:22pt">Private journeys</div></div>
<div class="sc"><span class="tag">H3 · Playfair 400 · 28/34 px · 16 pt</span><div class="pf" style="font-size:16pt">The Classic Silk Road</div></div>
<div class="sc"><span class="tag">Eyebrow · Manrope 600 · капитель, разрядка 0.2 em · 12 px · 8 pt</span><div class="eb" style="margin:0">PRIVATE JOURNEYS IN UZBEKISTAN</div></div>
<div class="sc"><span class="tag">Текст · Manrope 400 · 17/28 px · 10/15 pt</span><div style="font-size:10.5pt;max-width:150mm">Lunch with a family in Bukhara, then a walk through the old town with your guide.</div></div>
<div class="sc"><span class="tag">Кнопка · Manrope 600 · капитель, разрядка 0.15 em · 13 px</span><div><span class="btn">Enquire</span></div></div>
</div>''', S, title='Иерархия текста')

page(f'''{head('Signature device', 'Одно слово курсивом')}
<div class="cols2"><div>
<div class="pf" style="font-size:30pt;line-height:1.1">Private journeys along the <em>Silk Road</em></div>
<div class="pf" style="font-size:30pt;line-height:1.1;margin-top:8mm">Vivez l’Ouzbékistan <em>autrement.</em></div>
</div><div>
<p>В заголовке курсивом Playfair выделяется <b>одно</b> слово или короткое сочетание — место или ключевое понятие.</p>
<ul class="ok"><li>Не больше одного выделения на заголовок</li><li>Не выделять служебные слова (the, of, de, la)</li><li>Курсив того же цвета, что и заголовок; на тёмном фоне допустим Saffron</li></ul>
<div class="eb" style="margin-top:6mm">Правила EN и FR</div>
<ul class="ok"><li>EN: sentence case — «Private journeys along the Silk Road», не Title Case</li>
<li>FR: неразрывный пробел перед : ; ! ? и внутри « … »</li>
<li>FR: акценты на заглавных — <i>Évasion</i>, не <i>Evasion</i></li>
<li>Капитель — только для eyebrow и кнопок</li></ul>
</div></div>''', S, title='Фирменный приём')

page(f'''{head('Graphic element', 'Арка: обычная версия и акцент', 'Главный графический элемент — стрельчатая арка из логотипа. По умолчанию фото прямоугольные; кадр в арке — акцент: не больше одного на разворот и примерно 1 из 4–5 постов.')}
<div class="cols2" style="align-items:end">
<div><div class="mini-cover">{ph(style="position:absolute;right:0;top:0;bottom:0;width:45%")}<div class="mc-t"><div style="width:22mm;color:var(--brown)">{H_LOGO}</div><div class="mc-b"><div class="eb" style="font-size:5.5pt">PRIVATE JOURNEY · 8 DAYS</div><div class="pf" style="font-size:15pt">The Classic <em>Silk Road</em></div></div></div></div><div class="cap">Обычная версия — по умолчанию</div></div>
<div><div class="mini-cover"><div class="ph arch" style="position:absolute;right:8mm;bottom:0;{arch_clip(150,190)}"><span>фото</span></div><div class="mc-t"><div style="width:22mm;color:var(--brown)">{H_LOGO}</div><div class="mc-b"><div class="eb" style="font-size:5.5pt">PRIVATE JOURNEY · 8 DAYS</div><div class="pf" style="font-size:15pt">The Classic <em>Silk Road</em></div></div></div></div><div class="cap">Арка — акцент</div></div>
</div>
<p class="small">Арка всегда той же формы, что в знаке. Нельзя: луковичные купола, арки другой пропорции, орнамент внутри арки.</p>''', S, title='Арка')

ICONS = {
    'Перелёт': '<path d="M3 14l18-6-3 9-5-3-3 4v-5l8-6"/>',
    'Поезд': '<rect x="6" y="3" width="12" height="13" rx="2"/><path d="M6 10h12M9 19l-2 3M15 19l2 3M9 13h0M15 13h0"/>',
    'Трансфер': '<path d="M3 15V11l2-5h14l2 5v4H3zM3 11h18"/><circle cx="7" cy="16" r="1.6"/><circle cx="17" cy="16" r="1.6"/>',
    'Отель': '<path d="M4 21V5h11v16M15 9h5v12M7 8h2M11 8h1M7 12h2M11 12h1M7 16h2M11 16h1"/>',
    'Кухня': '<path d="M4 12h16a8 8 0 0 1-16 0zM12 4v4M8 6v2M16 6v2"/>',
    'Ремёсла': '<path d="M8 4h8l-1 4a6 6 0 1 1-6 0z"/>',
    'Гид': '<circle cx="12" cy="7" r="3"/><path d="M5 21a7 7 0 0 1 14 0"/>',
    'Фото': '<rect x="3" y="7" width="18" height="13" rx="1"/><circle cx="12" cy="13.5" r="3.5"/><path d="M9 7l1.5-3h3L15 7"/>',
    'Пустыня': '<path d="M2 19c4-6 7-6 10 0M10 19c3-4 6-5 12 0M17 8a2 2 0 1 0 0-.1"/>',
    'Горы': '<path d="M2 20l7-12 4 6 3-4 6 10z"/>',
    'Архитектура': '<path d="M5 21V12a7 7 0 0 1 14 0v9M5 21h14M9 21v-6a3 3 0 0 1 6 0v6"/>',
    'MICE': '<rect x="3" y="4" width="18" height="11"/><path d="M12 15v5M8 20h8"/>',
}
ic = ''.join(f'<div class="ic"><svg viewBox="0 0 24 24">{p}</svg><span>{n}</span></div>' for n, p in ICONS.items())
page(f'''{head('Lines, ornament, icons', 'Детали')}
<div class="cols3">
<div><div class="eb">Линии</div><div class="rule" style="width:40px"></div><p class="small">Тонкая линия 1 px (1 pt) Saffron или Brown 20%. Отрезок 40 px под eyebrow или заголовком — фирменный разделитель.</p>
<div style="border-top:1px solid var(--saffron);margin:5mm 0"></div><div style="border-top:1px solid rgba(74,59,48,.2)"></div></div>
<div><div class="eb">Орнамент</div><div class="orn"></div><p class="small">Одна полоса орнамента на носитель, монохромно (Sand на Ivory или Brown 10% на Sand). Рисуется по мотивам изразцов Самарканда и Бухары, не берётся из стоков.</p></div>
<div><div class="eb">Иконки</div><div class="ic-grid">{ic}</div><p class="small">Линейные, толщина линии как у знака, цвет Brown или Saffron, без заливки и скруглений.</p></div>
</div>''', S, title='Линии, орнамент, иконки')

pp = [('Регистан', 'Путешественник идёт по Регистану на рассвете'), ('Плов', 'Руки, готовящие плов на семейной кухне'),
      ('Керамика', 'Мастер работает с глиной в Риштане'), ('Пустой номер', 'Гость пьёт чай на террасе отеля')]
page(f'''{head('Photography', 'People &gt; places', 'Фото показывают не место, а опыт: человека в месте, руки за работой, момент встречи.')}
<div class="pp-grid">{''.join(f'<div class="ppc"><div class="no">Не так</div><div class="ph sm"><span>{a}</span></div><div class="yes">Так</div><div class="ph sm warm"><span>{b}</span></div></div>' for a,b in pp)}</div>
<div class="cols3 small"><p><b>Снимаем:</b> людей и встречи, руки и ремесло, еду в процессе, фактуры (изразец, ткань, глина, хлеб), архитектуру с человеком для масштаба, пейзажи, движение.</p>
<p><b>Свет:</b> рассвет, «золотой час», мягкая тень. Тёплая сдержанная обработка, без HDR, фильтров и перенасыщенной бирюзы неба.</p>
<p><b>Не используем:</b> стоки с постановочными улыбками, «этнические» костюмы ради экзотики, пустые открыточные панорамы (не больше 1 из 5 фото), чужие водяные знаки.</p></div>''', S, title='Фотография')

page(f'''{head('Photo captions &amp; rights', 'Подписи на фото и права')}
<div class="cols2"><div>
<div class="capdemo">{ph('фото', 'position:absolute;inset:0', 'warm')}<div class="capbar">BUKHARA · PO-I-KALYAN AT DAWN</div></div>
<div class="cap">Так: Ivory на затемнённой зоне или плашке Brown 70%</div>
</div><div>
<div class="capdemo">{ph('фото', 'position:absolute;inset:0', 'warm')}<div class="capbad">BUKHARA · PO-I-KALYAN AT DAWN</div><div class="cross"></div></div>
<div class="cap">Не так: тёмный текст прямо по фото</div>
<p class="small" style="margin-top:6mm">Подпись места: Manrope 600, капитель, разрядка 0.2 em, формат <b>ГОРОД · МЕСТО</b>.
Для каждого фото фиксируем автора, дату и разрешение людей в кадре на публикацию.</p>
</div></div>''', S, title='Подписи на фото')

# ================================================================ PART III
part('III', 'Communication', ['Тон голоса', 'Так и не так', 'Словарь бренда', 'Система слоганов', 'Текст «о компании»', 'Глоссарий'])
S = 'Communication'

page(f'''{head('Tone of voice', 'Warm + knowledgeable + sophisticated + human')}
<div class="tv-grid">
<div><div class="pil-n">01</div><h3>Говорим как хозяин, а не как каталог</h3><p>Приглашаем, рассказываем, советуем. Вместо превосходных степеней — конкретика.</p></div>
<div><div class="pil-n">02</div><h3>Факты вместо эпитетов</h3><p>Время в пути, размер группы, имя гида, название деревни. Конкретное убеждает лучше «удивительного».</p></div>
<div><div class="pil-n">03</div><h3>Короткие фразы</h3><p>Нас читают и не носители языка. Одна мысль — одно предложение.</p></div>
<div><div class="pil-n">04</div><h3>Французский пишется по-французски</h3><p>Адаптация, а не перевод. Обращение на <i>vous</i>. Типографика по французским правилам.</p></div>
<div><div class="pil-n">05</div><h3>Культура без пафоса</h3><p>История через людей и детали, без «жемчужин Востока» и «сказок 1001 ночи».</p></div>
<div><div class="pil-n">06</div><h3>Уверенно, без крика</h3><p>Без капслока и восклицательных знаков. Премиальность показываем качеством, а не словами.</p></div>
</div>''', S, title='Тон голоса')

dd = [('Discover the most AMAZING and UNFORGETTABLE Uzbekistan!!!', 'Discover Uzbekistan beyond the landmarks.'),
      ('We offer the BEST luxury tours in Uzbekistan!', 'Private journeys designed around the way you want to travel.'),
      ('Découvrez la magie envoûtante de l’Orient !', 'Déjeuner chez une famille à Boukhara, puis balade dans la vieille ville avec votre guide.'),
      ('We offer the best service on the market.', 'We reply to every request within 24 hours.')]
page(f'''{head('Do &amp; don’t', 'Так и не так')}
<div class="dd">{''.join(f'<div class="ddr"><div class="no-t"><span>Не так</span><s>{a}</s></div><div class="yes-t"><span>Так</span>{b}</div></div>' for a,b in dd)}</div>''', S, title='Так и не так')

use = ['Journey', 'Discover', 'Experience', 'Authentic', 'Tailor-made', 'Private', 'Small group', 'Silk Road*', 'Culture', 'Local', 'Craftsmanship', 'Cuisine', 'Hidden places', 'Meaningful travel']
avoid = ['Cheap', 'Best price', 'Amazing!!!', 'Unforgettable!!!', 'Cheap tours', 'Guaranteed best', 'Number one', 'Pearl of the Orient', 'Luxury experience (без содержания)']
page(f'''{head('Brand vocabulary', 'Словарь бренда')}
<div class="cols2"><div><div class="eb">Используем</div><div class="chips">{''.join(f'<span>{w}</span>' for w in use)}</div>
<p class="small">* Silk Road — не больше одного раза на носитель и рядом с конкретикой.</p></div>
<div><div class="eb">Избегаем</div><div class="chips bad">{''.join(f'<span>{w}</span>' for w in avoid)}</div></div></div>''', S, title='Словарь бренда')

tl = [('Основной', 'Experience Uzbekistan <em>Differently.</em>', 'Vivez l’Ouzbékistan <em>autrement.</em>'),
      ('Дескриптор', 'Private &amp; Small Group Tours in Uzbekistan', 'Voyages privés et en petits groupes en Ouzbékistan'),
      ('Эмоциональный', 'Discover the Uzbekistan Behind the Landmarks.', 'L’Ouzbékistan au-delà des monuments.'),
      ('Premium', 'Journeys into the Heart of Uzbekistan.', 'Voyages au cœur de l’Ouzbékistan.'),
      ('Гостеприимство (о нас)', 'Every traveller is our guest.', 'Chaque voyageur est notre hôte.'),
      ('Instagram', 'Silk Road • Culture • Hidden Places', 'Route de la Soie • Culture • Lieux secrets')]
page(f'''{head('Tagline system', 'Система слоганов')}
<table class="tb tl"><tr><th>Роль</th><th>EN</th><th>FR</th></tr>{''.join(f'<tr><td>{a}</td><td class="pf">{b}</td><td class="pf">{c}</td></tr>' for a,b,c in tl)}</table>
<p class="small">Французские версии — адаптация; перед публикацией вычитать носителем языка.</p>''', S, title='Слоганы')

page(f'''{head('Boilerplate', 'Текст «о компании»')}
<div class="cols2 small-text"><div><div class="eb">EN</div>
<p>Xanaka Travel is a destination management company based in Uzbekistan. We design and operate private tours, small-group journeys,
MICE programmes, food tours and multi-country itineraries across Central Asia for travellers, tour operators and travel agencies.
Our name comes from the khanaqah, the lodges where Silk Road travellers were welcomed, fed and sheltered. We work in the same spirit:
one dedicated manager per file, a reply within 24 hours and support on the ground 24/7.</p></div>
<div><div class="eb">FR</div>
<p>Xanaka Travel est une agence réceptive basée en Ouzbékistan. Nous concevons et opérons des circuits privés, des voyages en petits groupes,
des programmes MICE, des circuits gastronomiques et des itinéraires combinés en Asie centrale, pour les voyageurs, les tour-opérateurs et les
agences de voyages. Notre nom vient de la khanaqah, ces maisons d’accueil où les voyageurs de la Route de la Soie trouvaient un repas et un abri.
Nous travaillons dans le même esprit&#8239;: un interlocuteur unique par dossier, une réponse sous 24&#160;heures et une assistance sur place 24&#160;h/24 et 7&#160;j/7.</p></div></div>''', S, title='Текст о компании')

gl = [('Принимающая компания (DMC)', 'Destination management company', 'Agence réceptive'), ('Туроператор', 'Tour operator', 'Tour-opérateur'),
      ('Индивидуальный тур', 'Private tour / tailor-made journey', 'Circuit privé / voyage sur mesure'), ('Мини-группа', 'Small group', 'Petit groupe'),
      ('Комбинированный тур', 'Multi-country journey', 'Circuit combiné'), ('Программа тура', 'Itinerary', 'Programme / itinéraire'),
      ('Заказ', 'File / booking', 'Dossier'), ('Нетто-цена', 'Net rate', 'Tarif net'), ('Гид', 'Guide', 'Guide / accompagnateur'), ('Ханака', 'Khanaqah', 'Khanaqah')]
page(f'''{head('Glossary', 'Глоссарий')}<table class="tb"><tr><th>RU</th><th>EN</th><th>FR</th></tr>{''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a,b,c in gl)}</table>''', S, title='Глоссарий')

# ================================================================ PART IV
part('IV', 'Social Media &amp; Digital', ['Контент-микс Instagram', 'Восемь шаблонов', 'Сайт', 'Карточка тура', 'Подпись в email'])
S = 'Social &amp; Digital'

page(f'''{head('Instagram content mix', 'Лента — не каталог агентства')}
<div class="mix"><div style="flex:40;background:var(--brown);color:var(--ivory)"><b>40%</b>Destination<span>Самарканд, Бухара, Хива, Ташкент, Центральная Азия</span></div>
<div style="flex:25;background:var(--teal);color:var(--ivory)"><b>25%</b>People &amp; Culture<span>Люди, ремесленники, гиды</span></div>
<div style="flex:20;background:var(--sand)"><b>20%</b>Experiences<span>Кухня, вино, поезд, мастерские, дома</span></div>
<div style="flex:15;background:var(--ivory);border:1px solid var(--line)"><b>15%</b>Xanaka<span>Команда, закулисье, гости</span></div></div>
<div class="cols3 small"><p><b>Сетка:</b> чередуем фото на весь кадр и шаблоны с текстом; не больше 2 текстовых постов подряд.</p>
<p><b>Подписи:</b> первая строка — конкретный факт или вопрос; 3–6 хэштегов; EN и FR версии одного поста.</p>
<p><b>Арка:</b> примерно 1 из 4–5 постов. Логотип в постах — знак, в углу, светлая или тёмная версия.</p></div>''', S, title='Контент-микс')

tpls = [('Destination Cover', 'SAMARKAND', 'The city of <em>blue domes.</em>', 'photo'),
        ('Tour Cover', '8 DAYS · PRIVATE', 'The Classic <em>Silk Road</em>', 'arch'),
        ('Travel Tip', 'TRAVEL TIP', 'Best months: <em>April–May,</em> Sept–Oct.', 'sand'),
        ('Quote', 'GUEST STORY', '“It felt like visiting <em>friends.</em>”', 'brown'),
        ('Guest Story', 'MARIE &amp; PAUL · LYON', 'Ten days, <em>three</em> family dinners.', 'photo'),
        ('Experience', 'EXPERIENCE', 'Plov with a family in <em>Bukhara.</em>', 'arch'),
        ('Hidden Place', 'HIDDEN UZBEKISTAN', 'A place most travellers <em>never see.</em>', 'brownphoto'),
        ('CTA', 'PLAN YOUR JOURNEY', 'Tell us how you <em>like to travel.</em>', 'teal')]
def tpl(name, eb, t, kind):
    m = f'<div class="t-mark">{MARK}</div>'
    if kind == 'photo':
        body = f'{ph(style="position:absolute;inset:0", cls="warm")}<div class="t-shade"></div>{m}<div class="t-txt light"><div class="eb">{eb}</div><div class="pf">{t}</div></div>'
    elif kind == 'arch':
        body = f'<div class="ph warm" style="position:absolute;left:50%;top:7mm;transform:translateX(-50%);{arch_clip(80,96)}"><span></span></div>{m}<div class="t-txt c"><div class="eb">{eb}</div><div class="pf">{t}</div></div>'
    elif kind == 'brownphoto':
        body = f'{ph(style="position:absolute;inset:0 0 42% 0", cls="warm")}{m}<div class="t-txt light"><div class="eb" style="color:var(--saffron)">{eb}</div><div class="pf">{t}</div></div>'
    else:
        body = f'{m}<div class="t-txt {"light" if kind in ("brown","teal") else ""}"><div class="eb">{eb}</div><div class="pf">{t}</div></div>'
    bg = {'sand': 'var(--sand)', 'brown': 'var(--brown)', 'teal': 'var(--teal)', 'brownphoto': 'var(--brown)', 'arch': 'var(--ivory)'}.get(kind, 'var(--sand)')
    return f'<div class="tp"><div class="tp-box k-{kind}" style="background:{bg}">{body}</div><span>{name}</span></div>'
page(f'''{head('Social templates', 'Восемь шаблонов')}<div class="tp-grid">{''.join(tpl(*x) for x in tpls)}</div>''', S, title='Шаблоны соцсетей')

page(f'''{head('Website', 'Главный экран и структура сайта')}
<div class="web">
<div class="web-nav"><div style="width:30mm;color:var(--brown)">{H_LOGO}</div><div class="web-links">Journeys&nbsp;&nbsp;&nbsp;Experiences&nbsp;&nbsp;&nbsp;MICE&nbsp;&nbsp;&nbsp;For partners&nbsp;&nbsp;&nbsp;Journal&nbsp;&nbsp;&nbsp;EN | FR</div><span class="btn">Enquire</span></div>
<div class="web-hero">{ph(style="position:absolute;inset:0", cls="warm")}<div class="web-card"><div class="eb">PRIVATE &amp; SMALL GROUP TOURS IN UZBEKISTAN</div><div class="pf" style="font-size:22pt;line-height:1.08">Experience Uzbekistan <em>Differently.</em></div><p class="small">Private &amp; small group journeys through the heart of Central Asia.</p><span class="lnk">Explore our journeys →</span></div></div>
</div>
<div class="cols3 small"><p><b>Структура:</b> Journeys · Experiences · Hidden Uzbekistan · MICE · Central Asia · For partners (B2B) · Journal · About · Contact.</p>
<p><b>B2B-раздел:</b> отдельная страница для туроператоров: стандарты сервиса, нетто-цены по запросу, форма запроса группы, контакт менеджера.</p>
<p><b>Кнопки:</b> основная — Teal, текст белый капителью; вторичная — ссылка Brown с линией Saffron. Контакт WhatsApp в шапке.</p></div>''', S, title='Сайт')

page(f'''{head('Tour card', 'Единая карточка тура')}
<div class="cols2" style="align-items:start"><div class="tour">
{ph(style="height:42mm", cls="warm")}
<div class="tour-b"><div class="eb" style="color:var(--teal)">SAMARKAND → BUKHARA → KHIVA</div>
<div class="tmeta"><span>8 DAYS</span><span>PRIVATE JOURNEY</span></div>
<div class="pf" style="font-size:17pt">The Classic <em>Silk Road</em></div>
<ul><li>Registan at sunrise</li><li>Traditional Uzbek cuisine</li><li>Local crafts</li><li>Desert landscapes</li></ul>
<div class="tfoot"><span>From $X</span><span class="lnk">View Journey →</span></div></div></div>
<div><p>Каждый тур на сайте, в соцсетях и в предложениях описывается в одном порядке:</p>
<ol class="ol"><li><b>Маршрут</b> — города через стрелку, капитель, Teal</li><li><b>Длительность и формат</b> — DAYS · PRIVATE / SMALL GROUP / EXPERIENCE</li>
<li><b>Название</b> — Playfair, одно слово курсивом</li><li><b>3–5 впечатлений</b> — конкретные, не «удивительные»</li><li><b>Цена «от»</b> и ссылка «View Journey →»</li></ol>
<p class="small">Для B2B-предложений вместо цены «от» — «Net rates on request».</p></div></div>''', S, title='Карточка тура')

page(f'''{head('Email signature', 'Подпись в письмах')}
<div class="sig"><div style="width:34mm;color:var(--brown)">{H_LOGO}</div><div class="sig-t">
<div class="pf" style="font-size:13pt">Name Surname</div><div class="eb" style="margin:1mm 0 2mm">POSITION · XANAKA TRAVEL</div>
<div>WhatsApp +998 90 447 31 93 · name@xanaka.uz · xanaka.uz</div>
<div class="small" style="margin-top:2mm;color:var(--teal)">Experience Uzbekistan Differently.</div></div></div>
<ul class="ok" style="margin-top:8mm"><li>Только текст и логотип PNG 2× (ширина 140 px на экране), без баннеров и цитат</li><li>Шрифт письма — Arial/Helvetica (Manrope в письмах не гарантирован), цвет текста Brown</li>
<li>Строка слогана — на языке письма: EN или FR</li><li>Email и должность — у каждого сотрудника свои; телефон — общий WhatsApp или личный</li></ul>''', S, title='Подпись в email')

# ================================================================ PART V
part('V', 'Brand Applications', ['Визитка', 'Предложение и программа тура', 'Ваучер и приветственная карточка', 'Встреча, бейдж, бирка', 'Мерч', 'Список носителей'])
S = 'Applications'

page(f'''{head('Business card', 'Визитка · 90 × 50 мм')}
<div class="cards"><div class="bc front"><div style="width:42mm;color:var(--brown)">{S_LOGO}</div></div>
<div class="bc back"><div><div class="pf" style="font-size:12pt">Name Surname</div><div class="eb" style="font-size:5.5pt;margin-top:1mm">POSITION</div></div>
<div class="bc-c">WhatsApp +998 90 447 31 93<br>name@xanaka.uz<br>xanaka.uz</div><div class="bc-m">{MARK}</div></div></div>
<p class="small">Лицо: Ivory, вертикальный логотип по центру. Оборот: Ivory, имя Playfair, должность капителью, контакты Manrope 7 pt; знак в углу.
Бумага: плотный дизайнерский картон 350–400 г/м², матовый, тёплого белого оттенка. Опционально — конгрев знака.</p>''', S, title='Визитка')

page(f'''{head('Proposal &amp; itinerary', 'Предложение и программа тура · A4')}
<div class="docs">
<div class="doc"><div style="width:26mm;color:var(--brown)">{H_LOGO}</div>{ph(style="height:56mm;margin:7mm 0 5mm", cls="warm")}<div class="eb" style="font-size:5.5pt">PRIVATE JOURNEY · 8 DAYS</div><div class="pf" style="font-size:16pt;line-height:1.1">The Classic <em>Silk Road</em></div><div class="tiny">Prepared for M. &amp; Mme Laurent · May 2027</div></div>
<div class="doc"><div class="eb" style="font-size:5.5pt">DAY 3 · BUKHARA</div><div class="pf" style="font-size:12pt">Lunch with a <em>family</em></div><div class="rule" style="width:20px"></div>
<div class="tiny lines"><p>09:00 Walk through the old town with your guide</p><p>13:00 Lunch with the Karimov family</p><p>16:00 Free time at Lyabi-Hauz</p><p>Hotel: boutique hotel, old town</p></div>{ph(style="height:34mm;margin-top:4mm", cls="warm")}</div>
<div class="doc"><div class="eb" style="font-size:5.5pt">YOUR JOURNEY INCLUDES</div><div class="tiny lines"><p>Private guide (EN/FR)</p><p>All transfers &amp; Afrosiyob train</p><p>7 nights, breakfast</p><p>24/7 support</p></div><div class="rule" style="width:20px"></div><div class="eb" style="font-size:5.5pt">YOUR MANAGER</div><div class="tiny">Name Surname · WhatsApp</div><div class="docm">{MARK}</div></div>
</div>
<p class="small">Три шаблона по одной сетке: <b>Private</b> (имя гостя на обложке), <b>Small Group</b> (даты выездов), <b>MICE</b> (программа по часам, площадки, логистика). Поля 20 мм, текст 10/15 pt, один акцентный кадр в арке на документ.</p>''', S, title='Предложение и программа')

page(f'''{head('Voucher &amp; welcome card', 'Ваучер и приветственная карточка')}
<div class="cols2" style="align-items:start"><div><div class="vch"><div class="vch-l"><div style="width:24mm;color:var(--brown)">{H_LOGO}</div><div class="eb" style="font-size:5.5pt;margin-top:auto">SERVICE VOUCHER</div><div class="pf" style="font-size:12pt">No. XT-2027-0412</div></div>
<div class="vch-r tiny lines"><p><b>Guest:</b> M. &amp; Mme Laurent</p><p><b>Service:</b> Hotel, 2 nights, BB</p><p><b>Dates:</b> 12–14 May 2027</p><p><b>Emergency 24/7:</b> +998 90 447 31 93</p></div></div>
<div class="cap">Ваучер: A5 горизонтально или PDF, две колонки, номер досье крупно</div></div>
<div><div class="wc"><div style="width:14mm;margin:0 auto;color:var(--brown)">{MARK}</div><div class="pf" style="font-size:15pt;text-align:center;margin-top:4mm">Welcome to <em>Bukhara,</em><br>Marie &amp; Paul</div><div class="tiny" style="text-align:center;margin-top:3mm">Your guide Dilshod will meet you at 9:00 in the lobby.<br>Every traveller is our guest.</div></div>
<div class="cap" style="text-align:center">Приветственная карточка: 105 × 148 мм, в номере отеля, от руки дописывается имя</div></div></div>''', S, title='Ваучер и карточка')

page(f'''{head('On the ground', 'Встреча, бейдж гида, багажная бирка')}
<div class="ground">
<div><div class="sign"><div style="width:30mm;color:var(--ivory)">{H_LOGO}</div><div class="pf" style="font-size:24pt">M. &amp; Mme Laurent</div><div class="eb" style="color:var(--saffron);font-size:6pt">WELCOME TO UZBEKISTAN</div></div><div class="cap">Табличка для встречи: A3, Brown, имя гостя крупно</div></div>
<div><div class="badge"><div style="width:12mm;color:var(--brown)">{MARK_B}</div><div class="pf" style="font-size:12pt;margin-top:3mm">Dilshod</div><div class="eb" style="font-size:5pt">GUIDE · EN · FR</div></div><div class="cap">Бейдж гида: 54 × 86 мм, имя и языки</div></div>
<div><div class="tag-l"><div class="hole"></div><div style="width:12mm;color:var(--ivory)">{MARK_B}</div><div class="eb" style="color:var(--ivory);font-size:5pt;margin-top:3mm">XANAKA TRAVEL</div><div class="tiny" style="color:var(--ivory)">Name ·<br>Hotel ·</div></div><div class="cap">Багажная бирка: кожа или плотный картон, Teal или Brown</div></div>
</div>''', S, title='Встреча, бейдж, бирка')

page(f'''{head('Merchandise', 'Мерч')}
<div class="merch">
<div><div class="m tee"><div style="width:14mm;color:var(--brown)">{MARK_B}</div></div><span>Футболка: Ivory или Sand, знак на груди слева, 7 см, шелкография Brown</span></div>
<div><div class="m cap-i"><div style="width:9mm;color:var(--ivory)">{MARK_B}</div></div><span>Кепка: Brown, знак спереди, вышивка Ivory (только утолщённый знак)</span></div>
<div><div class="m note-i"><div style="width:22mm;color:var(--brown)">{S_LOGO}</div></div><span>Блокнот: обложка Sand, вертикальный логотип, тиснение</span></div>
<div><div class="m folder"><div style="width:24mm;color:var(--ivory)">{H_LOGO}</div></div><span>Папка для документов: Teal, горизонтальный логотип, внутри — программа и ваучеры</span></div>
</div>
<p class="small">Мерч — для гостей и команды. Минимум логотипов: один знак на изделие. Никаких слоганов на одежде, кроме Every traveller is our guest на подарочной коробке.</p>''', S, title='Мерч')

tps = [('Цифровые', ['Сайт', 'Instagram', 'Facebook', 'Email и подпись', 'WhatsApp-профиль и шаблоны ответов']),
       ('Продажи', ['Коммерческое предложение (Private / Small Group / MICE)', 'Программа тура', 'Презентация для партнёров и выставок', 'Стенд (ITB Berlin, IFTM Top Resa, WTM)']),
       ('В поездке', ['Ваучер', 'Приветственная карточка в отеле', 'Табличка для встречи', 'Бейдж гида', 'Багажная бирка', 'Брендинг автомобиля (знак на двери)']),
       ('Подарки и мерч', ['Футболка, кепка', 'Блокнот', 'Папка для документов', 'Подарочная коробка'])]
page(f'''{head('Touchpoints', 'Список носителей')}<div class="tps">{''.join(f'<div><div class="eb">{a}</div><ul class="ok">{"".join(f"<li>{x}</li>" for x in b)}</ul></div>' for a,b in tps)}</div>
<p class="small">Каждый новый носитель проверяем по чек-листу: логотип из файлов и с охранным полем · цвета из палитры · Playfair + Manrope · одно слово курсивом · люди в фото · текст по тону голоса.</p>''', S, title='Список носителей')

# ---------------------------------------------------------------- back cover
page(f'''<div class="back"><div style="width:70mm;color:var(--ivory)">{S_LOGO}</div>
<p class="pf" style="font-size:20pt;margin-top:12mm">Experience Uzbekistan <em>Differently.</em></p>
<p class="small" style="margin-top:6mm;color:var(--sand)">xanaka.uz · WhatsApp +998 90 447 31 93</p></div>''', cls='dark', num=False)

# ---------------------------------------------------------------- contents
rows = ''
for t, n, sec in TOC:
    if t.startswith('Part'):
        rows += f'<div class="toc-p"><span>{t}</span><span>{n:02d}</span></div>'
    else:
        rows += f'<div class="toc-r"><span>{t}</span><span>{n:02d}</span></div>'
toc = f'<section class="pg">{head("Contents", "Содержание")}<div class="toc">{rows}</div></section>'
pages[pages.index('__TOC__')] = toc

html = f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>Xanaka Travel Brand Book</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
out_html = os.path.join(HERE, 'brandbook.html')
open(out_html, 'w').write(html)
out_pdf = os.path.abspath(os.path.join(ROOT, 'Xanaka-Travel-Brandbook.pdf'))
subprocess.run([CHROME, '--headless', '--no-sandbox', '--disable-gpu', '--allow-file-access-from-files',
                '--no-pdf-header-footer', f'--print-to-pdf={out_pdf}', 'file://' + out_html],
               check=True, stderr=subprocess.DEVNULL)
print('pages:', len(pages), '->', out_pdf)
