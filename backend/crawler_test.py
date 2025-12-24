import requests
import urllib3
from bs4 import BeautifulSoup

# 경고 끄기
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_ethical_bot():
    url = "https://www.daangn.com/kr/buy-sell/?search=스토케"
    
    # ✅ 여기가 핵심입니다.
    # 브라우저인 척 위장(Spoofing)하는 내용을 다 지우고, 솔직하게 작성합니다.
    headers = {
        'User-Agent': 'DangnMarketStudyBot/1.0 (+mailto:saraitne11@naver.com)', 
        'Accept': '*/*', 
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }

    try:
        print(f"🤖 [윤리적 봇 모드] 접속 시도 중... \nHeader: {headers['User-Agent']}")
        
        # verify=False는 회사 보안망 때문에 유지
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.encoding = 'utf-8'
        
        print(f"📡 응답 코드: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ 성공! 당근마켓이 당신의 정직한 봇을 허용했습니다.")
            # 응답 본문을 txt 파일로 저장
            with open("response.txt", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("💾 response.txt로 저장 완료")
            # 데이터 확인
            if 'application/ld+json' in response.text:
                print("📦 데이터 수집도 가능합니다.")
                
        elif response.status_code == 403:
            print("⛔ 차단됨 (403 Forbidden)")
            print("👉 원인: robots.txt는 허용했지만, 앞단의 보안 장비(Cloudflare 등)가 '알 수 없는 봇'을 자동으로 막았습니다.")
        else:
            print(f"❓ 기타 응답: {response.status_code}")

    except Exception as e:
        print(f"❌ 에러 발생: {e}")

if __name__ == "__main__":
    test_ethical_bot()