from datetime import datetime
from src.ttgdtparser.types import Change, Group


changes_expected = {
    "151": [
        Change(date=datetime(2025, 10, 3), index=2, discipline="История", room="310", by_base=False),
        Change(date=datetime(2025, 10, 2), index=2, discipline="Индивидуальный проект", room="308", by_base=False),
        Change(date=datetime(2025, 10, 2), index=4, discipline="Индивидуальный проект", room="308", by_base=False)
    ],
    "153": [
        Change(date=datetime(2025, 10, 3), index=2, discipline="Химия", room="400", by_base=False),
        Change(date=datetime(2025, 10, 3), index=3, discipline="Физкультура", room="", by_base=False),
        Change(date=datetime(2025, 10, 3), index=4, discipline="Индивидуальный проект", room="304", by_base=False),
        Change(date=datetime(2025, 10, 2), index=2, discipline="Химия", room="400", by_base=False),
        Change(date=datetime(2025, 10, 2), index=3, discipline="Физкультура", room="", by_base=False),
        Change(date=datetime(2025, 10, 2), index=4, discipline="Математика", room="604", by_base=False)
    ],
    "251-П,253-П": [
        Change(date=datetime(2025, 10, 3), index=2, discipline="Литература", room="611", by_base=False),
        Change(date=datetime(2025, 10, 3), index=3, discipline="Химия", room="400", by_base=False),
        Change(date=datetime(2025, 10, 3), index=4, discipline="Ин. язык", room="602.606", by_base=False),
        Change(date=datetime(2025, 10, 2), index=1, discipline="Физика", room="301", by_base=False),
        Change(date=datetime(2025, 10, 2), index=3, discipline="Математика", room="604", by_base=False)
    ],
    "351,353": [
        Change(date=datetime(2025, 10, 3), index=1, discipline="Математика", room="612", by_base=False),
        Change(date=datetime(2025, 10, 3), index=2, discipline="Русский язык", room="603", by_base=False),
        Change(date=datetime(2025, 10, 3), index=4, discipline="История", room="310", by_base=False)
    ],
    "551-П": [
        Change(date=datetime(2025, 10, 3), index=1, discipline="Информатика", room="107.305", by_base=False),
        Change(date=datetime(2025, 10, 3), index=2, discipline="Физика", room="500", by_base=False),
        Change(date=datetime(2025, 10, 3), index=4, discipline="Химия", room="400", by_base=False),
        Change(date=datetime(2025, 10, 2), index=1, discipline="Русский язык", room="603", by_base=False),
    ],
    "553,555": [
        Change(date=datetime(2025, 10, 3), index=1, discipline="Русский язык", room="603", by_base=False),
        Change(date=datetime(2025, 10, 2), index=4, discipline="Химия", room="400", by_base=False)
    ],
    "751,753": [
        Change(date=datetime(2025, 10, 3), index=1, discipline="Математика", room="206", by_base=False),
        Change(date=datetime(2025, 10, 3), index=2, discipline="География", room="309", by_base=False),
        Change(date=datetime(2025, 10, 3), index=4, discipline="География", room="309", by_base=False)
    ],
    "755,757": [
        Change(date=datetime(2025, 10, 3), index=1, discipline="География", room="309", by_base=False),
        Change(date=datetime(2025, 10, 3), index=2, discipline="Физика", room="301", by_base=False),
        Change(date=datetime(2025, 10, 3), index=3, discipline="География", room="309", by_base=False),
        Change(date=datetime(2025, 10, 3), index=4, discipline="Физика", room="301", by_base=False),
        Change(date=datetime(2025, 10, 2), index=1, discipline="Ин. язык", room="602,606", by_base=False)
    ],
    "851,853": [
        Change(date=datetime(2025, 10, 3), index=1, discipline="История", room="310", by_base=False),
        Change(date=datetime(2025, 10, 3), index=2, discipline="Математика", room="206", by_base=False),
        Change(date=datetime(2025, 10, 3), index=3, discipline="Информатика", room="107.305", by_base=False),
        Change(date=datetime(2025, 10, 2), index=3, discipline="Основы безоп-ти и защиты Родины", room="310", by_base=False)
    ],
    "951,953": [
        Change(date=datetime(2025, 10, 3), index=1, discipline="НЕТ", room="", by_base=False),
        Change(date=datetime(2025, 10, 3), index=2, discipline="По расписанию", room="208", by_base=True),
        Change(date=datetime(2025, 10, 3), index=3, discipline="Русский язык", room="603", by_base=False),
        Change(date=datetime(2025, 10, 3), index=[4, 5], discipline="Литература", room="603", by_base=False),
        Change(date=datetime(2025, 10, 2), index=3, discipline="Русский язык", room="603", by_base=False)
    ],
    "141,152": [
        Change(date=datetime(2025, 10, 3), index=2, discipline="Трансп. система России", room="304", by_base=False),
        Change(date=datetime(2025, 10, 3), index=3, discipline="История России", room="310", by_base=False),
        Change(date=datetime(2025, 10, 3), index=4, discipline="Физкультура", room="", by_base=False),
        Change(date=datetime(2025, 10, 2), index=3, discipline="Трансп. система России", room="304", by_base=False)
    ],
    "143,154": [
        Change(date=datetime(2025, 10, 3), index=1, discipline="История России", room="208", by_base=False),
        Change(date=datetime(2025, 10, 3), index=4, discipline="Инженерная графика", room="103", by_base=False),
        Change(date=datetime(2025, 10, 2), index=1, discipline="Трансп. система России", room="304", by_base=False)
    ],
    "241-П": [
        Change(date=datetime(2025, 10, 3), index=1, discipline="ОКЖД", room="405", by_base=False),
        Change(date=datetime(2025, 10, 3), index=4, discipline="БЖ: Бабенко Е.А.", room="202", by_base=False)
    ],
    "341,343,352": [
        Change(date=datetime(2025, 10, 3), index=1, discipline="Технол. монтажа эл.устр-в и систем", room="614", by_base=False),
        Change(date=datetime(2025, 10, 2), index=2, discipline="Основы эл. и выч. техники", room="614", by_base=False),
        Change(date=datetime(2025, 10, 2), index=4, discipline="Ин. язык", room="602,606", by_base=False)
    ],
    "541-П": [
        Change(date=datetime(2025, 10, 3), index=0, discipline="НЕТ", room="", by_base=False),
        Change(date=datetime(2025, 10, 3), index=1, discipline="Метрология", room="500", by_base=False),
        Change(date=datetime(2025, 10, 3), index=2, discipline="Ин. язык", room="602", by_base=False),
        Change(date=datetime(2025, 10, 3), index=4, discipline="Физкультура", room="", by_base=False),

        Change(date=datetime(2025, 10, 2), index=1, discipline="НЕТ", room="", by_base=False),
        Change(date=datetime(2025, 10, 2), index=[2, 3], discipline="По расписанию", room="", by_base=True),
        Change(date=datetime(2025, 10, 2), index=4, discipline="Техническая механика", room="503", by_base=False),
    ],
    "543,552": [
        Change(date=datetime(2025, 10, 3), index=2, discipline="Прикладная математика", room="612", by_base=False),
        Change(date=datetime(2025, 10, 3), index=4, discipline="Прикладная математика", room="612", by_base=False),
        Change(date=datetime(2025, 10, 2), index=1, discipline="ОКЖД", room="503", by_base=False),
        Change(date=datetime(2025, 10, 2), index=3, discipline="Техническая механика", room="503", by_base=False),
        Change(date=datetime(2025, 10, 2), index=4, discipline="Прикладная математика", room="612", by_base=False)
    ],
    "741": [
        Change(date=datetime(2025, 10, 3), index=1, discipline="Основы алгоритмизации", room="102", by_base=False),
        Change(date=datetime(2025, 10, 3), index=3, discipline="Проектир. и разр. интерф.польз.", room="307", by_base=False),
        Change(date=datetime(2025, 10, 3), index=4, discipline="История", room="208", by_base=False),
        Change(date=datetime(2025, 10, 2), index=2, discipline="Основы алгоритмизации", room="102", by_base=False)
    ],
    "743,752": [
        Change(date=datetime(2025, 10, 3), index=1, discipline="Ин. язык", room="606", by_base=False),
        Change(date=datetime(2025, 10, 3), index=[2, 3], discipline="Основы алгоритмизации", room="102", by_base=False),
        Change(date=datetime(2025, 10, 3), index=4, discipline="Проектир. и разр. интерф.польз.", room="307", by_base=False),
        Change(date=datetime(2025, 10, 2), index=1, discipline="НЕТ", room="", by_base=False),
        Change(date=datetime(2025, 10, 2), index=2, discipline="По расписанию", room="", by_base=True),
        Change(date=datetime(2025, 10, 2), index=3, discipline="Основы алгоритмизации", room="102", by_base=False),
        Change(date=datetime(2025, 10, 2), index=4, discipline="Элементы высшей математики", room="206", by_base=False)
    ],
    "841,843,852": [
        Change(date=datetime(2025, 10, 3), index=1, discipline="НЕТ", room="", by_base=False),
        Change(date=datetime(2025, 10, 3), index=2, discipline="Трансп. сист. России и тр. геогр.", room="305", by_base=False),
        Change(date=datetime(2025, 10, 3), index=[4, 5], discipline="Трансп. сист. России и тр. геогр.", room="305", by_base=False),
        
        Change(date=datetime(2025, 10, 2), index=1, discipline="Технология бронирования", room="202", by_base=False),
        Change(date=datetime(2025, 10, 2), index=2, discipline="Технология бронирования", room="310", by_base=False),
        Change(date=datetime(2025, 10, 2), index=4, discipline="Трансп. сист. России и тр. геогр.", room="305", by_base=False)
    ],
    "941,952": [
        Change(date=datetime(2025, 10, 3), index=2, discipline="Ин. язык", room="201-а,606", by_base=False),
        Change(date=datetime(2025, 10, 3), index=[3, 4], discipline="Охрана труда", room="406", by_base=False),
        
        Change(date=datetime(2025, 10, 2), index=1, discipline="НЕТ", room="", by_base=False),
        Change(date=datetime(2025, 10, 2), index=2, discipline="Техническая механика", room="502", by_base=False),
        Change(date=datetime(2025, 10, 2), index=[3, 4], discipline="Технологич. проц. в машиностроении", room="208", by_base=False),
    ],
    "131,135,142": [
        Change(date=datetime(2025, 10, 3), index=2, discipline="ТЭ и БД", room="409", by_base=False),
        Change(date=datetime(2025, 10, 3), index=[3, 4], discipline="Психология общения", room="401", by_base=False),
        
        Change(date=datetime(2025, 10, 2), index=2, discipline="ТЭ и БД", room="409", by_base=False),
        Change(date=datetime(2025, 10, 2), index=3, discipline="Инф. обеспеч. перевозочн.проц.", room="308", by_base=False),
        Change(date=datetime(2025, 10, 2), index=4, discipline="СРД: 2-ая подгруппа", room="409", by_base=False)
    ],
    "231-П": [
        Change(date=datetime(2025, 10, 3), index=2, discipline="Вып-е раб. по проф. \"Монтер пути\"", room="300", by_base=False),
        Change(date=datetime(2025, 10, 2), index=4, discipline="ЦСХ", room="500", by_base=False)
    ],
    "331": [
        Change(date=datetime(2025, 10, 3), index=1, discipline="НЕТ", room="", by_base=False),
        Change(date=datetime(2025, 10, 3), index=2, discipline="Осн.постр.и ТЭ МКСП:Кабанова А.А.", room="614", by_base=False),
        Change(date=datetime(2025, 10, 3), index=4, discipline="Теория электросвязи", room="609", by_base=False),

        Change(date=datetime(2025, 10, 2), index=[3, 4], discipline="Теор. основы монтажа: Гирякова Ю.Л.", room="609", by_base=False),
    ],
    "531-П": [
        Change(date=datetime(2025, 10, 3), index=[1, 2], discipline="БЖ: Немтинов В.П.", room="613", by_base=False),
        Change(date=datetime(2025, 10, 3), index=3, discipline="По расписанию", room="300", by_base=True),

        Change(date=datetime(2025, 10, 2), index=1, discipline="НЕТ", room="", by_base=False),
        Change(date=datetime(2025, 10, 2), index=2, discipline="По расписанию", room="309", by_base=True),
        Change(date=datetime(2025, 10, 2), index=[3, 4], discipline="БЖ: Немтинов В.П.", room="613", by_base=False),
    ],
    "535": [
        Change(date=datetime(2025, 10, 3), index=1, discipline="БЖ: Бабенко Е.А. (вся группа)", room="202", by_base=False),
        Change(date=datetime(2025, 10, 3), index=[3, 4], discipline="Изыскания", room="500", by_base=False),
        Change(date=datetime(2025, 10, 2), index=2, discipline="Устройство жд пути", room="503", by_base=False),
        Change(date=datetime(2025, 10, 2), index=3, discipline="Изыскания", room="500", by_base=False),
        Change(date=datetime(2025, 10, 2), index=4, discipline="Классный час", room="103", by_base=False)
    ],
    "731,733,742": [
        Change(date=datetime(2025, 10, 3), index=2, discipline="Численные методы", room="604", by_base=False),
        Change(date=datetime(2025, 10, 3), index=4, discipline="Проектир. и разр. веб-приложений", room="102", by_base=False),
        
        Change(date=datetime(2025, 10, 2), index=1, discipline="Проектир. и разр. веб-приложений", room="102", by_base=False),
        Change(date=datetime(2025, 10, 2), index=2, discipline="Ин. язык", room="602.606", by_base=False),
        Change(date=datetime(2025, 10, 2), index=3, discipline="Физкультура", room="", by_base=False)
    ],
    "735,737": [
        Change(date=datetime(2025, 10, 3), index=[1, 2], discipline="НЕТ", room="", by_base=False),
        Change(date=datetime(2025, 10, 3), index=[3, 4], discipline="Численные методы", room="604", by_base=False),
        Change(date=datetime(2025, 10, 3), index=5, discipline="Проектирование и дизайн ИС", room="307", by_base=False),
        Change(date=datetime(2025, 10, 2), index="8.00", discipline="УП.09: 2-ая подгруппа", room="307", by_base=False),
        Change(date=datetime(2025, 10, 2), index="11.30", discipline="УП.09: 1-ая подгруппа", room="307", by_base=False)
    ],
    "831,833,842": [
        Change(date=datetime(2025, 10, 3), index=2, discipline="Организация сервиса", room="202", by_base=False),

        Change(date=datetime(2025, 10, 2), index=1, discipline="Орг-ция безоп-ти на жд трансп.:2-ая подгр.", room="400", by_base=False),
        Change(date=datetime(2025, 10, 2), index=2, discipline="Специальные технологии", room="202", by_base=False),
        Change(date=datetime(2025, 10, 2), index=3, discipline="Основы финанс. грамотности", room="202", by_base=False),
        Change(date=datetime(2025, 10, 2), index=4, discipline="Организация сервиса", room="202", by_base=False)
    ],
    "931": [
        Change(date=datetime(2025, 10, 3), index="8.00", discipline="Технол.сварочных работ (8 часов)", room="504", by_base=False),
        Change(date=datetime(2025, 10, 2), index=1, discipline="НЕТ", room="", by_base=False),
        Change(date=datetime(2025, 10, 2), index=[2, 3, 4, 5], discipline="Технология сварочных работ", room="504", by_base=False),
    ],
    "321": [
        Change(date=datetime(2025, 10, 3), index=[1, 2], discipline="НЕТ", room="", by_base=False),
        Change(date=datetime(2025, 10, 3), index=3, discipline="По расписанию", room="601", by_base=True),
        Change(date=datetime(2025, 10, 3), index=[4, 5], discipline="Современные системы связи", room="614", by_base=False),

        Change(date=datetime(2025, 10, 2), index=1, discipline="НЕТ", room="", by_base=False),
        Change(date=datetime(2025, 10, 2), index=[2, 3], discipline="По расписанию", room="", by_base=True),
        Change(date=datetime(2025, 10, 2), index=[4, 5], discipline="Современные системы связи", room="614", by_base=False),
    ]
}


all_groups = [
    Group(number='121,123,132'),
    Group(number='131,135,142'),
    Group(number='141,152'),
    Group(number='143,154'),
    Group(number='151'),
    Group(number='153'),
    Group(number='221-П,232-П'),
    Group(number='231-П'),
    Group(number='241-П'),
    Group(number='251-П,253-П'),
    Group(number='321'),
    Group(number='331'),
    Group(number='341,343,352'),
    Group(number='351,353'),
    Group(number='523'),
    Group(number='531-П'),
    Group(number='535'),
    Group(number='541-П'),
    Group(number='543,552'),
    Group(number='551-П'),
    Group(number='553,555'),
    Group(number='721,732'),
    Group(number='725,734'),
    Group(number='731,733,742'),
    Group(number='735,737'),
    Group(number='741'),
    Group(number='743,752'),
    Group(number='751,753'),
    Group(number='755,757'),
    Group(number='831,833,842'),
    Group(number='841,843,852'),
    Group(number='851,853'),
    Group(number='921'),
    Group(number='931'),
    Group(number='941,952'),
    Group(number='951,953')
]