import os
import json
import datetime
from multiprocessing import Pool

# Giả sử Crawl là một lớp được định nghĩa ở nơi khác
from your_crawl_module import Crawl

# Hàm để thực hiện crawl và lưu dữ liệu
def crawl_and_save(browser, payload, BROWSERS_DIR):
    browserDir = os.path.join(os.path.join(BROWSERS_DIR, browser['browsername']))
    crawl = Crawl(browserDir)
    data = crawl.crawlControl(browser['url'], payload['keywords'], 3)

    groupUID = browser['url'].split('/')[-2]
    now = datetime.datetime.now()
    filename = f'{now.month}-{now.day}.{now.hour}h{now.minute}.{browser["browsername"]}-{groupUID}.json'
    
    # Đảm bảo đường dẫn tồn tại
    output_dir = os.path.join(os.path.dirname(__file__), 'views', 'models')
    os.makedirs(output_dir, exist_ok=True)
    
    with open(os.path.join(output_dir, filename), 'w', encoding='utf8') as f:
        json.dump({'data': data}, f, ensure_ascii=False, indent=4)

def main(payload, BROWSERS_DIR):
    # Số lượng tiến trình có thể thay đổi tùy thuộc vào hệ thống của bạn
    num_processes = os.cpu_count()  # Hoặc số lượng tiến trình bạn muốn sử dụng

    # Tạo đối số cho mỗi tiến trình
    args = [(browser, payload, BROWSERS_DIR) for browser in payload['browsers']]

    # Sử dụng multiprocessing Pool để chạy các tiến trình song song
    with Pool(processes=num_processes) as pool:
        pool.starmap(crawl_and_save, args)

if __name__ == "__main__":
    # Định nghĩa payload và BROWSERS_DIR theo cấu trúc của bạn
    payload = {
        "browsers": [
            # Thêm các trình duyệt cần crawl ở đây
            {"browsername": "chrome", "url": "http://example.com"}
            # ...
        ],
        "keywords": ["keyword1", "keyword2"]
    }
    
    BROWSERS_DIR = "/path/to/browsers/dir"

    main(payload, BROWSERS_DIR)
