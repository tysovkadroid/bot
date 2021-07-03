from bot.msgs.emojis import emoji_22, emoji_30, emoji_31, emoji_32, emoji_33, emoji_34, emoji_35, \
                            emoji_36, emoji_37, emoji_38, emoji_39, emoji_40, emoji_41, emoji_42, \
                            emoji_43, emoji_44, emoji_45, emoji_46, emoji_47, emoji_48, emoji_49, \
                            emoji_50, emoji_51, emoji_52, emoji_53


def time_emoji(timesetting):
    if timesetting in ['12:00', '00:00']:
        out = emoji_30
    elif timesetting in ['12:30', '00:30']:
        out = emoji_31
    elif timesetting in ['01:00', '13:00']:
        out = emoji_32
    elif timesetting in ['01:30', '13:30']:
        out = emoji_33
    elif timesetting in ['02:00', '14:00']:
        out = emoji_34
    elif timesetting in ['02:30', '14:30']:
        out = emoji_35
    elif timesetting in ['03:00', '15:00']:
        out = emoji_36
    elif timesetting in ['03:30', '15:30']:
        out = emoji_37
    elif timesetting in ['04:00', '16:00']:
        out = emoji_38
    elif timesetting in ['04:30', '16:30']:
        out = emoji_39
    elif timesetting in ['05:00', '17:00']:
        out = emoji_40
    elif timesetting in ['05:30', '17:30']:
        out = emoji_41
    elif timesetting in ['06:00', '18:00']:
        out = emoji_42
    elif timesetting in ['06:30', '18:30']:
        out = emoji_43
    elif timesetting in ['07:00', '19:00']:
        out = emoji_44
    elif timesetting in ['07:30', '19:30']:
        out = emoji_45
    elif timesetting in ['08:00', '20:00']:
        out = emoji_46
    elif timesetting in ['08:30', '20:30']:
        out = emoji_47
    elif timesetting in ['09:00', '21:00']:
        out = emoji_48
    elif timesetting in ['09:30', '21:30']:
        out = emoji_49
    elif timesetting in ['10:00', '22:00']:
        out = emoji_50
    elif timesetting in ['10:30', '22:30']:
        out = emoji_51
    elif timesetting in ['11:00', '23:00']:
        out = emoji_52
    elif timesetting in ['11:30', '23:30']:
        out = emoji_53
    else:
        out = emoji_22
    return out
