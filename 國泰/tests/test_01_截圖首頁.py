import os
from .Base import *
case = os.path.basename(__file__)
file_name = os.path.splitext(case)[0]  # 去除副檔名，只留下檔名
yaml_path = os.path.join(os.getcwd(), 'data', 'env.yaml')


class Test(Base):
    def testRun(self, driver):
        '''使用Chrome App到國泰世華銀行官網(https://www.cathaybk.com.tw/cathaybk/)並將畫面截圖'''    
        Screenshot(file_name)
        logging.info('end ' + case)
