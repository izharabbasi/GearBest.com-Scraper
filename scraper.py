import requests
from lxml import html
import csv

def get(l):
    try:
        return l.pop(0)
    except:
        return ''

def write_csv(data):
    headers = ['title','url','price','company']
    with open('deals.csv','w', encoding='utf-8') as f:
        writer = csv.DictWriter(f,headers)
        writer.writeheader()
        writer.writerows(data)


scraped_deals = []

script = '''
    local num_scrolls = 10
        local scroll_delay = 1

        local scroll_to = splash:jsfunc("window.scrollTo")
        local get_body_height = splash:jsfunc(
            "function() {return document.body.scrollHeight;}"
        )
     headers = {
      ['User-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.64',
      ['cookie'] = 'AKAM_CLIENTID=4d6ca46d54bf26e6d5266d9f655cdf25; gb_lang=en; gb_pipeline=GB; aff_mss_info_bak={"bak":"bak"}; reffer_channel=; gb_countryCode=PK; gb_currencyCode=USD; gb_vsign=2e9d46677e21a76e16cd3fed3f3b5cb30bdaa8b6; _gcl_au=1.1.987026686.1594574366; _ga=GA1.2.1402803928.1594574367; globalegrow_user_id=2cb47937-242e-a9c1-b224-215681d91520; od=nmwjbxjpnpfz1594574371367; osr_landing=https%3A%2F%2Fwww.gearbest.com%2Fflash-sale.html; osr_referrer=originalurl; _gid=GA1.2.400015159.1594895601; gb_fcm=2; gb_fcmPipeLine=GB; WEBF_guid=4d6ca46d54bf26e6d5266d9f655cdf25_1594932838; globalegrowbigdata2018_globalegrow_session_id=76b2edf5-ab49-ae56-8edd-974e84e5003e; cdn_countryCode=PK; ak_bmsc=3A34D0870F9FC61D512CCDC44F51983817D7BD84E0300000F2C0105FB5B93728~plkUwv4srSdUqWxEUXHjfIhDhOY/SscE0Uj/HIPqDt/uQMvZyivs7bDaFZXKFVtt7Vk0wUjZUChFUcruPloFZo7ZVcdDLVh6RU7NTmlFmoQFWb8SkbN7LBXf+SGAiLFC0X00EuCRj7JqSAbeVCUYsI9qVpLla6204kTKDpP0jJ919BqtIlI4OqPfBwhbBgqONJGiepo+IVkKmNuPDRh6RcJsdCtmkMPFN+TTfxISfscZ5GnCccgfppdM1kBgjAUkTE; AKA_A2=A; landingUrl=https://www.gearbest.com/flash-sale-14.html; gb_soa_www_session=eyJpdiI6IlNRNXZocTNQRWJ1NFNTVkF4N01xUWc9PSIsInZhbHVlIjoiMlRKSG1Lc3hyZFNcL2xSRDhmeWNEcVY4SHNicnlvNEZTVmVka3NzbnMxbGRzQlRmYkVaMTVOMTc0eWF0SWtRRFN6OFwvN3pVc1wvVUxjcnFQdWp6anlHZXc9PSIsIm1hYyI6ImU2NDFiYzI2NGVlNjA4NjJhMThlNzI2YTdhNmFkZDUyOTNiOGJkMTJlNDE1NWNmOTM5YmRjZmNmMzMxNWM2OGUifQ%3D%3D; WEBF_predate=1594938117; _uetsid=9824154d4626713aa6ffa0bf551cd839; _uetvid=89d96680b423b23aaa35aabb09824cbb; globalegrowbigdata2018_globalegrow_session_id_76b2edf5-ab49-ae56-8edd-974e84e5003e=false; gb_pf=%7B%22rp%22%3A%22originalurl%22%2C%22lp%22%3A%22https%3A%2F%2Fwww.gearbest.com%2Fflash-sale.html%22%2C%22wt%22%3A1594938119467%7D; bm_sv=5DACE0865F68BD2B560D329AB73BECB8~b3a3LJ8DMWEEPfJ21AYc1gz4HXcUjOqngviHvb2xO04z4amBcvgsQEpm51NMGRdpp8hJ9qWRcw1rDmGncLSh9zeL1gD83X2qrLIJEY8StBNvmvahHUlGLFRAczeKDAa/54w+c2HlNgG09KgDCmdXJKBAoKxF1j6yK71/6/NX7qQ='
    }
    splash:set_custom_headers(headers)
    splash.private_mode_enabled = false
    splash.images_enabled = false
    assert(splash:go(splash.args.url))
    splash:wait(splash.args.wait)
  	splash:set_viewport_full()
  

    for _ = 1, num_scrolls do
            local height = get_body_height()
            for i = 1, 10 do
                scroll_to(0, height * i/10)
                splash:wait(scroll_delay/10)
            end
        end        
        return splash:html()
'''

for x in range(1,14):
    resp = requests.post(url='http://localhost:8050/run', json={
        'lua_source' : script,
        'wait': 2,
        'url': f'https://www.gearbest.com/flash-sale-{x}.html'
        
    })

    tree = html.fromstring(html=resp.content)

    deals = tree.xpath("//section[@class='flash_content']/div/ul/li")

    for deal in deals:
        d = {
            'title': get(deal.xpath(".//div[@class='goodsItem_content']/div[2]/a/text()")).strip(),
            'url': get(deal.xpath(".//div[@class='goodsItem_content']/div[2]/a/@href")),
            'price': get(deal.xpath(".//div[@class='goodsItem_content']/div[3]/span[1]/text()")),
            'company': get(deal.xpath(".//div[@class='goodsItem_content']/div[5]/a/span/text()"))
        }
        scraped_deals.append(d)

print(len(scraped_deals))

write_csv(scraped_deals)
