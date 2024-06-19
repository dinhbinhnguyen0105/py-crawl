from seleniumcontrol import SeleniumControl
from seleniumcontrol import SeleniumControl
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, StaleElementReferenceException, ElementNotInteractableException, NoSuchElementException


class Crawl(SeleniumControl):
    def __init__(self, browsername, parent=None):
        super().__init__(browsername, parent)
    
    def crawlControl(self, url, keywords, max=200):
        self.driver = self.initDriver()
        if not self.driver: return
        self.driver.get(url)
        postElms = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[aria-describedby]')))
        # count = 0
        for postElm in postElms:
            attributes = postElm.get_attribute('aria-describedby').split(' ')
            itemInfos = []

            postInfoElm = self.driver.find_elements(By.ID, attributes[0])
            if len(postInfoElm) > 0:
                postInfoElm = postInfoElm[0]
                ActionChains(self.driver).move_to_element(postInfoElm).perform()
                urlInfoElm = postInfoElm.find_elements(By.TAG_NAME, 'a')
                if len(urlInfoElm) > 0:
                    urlInfoElm = urlInfoElm[0].get_attribute('href')
                    itemInfos.append({ 'url' : urlInfoElm })
                else: itemInfos.append({ 'url' : None})
            else: itemInfos.append({ 'url' : None})

            postDesElm = self.driver.find_elements(By.ID, attributes[1])
            if len(postDesElm) > 0:
                postDesElm = postDesElm[0]
                ActionChains(self.driver).move_to_element(postDesElm).perform()
                readMoreBtn = postDesElm.find_elements(By.CSS_SELECTOR, 'div[role="button"]')
                if len(readMoreBtn) > 0: readMoreBtn[0].click()
                itemInfos.append({ 'description' : postDesElm.text})
            else: itemInfos.append({ 'desription': None})

            postImgsElm = self.driver.find_elements(By.ID, attributes[2])
            if len(postImgsElm) > 0:
                itemInfos.append({ 'images': []})
                postImgsElm = postImgsElm[0]
                ActionChains(self.driver).move_to_element(postImgsElm).perform()
                imgElms = postImgsElm.find_elements(By.TAG_NAME, 'img')
                for imgElm in imgElms:
                    ActionChains(self.driver).move_to_element(imgElm).perform()
                    itemInfos['images'].append(imgElm.get_attribute('src'))
            else: itemInfos.append({ 'images': []})

            postInteractElm = self.driver.find_elements(By.ID, attributes[3])
            if len(postInteractElm) > 0:
                itemInfos.append({ 'interact' : postInteractElm[0].text})
            else: itemInfos.append({ 'interact' : None})

            postCommentElm = self.driver.find_elements(By.ID, attributes[4])
            if len(postCommentElm) > 0:
                itemInfos.append({ 'comment' : postCommentElm[0].text})
            else: itemInfos.append({ 'comment' : None})

            # count += 1



            # self.driver.execute_script('arguments[0].remove();', postElm)
            print(itemInfos)

    def crawlControl2(self, url, keywords, max=200):
        self.driver = self.initDriver()
        if not self.driver: return
        self.driver.get(url)
        count = 0
        results = []
        while count < max:
            postElm = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-describedby]')))
            attributes = postElm.get_attribute('aria-describedby').split(' ')
            itemInfos = { 'no': count }

            postInfoElms = self.driver.find_elements(By.ID, attributes[0])
            if len(postInfoElms) > 0:
                itemInfos['url'] = []
                for postInfoElm in postInfoElms:                
                    ActionChains(self.driver).move_to_element(postInfoElm).perform()
                    urlInfoElm = postInfoElm.find_elements(By.TAG_NAME, 'a')
                    if len(urlInfoElm) > 0:
                        urlInfoElm = urlInfoElm[0].get_attribute('href')
                        itemInfos['url'].append(urlInfoElm)
                    # else: continue
            else:
                itemInfos['url'] = None
                self.driver.execute_script('arguments[0].remove();', postElm)
                continue

            postDesElm = self.driver.find_elements(By.ID, attributes[1])
            if len(postDesElm) > 0:
                postDesElm = postDesElm[0]
                ActionChains(self.driver).move_to_element(postDesElm).perform()
                readMoreBtn = postDesElm.find_elements(By.CSS_SELECTOR, 'div[role="button"]')
                if len(readMoreBtn) > 0:
                    try:
                        readMoreBtn[0].click()
                    except ElementClickInterceptedException:
                        self.driver.execute_script('arguments[0].remove();', postElm)
                        continue
                hasKeyword = False
                for keyword in keywords:
                    if keyword in postDesElm.text:
                        hasKeyword = True
                        break
                if hasKeyword == True:
                    itemInfos['description'] = postDesElm.text
                else:
                    self.driver.execute_script('arguments[0].remove();', postElm)
                    continue
            else:
                itemInfos['desription'] = None
                self.driver.execute_script('arguments[0].remove();', postElm)
                continue

            postImgsElm = self.driver.find_elements(By.ID, attributes[2])
            if len(postImgsElm) > 0:
                itemInfos['images'] = []
                postImgsElm = postImgsElm[0]
                ActionChains(self.driver).move_to_element(postImgsElm).perform()
                imgElms = postImgsElm.find_elements(By.TAG_NAME, 'img')
                for imgElm in imgElms:
                    ActionChains(self.driver).move_to_element(imgElm).perform()
                    itemInfos['images'] = imgElm.get_attribute('src')

            else: itemInfos['images'] = []

            postInteractElm = self.driver.find_elements(By.ID, attributes[3])
            if len(postInteractElm) > 0:
                itemInfos['interact'] = postInteractElm[0].text
            else: itemInfos['interact'] = None

            postCommentElm = self.driver.find_elements(By.ID, attributes[4])
            if len(postCommentElm) > 0:
                itemInfos['comment'] = postCommentElm[0].text
            else: itemInfos['comment'] = None

            self.driver.execute_script('arguments[0].remove();', postElm)

            results.append(itemInfos)
            count += 1
        print(results)
            
if __name__ == '__main__':
    crawl = Crawl('/Users/dinhbinh/Workspace/mymanager/bin/browsers/100090154285287')
    # crawl.crawlControl('https://www.facebook.com/groups/feed/', [])
    crawl.crawlControl2('https://www.facebook.com/groups/feed/', ['nhà', 'khách sạn', 'thuê'], 1)
    # crawl.crawlControl2('https://www.facebook.com/groups/feed/', [''], 1)
    