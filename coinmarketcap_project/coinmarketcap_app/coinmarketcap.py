from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller
import re

class CoinMarketCap:
    
    def __init__(self):
        self.option = webdriver.ChromeOptions()
        self.option.add_argument("disable-gpu")
        self.option.add_argument('--headless')
        self.option.add_argument('--no-sandbox')
        self.option.add_argument('--disable-dev-sh-usage')
        self.option.add_experimental_option('excludeSwitches', ['enable-logging'])

        chromedriver_autoinstaller.install()
        self.driver = webdriver.Chrome(options=self.option)

    def getData(self, name):
        self.driver.get(f'https://coinmarketcap.com/currencies/{name}/')
        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        error_tag = self.soup.find('p', string=re.compile("Sorry"))

        if error_tag:
            return {'error': 'Coin not Found'}
        
        def getMetrics():
            dl_element = self.soup.find('dl', class_='coin-metrics-table')
            metrics_values = {}
            metric_mapping = {
                'Market cap': 'market_cap',
                'Volume (24h)': 'volume',
                'Volume/Market cap (24h)': 'volume_change',
                'Circulating supply': 'circulating_supply',
                'Total supply': 'total_supply',
                'Max. supply': 'max_supply',
                'Fully diluted market cap': 'diluted_market_cap'
            }

            for child in dl_element.children:
                if child.name == 'div':
                    dt_element = child.find('dt')
                    dd_element = child.find('dd')
                    if dt_element and dd_element:
                        metric_name = dt_element.find('div').text.strip()
                        metric_value = dd_element.get_text(strip=True).replace('(1d)', '')
                        rank_value_span = child.find('span', class_='rank-value')
                        rank_value = rank_value_span.get_text(strip=True).replace('(1d)', '') if rank_value_span else None
                        
                        if metric_name in metric_mapping:
                            key = metric_mapping[metric_name]
                            if key == 'volume_change':
                                match = re.search(r'([\d.]+%)', metric_value)
                                if match:
                                    volume_change = float(match.group(1).strip('%').replace('(1d)', ''))
                                    change_direction = dd_element.find('p', attrs={'data-change': True})
                                    if change_direction and change_direction['data-change'] == 'down':
                                        volume_change *= -1
                                    metrics_values[key] = volume_change
                                else:
                                    metrics_values[key] = None
                            else:
                                match = re.search(r'([\d,.]+)', metric_value)
                                value = match.group(1).replace(',', '').replace('(1d)', '') if match else None
                                if value:
                                    metrics_values[key] = float(value) if '.' in value else int(value)
                                else:
                                    metrics_values[key] = None
                                    
                            if rank_value is not None:
                                metrics_values[f'{key}_rank'] = int(re.search(r'\d+', rank_value).group()) if rank_value else None

            output = {
                "price": None,
                "price_change": None,
                "market_cap": metrics_values.get("market_cap"),
                "market_cap_rank": metrics_values.get("market_cap_rank"),
                "volume": metrics_values.get("volume"),
                "volume_rank": metrics_values.get("volume_rank"),
                "volume_change": metrics_values.get("volume_change"),
                "circulating_supply": metrics_values.get("circulating_supply"),
                "total_supply": metrics_values.get("total_supply"),
                "max_supply": metrics_values.get("max_supply"),
                "diluted_market_cap": metrics_values.get("diluted_market_cap"),
            }

            return output

        def getSocials():
            coin_info_links = self.soup.find('div', class_='coin-info-links')
            social_links = coin_info_links.find_all('a', href=True)
            official_links = []
            socials = []
            
            for link in social_links:
                url = link['href']
                text = link.get_text(strip=True)
                if "0x" in text:
                    continue
                
                link_data = {'name': text.lower(), 'url': url}
                if text.lower() == 'website':
                    official_links.append({'name': 'website', 'link': url})
                else:
                    socials.append(link_data)

            contract_element = self.soup.find('a', class_='chain-name')
            try:
                contract_name = contract_element.get_text(strip=True)
                contract_url = contract_element['href']
                contract_address = contract_url.split('/')[-1]
            except (AttributeError, KeyError):
                contract_name = None
                contract_address = None
                
            output = {
                "contracts": [{
                    'name': contract_name,
                    'address': contract_address
                }],
                'official_links': official_links,
                'socials': socials
            }
            return output

        def getPrice():
            price_div = self.soup.find('div', {'data-role': 'el'}).find_next('div', {'data-role': 'el'})
            price_span = price_div.find('span')
            price_text = price_span.get_text(strip=True).replace('(1d)', '') if price_span else "N/A"

            percentage_change_div = price_div.find_next('div')
            percentage_change_p = percentage_change_div.find('p') if percentage_change_div else None
            percentage_change_text = percentage_change_p.get_text(strip=True).replace('(1d)', '') if percentage_change_p else "N/A"
            change_direction = percentage_change_p['data-change'] if percentage_change_p and 'data-change' in percentage_change_p.attrs else None

            price = float(price_text.replace('$', '').replace(',', '').replace('(1d)', '')) if price_text != "N/A" else None
            percentage_change = float(percentage_change_text.replace('%', '').replace('\xa0(1d)', '').replace('(1d)', '')) if percentage_change_text != "N/A" else None

            if change_direction == 'down':
                percentage_change *= -1

            output = {
                "price": price,
                "price_change": percentage_change
            }

            return output
        
        data = (getPrice(), getMetrics(), getSocials())
        x = data[1]
        x['price'] = data[0]['price']
        x['price_change'] = data[0]['price_change']
        x['contracts'] = data[2]['contracts']
        x['official_links'] = data[2]['official_links']
        x['socials'] = data[2]['socials']
        
        return x
            
    def closeDriver(self):
        self.driver.quit()
    
    def __del__(self):
        try:
            self.closeDriver()
        except:
            pass
