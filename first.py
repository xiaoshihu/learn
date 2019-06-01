import time
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('http://www.esensoft.com/')
# 设置默认等待时间30s
browser.implicitly_wait(30)

button1 = browser.find_element_by_xpath('//div[@class="col-md-12 indexvideo1"]')
# 进入登陆界面
button1.click()
# print(browser.title)
# 获取当前页面的标签
windows = browser.current_window_handle
handle = browser.window_handles
for handl in handle:
    if handl != windows:
        # 切换到新的标签
        browser.switch_to.window(handl)
# print(browser.title)
button2 = browser.find_element_by_xpath('//a')
# 进入导航界面
time.sleep(0.5)
button2.click()

windows2 = browser.current_window_handle
# 定位导航界面iframe
iframe = browser.find_element_by_xpath('//div/iframe')
browser.switch_to.frame(iframe)

button3 = browser.find_elements_by_xpath('//div[@id="pagination"]/span')
button3[1].click()
# 肯定是这个地方有问题
time.sleep(0.5)
button4 = browser.find_element_by_xpath('//div[@class="swiper-slide swiper-slide-active"]//a')
button4.click()
# 打开表格应用页面
windows3 = browser.current_window_handle
win_list = [windows,windows2,windows3]
handles = browser.window_handles
for handl in handles:
    if handl not in win_list:
        # 切换到表格应用标签
        browser.switch_to.window(handl)

finds = browser.find_elements_by_xpath('//span[@class="standartTreeRow"]')
for find in finds:
    if find.get_attribute('title') == '参数查询':
        find.click()

iframe2 = browser.find_element_by_xpath('//iframe')
browser.switch_to.frame(iframe2)

area_but = browser.find_element_by_xpath('//div[@class="cmbBtOut"]')
area_but.click()
drop_down = browser.find_element_by_xpath('//div[@class="xfloatdiv_basecontainer"]')
# print(drop_down.get_attribute('id'))
areas = drop_down.find_elements_by_xpath('//div[@class="xtree_uncheck"]')
areas[0].click()
sale = browser.find_elements_by_xpath('//input[@class="html_edit"]')
sale[3].send_keys('750')
button5 = browser.find_element_by_xpath('//div[@id="WidgetParamButton40"]')
button5.click()
# 如果不等待，会抓取没有经过筛选的表的数据，能否自动等待前面的操作运行完成？
time.sleep(3)
# browser.refresh()
grid = browser.find_elements_by_xpath('//div[@id="GRID1"]//tr[@row="2"]//span')[2]
sale_num = grid.text
num = float(sale_num.replace(',',''))
# time.sleep(2)
# browser.quit()
print(num)