import time
from selenium import webdriver
import requests
import io
from PIL import Image
from selenium.webdriver.common.by import By

web_scraper_PATH = "C:\\Users\\91773\\OneDrive\\Documents\\Coding\\Python\\Web Scraping\\chromedriver.exe"
wd = webdriver.Chrome(web_scraper_PATH)


def download_from_google_images(wd, delay, max_images):
    def scroll_bottom(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    url = "https://www.google.com/search?q=spiderman&tbm=isch&ved=2ahUKEwjU4YCg_cL0AhXOXysKHYPsD5MQ2-cCegQIABAA&oq=spi&gs_lcp=CgNpbWcQARgAMgcIABCxAxBDMgcIABCxAxBDMgQIABBDMgQIABBDMgQIABBDMgQIABBDMgQIABBDMgQIABBDMgQIABBDMgQIABBDOgUIABCABDoICAAQgAQQsQM6CAgAELEDEIMBULAIWI8SYNcZaABwAHgAgAFviAHYA5IBAzQuMZgBAKABAaoBC2d3cy13aXotaW1nsAEAwAEB&sclient=img&ei=Cp2nYdS0Gc6_rQGD2b-YCQ&bih=763&biw=1536&rlz=1C1RXQR_enIN973IN973"
    wd.get(url)
    skips = 0

    image_urls = set()
    while len(image_urls) + skips < max_images:
        scroll_bottom(wd)
        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        for img in thumbnails[len(image_urls):max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                print('Failed!')

            images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
            for image in images:
                if image.get_attribute('src') in image_urls:
                    max_images += 1
                    skips += 1
                    break
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print('Success!!')
    return image_urls


def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as c:
            image.save(c, "JPEG")
    except Exception as e:
        print('Failed!!', e)

    print('Success')


urls = download_from_google_images(wd, 1, 5)

for i, url in enumerate(urls):
    download_image("", url, str(i)+'.jpg')
wd.quit()
