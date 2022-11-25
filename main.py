# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import undetected_chromedriver as uc


# 模拟人的延迟
def human_delay(delay=2.5):
    sleep(delay)


# selenium寻找标签，并且对标签发送数据
def test1():
    service0 = Service('../tec/chromedriver')
    bro = webdriver.Chrome(service=service0)
    bro.get('https://www.taobao.com/')
    # 标签定位
    search_input = bro.find_element(by='id', value='q')
    search_input.send_keys('Iphone')

    # 执行script程序
    bro.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    sleep(2)

    # 点击搜索
    search_btn = bro.find_element(By.CLASS_NAME, value='btn-search')
    search_btn.click()

    bro.get('https://www.baidu.com')
    sleep(2)
    bro.back()

    sleep(5)
    bro.quit()


# 使用selenium对模块进行拖动
def test2():
    service0 = Service('../tec/chromedriver')
    bro = webdriver.Chrome(service=service0)
    bro.get('https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable')

    # 如果定位的标签是存在于iframe标签之中的，必须先切换到iframe，然后再定位
    bro.switch_to.frame('iframeResult')
    div = bro.find_element(By.ID, value='draggable')

    # 动作链的使用
    action = ActionChains(bro)
    action.click_and_hold(div)
    for i in range(5):
        action.move_by_offset(52, 0).perform()
        sleep(0.2)

    # 释放动作链
    action.release()
    print(div)


# selenium 模拟登录;可以键入用户名和密码，但是对于有滑块验证的情况，还没有办法解决
def test3():
    service0 = Service('../tec/chromedriver')
    bro = webdriver.Chrome(service=service0)
    bro.get('https://qzone.qq.com/')
    bro.switch_to.frame('login_frame')
    plogin = bro.find_element(By.ID, value='switcher_plogin')
    plogin.click()

    user_name = bro.find_element(By.ID, value='u')
    password = bro.find_element(By.ID, value='p')
    confirm_btn = bro.find_element(By.ID, value='login_button')

    user_name.send_keys('2906302476')
    sleep(2)
    password.send_keys('Ll7717550810')
    sleep(2)
    confirm_btn.click()

    sleep(5)
    bro.quit()


# selenium 无头浏览器测试案例,要规避被门户网站检测到的风险

def test4():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    # 实现规避监测风险
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])

    service0 = Service('../tec/chromedriver')
    bro = webdriver.Chrome(service=service0, chrome_options=chrome_options, options=option)

    bro.get('https://www.baidu.com')
    print(bro.page_source)
    bro.quit()


def login_ali():
    # 实现规避监测风险
    option = ChromeOptions()
    # 不提示现在正是程序控制
    option.add_argument('disable-infobars')
    # 设置为开发者模式，防止网站识别
    option.add_experimental_option('excludeSwitches', ['enable-automation'])

    service0 = Service('../tec/chromedriver')

    bro = uc.Chrome(version_main=107)

    # 等待时间,加载网页的等待
    wait = WebDriverWait(bro, 20, 0.5)
    # 切换窗口的等待
    wait_window = WebDriverWait(bro, 20)

    # 跳过阿里的滑块验证
    bro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })

    bro.get(
        'https://login.taobao.com/?redirect_url=https%3A%2F%2Flogin.1688.com%2Fmember%2Fjump.htm%3Ftarget%3Dhttps%253A%252F%252Flogin.1688.com%252Fmember%252FmarketSigninJump.htm%253FDone%253Dhttps%25253A%25252F%25252Fwork.1688.com%25252Fhome%25252Fseller.htm%25253Fspm%25253Da2638t.27033214.0.d12.3836436cIjk2ee&style=tao_custom&from=1688web')

    user_name = bro.find_element(By.ID, value='fm-login-id')
    password = bro.find_element(By.ID, value='fm-login-password')
    confirm_btn = bro.find_element(By.CLASS_NAME, value='password-login')

    user_name.send_keys('温州迅诚鞋业')
    human_delay()
    password.send_keys('Ll7717550810')
    human_delay()
    confirm_btn.click()

    sleep(5)
    print(bro.current_url)

    all_handles = bro.window_handles
    # 点击退货退款，进入退款页面W
    refund_entrance = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                 '//*[@id="iwc-work-topframe-viewport"]/div/div[3]/div/div[1]/div[2]/div/div/div/div/div[1]/div/div[4]/div/div/div/a')))
    # 切换到退货退款页面
    refund_entrance.click()
    wait_window.until(EC.new_window_is_opened(all_handles))
    # 切换到最新窗口
    bro.switch_to.window(bro.window_handles[-1])
    # 切换进frame里面
    bro.switch_to.frame(
        bro.find_element(By.CSS_SELECTOR, 'iframe[src="https://dispute.1688.com/refund/sellerRefundList.htm?test="]'))

    wait_receive = wait.until(EC.presence_of_element_located((By.XPATH,
                                                              '//*[@id="app-content"]/div/div[2]/div/ul/li[6]/a')))

    human_delay()
    wait_receive.click()

    # 得到退款列表
    refund_list_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'mod-refund-list')))
    refund_list_li = refund_list_div.find_elements(By.TAG_NAME, 'li')
    refund_data = {}
    if len(refund_list_li) > 0:
        for li in refund_list_li:
            refund_data[li.get_attribute('data-refund-id')] = 0
    # 进入到退款详情页
    for refund_id, flag in refund_data.items():
        a_tag = bro.find_element(By.LINK_TEXT,
                                 'href="https://trade.1688.com/order/refund/assureRefundDetail.htm?refundId=%s&userType=seller' % refund_id)
        a_tag.click()
        sleep(10)

    # 选中目标数据，搜索
    search_btn = bro.find_element(By.XPATH, value='//*[@id="refund-search-form"]/button[1]')
    # search_btn.click()

    sleep(300)
    bro.quit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    login_ali()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
