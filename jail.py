import json
import os
import datetime
PLUGIN_METADATA = {
    'id': 'jail',
    'version': '2021208',
    'name': 'jail',
    'description': 'jail软封禁',
    'author': 'Guang_Chen_',
    'dependencies': {
        'mcdreforged': '>=1.0.0',
    }
}
config_path = '.\\config\\jail.json'
DefaultConfig = {
    'players': {}
}
config = DefaultConfig.copy()


def WriteConfig(newconfig=[]):
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(newconfig, sort_keys=True, indent=4,
                           ensure_ascii=False, separators=(',', ': ')))


def LoadConfig():
    global config
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.loads(f.read())


def on_load(server, prev_module):
    if os.path.isfile(config_path):
        LoadConfig()
    else:
        WriteConfig(DefaultConfig)


def on_user_info(server, info):
    t = info.content.split()
    p = server.get_permission_level(info)
    if p >= 3:
        if t[0] == '!!jail' and len(t) == 3:
            nowtime = datetime.datetime.now()
            targettime = (nowtime + datetime.timedelta(minutes=int(t[2]))).strftime("%Y-%m-%d %H:%M:%S")
            config['players'][t[1]] = targettime
            fuckplayer(server, t[1])
            server.reply(info, '§4§l完成，{}将被透到 {}'.format(t[1],targettime))
            WriteConfig(config)
        elif t[0] == '!!unjail' and len(t) == 2 and t[1] in config['players']:
            server.execute('/effect clear {}'.format(t[1]))
            server.reply(info, '§4§l{}不再被透了'.format(t[1]))
            del config['players'][t[1]]
            WriteConfig(config)

def calctime(player):
    nowtime = datetime.datetime.now()
    targettime = datetime.datetime.strptime(
        config['players'][player], "%Y-%m-%d %H:%M:%S")
    return (targettime - nowtime).seconds


def on_player_joined(server, player, info):
    if player in config['players']:
        nowtime = datetime.datetime.now().second
        targettime = datetime.datetime.strptime(
            config['players'][player], "%Y-%m-%d %H:%M:%S").second
        if calctime(player) <= 0:
            fuckplayer(server, player)
            server.tell(player, '§4§l您的下次苏醒时间为：{}'.format(
                config['players'][player]))
        else:
            del config['players'][player]
            WriteConfig(config)


def fuckplayer(server, player):
    server.execute(
        '/effect give {} minecraft:slowness {} 254 true'.format(player, calctime(player)))
    server.execute(
        '/effect give {} minecraft:mining_fatigue {} 254 true'.format(player, calctime(player)))
    server.execute(
        '/effect give {} minecraft:resistance {} 254 true'.format(player, calctime(player)))
    server.execute(
        '/effect give {} minecraft:invisibility {} 254 true'.format(player, calctime(player)))
    server.execute(
        '/effect give {} minecraft:blindness {} 254 true'.format(player, calctime(player)))
    server.execute(
        '/effect give {} minecraft:saturation {} 254 true'.format(player, calctime(player)))