import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import unittest


class Driver(webdriver.Chrome):

    def getelement(self, value=None, by=By.XPATH, outtime=10):
        '''
        返回xpath指向的元素，如果指向多个可见的，只返回第一个，能自动过滤网页中的隐藏元素，并且带超时等待
        :param value: xpath，或者是用其他方式查找元素依赖的参数
        :param by: 默认用xpath的方法去找，也可以根据自己的需求定义
        :param outtime: 一个作用是等待元素出现，第二是配置了超时时间,不能低于2s，有可能会导致元素获取不到
        :return: webelemnet元素
        '''
        starttime = int(time.time())
        count = 0
        while True:
            elements = self.find_elements(by=by, value=value)
            # 如果没有找到元素，循环找
            if not elements:
                time.sleep(0.1)
                nowtime = int(time.time())
                if nowtime - starttime > outtime:
                    raise TypeError('此xpath未找到元素：{}'.format(value))
                continue
            else:
                for element in elements:
                    size = element.size
                    height = size['height']
                    width = size['width']
                    # 元素大小为0，就是隐藏的元素
                    if not int(height) and not int(width):
                        continue
                    else:
                        if element.is_displayed():
                            return element
                        count += 1
                        if count == 10:
                            return element
                time.sleep(0.1)
                nowtime = int(time.time())
                if nowtime - starttime > outtime:
                    raise TypeError('此xpath指向元素是隐藏元素：{}'.format(value))

    def getelements(self, value=None, by=By.XPATH, filter=True) -> list:
        '''
        返回xpath指向的多个元素列表，默认会过滤掉隐藏的元素
        :param value: xpath
        :param by: 默认使用xpath，可以自己指定
        :param filter: 默认开启过滤
        :return: 元素列表
        '''
        elements = self.find_elements(by=by, value=value)
        if not filter:
            return elements
        else:
            reslist = []
            for element in elements:
                size = element.size
                height = size['height']
                width = size['width']
                # 元素大小为0，就是隐藏的元素
                if not int(height) and not int(width):
                    continue
                else:
                    if element.is_displayed():
                        reslist.append(element)
            return reslist

    def switch_to_window_byTagName(self, tag_name: str, timeout=10):
        """
        说明：
            切换窗口句柄(标签页)
        :param tag_name:
            1.可以使用窗口的标签页名称进行切换
        示例:
            1. driver.switch_to_window_byTagName("百度一下，你就知道")
        """
        # time_out = 10
        clock = 0
        while clock < timeout:
            for handle in self.window_handles:
                self.switch_to.window(handle)
                if self.title == tag_name:
                    # print(self.driver.title)
                    return True
            time.sleep(1)
            clock += 1
        raise TimeoutError("未找到您提供“{}”的标签名".format(tag_name))

    def waitelement(self, xpath=None, time=30, by=By.XPATH):
        '''
        等待元素出现，设置超时，需要注意iframe，需要对隐藏元素做优化,需要注意的是，首先确定xpath指向的网页元素
        是没有隐藏在网页中的，不然会立刻报错，因为selenium的等待函数是不能识别隐藏元素的
        :param xpath: 查找元素的xpath
        :param time: 查找超时时间，默认30s
        :param by: 定位元素的方法
        :return: 如果出现在网页中，返回True
                未出现，就返回False
        '''
        try:
            WebDriverWait(self, time).until(EC.presence_of_element_located((by, xpath)))
            # 解决有可能是隐藏元素的问题
            self.getelement(xpath, outtime=1)
        except:
            return False
        else:
            return True


# 对象库
class 登陆页面:
    用户名 = '//input[@name="userName"]'
    密码 = '//input[@id="password"]'
    登陆按钮 = '//input[@type="button"]'


class 首页:
    华为黄区 = '//div[@id="apDiv39"]/a[contains(text(),"新OA")]'


class 办公系统:
    考勤 = '//a[text()="考勤"]'
    个人打卡数据查询 = '//a[text()="个人打卡数据查询 "]'
    选中框 = '//td[@id="maingrid|1|r1001|c102"]'


# 页面方法
class 页面动作(object):

    def __init__(self, driver: Driver):
        self.driver = driver

    def 输入用户名(self, name):
        self.driver.getelement(登陆页面.用户名).clear()
        self.driver.getelement(登陆页面.用户名).send_keys(name)

    def 输入密码(self, psw):
        self.driver.getelement(登陆页面.密码).click()
        self.driver.getelement(登陆页面.密码).send_keys(psw)

    def 点击登陆(self):
        self.driver.getelement(登陆页面.登陆按钮).click()

    def switch_to_frame(self):
        iframe = self.driver.getelement('//iframe')
        self.driver.switch_to.frame(iframe)

    def 登陆(self, name, psw):
        self.输入用户名(name)
        self.输入密码(psw)
        self.点击登陆()


# 脚本类
class getrecord(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = Driver()
        # 设置隐示等待时间
        cls.driver.implicitly_wait(10)
        cls.driver.get('http://ics.chinasoftosg.com/SignOnServlet')
        cls.driver.maximize_window()
        cls.页面动作 = 页面动作(cls.driver)

    # @classmethod
    # def tearDownClass(cls):
    #     cls.driver.quit()

    def test_func(self):
        self.页面动作.登陆('用户名', '密码')
        self.driver.getelement(首页.华为黄区).click()
        time.sleep(2)
        self.driver.switch_to_window_byTagName('中软国际OA办公系统')
        self.driver.getelement(办公系统.考勤).click()
        time.sleep(2)
        self.页面动作.switch_to_frame()
        self.driver.getelement(办公系统.个人打卡数据查询).click()
        time.sleep(2)
        self.页面动作.switch_to_frame()
        self.driver.getelement(办公系统.选中框).click()


if __name__ == '__main__':
    unittest.main()
