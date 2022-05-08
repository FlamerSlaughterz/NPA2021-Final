import requests
import time
from ncclient import manager

def auto_bot():
    access_token = 'Mzk3MTU3NTgtZTRhZS00MGUzLTkyZGUtYjMzMWU2ZmYxNzE5YmJhNTc3ZDgtMGRm_P0A1_d068f91d-d29e-4173-a09d-365c3fb6e36e'
    room_id = 'Y2lzY29zcGFyazovL3VzL1JPT00vNjUwODkzMjAtY2QxOS0xMWVjLWE1NGUtNGQ2MmNhMWM4YmVl'
    url = 'https://webexapis.com/v1/messages'
    headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
    }
    params_get = {'roomId': room_id}
    params_lo_up = {'roomId': room_id, 'markdown': 'Loopback62070202 - Operational status is up'}
    params_lo_down = {'roomId': room_id, 'markdown': 'Loopback62070202 - Operational status is down'}


    res = requests.get(url, headers=headers, params=params_get)
    format_res = res.json()
    checkans = format_res['items'][0]['text']
    print("Recieved message:", checkans)

    

    netconf_filter = """
    <filter>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <interface>
            <Loopback>
                
            </Loopback>
            </interface>
        </native>
    </filter>
    """

    

    if checkans == "62070202":
        m = manager.connect(
        host="10.0.15.114",
        port=830,
        username="admin",
        password="cisco",
        hostkey_verify=False
        )
        
        netconf_reply = m.get_config(source="running", filter=netconf_filter)

        if "<shutdown/>" in str(netconf_reply):
            res = requests.post(url, headers=headers, json=params_lo_down)
        else:
            res = requests.post(url, headers=headers, json=params_lo_up)

def activate():
    while(True):
        auto_bot()
        time.sleep(1)

activate()