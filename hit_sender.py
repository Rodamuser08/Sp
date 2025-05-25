import requests

def send(cc, key, username, time_taken):
    ii = cc[:6]

    try:
        response = requests.get(f'https://binchk-api.vercel.app/bin={ii}')
        data = response.json()

        if data.get('status', False):
            bank = data.get('bank', 'Unknown')
            emj = data.get('flag', '🏳️')
            do = data.get('country', 'Unknown')
            dicr = data.get('brand', 'Unknown')
            typ = data.get('type', 'Unknown')
        else:
            bank = emj = do = dicr = typ = 'Unknown'
    except Exception as e:
        print(f"Error fetching data from binchk API: {e}")
        bank = emj = do = dicr = typ = 'Unknown'

    msg1 = f"""
<b>GATEWAY ➜ Shopify 5.00$</b>
<b>RESPONSE ➜</b> {key}

<b>CC ➜</b> <code>{cc}</code>

<b>BIN ➜</b> {ii}
<b>COUNTRY ➜</b> {do}
<b>BANK ➜</b> {bank}
<b>FLAG ➜</b> {emj}
<b>TIME ➜</b> {time_taken}s

<b>Check by:</b> @{username}
<b>Bot by:</b> @strawhatchannel96
"""

    return msg1
