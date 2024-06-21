import json, os, datetime, socket
from pycontrol.crawl import Crawl
from multiprocessing import Pool

PAYLOAD_PATH = os.path.join(os.path.dirname(__file__), 'payload.json')
BROWSERS_DIR = '/Users/ndb/Workspace/mymanager/bin/browsers/'
COUNT = 100

def crawlAndSave(browsername, urlTarget, keywords, port):
    browserDir = os.path.join(os.path.join(BROWSERS_DIR, browsername))
    crawl = Crawl(browserDir, port)
    data = crawl.crawlControl(urlTarget, keywords, COUNT)

    groupUID = urlTarget.split('/')[-2]
    now = datetime.datetime.now()
    filename = f'{now.month}-{now.day}.{now.hour}h{now.minute}.{browsername}-{groupUID}.json'
    with open(f'{os.path.join(os.path.dirname(__file__), 'views', 'models', filename)}', 'w', encoding='utf8') as f:
        json.dump({'data': data}, f, ensure_ascii=False, indent=4)

def main():
    with open(PAYLOAD_PATH, 'r') as f:
        payload = json.load(f)
    
    num_processes = os.cpu_count()
    print('Process vailable: ', num_processes)
    args =[]
    port = 9923
    for browser in payload['browsers']:
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                if s.connect_ex(('localhost', port)) == 0:
                    port += 1
                else: break
        print(port)
        args.append((browser['browsername'], browser['url'], payload['keywords'], port))
        port += 1

    with Pool(processes=num_processes) as pool:
        pool.starmap(crawlAndSave, args)


if __name__ == '__main__':
    main()

