#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
동양미래대학교 예산 공지 자동화 수집 프로그램
구매/입찰공고 게시판에서 예산 관련 정보를 수집하고 정리합니다.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime
import time
import json

class DongYangBudgetCollector:
    def __init__(self):
        self.base_url = "https://www.dongyang.ac.kr"
        self.list_url = "https://www.dongyang.ac.kr/bbs/dmu/699/artclList.do"
        self.notices = []
        self.budget_data = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
    def fetch_list_page(self, page=1):
        """공지사항 목록 페이지 가져오기"""
        try:
            params = {'page': page}
            response = requests.get(self.list_url, params=params, headers=self.headers, timeout=15)
            response.encoding = 'utf-8'
            return response.text
        except Exception as e:
            print(f"   ❌ 페이지 로드 오류: {e}")
            return None
    
    def parse_notice_list(self, html):
        """공지사항 목록 파싱"""
        notices = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # tbody 찾기
            tbody = soup.find('tbody')
            if not tbody:
                return notices
            
            rows = tbody.find_all('tr')
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) < 5:
                    continue
                
                # 두 번째 셀(인덱스 1)에서 제목과 링크 추출
                title_cell = cells[1]
                link_elem = title_cell.find('a')
                
                if not link_elem:
                    continue
                
                title = link_elem.get_text(strip=True)
                href = link_elem.get('href', '')
                
                # 분류 추출 (입찰공고, 유찰공고 등)
                classification_text = title.split()[0] if title else ''
                
                # 재공고와 유찰공고 제외
                if '재공고' in title or '유찰' in title:
                    continue
                
                # 작성자 (세 번째 셀, 인덱스 2)
                author = cells[2].get_text(strip=True) if len(cells) > 2 else ''
                
                # 날짜 (네 번째 셀, 인덱스 3)
                date_str = cells[3].get_text(strip=True) if len(cells) > 3 else ''
                
                # 조회수 (다섯 번째 셀, 인덱스 4)
                views_str = cells[4].get_text(strip=True) if len(cells) > 4 else ''
                
                if title and href:
                    notices.append({
                        'title': title,
                        'href': href,
                        'classification': classification_text,
                        'author': author,
                        'date': date_str,
                        'views': views_str
                    })
            
            return notices
            
        except Exception as e:
            print(f"   ❌ 파싱 오류: {e}")
            return notices
    
    def fetch_detail_page(self, href):
        """공지사항 상세 페이지 가져오기"""
        try:
            if not href.startswith('http'):
                href = self.base_url + (href if href.startswith('/') else '/' + href)
            
            response = requests.get(href, headers=self.headers, timeout=15)
            response.encoding = 'utf-8'
            return response.text
        except Exception as e:
            return None
    
    def extract_budget_amount(self, text):
        """텍스트에서 예산 금액 추출"""
        amounts = []
        
        # 다양한 형식의 금액 찾기
        patterns = [
            r'(\d{1,3}(?:,\d{3})+)\s*원',  # 1,000,000원
            r'(\d+)\s*만\s*원',              # 100만원
            r'예정가격\s*[:：]\s*(\d{1,3}(?:,\d{3})+)',  # 예정가격: 1,000,000
            r'예정금액\s*[:：]\s*(\d{1,3}(?:,\d{3})+)',  # 예정금액: 1,000,000
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                amount_str = match.group(1).replace(',', '')
                try:
                    amount = int(amount_str)
                    if amount > 100:  # 최소 100원 이상
                        amounts.append(amount)
                except:
                    pass
        
        return max(amounts) if amounts else None
    
    def extract_category(self, title):
        """제목에서 분류 추출"""
        if '용역' in title:
            return '용역'
        elif '납품' in title or '구입' in title:
            return '납품/구입'
        elif '도서' in title:
            return '도서'
        elif '유지관리' in title:
            return '유지관리'
        elif '구축' in title or '설계' in title:
            return '구축/설계'
        else:
            return '기타'
    
    def collect_notices(self, max_pages=3):
        """공지사항 수집"""
        print("\n📊 공지사항 목록 수집 중...\n")
        
        for page in range(1, max_pages + 1):
            print(f"  📄 페이지 {page} 처리...", end=" ", flush=True)
            
            html = self.fetch_list_page(page)
            if not html:
                print("오류")
                break
            
            page_notices = self.parse_notice_list(html)
            if not page_notices:
                print("공지사항 없음")
                break
            
            self.notices.extend(page_notices)
            print(f"✓ {len(page_notices)}개")
            
            time.sleep(1)  # 서버 부하 방지
        
        return len(self.notices)
    
    def process_notices(self):
        """공지사항 상세 정보 처리"""
        print(f"\n💰 예산 정보 추출 중... ({len(self.notices)}개)\n")
        
        for idx, notice in enumerate(self.notices, 1):
            print(f"  진행: {idx}/{len(self.notices)}", end="\r", flush=True)
            
            try:
                # 상세 페이지 가져오기
                detail_html = self.fetch_detail_page(notice['href'])
                if not detail_html:
                    continue
                
                # 텍스트 추출
                soup = BeautifulSoup(detail_html, 'html.parser')
                content_text = soup.get_text()
                
                # 제목과 내용 결합
                full_text = notice['title'] + ' ' + content_text
                
                # 예산 금액 추출
                budget = self.extract_budget_amount(full_text)
                
                # 분류
                category = self.extract_category(notice['title'])
                
                # 데이터 저장
                self.budget_data.append({
                    'title': notice['title'],
                    'classification': notice['classification'],
                    'category': category,
                    'budget': budget,
                    'date': notice['date'],
                    'author': notice['author'],
                    'extracted': budget is not None
                })
                
                time.sleep(0.5)  # 서버 부하 방지
                
            except Exception as e:
                # 오류 발생시 기본 정보만 저장
                self.budget_data.append({
                    'title': notice['title'],
                    'classification': notice['classification'],
                    'category': self.extract_category(notice['title']),
                    'budget': None,
                    'date': notice['date'],
                    'author': notice['author'],
                    'extracted': False
                })
        
        print(f"  진행: {len(self.notices)}/{len(self.notices)} ✓\n")
    
    def generate_report(self):
        """분석 보고서 생성"""
        df = pd.DataFrame(self.budget_data)
        
        total = len(df)
        extracted = df['extracted'].sum()
        rate = (extracted / total * 100) if total > 0 else 0
        
        print("=" * 70)
        print("🎓 동양미래대학교 예산 공지사항 분석 보고서")
        print("=" * 70)
        
        print(f"\n📊 수집 현황")
        print(f"  • 총 공지사항: {total}개")
        print(f"  • 예산 정보 추출: {extracted}개")
        print(f"  • 추출율: {rate:.1f}%\n")
        
        if extracted > 0:
            # 분류별 통계
            extracted_df = df[df['extracted'] == True]
            
            print(f"📑 분류별 예산 현황\n")
            category_stats = extracted_df.groupby('category')['budget'].agg(['count', 'sum', 'mean'])
            
            for cat in sorted(category_stats.index):
                count = int(category_stats.loc[cat, 'count'])
                total_budget = int(category_stats.loc[cat, 'sum'])
                avg_budget = int(category_stats.loc[cat, 'mean'])
                
                print(f"  [{cat}]")
                print(f"    건수: {count}개")
                print(f"    총액: {total_budget:,}원")
                print(f"    평균: {avg_budget:,}원\n")
            
            # 상위 예산 항목
            print(f"💵 예산 상위 10건\n")
            top_10 = df[df['budget'].notna()].nlargest(10, 'budget')
            
            for idx, (i, row) in enumerate(top_10.iterrows(), 1):
                print(f"  {idx:2}. {row['title'][:50]}")
                print(f"      └─ 예산: {row['budget']:>12,}원 | {row['category']:8} | {row['date']}\n")
        
        print("=" * 70)
        
        return df
    
    def save_results(self, df):
        """결과 저장"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # CSV 저장
        csv_file = f"budget_report_{timestamp}.csv"
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        
        # 텍스트 보고서 저장
        txt_file = f"budget_report_{timestamp}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("🎓 동양미래대학교 예산 공지사항 분석 보고서\n")
            f.write("=" * 70 + "\n\n")
            
            total = len(df)
            extracted = df['extracted'].sum()
            rate = (extracted / total * 100) if total > 0 else 0
            
            f.write(f"📊 수집 현황\n")
            f.write(f"  • 총 공지사항: {total}개\n")
            f.write(f"  • 예산 정보 추출: {extracted}개\n")
            f.write(f"  • 추출율: {rate:.1f}%\n\n")
            
            if extracted > 0:
                extracted_df = df[df['extracted'] == True]
                
                f.write(f"📑 분류별 예산 현황\n\n")
                category_stats = extracted_df.groupby('category')['budget'].agg(['count', 'sum', 'mean'])
                
                for cat in sorted(category_stats.index):
                    count = int(category_stats.loc[cat, 'count'])
                    total_budget = int(category_stats.loc[cat, 'sum'])
                    avg_budget = int(category_stats.loc[cat, 'mean'])
                    
                    f.write(f"  [{cat}]\n")
                    f.write(f"    건수: {count}개\n")
                    f.write(f"    총액: {total_budget:,}원\n")
                    f.write(f"    평균: {avg_budget:,}원\n\n")
                
                f.write(f"💵 예산 상위 10건\n\n")
                top_10 = df[df['budget'].notna()].nlargest(10, 'budget')
                
                for idx, (i, row) in enumerate(top_10.iterrows(), 1):
                    f.write(f"  {idx:2}. {row['title']}\n")
                    f.write(f"      예산: {row['budget']:>12,}원 | {row['category']} | {row['date']}\n\n")
        
        print(f"\n✅ CSV 저장: {csv_file}")
        print(f"✅ 보고서 저장: {txt_file}")
        
        return csv_file, txt_file


def main():
    """메인 함수"""
    print("\n" + "=" * 70)
    print("🚀 동양미래대학교 예산 공지사항 자동 수집 시작")
    print("=" * 70)
    
    collector = DongYangBudgetCollector()
    
    # 1. 공지사항 수집
    notice_count = collector.collect_notices(max_pages=3)
    
    if notice_count == 0:
        print("\n❌ 수집된 공지사항이 없습니다.")
        return
    
    print(f"\n✓ 총 {notice_count}개 공지사항 수집 완료")
    
    # 2. 상세 정보 처리
    collector.process_notices()
    
    # 3. 보고서 생성
    df = collector.generate_report()
    
    # 4. 결과 저장
    collector.save_results(df)
    
    print("\n✨ 프로그램 완료!\n")


if __name__ == "__main__":
    main()
