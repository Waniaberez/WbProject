from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup, InlineKeyboardButton

btnUs = KeyboardButton("Профиль")
btnReviewPol = KeyboardButton('Ответ на положительные отзывы')
btnReviewCheck = KeyboardButton('Отправить отзывы на проверку')
btnReviewBad = KeyboardButton('Ответить на негативные отзывы')
btnInf = KeyboardButton('Информация про бота')


mainMenu = ReplyKeyboardMarkup(resize_keyboard=True)
mainMenu.add(btnInf)
mainMenu.insert(btnReviewBad)
mainMenu.add(btnReviewCheck)
mainMenu.insert(btnReviewPol)
mainMenu.add(btnUs)