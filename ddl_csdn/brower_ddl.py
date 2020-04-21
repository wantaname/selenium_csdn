import os
import shutil
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from ddl_csdn.config import brower_path, save_path, ddl_path, my_profile


#根据不同的账户返回浏览器对象
def init_brower()->webdriver.Firefox:
    binary = brower_path

    #options = webdriver.FirefoxOptions()
    # options.add_argument()
    # 用户数据

    profile_path = my_profile
    # 加载配置数据
    profile = webdriver.FirefoxProfile(profile_path)
    # 2表示下载到自定义路径
    # profile.set_preference('browser.download.folderList', 2)
    # # 下载目录
    # profile.set_preference('browser.download.dir', ddl_path)
    #
    # # 是否显示开始下载
    # profile.set_preference('browser.download.manager.showWhenStarting', False)
    # # 对所给文件类型不询问
    # profile.set_preference('browser.helperApps.neverAsk.saveToDisk',file_type)
    brower = webdriver.Firefox(firefox_profile=profile, firefox_binary=binary)
    return brower


def download(url,driver)->dict:

    for count in range(0,2):
        driver.get(url)
        # 等待加载标题
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/div[1]/div[1]/div[1]/h3/span[1]"))
            )
        except:
            # 尝试一次
            if count == 0:
                continue
            else:
                return {
                    'result':False,
                    'msg':'加载失败！请稍后再试'
                }

        print("获取文件信息")
        try:
            score = driver.find_element_by_xpath(
                "/html/body/div[3]/div[2]/div[1]/div[1]/div[1]/dl/dd/div/div[2]/strong/span[1]/em").text
        except:
            # 尝试一次
            if count == 0:
                continue
            else:
                return {
                    'result': False,
                    'msg': '版权限制，不可下载'
                }

        file_score = int(score)
        print("所需积分:" + str(file_score))

        file_size = driver.find_element_by_xpath(
            "/html/body/div[3]/div[2]/div[1]/div[1]/div[1]/dl/dd/div/div[2]/strong/span[3]/em").text
        print("文件大小:" + file_size)

        file_title = driver.find_element_by_xpath(
            "/html/body/div[3]/div[2]/div[1]/div[1]/div[1]/h3/span[1]").text.strip()
        print("标题:" + file_title)

        try:
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "c_dl_btn"))
            )
            vip_download_btn = driver.find_element_by_class_name("c_dl_btn")
            driver.execute_script("arguments[0].click();", vip_download_btn)
        except:
            print("点击下载按钮失败！")
            # 尝试一次
            if count == 0:
                continue
            else:
                return {
                    'result':False,
                    'msg':'下载失败！请稍后再试'
                }

        try:
            element = WebDriverWait(driver, 6).until(
                EC.presence_of_element_located((By.CLASS_NAME, "dl_btn"))

            )
            vip_btn = driver.find_element_by_class_name("dl_btn")
            driver.execute_script("arguments[0].click();", vip_btn)
        except:
            # 尝试一次
            if count==0:
                continue
            else:
                #第二次仍然失败
                return {
                    'result': False,
                    'msg': '下载失败！请稍后再试'
                }

        #下载成功，处理文件
                ##处理文件
        print("正在处理文件...")
        url_id = url.split("/")[-1]
        file_name=file_handle(url_id)
        print("处理完成")

        #返回文件信息
        return {
            'result':True,
            'msg':'下载成功',
            'info':{
                'url':url,
                'file_score':file_score,
                'file_size':file_size,
                'file_title':file_title,
                'file_name':file_name
            }
        }

# 测试
# def download(url):
#     return {
#         'result':True,
#         'msg':'下载成功',
#         'info':{
#             'url':url,
#             'file_score':3,
#             'file_size':'size',
#             'file_title':'title',
#             'file_name':'name'
#         }
#     }


# 文件处理：等待文件下载完成，压缩文件，删除文件
def file_handle(url_id: str):
    """
    :param file: 文件全路径
    :return: 处理后的文件路径

    """

    download_path = ddl_path
    save_file_path =save_path

    while True:
        time.sleep(0.5)
        file_list = os.listdir(download_path)
        # 确保有文件
        if not file_list:
            continue
        if len(file_list)>1:
            continue

        if len(file_list) == 1:
            file_name =file_list[0]
            # 文件全路径
            file_path = os.path.join(download_path,file_name)

            print("下载完成")
            break
    dst_path=os.path.join(save_file_path,url_id)
    # 移动文件
    shutil.move(src=file_path,dst=dst_path)
    return file_name
    #
