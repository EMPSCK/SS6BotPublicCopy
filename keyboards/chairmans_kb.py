from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio
from queries import chairman_queries
import pymysql
import config
from chairman_moves import generation_logic

async def gen_list_comp(tg_id):
    list_comp_buttons = []

    competitions = await chairman_queries.get_list_comp(tg_id)
    for comp in competitions:
        b = InlineKeyboardButton(text=comp['compName'], callback_data=f"comp_{comp['compId']}")
        list_comp_buttons.append([b])
    list_comp_buttons.append([InlineKeyboardButton(text='Вернуться к меню', callback_data='back_to_chairman_menu')])

    return InlineKeyboardMarkup(inline_keyboard=list_comp_buttons)

confirm_choice_button = InlineKeyboardButton(text='Да', callback_data=f"confirm_choice")
confirm_choice_button1 = InlineKeyboardButton(text='Нет', callback_data=f"confirm_choice_back")
confirm_choice_kb = load_judges_kb = InlineKeyboardMarkup(inline_keyboard=[[confirm_choice_button, confirm_choice_button1]])

cancel_button = [InlineKeyboardButton(text="Завершить загрузку списка", callback_data='cancel_load')]
load_judges_kb = InlineKeyboardMarkup(inline_keyboard=[cancel_button])

edit_problem_judges_info = [InlineKeyboardButton(text="Редактировать информацию", callback_data='edit_problem_judges_info')]
judges_problem_kb = InlineKeyboardMarkup(inline_keyboard=[cancel_button, edit_problem_judges_info])

take_as_is = [InlineKeyboardButton(text="Отправить как есть", callback_data='take_as_is')]
enter_book_number = [InlineKeyboardButton(text="Ввести номер книжки", callback_data='enter_book_number')]
search_for_db = [InlineKeyboardButton(text="Поиск по общей бд", callback_data='search_for_db')]
do_gap = [InlineKeyboardButton(text="Удалить", callback_data='do_gap')]
choose_problem_jud_action_kb  = InlineKeyboardMarkup(inline_keyboard=[take_as_is, enter_book_number, search_for_db, do_gap, cancel_button])

take_as_is_1 = [InlineKeyboardButton(text="Отправить как есть", callback_data='take_as_is_1')]
take_as_is_2 = [InlineKeyboardButton(text="Действующая спорт категория", callback_data='real_sport_category')]
choose_problem_jud_action_kb_1 = InlineKeyboardMarkup(inline_keyboard=[take_as_is_2, take_as_is_1,do_gap ,cancel_button])

async def gen_similar_judges(jud):
    list_comp_buttons = []

    judges = await chairman_queries.get_similar_judges(jud)
    for jud in judges:
        list_comp_buttons.append([InlineKeyboardButton(text=jud['LastName'] + ' ' +  jud['FirstName'] + ' | ' + jud['City'], callback_data=f"jud_{jud['BookNumber']}")])
    list_comp_buttons.append([InlineKeyboardButton(text='Назад', callback_data='back_to_edit_jud')])
    return InlineKeyboardMarkup(inline_keyboard=list_comp_buttons)

book_number_button = [InlineKeyboardButton(text='Назад', callback_data='back_to_edit_jud')]
book_number_kb = InlineKeyboardMarkup(inline_keyboard=[book_number_button])


menu_button = [InlineKeyboardButton(text='Задать активное соревнование', callback_data='set_active_competition')]
menu_kb = InlineKeyboardMarkup(inline_keyboard=[menu_button])

list_jud_send_b1 = [InlineKeyboardButton(text='Подтвердить отправку', callback_data='send_list_anyway')]
list_jud_send_b2 = [InlineKeyboardButton(text='показать свободных судей', callback_data='show_free_judges')]
list_jud_send_kb = InlineKeyboardMarkup(inline_keyboard=[list_jud_send_b1, list_jud_send_b2])


to_edit_linlist = [InlineKeyboardButton(text="Редактировать по элементам", callback_data='to_edit_linlist')]
send_with_replace = [InlineKeyboardButton(text="Заменить", callback_data='send_with_replace')]
solve_problem_linjudges_kb = InlineKeyboardMarkup(inline_keyboard=[to_edit_linlist, send_with_replace])


send_id_to_admin_b = [InlineKeyboardButton(text="Отправить данные администратору", callback_data='send_id_to_admin')]
send_id_to_admin_kb = InlineKeyboardMarkup(inline_keyboard=[send_id_to_admin_b])

update_status_b = [InlineKeyboardButton(text="Обновить статус", callback_data='update_status')]
update_status_b_1 = [InlineKeyboardButton(text="Написать администратору", url='https://t.me/mitkrivich')]
update_status_kb = InlineKeyboardMarkup(inline_keyboard=[update_status_b, update_status_b_1])

edit_02_b = [InlineKeyboardButton(text="Редактировать", callback_data='edit_02')]
edit_02_kb = InlineKeyboardMarkup(inline_keyboard=[edit_02_b])


async def get_markup_EV(user_id, text):

    judges_replace = await chairman_queries.get_free_judges_for_wrong(user_id, text)
    if judges_replace == 'свободных судей нет':
        return 0

    sim_jud_buttons = []
    sjb5 = []
    for jud_rep in range(len(judges_replace)):
        i = jud_rep
        jud_rep = judges_replace[jud_rep]
        if jud_rep['City'] is None:
            k = 'не установлено'
        else:
            k = jud_rep['City']

        sjb5.append(InlineKeyboardButton(
            text=jud_rep['lastName'] + ' ' + jud_rep['firstName'] + ' | ' + k,
            callback_data=f"01jud_rep_{jud_rep['bookNumber']}_{jud_rep['lastName']}_{jud_rep['firstName']}"))

        if len(sjb5) % 2 == 0 or i == len(judges_replace) - 1:
            sim_jud_buttons.append(sjb5)
            sjb5 = []

    sim_jud_buttons.append(
        [InlineKeyboardButton(text='Завершить и отменить редактирование', callback_data='end_edit_02')])
    return sim_jud_buttons


