from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import types
import config
from queries import get_user_status_query
from queries import general_queries
from keyboards import chairmans_kb
from keyboards import scrutineer_kb
from keyboards import admins_kb
from queries import chairman_queries
from aiogram.fsm.context import FSMContext
from admin_moves import update_fttsar_judges
from aiogram.fsm.state import StatesGroup, State
from queries import scrutineer_queries
router = Router()
enter_pin_messages = {}


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await message.delete()
    await state.clear()
    text, status = await get_mes_menu(message)
    if status == 0:
        await message.answer(text, reply_markup=scrutineer_kb.scrutiner_chairman_mark)
    if status == 1:
        await message.answer(text, reply_markup=admins_kb.menu_kb)
    if status == 2:
        await message.answer(text, reply_markup=scrutineer_kb.menu_kb)
    if status == 3:
        await message.answer(text, reply_markup=chairmans_kb.menu_kb)

@router.message(Command("id"))
async def cmd_start(message: Message, state: FSMContext):
    await message.delete()
    await message.answer(f'🗓Telegram_id: <code>{message.from_user.id}</code>', parse_mode='HTML')




@router.callback_query(F.data == 'scrutiner_role')
async def cmd_start(callback: types.CallbackQuery):
    await callback.message.edit_text(f"🗓Telegram_id: <code>{callback.from_user.id}</code>\n\nИнструкция №1", reply_markup=scrutineer_kb.back_mark, parse_mode='HTML')


@router.callback_query(F.data == 'chairman_role')
async def cmd_start(callback: types.CallbackQuery):
    await callback.message.edit_text(f'🗓Telegram_id: <code>{callback.from_user.id}</code>\n\nИнструкция №2', reply_markup=scrutineer_kb.chairman_reg_mark, parse_mode='HTML')
    pass


class Chairman_reg_states(StatesGroup):
    firstState = State()

