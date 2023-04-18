import requests
from bs4 import BeautifulSoup

#Setup User-Agent cho trang web vietnamnet.vn, đối với mỗi máy tính sẽ có một User-Agent khác nhau
#Nên nếu muốn tìm User-Agent của máy tính của mình, ta sẽ làm các bước sau:
#Bấm F12 --> Vào Tab "Network" --> Bấm F5 --> Tìm ra trang web nào có tên giống với trang web hiện tại --> Ở mục "Headers", lướt xuống sẽ có mục "Request-Headers" --> Tìm ra User-Agent ạ
request_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.123 Safari/537.36'}

#Tạo hàm bai_viet() có tham số là url: các link của bài viết
def bai_viet(url):
    r = requests.get(url, headers=request_headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    div = soup.find_all('div', class_='ArticleDetail w-660 d-ib') 
    
    #Tìm ra những thẻ, nội dung không liên quan tới bài viết và sử dụng vòng lặp và hàm decompose() để xóa toàn bộ đi
    unrelated_div = soup.find_all('div', class_=["article-relate","template-ReferToMore right","inner-article"])
    for x in range(len(unrelated_div)):
        unrelated_div[x].decompose() 

    #Tìm thẻ span chứa nội dung là ngày và giờ. Vì khi .text thì có khoảng cách lớn
    # --> Giải pháp: sử dụng hàm join() và split() để có thể đọc dễ dàng hơn
    strings = soup.find_all('span', class_='ArticleDate')[0].text 
    ngay_gio = " ".join(strings.split())
    noi_dung = ""

    #Đặt tên cho file .txt có chứa tên của url. Vì khi xuất ra file .txt thì có lỗi là không được sử dụng các ký hiệu đặc biệt (VD: / \ * : ?)
    # --> Giải pháp: Thay các ký hiệu đó bằng ký hiệu thường để có thể lưu được tên file .txt giống với tên của url 
    file_name = url.replace('/','-').replace(':','')
    f = open(file_name + '.txt', 'w+', encoding='UTF-8') 
    for info in div:
        tieu_de = info.find('h1', class_='title f-22 c-3e').text
        phong_vien = info.find_all('p')[-1].text   #Qua các bước xử lý thẻ không liên quan, thì ta nhận ra thẻ <p> cuối cùng thường là tên phóng viên --> chọn giá trị [-1]
        nd = info.find_all(['p','td'])[:-1]    #Tìm lần lượt tất cả các thẻ <p> và thẻ <td> --> giá trị [-1] là tên tác giả nên [:-1] là lấy hết ngoại trừ giá trị -1
        for x in nd:   #Chạy vòng lặp để chuyển thành văn bản của các phần tử trong danh sách nd
            noi_dung += x.text   #Các phần tử đó lần lượt thêm vào biến noi_dung có dạng là str
        f.write('Tiêu đề bản tin: ' + tieu_de + '\nNgày giờ: ' + ngay_gio + '\nNội dung: ' + noi_dung + '\nPhóng viên đưa tin: ' + phong_vien)  
        #Viết lần lượt giá trị vào file .txt mà ta đã tạo, nếu tên file .txt chưa được tạo, máy tính sẽ tự động khởi tạo 1 file .txt mới có tên là file_name
    f.close() #Đóng file .txt

#Mở file .txt mà có chứa các đường link của trang web vietnamnet.vn
f_url = open('url_file.txt', 'r')
url_links = f_url.readlines()   #readline() giúp ta có thể đọc riêng từng dòng một trong file .txt 
cac_bai_viet = []  #Định nghĩa biến cac_bai_viet là ở dạng danh sách 


#Chạy vòng lặp để xóa các giá trị \n trong các phần tử của danh sách cac_bai_viet
for n in url_links: 
    cac_bai_viet.append(n.strip())

#KQ trả về là:
# cac_bai_viet =['https://vietnamnet.vn/vn/the-thao/euro/keo-y-vs-anh-keo-chung-ket-euro-2020-bat-ngo-azzurri-754774.html', 
#                 'https://vietnamnet.vn/vn/cong-nghe/vien-thong/huong-dan-cach-dang-ky-tiem-vac-xin-covid-19-qua-so-suc-khoe-dien-tu-754775.html',
#                 'https://vietnamnet.vn/vn/tuanvietnam/tieudiem/khi-trung-quoc-tro-lai-la-mot-trung-tam-quyen-luc-cua-the-gioi-754511.html',
#                 'https://vietnamnet.vn/vn/cong-nghe/ung-dung-cong-nghe-de-cong-khai-minh-bach-thong-tin-chien-dich-tiem-vac-xin-covid-19-754608.html',
#                 'https://vietnamnet.vn/vn/kinh-doanh/tai-chinh/trung-doc-dac-vietlott-hon-35-ty-dong-755006.html',
#                 'https://vietnamnet.vn/vn/kinh-doanh/thi-truong/nguon-goc-dac-san-luon-nhat-nuong-bao-ngu-kho-gia-re-754803.html',
#                 'https://vietnamnet.vn/vn/thoi-su/pho-thu-tuong-uu-tien-lon-nhat-voi-tp-hcm-hien-nay-la-giu-khoang-cach-nguoi-voi-nguoi-754942.html',
#                 'https://vietnamnet.vn/vn/giao-duc/guong-mat-tre/do-bach-khoa-giai-nhat-hoc-sinh-gioi-quoc-gia-mon-toan-732121.html',
#                 'https://vietnamnet.vn/vn/giao-duc/nguoi-thay/dh-bach-khoa-ly-giai-viec-lay-diem-sat-1520-cao-hon-ca-dai-hoc-my-744355.html',
#                 'https://vietnamnet.vn/vn/the-gioi/the-gioi-do-day/ca-si-bi-ban-tu-vong-trong-khi-livestream-tren-mang-755001.html',
#                 ]


#Chạy vòng lặp và sử dụng hàm bai_viet() để trích xuất từng url vào từng file .txt một
for x in range(len(cac_bai_viet)):
    bai_viet(cac_bai_viet[x])