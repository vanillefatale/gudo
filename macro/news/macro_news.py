import requests
import feedparser
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import re
import time
import logging
import os
from dotenv import load_dotenv
import openai
import random

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# OpenAI API 키 설정
load_dotenv()  # .env에서 OPENAI_API_KEY 로드
openai.api_key = os.getenv("OPENAI_API_KEY")

class MacroNewsCollector:
    def __init__(self):
        self.today_date = datetime.now().strftime('%y%m%d')
        self.news_data = {
            "US": [],
            "China": [],
            "Russia": [],
            "Korea": [],
            "Japan": [],
            "Europe": [],
            "MiddleEast": [],
            "SoutheastAsia": [],
            "Others": []
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9,ko;q=0.8',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive'
        }
    
    def collect_global_news(self):
        """글로벌 뉴스 소스에서 데이터 수집"""
        logger.info("글로벌 뉴스 수집 시작")
        self._collect_bloomberg()
        time.sleep(random.uniform(1, 3))  # 무작위 지연 추가
        self._collect_cnbc()
        time.sleep(random.uniform(1, 3))
        self._collect_reuters()
        logger.info("글로벌 뉴스 수집 완료")
        
    def collect_korean_news(self):
        """국내 뉴스 소스에서 데이터 수집"""
        logger.info("국내 뉴스 수집 시작")
        self._collect_hankyung()
        time.sleep(random.uniform(1, 3))
        self._collect_yonhap()
        time.sleep(random.uniform(1, 3))
        self._collect_edaily()
        logger.info("국내 뉴스 수집 완료")

    def _make_request(self, url, max_retries=3):
        """요청 재시도 로직이 포함된 요청 함수"""
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    return response
                elif response.status_code == 403:
                    logger.warning(f"접근 거부 (403): {url} - 다른 헤더로 재시도 중...")
                    # 헤더 변경 시도
                    self.headers['User-Agent'] = f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(100, 120)}.0.0.0 Safari/537.36'
                elif response.status_code == 404:
                    logger.error(f"페이지 찾을 수 없음 (404): {url}")
                    return None
                else:
                    logger.warning(f"요청 실패 ({response.status_code}): {url} - 재시도 중...")
                
                # 재시도 간 지연
                time.sleep(random.uniform(2, 5))
            except Exception as e:
                logger.warning(f"요청 중 오류 발생: {str(e)} - 재시도 중...")
                time.sleep(random.uniform(2, 5))
        
        logger.error(f"최대 재시도 횟수 초과: {url}")
        return None

    def _collect_bloomberg(self):
        """Bloomberg 뉴스 크롤링"""
        try:
            logger.info("Bloomberg 뉴스 수집 중...")
            
            # 마켓 뉴스 수집
            url = "https://www.bloomberg.com/markets"
            response = self._make_request(url)
            
            if response:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Top News 섹션 수집
                news_items = soup.select('article h3 a')
                
                if not news_items:
                    # 대체 선택자 시도
                    news_items = soup.select('.story-list-story__info__headline-link')
                
                for item in news_items[:10]:  # 상위 10개 뉴스만 수집
                    title = item.text.strip()
                    link = f"https://www.bloomberg.com{item['href']}" if item.get('href', '').startswith('/') else item.get('href', '')
                    
                    news_item = {
                        'title': title,
                        'link': link,
                        'source': 'Bloomberg',
                        'published': datetime.now().strftime('%Y-%m-%d'),
                    }
                    
                    # 국가별 분류
                    self._categorize_news(news_item)
            else:
                logger.error("Bloomberg 접속 실패")
                
                # 백업: 블룸버그 RSS 사용
                backup_feed = feedparser.parse('https://www.bloomberg.com/feeds/markets')
                for entry in backup_feed.entries[:10]:
                    news_item = {
                        'title': entry.title,
                        'link': entry.link,
                        'summary': entry.summary if hasattr(entry, 'summary') else '',
                        'published': entry.published if hasattr(entry, 'published') else datetime.now().strftime('%Y-%m-%d'),
                        'source': 'Bloomberg',
                    }
                    self._categorize_news(news_item)
        except Exception as e:
            logger.error(f"Bloomberg 수집 오류: {str(e)}")
    
    def _collect_cnbc(self):
        """CNBC RSS 피드 수집"""
        try:
            logger.info("CNBC 뉴스 수집 중...")
            
            # Economy 섹션
            economy_feed = feedparser.parse('https://www.cnbc.com/id/10000113/device/rss/rss.html')
            # Markets 섹션
            markets_feed = feedparser.parse('https://www.cnbc.com/id/10000115/device/rss/rss.html')
            # World News 섹션
            world_feed = feedparser.parse('https://www.cnbc.com/id/100727362/device/rss/rss.html')
            
            all_entries = economy_feed.entries + markets_feed.entries + world_feed.entries
            
            for entry in all_entries[:15]:  # 상위 15개 뉴스만 수집
                news_item = {
                    'title': entry.title,
                    'link': entry.link,
                    'summary': entry.summary if hasattr(entry, 'summary') else '',
                    'published': entry.published if hasattr(entry, 'published') else datetime.now().strftime('%Y-%m-%d'),
                    'source': 'CNBC',
                }
                
                # 국가별 분류
                self._categorize_news(news_item)
        except Exception as e:
            logger.error(f"CNBC 수집 오류: {str(e)}")
    
    def _collect_reuters(self):
        """Reuters RSS 피드 수집"""
        try:
            logger.info("Reuters 뉴스 수집 중...")
            
            # 다양한 Reuters 피드 시도
            feeds = [
                'https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best',
                'https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best',
                'http://feeds.reuters.com/reuters/businessNews',
                'http://feeds.reuters.com/reuters/topNews'
            ]
            
            all_entries = []
            for feed_url in feeds:
                try:
                    feed_data = feedparser.parse(feed_url)
                    if feed_data.entries:
                        all_entries.extend(feed_data.entries)
                except Exception as feed_error:
                    logger.warning(f"피드 파싱 오류 ({feed_url}): {str(feed_error)}")
            
            for entry in all_entries[:15]:  # 상위 15개 뉴스만 수집
                news_item = {
                    'title': entry.title,
                    'link': entry.link,
                    'summary': entry.summary if hasattr(entry, 'summary') else '',
                    'published': entry.published if hasattr(entry, 'published') else datetime.now().strftime('%Y-%m-%d'),
                    'source': 'Reuters',
                }
                
                # 국가별 분류
                self._categorize_news(news_item)
        except Exception as e:
            logger.error(f"Reuters 수집 오류: {str(e)}")
    
    def _collect_hankyung(self):
        """한국경제 뉴스 크롤링"""
        try:
            logger.info("한국경제 뉴스 수집 중...")
            
            # 아침 시황
            urls = [
                "https://www.hankyung.com/economy",
                "https://www.hankyung.com/market"
            ]
            
            for url in urls:
                response = self._make_request(url)
                
                if response:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # 주요 뉴스 수집
                    news_items = soup.select('.news-list a')
                    
                    if not news_items:
                        # 대체 선택자 시도
                        news_items = soup.select('.list-box a')
                    
                    for item in news_items[:10]:  # 상위 10개 뉴스만 수집
                        title_elem = item.select_one('.tit') or item.select_one('h3')
                        if title_elem:
                            title = title_elem.text.strip()
                            link = item['href'] if item.get('href') else ''
                            
                            # 요약 정보 가져오기
                            summary_elem = item.select_one('.lead') or item.select_one('.desc')
                            summary = summary_elem.text.strip() if summary_elem else ''
                            
                            news_item = {
                                'title': title,
                                'link': link,
                                'summary': summary,
                                'source': '한국경제',
                                'published': datetime.now().strftime('%Y-%m-%d'),
                            }
                            
                            # 국가별 분류
                            self._categorize_news(news_item)
                else:
                    logger.error(f"한국경제 접속 실패: {url}")
        except Exception as e:
            logger.error(f"한국경제 수집 오류: {str(e)}")
    
    def _collect_yonhap(self):
        """연합뉴스 뉴스 크롤링"""
        try:
            logger.info("연합뉴스 수집 중...")
            
            url = "https://www.yna.co.kr/economy"
            response = self._make_request(url)
            
            if response:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 주요 뉴스 수집
                news_items = soup.select('.section-list li .item-box01')
                
                if not news_items:
                    # 대체 선택자 시도
                    news_items = soup.select('.list li .item-box')
                
                for item in news_items[:10]:  # 상위 10개 뉴스만 수집
                    title_elem = item.select_one('strong.tit-news') or item.select_one('.news-tit')
                    if title_elem:
                        title = title_elem.text.strip()
                        link_elem = item.select_one('a')
                        link = f"https://www.yna.co.kr{link_elem['href']}" if link_elem and link_elem.get('href') else ''
                        
                        # 요약 정보 가져오기
                        summary_elem = item.select_one('.lead')
                        summary = summary_elem.text.strip() if summary_elem else ''
                        
                        news_item = {
                            'title': title,
                            'link': link,
                            'summary': summary,
                            'source': '연합뉴스',
                            'published': datetime.now().strftime('%Y-%m-%d'),
                        }
                        
                        # 국가별 분류
                        self._categorize_news(news_item)
            else:
                logger.error("연합뉴스 접속 실패")
        except Exception as e:
            logger.error(f"연합뉴스 수집 오류: {str(e)}")
    
    def _collect_edaily(self):
        """이데일리 뉴스 크롤링"""
        try:
            logger.info("이데일리 수집 중...")
            
            urls = [
                "https://www.edaily.co.kr/news/economy",
                "https://www.edaily.co.kr/stock/market"
            ]
            
            for url in urls:
                response = self._make_request(url)
                
                if response:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # 주요 뉴스 수집
                    news_items = soup.select('.newsbox_list')
                    
                    if not news_items:
                        # 대체 선택자 시도
                        news_items = soup.select('.article_list .newsbox')
                    
                    for item in news_items[:10]:  # 상위 10개 뉴스만 수집
                        title_elem = item.select_one('.newstit a') or item.select_one('h2 a')
                        if title_elem:
                            title = title_elem.text.strip()
                            link = title_elem['href'] if title_elem.get('href') else ''
                            
                            # 요약 정보 가져오기
                            summary_elem = item.select_one('.newscont') or item.select_one('.newstxt')
                            summary = summary_elem.text.strip() if summary_elem else ''
                            
                            news_item = {
                                'title': title,
                                'link': link,
                                'summary': summary,
                                'source': '이데일리',
                                'published': datetime.now().strftime('%Y-%m-%d'),
                            }
                            
                            # 국가별 분류
                            self._categorize_news(news_item)
                else:
                    logger.error(f"이데일리 접속 실패: {url}")
        except Exception as e:
            logger.error(f"이데일리 수집 오류: {str(e)}")
    
    def _categorize_news(self, news_item):
        """뉴스를 국가/지역별로 분류"""
        title = news_item.get('title', '').lower()
        summary = news_item.get('summary', '').lower()
        content = title + ' ' + summary

        # 영어/한글 국가명 키워드 확장
        if any(k in content for k in ['u.s.', 'us ', 'united states', 'america', 'fed', 'federal reserve', 'powell', 'trump', 'biden', 'harris', 'wall street', 'dow', 'nasdaq', 's&p', 'treasury', '미국', '연준', '파월', '트럼프', '바이든', '해리스']):
            self.news_data["US"].append(news_item)

        elif any(k in content for k in ['china', 'chinese', 'beijing', 'shanghai', 'pboc', 'yuan', 'renminbi', 'xi jinping', '중국', '베이징', '상하이', '인민은행', '위안화', '시진핑']):
            self.news_data["China"].append(news_item)

        elif any(k in content for k in ['russia', 'russian', 'moscow', 'putin', 'ukraine', 'kyiv', '러시아', '모스크바', '푸틴', '우크라이나', '키예프']):
            self.news_data["Russia"].append(news_item)

        elif any(k in content for k in ['korea', 'korean', 'seoul', 'won', 'kospi', 'kosdaq', '한국', '서울', '원화', '코스피', '코스닥']):
            self.news_data["Korea"].append(news_item)

        elif any(k in content for k in ['japan', 'tokyo', 'boj', 'yen', 'nikkei', '일본', '도쿄', '일본은행', '엔화', '닛케이']):
            self.news_data["Japan"].append(news_item)

        elif any(k in content for k in ['germany', 'france', 'uk', 'europe', 'european union', 'eu', 'ecb', 'eurozone', 'eur', 'brussels', '유럽', '독일', '프랑스', '영국', '유럽연합', '유로존', '유로화', '브뤼셀']):
            self.news_data["Europe"].append(news_item)

        elif any(k in content for k in ['iran', 'iraq', 'israel', 'gaza', 'saudi', 'uae', 'middle east', 'qatar', 'opec', '이란', '이라크', '이스라엘', '가자', '사우디', '중동', '카타르', '오펙']):
            self.news_data["MiddleEast"].append(news_item)

        elif any(k in content for k in ['vietnam', 'thailand', 'malaysia', 'philippines', 'indonesia', 'asean', 'singapore', '베트남', '태국', '말레이시아', '필리핀', '인도네시아', '아세안', '싱가포르']):
            self.news_data["SoutheastAsia"].append(news_item)

        else:
            self.news_data["Others"].append(news_item)
    
    def summarize_news_with_gpt(self):
        """GPT를 사용하여 국가별로 뉴스 요약"""
        summary_result = {}

        print("🧠 GPT를 통한 뉴스 요약 시작...")

        for country, news_list in self.news_data.items():
            if not news_list:
                continue

            print(f"✍️ {country} 뉴스 요약 중...")

            recent_news = news_list[:5]

            prompt = f"""다음은 오늘({self.today_date}) {country} 관련 주요 경제/금융 뉴스입니다.
                    각 뉴스의 제목과 요약을 참고하여 **가장 중요한 이슈 2~3개**만 선별하고,
                    **각 이슈를 한 줄(25단어 이내)**로 간결하게 요약해주세요.\n\n"""
            
            for idx, news in enumerate(recent_news, 1):
                title = news.get("title", "").strip()
                summary = news.get("summary", "").strip()
                source = news.get("source", "").strip()
                prompt += f"{idx}. [{source}] {title}\n{summary}\n\n"

            try:
                # OpenAI API 호출 (updated to current response)
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system",
                            "content": "당신은 거시경제 및 금융 뉴스를 요약하는 전문가입니다. 불필요한 뉴스는 제외하고 핵심 이슈만 요약하세요.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    max_tokens=300,
                    temperature=0.3,
                )

                # And then use:
                reply = response['choices'][0]['message']['content'].strip()
                summary_result[country] = reply
                print(f"✅ {country} 뉴스 요약 완료")

                # API rate limit 방지를 위한 지연
                time.sleep(random.uniform(1, 2))

            except Exception as e:
                error_msg = f"요약 실패: {str(e)}"
                summary_result[country] = error_msg
                print(f"❌ {country} 요약 실패: {error_msg}")
                time.sleep(random.uniform(3, 5))  # 오류 발생 시 더 긴 지연

        return summary_result
    
    def generate_final_report(self, summary_result):
        """최종 보고서 생성"""
        print("📄 최종 보고서 생성 중...")

        report = f"*MACRO({self.today_date})*\n\n"
        report += "◎ 주요 이슈\n\n"

        # 국가별 이모지 및 이름 정의
        country_emojis = {
            "US": "🇺🇸",
            "China": "🇨🇳",
            "Russia": "🇷🇺",
            "Korea": "🇰🇷",
            "Japan": "🇯🇵",
            "Europe": "🇪🇺",
            "MiddleEast": "🇮🇷",
            "SoutheastAsia": "🌏",
            "Others": "🌐"
        }

        country_names = {
            "US": "미국",
            "China": "중국",
            "Russia": "러시아",
            "Korea": "한국",
            "Japan": "일본",
            "Europe": "유럽",
            "MiddleEast": "중동",
            "SoutheastAsia": "동남아",
            "Others": "기타"
        }

        # 데이터가 있는 국가만 출력
        for country, summary in summary_result.items():
            if not summary:
                continue

            emoji = country_emojis.get(country, "")
            name = country_names.get(country, country)

            report += f"■ {emoji} {name}\n"

            # 요약 텍스트 정리
            for line in summary.split('\n'):
                clean = line.strip()
                if not clean:
                    continue
                # 숫자/기호 시작 제거
                if re.match(r'^[\d\.\-•➤①②③]+\s+', clean):
                    clean = re.sub(r'^[\d\.\-•➤①②③]+\s+', '', clean)
                report += f"- {clean}\n"

        # GPT 종합 정리 요청
        try:
            prompt = f"""다음은 {self.today_date} 글로벌 주요 매크로 경제 뉴스 요약입니다.
        이 내용을 바탕으로 전체 시장 상황을 2~3문장으로 종합 정리해주세요.

        {report}
        """

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 글로벌 금융시장을 분석하는 전문가입니다. 요약된 국가별 이슈를 종합해 전반적 시장 분위기를 요약하세요."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=200,
                temperature=0.3,
            )

            conclusion = response['choices'][0]['message']['content'].strip()
            report += "\n◎ 종합 정리\n"
            report += conclusion

        except Exception as e:
            print(f"❌ 종합 정리 생성 실패: {str(e)}")
            report += "\n◎ 종합 정리\n"
            report += "글로벌 시장은 다양한 변수에 반응하며 방향성을 탐색 중입니다."

        print("✅ 최종 보고서 생성 완료")
        return report
    
    def run(self):
        """전체 프로세스 실행"""
        logger.info("매크로 경제 보고서 생성 프로세스 시작")
        
        # 1. 글로벌 뉴스 수집
        self.collect_global_news()
        
        # 2. 국내 뉴스 수집
        self.collect_korean_news()
        
        # 3. GPT를 통한 요약
        summary_result = self.summarize_news_with_gpt()
        
        # 4. 최종 보고서 생성
        final_report = self.generate_final_report(summary_result)
        
        logger.info("매크로 경제 보고서 생성 프로세스 완료")
        return final_report

# 실행 함수
def generate_macro_report():
    collector = MacroNewsCollector()
    report = collector.run()
    
    # 보고서 저장
    report_filename = f"MACRO_REPORT_{collector.today_date}.txt"
    with open(report_filename, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"===== 매크로 경제 보고서 ({report_filename}) =====")
    print(report)
    print("============================")
    
    return report

if __name__ == "__main__":
    generate_macro_report()