import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


while True:
    try:
        count = 0
        options = webdriver.ChromeOptions()
        # options.add_argument("headless")

        driver = webdriver.Chrome('C:\chromedriver.exe', options=options)
        driver.implicitly_wait(10)
        driver.get('https://bible.ctm.kr/')
        driver.implicitly_wait(10)

        driver.switch_to.frame('ctmhome')
        print('open success')

        driver.find_element_by_name('id').send_keys('hj9413')
        time.sleep(3)
        driver.find_element_by_name('pwd').send_keys('hj441015')
        time.sleep(3)
        print('enter account')

        driver.find_element_by_xpath('/html/body/center/table/tbody/tr/td/table/tbody/tr/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/input').click()
        driver.implicitly_wait(10)
        print('click login')

        driver.switch_to.frame('ctmhome')
        print('login success')

        bibles = driver.find_elements_by_xpath(".//td[contains(@onclick, 'gotype_bible')]")
        driver.implicitly_wait(10)
        unread_bibles = [b for b in bibles if '통독완료' not in b.text]
        unread_bibles[0].click()
        driver.implicitly_wait(10)
        print('click unread bible')
        time.sleep(3)

        driver.implicitly_wait(15) # TODO: 20

        frame_name = driver.find_element_by_name('l').get_attribute('value')

        driver.switch_to.frame('shFrame' + frame_name)
        driver.implicitly_wait(5)

        targets = driver.find_elements_by_xpath(".//span[contains(@id, 'sp')]")
        blanks = driver.find_elements_by_xpath(".//input[contains(@name, 'bscript')]")

        i = 0
        retry_count = 0
        while i < len(targets):
            target, blank = targets[i], blanks[i]

            try:
                blank_element = driver.find_element_by_name(blank.get_attribute('name'))
                driver.implicitly_wait(3)
                blank_element.send_keys(target.text)
                print('[{}/{}]: {}'.format(i + 1, len(targets), target.text))
                time.sleep(0.1)
                blank_element.send_keys(Keys.ENTER)
                time.sleep(0.2)

                i += 1

            except Exception as e:
                print(e)
                time.sleep(1)
                i -= 1
                retry_count += 1

                if retry_count == 30:
                    raise ValueError

            count += 1

        # driver.find_element_by_xpath('/html/body/center/form/table[2]/tbody/tr[5]/td/a/img').click()
        print('DONE')
        time.sleep(5)

    except Exception as e:
        pass

    time.sleep(1)
    driver.close()
    driver.quit()

    time.sleep(5)