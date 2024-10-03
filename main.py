import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 크롬 드라이버 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # 백그라운드 실행 (옵션)
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# 드라이버 설정
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def search_youtube(song_title, gender):
    query = f"{song_title} {gender} 커버"
    search_url = f"https://www.youtube.com/results?search_query={query}"
    
    print(f"유튜브에서 '{query}'로 검색 중...")

    # 유튜브 검색 결과 페이지 접속
    driver.get(search_url)
    time.sleep(3)  # 페이지 로딩 대기
    print("검색 결과 페이지 로딩 완료.")

    # 검색 결과에서 영상 링크, 채널 이름, 썸네일 이미지 수집
    video_links = []
    channel_names = []
    thumbnail_urls = []
    
    videos = driver.find_elements(By.XPATH, '//*[@id="video-title"]')
    channels = driver.find_elements(By.XPATH, '//*[@id="text"]/a')
    thumbnails = driver.find_elements(By.XPATH, '//*[@id="img"]')

    print(f"총 {len(videos)}개의 영상 정보 수집 중...")

    for video, channel, thumbnail in zip(videos, channels, thumbnails):
        video_links.append(video.get_attribute('href'))
        channel_names.append(channel.text)
        thumbnail_urls.append(thumbnail.get_attribute('src'))

    print(f"영상 링크 및 채널 이름, 썸네일 이미지 URL 수집 완료. ({len(video_links)}개)")

    return video_links, channel_names, thumbnail_urls

def save_to_excel(data, song_title, gender):
    # 파일명을 곡명과 성별을 이용해 동적으로 생성
    filename = f"{song_title}_{gender}_1차수집.xlsx"
    
    # Pandas 데이터프레임으로 변환 후 CSV 저장
    df = pd.DataFrame(data, columns=['Video Link', 'Channel Name', 'Thumbnail URL'])
    df.to_excel(filename, index=False)
    print(f"결과를 '{filename}' 파일로 저장했습니다.")

if __name__ == "__main__":
    # 검색어와 성별 설정 (사용자가 직접 입력)
    song_title = input("곡명을 입력하세요: ")
    gender = input("성별을 입력하세요 (예: 남자, 여자): ")

    print(f"'{song_title}' 곡의 '{gender}' 커버 영상을 수집합니다...")

    # 유튜브 검색 및 데이터 수집
    video_links, channel_names, thumbnail_urls = search_youtube(song_title, gender)

    # 결과를 CSV로 저장
    data = list(zip(video_links, channel_names, thumbnail_urls))
    save_to_excel(data, song_title, gender)

    # 크롬 드라이버 종료
    driver.quit()
    print("크롬 드라이버 종료 완료.")
