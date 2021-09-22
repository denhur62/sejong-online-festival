import requests
from bs4 import BeautifulSoup as bs


class SejongAuth:

    def __init__(self):
        self.TIMEOUT_SEC = 3

    def do_sejong(self, id: str, pw: str):
        header = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)\
            AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
            "Accept":"text/html,application/xhtml+xml,application/xml;\
            q=0.9,imgwebp,*/*;q=0.8"
        }
        data = {
            'email': id,
            'password': pw
        }

        with requests.Session() as s:
            html = s.post(
                "https://do.sejong.ac.kr/ko/process/member/login", 
                headers=header, data=data, timeout=self.TIMEOUT_SEC
            ).content
            html = s.get(
                "https://do.sejong.ac.kr/", 
                timeout=self.TIMEOUT_SEC
            ).text
            soup = bs(html, "html.parser")
            soup = soup.select("div.info")
            if soup == []: 
                return {"result": False}
            name = soup[0].find("b").get_text().strip()
            major = soup[0].find("small").get_text().strip().split(" ")[1]
            return {
                "result": True,
                "name": name,
                "id": id,
                "major": major
            }

    def portal_sejong(self, id: str, pw: str):
        header = {
            "Referer": "https://portal.sejong.ac.kr",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
        }
        data = {
            "id": id,
            "password": pw,
            'rtUrl': '',
        }
        with requests.Session() as s:
            s.post(
                'https://portal.sejong.ac.kr/jsp/login/login_action.jsp', 
                headers=header, data=data, timeout=self.TIMEOUT_SEC
            )
            res = s.get('https://portal.sejong.ac.kr/main.jsp', timeout=self.TIMEOUT_SEC)
            soup = bs(res.content, 'html.parser')
            name = soup.select_one('div.info0 > div')
            if name is None: 
                return {"result":False}
            name = name.get_text().split("(")[0]
            return {
                "result": True,
                "name": name,
                "id": id,
            }


if __name__ == '__main__':
    auth = SejongAuth()
    id, pw = "16011089", "1234"
    print(auth.do_sejong(id, pw))
    print(auth.portal_sejong(id, pw))
