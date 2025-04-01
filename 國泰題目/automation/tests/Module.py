import os, logging, yaml, time
from selenium.webdriver.common.by import By
from pathlib import Path
from selenium.webdriver.support.wait import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class Module:
    def __init__(self):
        '''啟動時自動導入'''
        self.LoadData()
# WebDriver 控制類別 ===================================================================================================================

    def InIDiver(self, driver):
        '''透過外部參數導入 driver'''
        self.driver = driver

    def GoToWindow(self, url):
        '''開啟當前視窗'''
        try:
            self.driver.get(url)
            logging.info(f'{url}，GoToWindow Success')
        except Exception as e:
            logging.error(str(e))

    def GetEleExceptionEle(self, ele_name, sleep_time=30):
        '''隱式等待 + 讀取物件設定'''
        try:
            ele_info = self.elementsData[ele_name]
            ele_value = ele_info['value']
        except KeyError:
            logging.error(f"{ele_name} Incorrect setting!")
            raise Exception(f"{ele_name} Incorrect setting!")
        try:
            element = WDW(self.driver, sleep_time).until(EC.presence_of_element_located((By.XPATH, ele_value)))
            return element
        except Exception as e:
            return None

    def GetElementByXPath(self, xpath):
        '''直接使用 XPath 查找元素，無需依賴 YAML 檔案'''
        try:
            # 使用 XPath 查找元素
            element = self.driver.find_element(By.XPATH, xpath)
            return element
        except Exception as e:
            logging.error(f"Error finding element with XPath '{xpath}': {str(e)}")
            return None
        
    def CountElements(self, ele_name):
        """計算符合 XPath 條件的元素數量"""
        ele_info = self.elementsData[ele_name]
        ele_value = ele_info['value']
        try:
            elements = self.driver.find_elements(By.XPATH, ele_value)  
            return len(elements)  # 回傳子元素數量
        except:
            logging.info(ele_name + ' - CountChildElements Fail')
            return None

    def CountChildElements(self, parent_ele_name, child_tag):
        """
        計算某個父元素下符合 XPath 條件的子元素數量"""
        try:
            # 取得父元素的 XPath
            parent_info = self.elementsData[parent_ele_name]
            parent_value = parent_info['value']
            # 找到父元素
            parent_element = self.driver.find_element(By.XPATH, parent_value)
            # 在父元素內查找指定標籤的子元素
            elements = parent_element.find_elements(By.TAG_NAME, child_tag)
            return len(elements)  # 回傳符合條件的子元素數量
        except Exception as e:
            logging.error(f"{parent_ele_name} - CountElements Fail: {e}")
            return None


# 網頁操作 ===================================================================================================================

    def WaitClickEle(self, eleName, img=True, raise_exception=True, timeout=30):
        '''隱式等待 + click 以及新增是否要跳出錯誤訊息的開關，並可調整等待時間'''
        ele = self.GetEleExceptionEle(eleName, sleep_time=timeout)
        
        if ele is None:  # GetEleExceptionEle = None 時觸發
            if raise_exception:
                self.dealError('WaitClickEle', eleName, img)
        else:
            try:
                ele.click()
                time.sleep(1)
                logging.info(eleName + ' - WaitClickEle Success')
            except Exception as e:
                if raise_exception:
                    self.exc('WaitClickEle', eleName, e, img)

    def ClickElementByXPath(self, xpath):
        '''使用指定的 XPath 查找並點擊一個符合的元素，可選擇從父元素查找。'''
        try:
            # 使用 GetElementByXPath 函數來獲取元素
            element = self.GetElementByXPath(xpath)
            # 如果找到的元素不為空，則點擊
            if element:
                try:
                    element.click()
                    logging.info(f"{xpath} - ClickEle Success")
                except Exception as e:
                    logging.error(f"Failed to click element found by XPath: {xpath} - {str(e)}")
            else:
                logging.warning(f"No element found for XPath: {xpath} to click.")
                    
        except Exception as e:
            logging.error(f"Error in ClickElementByXPath with XPath '{xpath}' - {str(e)}")

    def scroll_to_element(self, ele_name):
        """滾動到指定元素"""
        actions = ActionChains(self.driver)
        ele_info = self.elementsData[ele_name]
        ele_value = ele_info['value']
        element = self.driver.find_element(By.XPATH, ele_value)
        actions.move_to_element(element).perform()


