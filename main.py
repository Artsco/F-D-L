import os
import requests
import time
import json
import fgourl
import user
import coloredlogs
import logging
import sys

userIds = os.environ['userIds'].split(',')
authKeys = os.environ['authKeys'].split(',')
secretKeys = os.environ['secretKeys'].split(',')
webhook_discord_url = os.environ['webhookDiscord']
device_infos = (os.environ.get('DEVICE_INFO_SECRET') or '').split(',')
appCheck = os.environ.get('APP_CHECK_SECRET')
user_agents = (os.environ.get('USER_AGENT_SECRET_2') or '').split(',')
fate_region = 'JP'

userNums = len(userIds)
authKeyNums = len(authKeys)
secretKeyNums = len(secretKeys)

logger = logging.getLogger("FGO Daily Login")
coloredlogs.install(fmt='%(asctime)s %(name)s %(levelname)s %(message)s')

def get_latest_verCode():
    endpoint = "https://raw.githubusercontent.com/DNNDHH/FGO-VerCode-extractor/JP/VerCode.json"
    response = requests.get(endpoint).text
    response_data = json.loads(response)

    return response_data['verCode']
    
def get_latest_appver():
    endpoint = "https://raw.githubusercontent.com/DNNDHH/FGO-VerCode-extractor/JP/VerCode.json"
    response = requests.get(endpoint).text
    response_data = json.loads(response)

    return response_data['appVer']


def main():
    if userNums == authKeyNums and userNums == secretKeyNums:
        fgourl.set_latest_assets()
        for i in range(userNums):
            try:
                ua = user_agents[i].strip() if len(user_agents) > 1 else user_agents[0].strip()
                di = device_infos[i].strip() if len(device_infos) > 1 else device_infos[0].strip()
                os.environ['USER_AGENT_SECRET_2'] = ua
                os.environ['DEVICE_INFO_SECRET'] = di
                fgourl.httpheader['User-Agent'] = ua
                instance = user.user(userIds[i], authKeys[i], secretKeys[i])
                time.sleep(1)
                instance.topLogin()
                time.sleep(2)
                instance.topHome()
                time.sleep(0.5)
                instance.lq001()
                time.sleep(0.5)
                instance.Present()
                time.sleep(0.5)
                instance.lq002()
                time.sleep(2)
                instance.buyBlueApple()
                time.sleep(1)
                instance.lq003()
                time.sleep(1)

                #if "--Free_Gacha" in sys.argv:
                    #instance.Free_Gacha()

                instance.drawFP()
                time.sleep(1)
                #instance.LTO_Gacha()
                #instance.LTO_drawFP()

            


            except Exception as ex:
                logger.error(ex)

if __name__ == "__main__":
    main()
