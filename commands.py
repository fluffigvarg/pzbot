import json
import locale
import random

locale.setlocale(locale.LC_ALL, '')

PREFIX = "!"


def process(bot, user, message, channel_name):
    if message.startswith(PREFIX):
        cmd = message.split(" ")[0][len(PREFIX):]
        args = message.split(" ")[1:]
        perform(bot, user, message, channel_name, cmd, *args)


def perform(bot, user, message, channel_name, cmd, *args):
    for name, func in cmds.items():
        if cmd == name:
            func(bot, user, message, channel_name, *args)


def bartab(bot, user, message, channel_name, *args):
    file_awoo = 'awoo.json'
    file_oowa = 'oowa.json'

    dict_awoo = {}
    dict_oowa = {}

    with open(file_awoo) as f:
        dict_awoo = json.load(f)
    with open(file_oowa) as f:
        dict_oowa = json.load(f)

    try:
        awoo_count = dict_awoo[user]
    except:
        awoo_count = 0

    try:
        oowa_count = dict_oowa[user]
    except:
        oowa_count = 0

    tab = (awoo_count * 350) + (oowa_count * 35000)
    bot.send_message(channel_name, f"Hey {user}! You owe the pub {tab:n} bits!")


def magic8ball(bot, user, message, channel_name, *args):
    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]

    if args:
        question = ' '.join(args)
        bot.send_message(channel_name, f"{question} - " + random.choice(responses))
    else:
        bot.send_message(channel_name, random.choice(responses))


def coinflip(bot, user, message, channel_name, *args):
    coin = ["Heads", "Tails"]
    bot.send_message(channel_name, random.choice(coin))


def points(bot, user, message, channel_name, *args):
    dict_pub_points = {}
    file_pub_points = 'pub_points.json'

    with open(file_pub_points) as f:
        dict_pub_points = json.load(f)

    try:
        pub_points = dict_pub_points[user]
    except:
        pub_points = 0
    
    bot.send_message(channel_name, f"{user} has {pub_points} Pub Points!")

def givepoints(bot, user, message, channel_name, *args):
    file_pub_points = 'pub_points.json'
    dict_pub_points = {}
    target_user = args[0]
    points = int(args[1])

    if user == 'prawnzo':
        with open(file_pub_points) as f:
            dict_pub_points = json.load(f)

        try:
            dict_pub_points[target_user] += points
            bot.send_message(channel_name, f"{points} Pub Points given to {target_user}!")
        except:
            bot.send_message(channel_name, "Couldn't add points, try again!")
            return

        with open(file_pub_points, 'w') as f:
                json.dump(dict_pub_points, f)
    
    else:
        bot.send_message(channel_name, "How dare you! You can't give out points!")

def slots(bot, user, message, channel_name, *args):
    dict_pub_points = {}
    file_pub_points = 'pub_points.json'

    with open(file_pub_points) as f:
        dict_pub_points = json.load(f)

    try:
        pub_points = dict_pub_points[user]
    except:
        pub_points = 0

    try:
        bet = int(args[0])
    except:
        bot.send_message(channel_name, f"Sorry {user}, that's not a valid bet!")
        return

    win = bet * 10
    default_reel_1 = ["ConcernGold", "ConcernWealthe"]
    default_reel_2 = ["ConcernGold", "ConcernWealthe"]
    default_reel_3 = ["ConcernGold", "ConcernWealthe"]

    reel_1 = random.choice(default_reel_1)
    reel_2 = random.choice(default_reel_2)
    reel_3 = random.choice(default_reel_3)

    if pub_points < bet:
        bot.send_message(channel_name, f"Sorry {user}, you don't have enough points to play!")
        return
    else:
        bot.send_message(channel_name, f"{reel_1} | {reel_2} | {reel_3}")

        if reel_1 == reel_2 and reel_2 == reel_3:
            bot.send_message(channel_name, f"{user} bet {bet} and won {win} Pub Points!")
            dict_pub_points[user] += win
        else:
            bot.send_message(channel_name, f"{user} bet {bet} and lost {bet} Pub Points!")
            dict_pub_points[user] -= bet
        
        with open(file_pub_points, 'w') as f:
            json.dump(dict_pub_points, f)

    
cmds = {
    "bartab": bartab,
    "magic8ball": magic8ball,
    "coinflip": coinflip,
    # "slots" : slots,
    "points" : points,
    "givepoints" : givepoints,
}
