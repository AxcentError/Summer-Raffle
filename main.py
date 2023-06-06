import datetime
from telethon import TelegramClient
import asyncio
import re
import random
import os
import config


async def main():
    print('Сессия найдена!')
    await client.send_message(entity='wallet', message='/start')

    while True:
        await asyncio.sleep(random.uniform(0.01, 0.05))
        try:
            messages = await client.get_messages('wallet')
            if "👛" in messages[0].reply_markup.rows[0].buttons[0].text:
                break
        except: pass

    await client.send_message('wallet', message='/settings')
    while True:
        await asyncio.sleep(random.uniform(0.01, 0.1))
        try:
            messages = await client.get_messages('wallet')
            if "⚙" in messages[0].message:
                break
        except: pass

    await messages[0].click(0)
    while True:
        await asyncio.sleep(random.uniform(0.01, 0.1))
        try:
            messages = await client.get_messages('wallet')
            if "🇬🇧" in messages[0].reply_markup.rows[0].buttons[0].text:
                break
        except: pass
    await messages[0].click(0)

    # оправляем команду валлет
    await client.send_message(entity='wallet', message='/wallet')

    # проверяем ответ
    while True:
        await asyncio.sleep(random.uniform(0.01, 0.05))
        try:
            messages = await client.get_messages('wallet')
            if "💰" in messages[0].text:
                break
        except: pass

    # нажимаем пополнить
    await asyncio.sleep(0.02)
    await messages[0].click(0)

    # ждем ответ
    while True:
        try:
            messages = await client.get_messages('wallet')
            if "➕" in messages[0].text or "📱" in messages[0].text:
                break
        except:
            pass

    # если нужно, делимся номером телефона
    if '📱' in str(messages[0].message):
        await messages[0].click(0, share_phone=True)
        messages_temp = await client.get_messages('wallet')

        # ждем ответ после отправки телефона
        while True:
            await asyncio.sleep(random.uniform(0.01, 0.05))
            messages = await client.get_messages('wallet')

            if messages_temp[0].text != messages[0].text:
                break

    # выбираем тон
    await messages[0].click(1)

    # ждем ответ
    while True:
        await asyncio.sleep(random.uniform(0.01, 0.05))
        messages = await client.get_messages('wallet')

        if "The Open Network - TON" in messages[0].message:
            break

    # получаем адрес для пополнения
    wallet_address = re.search(r"\b[A-Za-z0-9_\-]{32,64}\b", messages[0].message).group()
    print(f'Переведите 1 платежом ровно {(-(-config.tickets // 3))*0.001} ton на адрес "{wallet_address}"')

    # проверяем пополнение
    while True:
        await asyncio.sleep(random.uniform(0.01, 0.05))
        messages = await client.get_messages('wallet')
        if str((-(-config.tickets // 3))*0.001) in messages[0].message or '🎉' in messages[0].message:
            break

    print('Перевод найден!')

    # начинаем выводить на каждый адрес тон
    with open('wallets.txt', 'r') as file:
        wallets = [line.strip() for line in file]

    number = 0
    for wallet in wallets:
        if number == -(-config.tickets // 3):
            break

        if len(wallets) < -(-config.tickets // 3):
            print(f'Не достаточно адресов! Нужно ещё {(-(-config.tickets // 3))-len(wallets)} адресов')
            break
        now = datetime.datetime.now()

        # отправляем команду валет
        await client.send_message(entity='wallet', message='/wallet')

        # ждем ответ
        while True:
            await asyncio.sleep(random.uniform(0.01, 0.05))
            try:
                messages = await client.get_messages('wallet')
                if "💰" in messages[0].text:
                    break
            except:
                pass

        # нажимаем вывести
        await messages[0].click(1)

        # ждем ответ, клик тон
        while True:
            await asyncio.sleep(random.uniform(0.01, 0.05))
            messages = await client.get_messages('wallet')

            if '➡' in messages[0].message:
                await messages[0].click(1)
                break

        # ждём ответ
        while True:
            await asyncio.sleep(random.uniform(0.01, 0.05))
            messages = await client.get_messages('wallet')

            if 'Send your TON wallet address in text message here.' in messages[0].message or "Отправьте в сообщении адрес вашего TON кошелька." in messages[0].message:
                break

        # вводим адрес для вывода
        await client.send_message(entity='wallet', message=wallet)

        # ждём ответ
        while True:
            await asyncio.sleep(0.01, 0.05)
            messages = await client.get_messages('wallet')

            if '0.001 TON' in messages[0].message and "0 TON" in messages[0].message:
                break

        # вводим сумму
        await client.send_message(entity='wallet', message='0.001')

        # ждём ответ
        while True:
            await asyncio.sleep(0.01, 0.05)
            messages = await client.get_messages('wallet')

            if f'Address: {wallet}' in messages[0].message and "0 TON" in messages[0].message:
                break

        # подтверждаем
        await messages[0].click(0)

        await asyncio.sleep(random.uniform(0.5, 1))
        number += 1
        print(f'{number}/{-(-config.tickets // 3)}/{len(wallets)} отправлено на "{wallet}" 0.001 TON | {datetime.datetime.now() - now}')

    await asyncio.sleep(2)
    messages = await client.get_messages('wallet')
    if "🎉" in messages[0].message:
        print("На аккаунте " + str(int(re.findall(r'\d+', messages[0].message)[-1])) + "тикетов ")
    else:
        print('Не удалось найти кол-во тикетов')


client = TelegramClient(config.session, config.api_id, config.api_hash)
client.start()
client.loop.run_until_complete(main())
