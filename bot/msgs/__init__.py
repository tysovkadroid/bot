from bot.msgs.emojis import emoji_4, emoji_6, emoji_7, emoji_8, emoji_9, emoji_10, emoji_11, \
                            emoji_12, emoji_13, emoji_14, emoji_15, emoji_16, emoji_17, \
                            emoji_18, emoji_19, emoji_20, emoji_21, emoji_22, emoji_23
from bot.tools.string_escape import string_escape

msg_1 = f'{{a}}я напомню {{b}} о днях рождения {{c}} друзей! {emoji_19}\n' \
        f'создатель — @{{d}} {emoji_6}{{e}}'
msg_2 = 'привет{a}! {b}'
msg_3 = f'как мне тебя называть? {emoji_11}'
msg_4 = f'как, говоришь? {emoji_7}'
msg_5 = f'такой пользователь уже есть, выбери другое имя! {emoji_17}'
msg_6 = f'выбери свой пол! {emoji_11}'
msg_7 = f'не совсем тебя понял {emoji_7}'
msg_8 = f'введи свою *дату рождения* в формате ДД.ММ.ГГГГ! {emoji_11}'
msg_9 = f'неверный формат, попробуй ещё раз {emoji_7}'
msg_10 = f'запомнил, *{{a}}*! {emoji_14}'
msg_11 = f'{{a}} сегодня {{b}}! {emoji_8}\n' \
         f'не забудь {{c}} поздравить! {{d}}'
msg_12 = f'{{a}} {{b}} свой день рождения через {{c}}! {emoji_22}'
msg_13 = f'{{a}} сегодня празднует свой день рождения! {emoji_23}'
msg_14 = f'{{a}} уже {{b}} свой день рождения в этом году! {emoji_17}'
msg_15 = f'для получения уведомлений определи свой *список людей*! {emoji_16}'
msg_16 = f'теперь ты *{{a}}* на уведомления! {emoji_8}\n' \
         f'они будут приходить к тебе ровно в {{b}}! {emoji_20}\n' \
         f'определи свой *список людей* {emoji_21}\n' \
         f'и, если хочешь, установи собственное *время* прихода уведомлений {emoji_22}'
msg_17 = f'ты уже *{{a}}* на уведомления {emoji_14}'
msg_18 = f'ты только что *{{a}}* от уведомлений {emoji_12}'
msg_19 = f'ты уже *{{a}}* от уведомлений {emoji_18}'
msg_20 = f'введи *время* в 24-часовом формате {emoji_15}'
msg_21 = f'для редактирования *времени* подпишись на уведомления {emoji_16}'
msg_22 = 'по умолчанию *({a})*'
msg_23 = 'на *{a}*'
msg_24 = '*время* прихода уведомлений установлено {a}, ' \
         'что бы изменить *время*, нажми на кнопку ниже {b}'
msg_25 = f'сегодня тебе уже приходило уведомление о том, что у {{a}} сегодня день рождения!\n' \
         f'напомнить ещё раз в *{{b}}*? {emoji_11}'
msg_26 = '*время* установлено на *{a}* b}'
msg_27 = f'для редактирования *списка людей* подпишись на уведомления {emoji_16}'
msg_28 = f'*список людей*, о чьих днях рождения\n' \
         f'ты будешь получать уведомления {emoji_21}'
msg_29 = f'в списке пока нет людей {emoji_7}'
msg_30 = f'охрана отменена, я могу для тебя что-нибудь ещё сделать? {emoji_9}'
msg_31 = f'охрана отменена, ты получишь уведомление через *{{a}}*! {emoji_13}\n' \
         f'я могу для тебя что-нибудь ещё сделать? {emoji_9}'
msg_32 = f'охрана отменена, *сегодня* больше напоминать не буду! {emoji_10}\n' \
         f'я могу для тебя что-нибудь ещё сделать? {emoji_9}'
msg_33 = f'охраны отмены не будет, определи свой *список людей* {emoji_21}'
msg_34 = f'охраны отмены не будет, отменять то и нечего {emoji_7}'
msg_35 = 'добро пожаловать в *тусовку*{a}! {b}'
msg_36 = f'пока, удачи{{a}}! {emoji_4}'
msg_37 = f'что хочешь изменить? {emoji_11}'
msg_38 = 'введи через запятую: *дату праздника* в формате ДД.ММ и *сообщение* для того, что бы ' \
         'добавить или редактировать праздник или *дату праздника* в формате ДД.ММ, что бы его ' \
         'удалить!'
msg_39 = 'список праздников пуст.'
msg_40 = 'праздник *({a})* не существует.'
msg_41 = 'произошла ошибка{a}!'

msg_1 = string_escape(msg_1, '!')
msg_2 = string_escape(msg_2, '!')
msg_6 = string_escape(msg_6, '!')
msg_8 = string_escape(msg_8, '.!')
msg_10 = string_escape(msg_10, '!')
msg_11 = string_escape(msg_11, '!')
msg_13 = string_escape(msg_13, '!')
msg_15 = string_escape(msg_15, '!')
msg_16 = string_escape(msg_16, '!')
msg_20 = string_escape(msg_20, '-')
msg_22 = string_escape(msg_22, '()')
msg_25 = string_escape(msg_25, '!')
msg_30 = string_escape(msg_30, '-')
msg_31 = string_escape(msg_31, '-!')
msg_32 = string_escape(msg_32, '-!')
msg_35 = string_escape(msg_35, '!')
msg_36 = string_escape(msg_36, '()!')
msg_38 = string_escape(msg_38, '.!')
msg_39 = string_escape(msg_39, '.')
msg_40 = string_escape(msg_40, '.()')
msg_41 = string_escape(msg_41, '!')