import aiohttp
import random
import re
import asyncio

async def reqproxy():
    try:
        with open('proxy.txt', 'r') as file:
            lines = {line.strip() for line in file if line.strip()}
    except FileNotFoundError:
        print("proxy.txt not found.")
        return None

    if not lines:
        print("No proxies found in proxy.txt.")
        return None

    for _ in range(len(lines)):
        proxy_str = random.choice(list(lines))
        proxy_parts = proxy_str.split(":")
        
        if len(proxy_parts) != 4:
            print(f"Invalid proxy format: {proxy_str}")
            continue
        
        ip, port, user, pass1 = proxy_parts
        main_proxy = f"http://{user}:{pass1}@{ip}:{port}"

        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30.0)) as client:
            try:
                test_url = "https://httpbin.org/ip"
                async with client.get(test_url, proxy=main_proxy) as test_response:
                    test_response.raise_for_status()
                    public_ip = (await test_response.json()).get("origin", "")

                    if not public_ip:
                        print(f"Proxy {main_proxy} failed: No IP returned")
                        continue

                    url = f"https://scamalytics.com/ip/{public_ip}"
                    headers = {
                        'User-Agent': "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
                        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                        'Accept-Language': "en-US,en;q=0.9",
                        'Referer': "https://scamalytics.com/ip",
                        'Sec-Fetch-Dest': "document",
                        'Sec-Fetch-Mode': "navigate",
                        'Sec-Fetch-Site': "same-origin",
                        'Sec-Fetch-User': "?1",
                        'Upgrade-Insecure-Requests': "1",
                        'sec-ch-ua': "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"",
                        'sec-ch-ua-mobile': "?1",
                        'sec-ch-ua-platform': "\"Android\"",
                    }

                    async with client.get(url, headers=headers, proxy=main_proxy) as score_response:
                        score_response.raise_for_status()
                        text = await score_response.text()
                        match = re.search(r'"score":"(\d+)"', text)
                        if match:
                            score = int(match.group(1))
                            if 0 <= score <= 50:
                                print(f"Live proxy with score {score} and IP {public_ip}")
                                
                                return aiohttp.ClientSession(
                                    timeout=aiohttp.ClientTimeout(total=30.0),
                                    connector=aiohttp.TCPConnector(ssl=False),
                                    proxy=main_proxy
                                )
                            else:
                                print(f"Proxy {main_proxy} has high fraud score: {score}")
                                continue
                        else:
                            print(f"Could not find fraud score for {public_ip}")
                            continue

            except aiohttp.ClientError as e:
                print(f"Proxy {main_proxy} failed: {e}")
                continue

    print("No valid proxies found.")
    return None
