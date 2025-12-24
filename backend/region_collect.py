import requests
import csv
import time
import random
import urllib3

# SSL 경고 끄기
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 1. 설정 ---
OUTPUT_FILE = "daangn_all_regions.csv"

# ✅ [중요] 봇 정보 입력
# 본인의 이메일 주소나 프로젝트 저장소 주소 등을 적어주세요.
BOT_USER_AGENT = 'DangnRegionCollector/1.0 (Toy Project; +mailto:saraitne@gmail.com)'

# 검색할 키워드 (전국 주요 시/군/구)
SEARCH_KEYWORDS = [
    # 서울 (구)
    "강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구",
    "노원구", "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구",
    "성북구", "송파구", "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구",
    # 경기 (시/군)
    "수원시", "성남시", "의정부시", "안양시", "부천시", "광명시", "평택시", "동두천시",
    "안산시", "고양시", "과천시", "구리시", "남양주시", "오산시", "시흥시", "군포시",
    "의왕시", "하남시", "용인시", "파주시", "이천시", "안성시", "김포시", "화성시",
    "광주시", "양주시", "포천시", "여주시", "연천군", "가평군", "양평군",
    # 인천 및 광역시 (구/군)
    "인천광역시", "대전광역시", "대구광역시", "부산광역시", "광주광역시", "울산광역시", "세종특별자치시",
    # 강원
    "춘천시", "원주시", "강릉시", "동해시", "태백시", "속초시", "삼척시", "홍천군", "횡성군",
    "영월군", "평창군", "정선군", "철원군", "화천군", "양구군", "인제군", "고성군", "양양군",
    # 충청
    "청주시", "충주시", "제천시", "천안시", "공주시", "보령시", "아산시", "서산시", "논산시", "계룡시", "당진시",
    "금산군", "부여군", "서천군", "청양군", "홍성군", "예산군", "태안군", "괴산군", "단양군", "보은군", "영동군", "옥천군", "음성군", "진천군", "증평군",
    # 전라
    "전주시", "군산시", "익산시", "정읍시", "남원시", "김제시", "목포시", "여수시", "순천시", "나주시", "광양시",
    "고창군", "부안군", "완주군", "임실군", "장수군", "진안군", "무주군", "순창군",
    "담양군", "곡성군", "구례군", "고흥군", "보성군", "화순군", "장흥군", "강진군", "해남군", "영암군", "무안군", "함평군", "영광군", "장성군", "완도군", "진도군", "신안군",
    # 경상
    "포항시", "경주시", "김천시", "안동시", "구미시", "영주시", "영천시", "상주시", "문경시", "경산시",
    "창원시", "진주시", "통영시", "사천시", "김해시", "밀양시", "거제시", "양산시",
    "의성군", "청송군", "영양군", "영덕군", "청도군", "고령군", "성주군", "칠곡군", "예천군", "봉화군", "울진군", "울릉군",
    "의령군", "함안군", "창녕군", "고성군", "남해군", "하동군", "산청군", "함양군", "거창군", "합천군",
    # 제주
    "제주시", "서귀포시"
]

def collect_regions_politely():
    url = "https://www.daangn.com/v1/api/search/kr/location"
    
    # ✅ 정직한 헤더 설정
    headers = {
        'User-Agent': BOT_USER_AGENT, 
        'Referer': 'https://www.daangn.com/',
        'Accept': 'application/json'
    }
    
    seen_ids = set() # 중복 체크용
    
    # UTF-8-SIG: 엑셀에서 한글 안 깨지게 저장
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['region_code', 'id', 'full_name', 'name1', 'name2', 'name3']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        print(f"🚀 [Polite Bot] 전국 지역 ID 수집 시작 (총 {len(SEARCH_KEYWORDS)}개 지역 검색)")
        print(f"📝 봇 식별자: {BOT_USER_AGENT}")
        print("-" * 60)

        for i, keyword in enumerate(SEARCH_KEYWORDS):
            try:
                # 진행률 표시
                print(f"[{i+1}/{len(SEARCH_KEYWORDS)}] 🔍 '{keyword}' 검색 중...", end=" ")
                
                params = {'keyword': keyword}
                
                # verify=False는 회사/보안망 환경 때문에 유지
                response = requests.get(url, headers=headers, params=params, verify=False, timeout=10)
                
                if response.status_code == 200:
                    locations = response.json().get('locations', [])
                    new_count = 0
                    
                    for loc in locations:
                        if loc['id'] in seen_ids:
                            continue
                        
                        seen_ids.add(loc['id'])
                        
                        # 우리가 필요한 포맷: "동네이름-ID"
                        region_code = f"{loc['name']}-{loc['id']}"
                        full_name = f"{loc['name1']} {loc['name2']} {loc['name3']}"
                        
                        writer.writerow({
                            'region_code': region_code,
                            'id': loc['id'],
                            'full_name': full_name,
                            'name1': loc['name1'],
                            'name2': loc['name2'],
                            'name3': loc['name3']
                        })
                        new_count += 1
                    
                    print(f"✅ {new_count}개 추가 (누적 {len(seen_ids)}개)")
                else:
                    print(f"❌ 실패 (Status: {response.status_code})")

                # ✅ [핵심] 서버 부하 방지를 위한 랜덤 대기 (1.5 ~ 3.5초)
                sleep_time = random.uniform(1.5, 3.5)
                time.sleep(sleep_time)

            except Exception as e:
                print(f"\n⚠️ 에러 발생 ({keyword}): {e}")
                time.sleep(5) # 에러 나면 좀 더 오래 쉬기

    print("-" * 60)
    print(f"🎉 수집 완료! '{OUTPUT_FILE}' 파일에 총 {len(seen_ids)}개의 지역 정보가 저장되었습니다.")

if __name__ == "__main__":
    collect_regions_politely()