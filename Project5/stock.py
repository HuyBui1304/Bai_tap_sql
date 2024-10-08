from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import sqlite3

######################################################
# 0. Tạo cơ sở dữ liệu
conn = sqlite3.connect('stock.db')
c = conn.cursor()
try:
    c.execute('''
        CREATE TABLE IF NOT EXISTS stock (
            id integer primary key autoincrement,
            _date text,
            open_price integer,
            highest_price integer,
            lowest_price integer,
            closing_price integer,
            changed_price integer,
            price_change_percentage integer,
            changed_volume integer
        )
    ''')
except Exception as e:
    print(e)

def insert_data(_date, open_price, highest_price, lowest_price, closing_price, changed_price, price_change_percentage, changed_volume):
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()
    # Thêm dữ liệu vào cơ sở dữ liệu
    c.execute('''
        INSERT INTO stock(_date, open_price, highest_price, lowest_price, closing_price, changed_price, price_change_percentage, changed_volume)
        VALUES (:_date, :open_price, :highest_price, :lowest_price, :closing_price, :changed_price, :price_change_percentage, :changed_volume)
    ''',
      {
          '_date': _date,
          'open_price': open_price,
          'highest_price': highest_price,
          'lowest_price': lowest_price,
          'closing_price': closing_price,
          'changed_price': changed_price,
          'price_change_percentage': price_change_percentage,
          'changed_volume': changed_volume,
      })
    conn.commit()
    conn.close()

######################################################
# 1. Thu thập dữ liệu
# Khởi tạo Webdriver

# Đường dẫn đến file thực thi chromedriver
chrome_path = "/Users/buiminhhuy/Downloads/chromedriver-mac-arm64/chromedriver"

# Khởi tạo đối tượng dịch vụ với đường dẫn chromedriver
ser = Service(chrome_path)

# Tạo tùy chọn cho Chrome
options = webdriver.ChromeOptions()
# Thiết lập chế độ không đầu (headless) nếu cần thiết
options.headless = False

# Khởi tạo driver
driver = webdriver.Chrome(options=options, service=ser)

# Truy cập trang web cần lấy dữ liệu
driver.get("https://simplize.vn/co-phieu/SAB/lich-su-gia")
time.sleep(5)

# Lấy toàn bộ hàng trong bảng
rows = driver.find_elements(By.CSS_SELECTOR, ".simplize-table-row.simplize-table-row-level-0")
print(rows)
print(len(rows))
for row in rows:
    columns = row.find_elements(By.TAG_NAME, "td")
    _date = columns[0].text
    open_price = columns[1].text.replace(",", "")
    highest_price = columns[2].text.replace(",", "")
    lowest_price = columns[3].text.replace(",", "")
    closing_price = columns[4].text.replace(",", "")
    changed_price = columns[5].text.replace(",", "")
    if (changed_price == '-'):
        changed_price = 0
    price_change_percentage = columns[6].text.replace(",", "")
    if (price_change_percentage == '-'):
        price_change_percentage = 0
    changed_volume = columns[7].text.replace(",", "")

    insert_data(_date, open_price, highest_price, lowest_price, closing_price, changed_price, price_change_percentage, changed_volume)

# Đóng driver
driver.quit()

# Câu 1
# SELECT
#     _date
# FROM
#     stock s
# WHERE
#     s.closing_price = (SELECT max(closing_price) from stock);