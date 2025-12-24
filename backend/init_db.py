import csv
import os
from sqlalchemy.orm import sessionmaker

from database import Base, DB_FILE, engine
from models import Region

# --- 1. 설정 ---
CSV_FILE = "daangn_all_regions.csv"


# --- 2. 초기화 및 데이터 적재 로직 ---
def import_regions_from_csv(engine):
    """CSV 파일을 읽어서 DB에 대량 삽입"""
    print(f"📂 '{CSV_FILE}' 로딩 중...")
    
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        with open(CSV_FILE, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            regions_buffer = []
            
            for row in reader:
                # CSV Row -> ORM 객체 변환
                region = Region(
                    region_code = row['region_code'],
                    id          = int(row['id']),
                    full_name   = row['full_name'],
                    name1       = row['name1'],
                    name2       = row['name2'],
                    name3       = row['name3'],
                    is_active   = True
                )
                regions_buffer.append(region)

            # Bulk Insert (속도 최적화)
            if regions_buffer:
                session.bulk_save_objects(regions_buffer)
                session.commit()
                print(f"🎉 성공! 총 {len(regions_buffer)}개의 지역 데이터가 DB에 적재되었습니다.")
            else:
                print("⚠️  CSV 파일이 비어있습니다.")

    except Exception as e:
        print(f"❌  데이터 로드 중 에러 발생: {e}")
        session.rollback()
    finally:
        session.close()


def init_database():
    print(f"🚀 당근마켓 DB 초기화 시작... ({DB_FILE})")
    
    # 엔진 생성
    # 3-1. 기존 DB 삭제 (Reset)
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print("🗑️  기존 DB 파일 삭제 완료")

    # 3-2. 테이블 생성
    Base.metadata.create_all(engine)
    print("✨  새로운 스키마 테이블 생성 완료")

    # 3-3. CSV 데이터 로드 (Seeding)
    if os.path.exists(CSV_FILE):
        import_regions_from_csv(engine)
    else:
        print(f"⚠️  경고: '{CSV_FILE}' 파일이 없습니다. 지역 데이터 없이 빈 테이블만 생성되었습니다.")
        print("    -> 먼저 지역 수집 스크립트(collect_regions.py)를 실행해주세요.")


if __name__ == "__main__":
    init_database()