generation_button_01 = InlineKeyboardButton(text="Отправить РСК", callback_data='send_generate_rsk')
generation_button_02 = InlineKeyboardButton(text="Перегенерировать", callback_data='regenerate_list')
generation_button_03 = [InlineKeyboardButton(text="Выйти из режима генерации", callback_data='end_generation_proces')]
generation_kb = InlineKeyboardMarkup(inline_keyboard=[[generation_button_01, generation_button_02], generation_button_03])

async def get_generation_kb(active_comp):
    mode = await chairman_queries.get_generation_mode(active_comp)
    if mode == 0:
        generation_button_01 = InlineKeyboardButton(text="Отправить РСК", callback_data='send_generate_rsk')
        generation_button_02 = InlineKeyboardButton(text="Перегенерировать", callback_data='regenerate_list')
        generation_button_03 = InlineKeyboardButton(text="Выйти из режима генерации", callback_data='end_generation_proces')
        generation_button_04 = InlineKeyboardButton(text="Редактировать", callback_data='edit_generation_result')
        generation_kb = InlineKeyboardMarkup(inline_keyboard=[[generation_button_01, generation_button_02], [generation_button_04, generation_button_03]])
        return generation_kb
    elif mode == 1:
        generation_button_01 = InlineKeyboardButton(text="Сохранить результат", callback_data='save_result')
        generation_button_02 = InlineKeyboardButton(text="Перегенерировать", callback_data='regenerate_list')
        generation_button_03 = InlineKeyboardButton(text="Выйти из режима генерации", callback_data='end_generation_proces')
        generation_button_04 = InlineKeyboardButton(text="Редактировать", callback_data='edit_generation_result')
        generation_kb = InlineKeyboardMarkup(inline_keyboard=[[generation_button_01, generation_button_02], [generation_button_04, generation_button_03]])
        return generation_kb

    elif mode == -1:
        return -1


async def get_gen_edit_markup(json):
    try:
        judges = json['judges']
        compid = json['compId']
        id_to_group = json['id_to_group']
        buttons = []
        but2 = []

        conn = pymysql.connect(
            host=config.host,
            port=3306,
            user=config.user,
            password=config.password,
            database=config.db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn:
            cur = conn.cursor()
            for i in judges:
                cur.execute(f"SELECT firstName, lastName FROM competition_judges WHERE compId = {compid} and id = {i}")
                ans = cur.fetchone()
                group = judges[i][0]
                but2.append(InlineKeyboardButton(text=ans['lastName'] + ' ' + ans['firstName'], callback_data=f"gen_choise_jud_01_{judges[i][1]}_{group}_{i}"))
                if len(but2) == 2:
                    buttons.append(but2)
                    but2 = []



        if len(but2) == 0:
            b = [InlineKeyboardButton(text='Назад', callback_data=f"back_to_generation")]
            buttons.append(b)
        else:
            but2.append(InlineKeyboardButton(text='Назад', callback_data=f"back_to_generation"))
            buttons.append(but2)

        return InlineKeyboardMarkup(inline_keyboard=buttons)
    except Exception as e:
        print(e)


async def edit_gen_judegs_markup(groupType, judgeId, judges, compId, json):
    try:
        buttons = []
        but2 = []
        conn = pymysql.connect(
            host=config.host,
            port=3306,
            user=config.user,
            password=config.password,
            database=config.db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

        with conn:
            cur = conn.cursor()
            cur.execute(f"SELECT firstName, lastName, id, DSFARR_Category_Id, SPORT_CategoryDate, SPORT_CategoryDateConfirm, SPORT_Category from competition_judges WHERE compId = {compId} and active = 1")
            all_judges = cur.fetchall()


            all_judges = await generation_logic.same_judges_filter(all_judges, list(judges.keys()))

            if groupType == 1:
                minCategoryId = await chairman_queries.get_min_catId(compId, judges[judgeId][0])
                all_judges = await generation_logic.category_filter(all_judges, minCategoryId, compId)


            if judges[judgeId][1] == 'l':
                lin_neibors_list = judges[judgeId][2].copy()
                lin_neibors_list.remove(judgeId)
                lin_neibors_clubs_list = await chairman_queries.get_lin_neibors_clubs(lin_neibors_list)
                all_judges = await generation_logic.distinct_clubs_filter(lin_neibors_clubs_list, all_judges)



            for j in range(len(all_judges)):
                but2.append(InlineKeyboardButton(text=f'{all_judges[j]["lastName"]} {all_judges[j]["firstName"]}',
                                                 callback_data=f'gen_choise_jud_02_{all_judges[j]["id"]}'))
                if j % 2 != 0:
                    buttons.append(but2)
                    but2 = []

            if len(but2) == 0:
                b = [InlineKeyboardButton(text='Назад', callback_data=f"back_to_generation")]
                buttons.append(b)
            else:
                but2.append(InlineKeyboardButton(text='Назад', callback_data=f"back_to_generation"))
                buttons.append(but2)

        return InlineKeyboardMarkup(inline_keyboard=buttons)

    except Exception as e:
        print(e)

