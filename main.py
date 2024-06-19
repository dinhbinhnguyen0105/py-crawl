import json, os, datetime
from pycontrol.crawl import Crawl

PAYLOAD_PATH = os.path.join(os.path.dirname(__file__), 'payload.json')
BROWSERS_DIR = '/Users/ndb/Workspace/mymanager/bin/browsers/'

def main():
    with open(PAYLOAD_PATH, 'r') as f:
        payload = json.load(f)

    for browser in payload['browsers']:
        browserDir = os.path.join(os.path.join(BROWSERS_DIR, browser['browsername']))
        crawl = Crawl(browserDir)
        data = crawl.crawlControl(browser['url'], payload['keywords'], 1)

        groupUID = browser['url'].split('/')[-2]
        now = datetime.datetime.now()
        filename = f'{now.month}-{now.day}.{now.hour}h{now.minute}.{browser["browsername"]}-{groupUID}.json'
        with open(f'{os.path.join(os.path.dirname(__file__), 'views', 'models', filename)}', 'w', encoding='utf8') as f:
            json.dump({'data': data}, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()

