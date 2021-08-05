import json
import re
from random import randint
import datetime

luck_sentiment = 1
bot_sentiment = 1
bot_sentiment_counter = 1
dayofweek = datetime.datetime.today().strftime("%A")


def process(bot, user, message, channel_name):
    global luck_sentiment
    global bot_sentiment
    global bot_sentiment_counter
    global dayofweek

    # Pub points
    if message:
        pub_points(bot, user, message, channel_name)

    # emote stats
    if "prawnz" in message.lower():
        emote(bot, user, message, channel_name)

    # !bartab
    if "awoo" in message.lower():
        awoo(bot, user, message, channel_name)
    if "oowa" in message.lower():
        oowa(bot, user, message, channel_name)

    # meow
    meow_chance = 10
    if "now" in message.lower() and one_in_x_chance(meow_chance, bot_sentiment, bot_sentiment_counter, None):
        meow(bot, user, message, channel_name)

    # luck sentiment tracker
    if "prawnzbless" in message.lower():
        luck_sentiment += 1

    if "prawnzgl" in message.lower():
        luck_sentiment += 1

    # bot sentiment tracker
    if message.lower() == 'prawnzbot yes':
        bot.send_message(channel_name, "JodiesSmile")
        bot_sentiment += 1
        bot_sentiment_counter += 1

    if message.lower() == 'prawnzbot no':
        bot.send_message(channel_name, ':(')
        bot_sentiment_counter += 1

    # teh urn
    urn_chance = 2000
    if one_in_x_chance(urn_chance, None, None, luck_sentiment):
        teh_urn(bot, user, message, channel_name)
        luck_sentiment = 1

    # durrrr
    if dayofweek == 'Thursday':
        replace_word_chance = 25
    else:
        replace_word_chance = 50
    if one_in_x_chance(replace_word_chance, bot_sentiment, bot_sentiment_counter, None):
        replace_word(bot, user, message, channel_name)

    # well actually
    well_actually_chance = 500
    if one_in_x_chance(well_actually_chance, bot_sentiment, bot_sentiment_counter, None):
        well_actually(bot, user, message, channel_name)


def one_in_x_chance(upper_bound, bot_sentiment, bot_sentiment_counter, luck_sentiment):
    if luck_sentiment is not None:  # for calling teh urn
        luck_sentiment_multiplier = randint(1, 5)
        luck_sentiment_adjusted = luck_sentiment * luck_sentiment_multiplier
        if luck_sentiment_adjusted < upper_bound:
            winning_number = (randint(1, upper_bound - luck_sentiment_adjusted))
            if winning_number == upper_bound - luck_sentiment_adjusted:
                return True
            else:
                return False
        else:
            return True

    else:  # for other odds calculations
        sentiment = bot_sentiment / bot_sentiment_counter
        gooder = .6
        good = .8
        neutral = 1
        bad = 1.2
        badder = 1.4
        if bot_sentiment_counter == 1:  # starting condition
            winning_number = (randint(1, int(upper_bound * neutral)))
            if winning_number == int(upper_bound * neutral):
                return True
            else:
                return False
        if sentiment >= .75 and bot_sentiment_counter >= 1:  # gooder sentiment
            winning_number = (randint(1, int(upper_bound * gooder)))
            if winning_number == int(upper_bound * gooder):
                return True
            else:
                return False
        if sentiment >= .5 and bot_sentiment_counter >= 1:  # good sentiment
            winning_number = (randint(1, int(upper_bound * good)))
            if winning_number == int(upper_bound * good):
                return True
            else:
                return False
        if sentiment >= .25 and bot_sentiment_counter >= 1:  # bad sentiment
            winning_number = (randint(1, int(upper_bound * bad)))
            if winning_number == int(upper_bound * bad):
                return True
            else:
                return False
        if sentiment >= 0 and bot_sentiment_counter >= 1:  # badder sentiment
            winning_number = (randint(1, int(upper_bound * badder)))
            if winning_number == int(upper_bound * badder):
                return True
            else:
                return False


def awoo(bot, user, message, channel_name):
    dict_awoo = {}
    file_awoo = 'awoo.json'
    with open(file_awoo) as f:
        dict_awoo = json.load(f)

    try:
        dict_awoo[user] += 1
    except:
        dict_awoo[user] = 1
    with open(file_awoo, 'w') as f:
        json.dump(dict_awoo, f)


def oowa(bot, user, message, channel_name):
    dict_oowa = {}
    file_oowa = 'oowa.json'
    with open(file_oowa) as f:
        dict_oowa = json.load(f)

    try:
        dict_oowa[user] += 1
    except:
        dict_oowa[user] = 1
    with open(file_oowa, 'w') as f:
        json.dump(dict_oowa, f)

def emote(bot, user, message, channel_name):
    dict_emotes = {}
    message_regex = []
    emote_regex = re.compile(r'[Pp][Rr][Aa][Ww][Nn][Zz][^Oo]\w+')
    message_regex = emote_regex.findall(message)

    file_emote = 'emote.json'
    with open(file_emote) as f:
        dict_emotes = json.load(f)

    for emote_used in message_regex:
        try:
            dict_emotes[emote_used] += 1
        except:
            dict_emotes[emote_used] = 1

    with open(file_emote, 'w') as f:
        json.dump(dict_emotes, f)


def replace_word(bot, user, message, channel_name):
    replacement_word = 'DURRRR'
    chat_list = message.split()
    chat_list_length = len(chat_list)
    if replacement_word in chat_list:
        pass
    else:
        if chat_list_length > 1:
            replace_index = randint(0, chat_list_length - 1)
            chat_list[replace_index] = replacement_word
            new_chat_message = " ".join(chat_list)
            return bot.send_message(channel_name, new_chat_message)
        else:
            pass

def meow(bot, user, message, channel_name):
    pattern = '\\b[Nn][Oo][Ww]\\b'
    match = re.search(pattern, message)
    if match != None:
        new_message = re.sub(pattern, 'meow', message)
        new_message += ' STMeow'
        return bot.send_message(channel_name, new_message)


def teh_urn(bot, user, message, channel_name):
    winning_statement = '/me ConcernGold THIS IS TEH URN ConcernGold'
    return bot.send_message(channel_name, winning_statement)


def well_actually(bot, user, message, channel_name):
    with open('well_actually.txt') as f:
        fun_facts = f.readlines()
        emote = 'prawnzWellActually '
        fun_fact = emote + fun_facts[randint(0, len(fun_facts) - 1)].rstrip()
    try:
        return bot.send_message(channel_name, fun_fact)
    except:
        pass


def pub_points(bot, user, message, channel_name):
    dict_pub_points = {}
    file_pub_points = 'pub_points.json'
    with open(file_pub_points) as f:
        dict_pub_points = json.load(f)

    message_length = int(len(message))
    message_points = 10 * (randint(1, message_length))

    try:
        dict_pub_points[user] += message_points
    except:
        dict_pub_points[user] = 1000
    with open(file_pub_points, 'w') as f:
        json.dump(dict_pub_points, f)