import os
from .Base import *
case = os.path.basename(__file__)
file_name = os.path.splitext(case)[0]  # 去除副檔名，只留下檔名
yaml_path = os.path.join(os.getcwd(), 'data', 'env.yaml')


class Test(Base):
    def testRun(self, driver): 
        '''個人金融 > 產品介紹 > 信用卡 > 卡片介紹 > 計算頁面上所有(停發)信用卡數量並截圖'''
        WaitClickEle('burger_menu')
        WaitClickEle('product_introduction')
        WaitClickEle('product_introduction_credit_card')
        WaitClickEle('credit_card_introduction')
        scroll_to_element('disabled_card_swiper_pagination_bullet')
        element_count = CountElements('disabled_card_swiper_pagination_bullet')# 取得停發卡bullet元素數量
        xpath = get_xpath_from_yaml('disabled_card_swiper_pagination_bullet')
        for i in range(element_count):
            ClickElementByXPath(f"{xpath}[{i+1}]")
            Screenshot(f'{file_name}_{i+1}')
        logging.info('end ' + case)
