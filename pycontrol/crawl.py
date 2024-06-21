from .seleniumcontrol import SeleniumControl
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException, JavascriptException

class Crawl(SeleniumControl):
    def __init__(self, browsername, parent=None):
        super().__init__(browsername, parent)
        # self.browsername
    
    def crawlControl(self, url, keywords, max=200):
        self.driver = self.initDriver()
        if not self.driver: return
        self.driver.get(url)
        count = 0
        results = []
        while count < max:
            postElm = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-describedby]')))
            attributes = postElm.get_attribute('aria-describedby').split(' ')
            itemInfos = { 'no': count }

            # post info
            postInfoElms = self.driver.find_elements(By.ID, attributes[0])
            if len(postInfoElms) > 0:
                itemInfos['url'] = []
                for postInfoElm in postInfoElms:
                    ActionChains(self.driver).move_to_element(postInfoElm).perform()
                    urlInfoElms = postInfoElm.find_elements(By.TAG_NAME, 'a')
                    if len(urlInfoElms) > 0:
                        for urlInfoElm in urlInfoElms:
                            ActionChains(self.driver).move_to_element(urlInfoElm).perform()
                            itemInfos['url'].append(urlInfoElm.get_attribute('href'))
            else:
                itemInfos['url'] = None
                self.driver.execute_script('arguments[0].remove();', postElm)
                continue

            # comments
            postCommentElm = self.driver.find_elements(By.ID, attributes[4])
            if len(postCommentElm) > 0:
                postCommentStr = postCommentElm[0].text
                postCommentNum = ''
                for ch in postCommentStr:
                    if ch.isnumeric():
                        postCommentNum += ch
                postCommentNum = int(postCommentNum)
                itemInfos['comment'] = postCommentElm[0].text
            else:
                itemInfos['comment'] = None
                postCommentNum = 0

            # description
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
                    
                itemInfos['description'] = postDesElm.text

                if hasKeyword == False and postCommentNum < 5: 
                    self.driver.execute_script('arguments[0].remove();', postElm)
                    continue

                # if hasKeyword == True:
                #     itemInfos['description'] = postDesElm.text
                # elif postCommentNum < 5:
                #     self.driver.execute_script('arguments[0].remove();', postElm)
                #         continue
                # else:
                #     itemInfos['description'] = 
                #     if postCommentNum < 5:
                #         self.driver.execute_script('arguments[0].remove();', postElm)
                #         continue
            else:
                itemInfos['description'] = None
                self.driver.execute_script('arguments[0].remove();', postElm)
                continue

            # images
            postImgsElm = self.driver.find_elements(By.ID, attributes[2])
            if len(postImgsElm) > 0:
                itemInfos['images'] = []
                postImgsElm = postImgsElm[0]
                ActionChains(self.driver).move_to_element(postImgsElm).perform()
                imgElms = postImgsElm.find_elements(By.TAG_NAME, 'img')
                for imgElm in imgElms:
                    try:
                        ActionChains(self.driver).move_to_element(imgElm).perform()
                        itemInfos['images'].append(imgElm.get_attribute('src'))
                    except JavascriptException:
                        continue

            else: itemInfos['images'] = []
            self.driver.execute_script('arguments[0].remove();', postElm)
            results.append(itemInfos)
            count += 1

        self.quitDriver()
        return results

            
if __name__ == '__main__':
    crawl = Crawl('/Users/ndb/Workspace/mymanager/bin/browsers/100090154285287')
    # crawl.crawlControl2('https://www.facebook.com/groups/feed/', ['nhà', 'khách sạn', 'thuê'], 100)
    crawl.crawlControl('https://www.facebook.com/groups/1279548102066153/', [
        "khách sạn",
        "ks",
        "4pn",
        "4 phòng ngủ",
        "homestay",
        "3wc",
        "3 nhà vệ sinh"
    ], 10)
    # crawl.crawlControl2('https://www.facebook.com/groups/feed/', [''], 1)
    