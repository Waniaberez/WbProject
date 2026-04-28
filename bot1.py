import logging
from aiogram import Bot, Dispatcher, executor, types
import markup as nav
from db import Database
import requests
import json
import openai
import datetime
from dateutil import parser


token_api=("")
openai.api_key = ''
bot = Bot(token_api)
dp = Dispatcher(bot)
db = Database('DataBase1.db')
url = "https://seller.wildberries.ru/ns/api/suppliers-portal-feedbacks-questions/api/v1/feedbacks"
logging.basicConfig(level=logging.INFO)

pol = 0
otr = 0
jal = 0


@dp.message_handler(commands=['start'])
async def send_greet(message: types.Message):
    if(not db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id)
        date1 = datetime.datetime.now().date()
        db.set_date_now(message.from_user.id, date1)
        db.set_time_sub(message.from_user.id, datetime.datetime.now().date() + datetime.timedelta(1))
        await bot.send_message(message.from_user.id, "Укажите номер телефона в формате 79000000000")
    else:
        await bot.send_message(message.from_user.id, "Вы зарегистрированы!")

@dp.message_handler()
async def bot_message(message: types.Message):
    rt1 = parser.parse(db.get_time_sub(message.from_user.id))
    rt2 = db.get_otz_count(message.from_user.id)
    if message.chat.type == 'private':
        if message.text == "Профиль":
            if int(rt2) < 0:
                await message.reply("У вас не осталось отзывов")
            else:
                await message.reply(f"У вас осталось {rt2} отзывов")
        if message.text == "Информация про бота":
            await message.answer(
                text="Привествую Вас в данном боте. Бот позволяет автоматически отвечать на положительные отзывы с помощью нейросети ChatGPT.\n"
                     "Также бот позволяет отправить жалобы на сомнительные отзывы и написать ответы на негативные отзывы.\n"
                     "При регистрации Вам даётся 30 бесплатных отзывов на то, чтобы опробовать бота. Подписку вы можете приобрести у @deep_dark_master.\n"
                     "В отличие от других данный бот имеет подписочную систему - то есть вы можете пользоваться им, пока подписка активна.\n"
                     "Если вы заметите какие-либо баги, вылеты, ошибки и т.д - просьба написать сюда -> @deep_dark_master.\n",
                reply_markup=nav.mainMenu)
        if (int(rt2) > 0):
            if message.text == "Ответ на положительные отзывы":
                params1 = {
                    'isAnswered': 'False',
                    'order': 'dateDesc',
                    'skip': '1',
                    'take': '10'}
                lk1 = json.dumps(params1)
                rg1 = json.loads(lk1)
                rm1 = rg1["take"]
                rm1 = int(rm1)
                headers_get1 = {"Cookie": 'WBToken='+db.get_auth_token(message.from_user.id)+'; x-supplier-id='+db.get_supplier(message.from_user.id),
                    "User-Agent": "PostmanRuntime/7.31.1",
                    "Accept": "*/*",
                    "Content-Type": "application/json",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive"}
                response_get1 = requests.get("https://seller.wildberries.ru/ns/api/suppliers-portal-feedbacks-questions/api/v1/feedbacks", params=params1, headers=headers_get1)
                rq1 = json.dumps(response_get1.json())
                lf1 = json.loads(rq1)
                data_feedback1 = lf1["data"]
                feedbacks1 = data_feedback1["feedbacks"]
                for i1 in feedbacks1:
                    global pol
                    if (i1.setdefault("productValuation")) > 3 and (i1.setdefault('isCreationSupplierComplaint')) == True:
                            # product_type = dict_goods.get(i.setdefault("nmId"))
                        url = "https://api.writesonic.com/v2/business/content/chatsonic?engine=premium"
                        payload = {"enable_google_results": "false",
                                       "enable_memory": False,
                                       "input_text":"Перефразируй отзыв: Мы очень рады, что Вы оценили наш товар положительно. "
                                                    "Не забудьте добавить наш бренд в избранное и будьте в курсе наших новинок. "
                                                    "Будем рады видеть Вас снова!",}
                        headers = {"accept": "application/json",
                                       "content-type": "application/json",
                                       "X-API-KEY": ""}
                        response = requests.post(url, json=payload, headers=headers)
                        dump = json.dumps(response.json())
                        load = json.loads(dump)
                        text1 = load["message"]

                        cookies = {'WBToken': db.get_auth_token(message.from_user.id),
                                                       'x-supplier-id': db.get_supplier(message.from_user.id),
                                                       'locate': 'ru'}

                        loadpay_feedback1 = json.dumps({"id": i1.setdefault('id'), "text": text1})
                        headers_patch1 = {'Content-Type': 'application/json', "User-Agent": "PostmanRuntime/7.31.1",
                                                "Cookie": 'WBToken=' + db.get_auth_token(message.from_user.id) + '; x-supplier-id=' + db.get_supplier(message.from_user.id)}
                        url1 = "https://seller.wildberries.ru/ns/api/suppliers-portal-feedbacks-questions/api/v1/feedbacks"
                        requests.request("PATCH", url1, headers=headers_patch1, data=loadpay_feedback1)
                        pol += 1
                        print(i1.setdefault('text'))
                        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                db.set_otz_count(message.from_user.id, int(db.get_otz_count(message.from_user.id)) - pol)
                await message.reply(text=f"Отвечено на {pol} положительных отзывов", reply_markup=nav.mainMenu)

            if message.text == "Отправить отзывы на проверку":
                params2 = {
                        'isAnswered': 'False',
                        'order': 'dateDesc',
                        'skip': '1',
                        'take': '1000'}
                lk2 = json.dumps(params2)
                rg2 = json.loads(lk2)
                rm2 = rg2["take"]
                rm2 = int(rm2)
                headers_get2 = {"Cookie": 'WBToken=' + db.get_auth_token(message.from_user.id) + '; x-supplier-id=' + db.get_supplier(message.from_user.id),
                                   "User-Agent": "PostmanRuntime/7.31.1",
                                   "Accept": "*/*",
                                   "Content-Type": "application/json",
                                   "Accept-Encoding": "gzip, deflate, br",
                                   "Connection": "keep-alive"}
                response_get2= requests.get("https://seller.wildberries.ru/ns/api/suppliers-portal-feedbacks-questions/api/v1/feedbacks", params=params2, headers=headers_get2)
                rq2 = json.dumps(response_get2.json())
                lf2 = json.loads(rq2)
                data_feedback2 = lf2["data"]
                feedbacks2 = data_feedback2["feedbacks"]
                for i2 in feedbacks2:
                    global jal
                    if (i2.setdefault("productValuation")) < 4 and (i2.setdefault('isCreationSupplierComplaint')) == True:
                            payload2 = json.dumps({"id": i2.setdefault('id'), "createSupplierComplaint": True})
                            headers_patch2 = {
                                        'Content-Type': 'application/json',
                                        "User-Agent": "PostmanRuntime/7.31.1",
                                        "Cookie": 'WBToken=' + db.get_auth_token(message.from_user.id) + '; x-supplier-id=' + db.get_supplier(message.from_user.id)}
                            url2 = "https://seller.wildberries.ru/ns/api/suppliers-portal-feedbacks-questions/api/v1/feedbacks"
                            requests.request("PATCH", url2, headers=headers_patch2, data=payload2)
                            jal+=1
                            print(i2.setdefault('text'))
                            print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                db.set_otz_count(message.from_user.id, int(db.get_otz_count(message.from_user.id)) - jal)
                await message.reply(text=f'Отправлено {jal} жалоб', reply_markup=nav.mainMenu)

            if message.text =='Ответить на негативные отзывы':
                params3 = {
                        'isAnswered': 'False',
                        'order': 'dateDesc',
                        'skip': '1',
                        'take': '35'}
                lk3 = json.dumps(params3)
                rg3 = json.loads(lk3)
                rm3 = rg3["take"]
                rm3 = int(rm3)
                headers_get3 = {"Cookie": 'WBToken='+db.get_auth_token(message.from_user.id)+'; x-supplier-id='+db.get_supplier(message.from_user.id),
                    "User-Agent": "PostmanRuntime/7.31.1",
                    "Accept": "*/*",
                    "Content-Type": "application/json",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive"}
                cookies3 = {'WBToken': db.get_auth_token(message.from_user.id), 'x-supplier-id': db.get_supplier(message.from_user.id), 'locate': 'ru'}
                response_get3 = requests.get("https://seller.wildberries.ru/ns/api/suppliers-portal-feedbacks-questions/api/v1/feedbacks",
                        params=params3, cookies=cookies3, headers=headers_get3)
                rq3 = json.dumps(response_get3.json())
                lf3= json.loads(rq3)
                data_feedback3 = lf3["data"]
                feedbacks3 = data_feedback3["feedbacks"]
                for i3 in feedbacks3:
                    global otr
                    if (i3.setdefault('supplierComplaint')) != None:
                            dict_badreview3 = (i3.setdefault("supplierComplaint"))
                            status3 = (dict_badreview3.get("state"))
                            text_review3 = i3.setdefault('text')
                            headers_patch3 = {
                                    'Content-Type': 'application/json',
                                    "User-Agent": "PostmanRuntime/7.31.1",
                                    "Cookie": 'WBToken=' + db.get_auth_token(message.from_user.id) + '; x-supplier-id=' + db.get_supplier(message.from_user.id)}
                            if status3 == "rejected":

                                url = "https://api.writesonic.com/v2/business/content/chatsonic?engine=premium"
                                payload = {"enable_google_results": "false",
                                               "enable_memory": False,
                                               "input_text":"Перефразируй отзыв и Не используй слово удовлетворение: Извините, что Вы остались недовольны. "
                                                            "Мы всегда стремимся обеспечить наилучший уровень обслуживания нашим клиентам."
                                                            "Спасибо за Ваше время. "}
                                headers = {"accept": "application/json",
                                               "content-type": "application/json",
                                               "X-API-KEY": ""}
                                response = requests.post(url, json=payload, headers=headers)
                                dump = json.dumps(response.json())
                                load = json.loads(dump)
                                text1 = load["message"]

                                loadpay_feedback3 = json.dumps({"id": i3.setdefault('id'), "text": text1})
                                url3 = "https://seller.wildberries.ru/ns/api/suppliers-portal-feedbacks-questions/api/v1/feedbacks"
                                response_patch3 = requests.request("PATCH", url3, headers=headers_patch3, data=loadpay_feedback3)
                                otr+=1
                                print(i3.setdefault('text'))
                                print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                db.set_otz_count(message.from_user.id, int(db.get_otz_count(message.from_user.id))-otr)
                await message.reply(text=f'Отвечено на {otr} отрицательных отзывов', reply_markup=nav.mainMenu)

            else:
                if db.get_signup(message.from_user.id) == "setnickname":
                    if (len(message.text) != 11):
                        db.delete_user(message.from_user.id)
                        await bot.send_message(message.from_user.id, "Вы ввели номер телефона неверно! Введите команду /start еще раз!")
                    elif '@' in message.text or '/' in message.text:
                        db.delete_user(message.from_user.id)
                        await bot.send_message(message.from_user.id, "Вы ввели недопустимый символ! Введите команду /start ещё раз!")
                    else:
                        db.set_phone(message.from_user.id, message.text)
                        url = "https://seller.wildberries.ru/passport/api/v2/auth/login_by_phone"
                        payload = json.dumps({
                            "phone": db.get_phone(message.from_user.id),
                            "is_terms_and_conditions_accepted": True})
                        headers = {
                            'Content-Type': 'application/json', 'User-Agent': 'PostmanRuntime/7.31.1'}
                        url = "https://seller.wildberries.ru/passport/api/v2/auth/login_by_phone"
                        response_user_token = requests.request("POST", url, headers=headers, data=payload)
                        Dat = json.dumps(response_user_token.json())
                        sonData = json.loads(Dat)
                        data_feedback1 = sonData['token']
                        db.set_user_token(message.from_user.id, data_feedback1)
                        db.set_signup(message.from_user.id, "setrt")
                        await bot.send_message(message.from_user.id, "Введите код из приложения ВБ")

                elif db.get_signup(message.from_user.id) == "setrt":
                    if (len(message.text) != 6):
                        db.delete_user(message.from_user.id)
                        await bot.send_message(message.from_user.id,
                                               "Вы ввели код авторизации неверно! Введите команду /start ещё раз!")
                    elif '@' in message.text or '/' in message.text:
                        db.delete_user(message.from_user.id)
                        await bot.send_message(message.from_user.id, "Вы ввели неверный символ! Введите команду /start ещё раз!")
                    else:
                        db.set_phone_code(message.from_user.id, message.text)
                        body_auth = json.dumps(
                            {"options": {"notify_code": db.get_phone_code(message.from_user.id)},
                             "token": db.get_user_token(message.from_user.id)})
                        urlurl = "https://seller.wildberries.ru/passport/api/v2/auth/login"
                        headers_auth = {'Content-Type': 'application/json',
                                        'User-Agent': 'PostmanRuntime/7.31.1'}
                        response_user_tokensw = requests.request("POST", urlurl, headers=headers_auth, data=body_auth)
                        r = response_user_tokensw.cookies['WBToken']
                        db.set_auth_token(message.from_user.id, r)
                        url = "https://seller.wildberries.ru/ns/suppliers/suppliers-portal-core/suppliers"
                        payload = "[\r\n    {\r\n        \"id\":\"json-rpc_4\",\r\n        \"jsonrpc\":\"2.0\",\r\n        \"method\":\"getUserSuppliers\"\r\n    }\r\n]"
                        headers = {
                            'Content-Type': 'application/javascript',
                            'Accept': '*/*',
                            'User-Agent': 'PostmanRuntime/7.31.1',
                            'Cookie': f'WBToken={db.get_auth_token(message.from_user.id)}'
                        }
                        response = requests.request("POST", url, headers=headers, data=payload)
                        repe = response.json()
                        ko = 0
                        for i in repe:
                            kr = i['result']
                            rt = kr['suppliers']
                            for k in rt:
                                ik = k['id']
                                ko = ik
                        db.set_supplier(message.from_user.id, ko)
                        in_six_days = datetime.datetime.today() + datetime.timedelta(6)
                        db.set_time_token(message.from_user.id, in_six_days)
                        db.set_otz_count(message.from_user.id, 30)
                        db.set_signup(message.from_user.id, "done")
                        await bot.send_message(message.from_user.id, "Готово!", reply_markup=nav.mainMenu)
        else:
            await message.answer("Купите подписку")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