@router.callback_query(F.data == 'enter_chairaman_pin')
async def cmd_start(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text('Введите код: ', reply_markup=scrutineer_kb.back_mark)
    enter_pin_messages[callback.from_user.id] = callback.message
    await state.set_state(Chairman_reg_states.firstState)

@router.message(Chairman_reg_states.firstState)
async def f2(message: Message, state: FSMContext):
    oldmessage = enter_pin_messages[message.from_user.id]
    try:
        pin = message.text
        if pin.isdigit():
            status = await scrutineer_queries.check_chairman_pin(message.from_user.id, int(pin), 0)
            if status == -1:
                await message.delete()
                await oldmessage.edit_text('❌Ошибка', reply_markup=scrutineer_kb.back_mark)

            if status == 1:
                text, userstatus = await get_mes_menu(message)
                await message.delete()
                if userstatus == 3:
                    await oldmessage.edit_text(text, reply_markup=chairmans_kb.menu_kb)
                    await state.clear()

            if status == 0:
                await message.delete()
                await oldmessage.edit_text('❌Ошибка. Пинкод не найден.', reply_markup=scrutineer_kb.back_mark)
        else:
            await message.delete()
            await oldmessage.edit_text('❌Ошибка. Неправильный формат пинкода.', reply_markup=scrutineer_kb.back_mark)
    except:
        pass

@router.callback_query(F.data == 'back_b')
async def cmd_start(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    text, status = await get_cal_menu(callback)
    if status == 0:
        await callback.message.edit_text(text, reply_markup=scrutineer_kb.scrutiner_chairman_mark)
    if status == 1:
        await callback.message.edit_text(text, reply_markup=admins_kb.menu_kb)
    if status == 2:
        await callback.message.edit_text(text, reply_markup=scrutineer_kb.menu_kb)
    if status == 3:
        await callback.message.edit_text(text, reply_markup=chairmans_kb.menu_kb)


@router.message(Command("updateftsarrlist"))
async def update_ftsarr_judges_list(message: types.Message):
    access = [6887839538, 834140698, 363846616, 5824158064]
    if message.from_user.id in access:
        await message.answer('Запущен процесс обновления данных\nПримерное время ожидания: 5 мин.')
        status = await update_fttsar_judges.update_judges_list()
        if status == 1:
            await message.answer('Процесс обновления данных завершен')
        else:
            await message.answer('❌Ошибка')


@router.message(Command("help"))
async def update_ftsarr_judges_list(message: types.Message):
    text = '''<b>Список команд:</b>\n/id - получить telegram_id, chairman/scrutineer\n\n/judges - начать загрузку списка судей, chairman/scrutineer\n\n/clean - удалить загруженных внутри соревнования, chairman/scrutineer\n\n/free - показать свободных после отправки последнего списка, chairman/scrutineer\n\n/updateftsarrlist - обновить общий список судей, Митя1/Митя2/Артем1/Артем2\n\n/delactive - снести активность всем судьям внутри соревнования, chairman/scrutineer\n\n/cleancounter - обнулить счетчик судейств в группах, chairman/scrutineer\n\n/change_generation_mode - изменить режим генерации списков в активном соревновании, chairman/scrutineer'''
    await message.answer(text, parse_mode='HTML')


async def get_cal_menu(callback: types.CallbackQuery):
    user_status = await get_user_status_query.get_user_status(callback.from_user.id)
    # Админ
    if user_status == 1:
        await callback.message.answer('👋Добро пожаловать в admin интерфейс бота SS6', reply_markup=admins_kb.menu_kb)
        return '👋Добро пожаловать в admin интерфейс бота SS6', 1

    # scrutinner
    if user_status == 2:
        active_comp = await general_queries.get_CompId(callback.message.from_user.id)
        if await chairman_queries.del_unactive_comp(callback.message.from_user.id, active_comp) == 1:
            active_comp = None
        info = await general_queries.CompId_to_name(active_comp)
        return f"👋Добро пожаловать в scrutineer интерфейс бота SS6\n\n/help - список всех команд\nАктивное соревнование: {info}", 2

    # chairman
    if user_status == 3:
        active_comp = await general_queries.get_CompId(callback.message.from_user.id)
        if await chairman_queries.del_unactive_comp(callback.message.from_user.id, active_comp) == 1:
            active_comp = None
        info = await general_queries.CompId_to_name(active_comp)
        return f"👋Добро пожаловать в scrutineer интерфейс бота SS6\n\n/help - список всех команд\nАктивное соревнование: {info}", 3

    if user_status == 0:
        return "👋Добро пожаловать в интерфейс бота SS6\n\nДля начала работы необходимо пройти регистрацию в системе\nВыберите роль:", 0

async def get_mes_menu(message: Message):
    user_status = await get_user_status_query.get_user_status(message.from_user.id)
    #Админ
    if user_status == 1:
        return '👋Добро пожаловать в admin интерфейс бота SS6', user_status

    #scrutinner
    if user_status == 2:
        active_comp = await general_queries.get_CompId(message.from_user.id)
        if await chairman_queries.del_unactive_comp(message.from_user.id, active_comp) == 1:
            active_comp = None
        info = await general_queries.CompId_to_name(active_comp)
        return f"👋Добро пожаловать в scrutineer интерфейс бота SS6\n\n/help - список всех команд\nАктивное соревнование: {info}", user_status
    #chairman
    if user_status == 3:
        active_comp = await general_queries.get_CompId(message.from_user.id)
        if await chairman_queries.del_unactive_comp(message.from_user.id, active_comp) == 1:
            active_comp = None
        info = await general_queries.CompId_to_name(active_comp)
        return f"👋Добро пожаловать в chairman интерфейс бота SS6\n\n/judges - отправить список судей\n/help - список всех команд\nАктивное соревнование: {info}", 3
    if user_status == 0:
        return "👋Добро пожаловать в интерфейс бота SS6\n\nДля начала работы необходимо пройти регистрацию в системе\nВыберите роль:", 0