# 截圖與錯誤記錄 ===================================================================================================================      

    def ImageDict(self):
        """獲取 image 資料夾的絕對路徑。"""
        # 獲取基本 image 資料夾的路徑
        basePath = os.path.abspath(os.path.join(os.getcwd(), "image"))
        # 如果資料夾不存在，則創建該資料夾
        if not os.path.isdir(basePath):
            os.makedirs(basePath)
        # 返回資料夾的絕對路徑
        return basePath
    
    def screenshot(self, filename):
        """截圖到指定資料夾"""
        # 使用指定的資料夾（可包含子資料夾）
        filenamePath = os.path.join(self.ImageDict(), filename + '.png')
        self.driver.get_screenshot_as_file(filenamePath)

    def Screenshot(self, name):
        image_name = name + self.GetTimeStr()
        self.screenshot(image_name)  # 截圖保存到指定子資料夾
        logging.info(image_name + ' - Screenshot Success')

# 資料讀取與設定 ===================================================================================================================
    def GetTimeStr(self):
        '''取得當前日期'''
        time.sleep(1)
        now = time.strftime(r"_%Y-%m-%d")
        return now

    def LoadData(self):
        '''從 cwd 或 __file__ 自動抓取 YAML，不受執行目錄影響'''

        # 可能從 Jenkins、本地國泰題目、或其他地方執行
        path_from_cwd = Path.cwd() / "國泰題目" / "automation" / "data" / "Page.yaml"
        path_from_module = Path(__file__).parent.parent / "data" / "Page.yaml"

        if path_from_cwd.exists():
            path = path_from_cwd
            print(f"[INFO] 使用 cwd 路徑載入：{path}")
        elif path_from_module.exists():
            path = path_from_module
            print(f"[INFO] 使用模組相對路徑載入：{path}")
        else:
            print("[ERROR] 找不到 Page.yaml，請確認路徑或啟動目錄是否正確")
            return

        try:
            with path.open(encoding="utf-8") as f:
                self.elementsData = yaml.safe_load(f)
        except yaml.YAMLError as e:
            logging.error(e)

    def env(self, key):
        '''從 cwd 或 Module.py 相對路徑讀取 data/env.yaml 並回傳對應 key'''
        
        # 嘗試從執行目錄找
        path_from_cwd = Path.cwd() / "國泰題目" / "automation" / "data" / "env.yaml"

        # fallback：從 Module.py 相對路徑找
        path_from_module = Path(__file__).parent.parent / "data" / "env.yaml"

        if path_from_cwd.exists():
            path = path_from_cwd
            print(f"[INFO] 使用 cwd 路徑載入 env.yaml：{path}")
        elif path_from_module.exists():
            path = path_from_module
            print(f"[INFO] 使用模組相對路徑載入 env.yaml：{path}")
        else:
            print("[ERROR] 找不到 env.yaml，請確認路徑是否正確")
            return None

        try:
            with path.open(encoding="utf-8") as f:
                env_config = yaml.safe_load(f)
                return env_config.get(key)
        except Exception as e:
            logging.error(f"載入 env.yaml 發生錯誤：{e}")
            return None
    
    def get_xpath_from_yaml(self, ele_name):
        ele_info = self.elementsData[ele_name]
        ele_value = ele_info['value']
        return ele_value




mod = Module()
Screenshot = mod.Screenshot
WaitClickEle = mod.WaitClickEle
GoToWindow = mod.GoToWindow
env = mod.env
InIDiver = mod.InIDiver
CountElements = mod.CountElements
scroll_to_element = mod.scroll_to_element
CountChildElements = mod.CountChildElements
ClickElementByXPath = mod.ClickElementByXPath
get_xpath_from_yaml = mod.get_xpath_from_yaml