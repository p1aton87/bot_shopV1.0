from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from dbscript import all_information, check, add_user, delete_no_payed_items, update_users, check_all_items
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from global_bot import bot
import data_token


class Unique_Id(StatesGroup):
    state_for_buy_item = State()


router = Router()


kb1 = [
    [KeyboardButton(text='Купить товар')],
    [KeyboardButton(text='Мои заказы')],
    [KeyboardButton(text='Каталог')],
    [KeyboardButton(text='Обратная связь')]
]
kb2 = [
    [KeyboardButton(text='Меню')]
]
keyboard1 = ReplyKeyboardMarkup(keyboard=kb1, resize_keyboard=True)
keyboard2 = ReplyKeyboardMarkup(keyboard=kb2, resize_keyboard=True)


@router.message(F.text == 'Каталог')
async def catalog(message: types.Message):
    for i in all_information:
        await message.answer(f'Артикул: {i[0]} {i[2]}')


@router.message(F.text == 'Купить товар')
async def buy_item(message: types.Message, state: FSMContext):
    await message.answer('Хорошо, введите артикул предмета и бот сразу сделает меню оплаты', reply_markup=ReplyKeyboardRemove())
    await state.set_state(Unique_Id.state_for_buy_item)


@router.message(F.text == 'Обратная связь')
async def links_admins(message: types.Message):
    await message.answer('Если вас интересуют какие-то вопросы или имеется проблема, напишите в телеграмм по этому номеру: +88800000000')


@router.message(F.text == 'Мои заказы')
async def my_buy(message: types.Message):
    orders = check_all_items(message.from_user.id)
    await message.answer('Ваши заказы:')
    for i in orders:
        await message.answer(f'Артикул заказа: {i[2]} \nСтатус: {i[3]}')


@router.message(F.text == 'Меню')
async def menu(message: types.Message):
    await message.answer('Возврат в меню', reply_markup=keyboard1)


@router.message(Unique_Id.state_for_buy_item)
async def buy_item1(message: types.Message, state: FSMContext):
    try:
        add_user(message.from_user.id, message.from_user.full_name, message.text)
        PRICE = types.LabeledPrice(label='Покупка товара', amount=check(message.text, 2) * 100)
        await bot.send_invoice(message.chat.id,
                             title=check(message.text, 0),
                             description=check(message.text, 1),
                             provider_token=data_token.PAY_TOKEN,
                             currency='rub',
                             is_flexible=False,
                             prices=[PRICE],
                             start_parameter="buy-item",
                             payload="test-invoice-payload")
        await state.clear()
    except TypeError:
        await message.answer('ОШИБКА: введен неверный артикул', reply_markup=keyboard2)


@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: types.Message):
    update_users(message.from_user.id)
    delete_no_payed_items(message.from_user.id)
    await message.answer('Оплата прошла успешна, наш оператор в скором времени свяжеться с вами', reply_markup=keyboard2)


@router.message()
async def none(message: types.Message):
    await message.answer('Не знаю такой команды', reply_markup=keyboard2)


