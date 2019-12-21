from helpers import httpClient

shodan_key = ""


class Shodan:
    def __init__(self):
        pass

    def check_honeypot(self, ipAddress):
        url = 'https://api.shodan.io/labs/honeyscore/'
        check = httpClient.Get(url+ipAddress+'?key='+shodan_key).response
        if check.status_code == 200:
            honeyInd = float(check.text)
            chance = honeyInd * 100
            print(f"Percent of HoneyPotChance {chance}")
            return honeyInd

    def shodan(self, target, hostname):
        response = httpClient.Get(
            'https://api.shodan.io/shodan/host/'+target+'?key='+shodan_key, isJson=True)
        payload = response["data"]
        try:
            for i in range(len(payload['data'])):
                try:
                    port = payload['data'][i]['port']
                except Exception as errPort:
                    port = 'Not Found'
                try:
                    product = payload['data'][i]['product']
                except Exception as errProduct:
                    product = 'Not Found'
                try:
                    banner = payload['data'][i]['banner']
                except Exception as error:
                    banner = 'Not Found'

                try:
                    ops = payload['data'][i]['os']
                except Exception as error:
                    ops = 'Not Found'
            print(
                '\t[+] Open Port: {} Product: {} Banner: {} OS: {}'.format(port, product, banner, ops))

        except Exception as err:
            print("\t[+] Miss or error: {}".format(err))
