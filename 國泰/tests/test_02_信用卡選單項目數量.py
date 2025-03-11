import os
from .Base import *
case = os.path.basename(__file__)
file_name = os.path.splitext(case)[0]  # 去除副檔名，只留下檔名
yaml_path = os.path.join(os.getcwd(), 'data', 'env.yaml')


class Test(Base):
    def testRun(self, driver):
        '''點選左上角選單，進入 個人金融 > 產品介紹 > 信用卡列表，需計算有幾個項目並將畫面截圖。'''    
        WaitClickEle('burger_menu')
        WaitClickEle('product_introduction')
        WaitClickEle('product_introduction_credit_card')
        Screenshot(file_name)
        list_item_count = CountElements('product_introduction_credit_card_list_count')
        logging.info(f'{file_name}list_item_count = {str(list_item_count)}')
        logging.info('end ' + case)
