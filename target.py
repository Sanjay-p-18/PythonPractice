'''Usage python target.py -a "url to be crawled"
List of urls 
https://www.target.com/p/-/A-79344798
https://www.target.com/p/-/A-13493042
https://www.target.com/p/-/A-85781566 '''
import requests
import lxml.html
from lxml import html
import re,json
import argparse
headers = {
    'authority': 'www.target.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en;q=0.9',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
}
def main():
    parser = argparse.ArgumentParser(description="Please pass the required args")
    parser.add_argument("-a", "--option_a", type=str, help="Please pass the url")
    args = parser.parse_args()
    if args.option_a:
        response = requests.get(args.option_a, headers=headers)
        respcontent=response.text
        data_dict = dict()
        resp_text=html.fromstring(respcontent)
        data_dict['url'] = vars(args).get("option_a")
        data_dict['tcin'] = ''.join(resp_text.xpath("//b[contains(text(), 'TCIN')]//parent::div//text()")).replace("TCIN:",'').strip()
        data_dict['upc'] = ''.join(resp_text.xpath("//b[contains(text(), 'UPC')]//parent::div//text()")).replace("UPC:",'').strip()
        data_dict['price_amount'] = re.search('current_retail(.*?),',respcontent).group(1).replace("\\",'').replace('":','').replace("_min","")
        data_dict['title']=''.join(resp_text.xpath("//h1[@id='pdp-product-title-id']//text()")).strip()
        data_dict['currency'] = 'USD'
        data_dict['description'] = ''.join(resp_text.xpath('//meta[@property="og:description"]/@content'))
        data_dict['bullets'] = '\n'.join(resp_text.xpath("//div[@class='styles__StyledCol-sc-fw90uk-0 hOcoMD h-padding-t-x2 h-padding-r-tight']//text()")).strip()
        #data_dict['upc'] = re.search('primary_barcode(.*?)",',respcontent).group(1).replace("\\",'').replace('":"','')
        feature_temp = '\n'.join(resp_text.xpath('//h4[contains(text(),"Specifications")]/following-sibling::div//text()'))
        data_dict['features'] = feature_temp.replace("\n ",'').replace("\n: \n",":").replace("\n:\n",":").split("\n")
        try:
            data_dict['ingredients'] = [re.search('"ingredients:(.*?)".',respcontent).group(1).replace("\\","").strip()]
        except Exception as e:
            data_dict['ingredients'] = []
        print(json.dumps(data_dict))
if __name__ == "__main__":
    main()
    print("\n\n---------------Happy Crawling---------------------\n\n")