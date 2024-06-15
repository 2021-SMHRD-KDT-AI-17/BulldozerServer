import cv2
import easyocr
import os
import re
from src import wordList as wl


reader = easyocr.Reader(['ko','en'])


def imageToText1(path):
    dictList=[]
    dictList=wl.getWordList()
    # 이미지 로드 및 전처리
    image = cv2.imread(path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 이미지에서 텍스트 추출
    results = reader.readtext(gray_image, detail=0)
    # 숫자와 특수문자 제거 후 띄어쓰기에 따라 텍스트 나누기
    # 추출된 텍스트(results)를 전처리
    cleaned_text = " ".join(results)
    cleaned_text = re.sub(r'[^가-힣a-zA-Z\s]', '', cleaned_text)
    splitted_text = cleaned_text.split()
    print("추출된 단어:")
    print(splitted_text)
    # 결과 저장할 리스트 초기화
    processed_text = []
    # 처리된 텍스트와 각 단어의 유사도 점수 저장할 리스트 초기화
    processed_text_with_scores = []


    # 함수 시작 ===========================================
        # 단어 사전과 비교하여 유사한 단어 찾기
        # 단어를 처리하여 유사한 단어 찾기
    def calculate_similarity(word1, word2):
        # 자음과 모음을 분리
        def separate_jamo(word):
            if not word:
                return []
            base = ord('가')
            chosung = [
                'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ',
                'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
            ]
            jungsung = [
                'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ',
                'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ'
            ]
            jongsung = [
                '', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ',
                'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
                'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
            ]
            result = []
            for char in word:
                if '가' <= char <= '힣':
                    char_code = ord(char) - base
                    chosung_index = char_code // 588
                    jungsung_index = (char_code - 588 * chosung_index) // 28
                    jongsung_index = char_code - 588 * chosung_index - 28 * jungsung_index
                    result.append((chosung[chosung_index], jungsung[jungsung_index], jongsung[jongsung_index]))
            return result
        # 자음과 모음을 비교하여 유사도 계산====
        def calculate_jamo_similarity(jamo1, jamo2):
            # 자음과 모음이 모두 같은 경우 1을 반환
            if jamo1 == jamo2:
                return 1
            # 모음이 같고 자음이 다른 경우 0.5를 반환
            if jamo1[1] == jamo2[1] and jamo1[0] != jamo2[0]:
                return 0.5
            # 자음과 모음이 다른 경우 0을 반환
            return 0
        jamo_list1 = separate_jamo(word1)
        jamo_list2 = separate_jamo(word2)
        total_similarity = 0
        # 각 자음/모음 별로 유사도 계산 후 평균을 구함
        for jamo1, jamo2 in zip(jamo_list1, jamo_list2):
            total_similarity += calculate_jamo_similarity(jamo1, jamo2)
        return total_similarity / max(len(jamo_list1), len(jamo_list2))
    # 함수 끝 ============================================
    # 단어 사전과 비교하여 유사한 단어 찾기
    for word in splitted_text:
        best_match = None
        best_similarity = 0
        # cleaned_list = 단어 사전
        for dict_word in dictList:
            similarity = calculate_similarity(word, dict_word)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = dict_word
        if best_similarity >= 0.6:
            processed_text.append(best_match)
        else:
            processed_text.append(word)
        processed_text_with_scores.append((best_match, best_similarity))

    # 처리된 텍스트 출력
    print("처리된 텍스트: ")
    print(processed_text)

    # # 각 단어의 유사도 점수 출력
    # print("\n각 단어의 유사도 점수:")
    # for word, score in processed_text_with_scores:
    #     print(f"{word}: {score}")
    return processed_text

def imageToText(path):
    dictList=wl.getWordList()
    image = cv2.imread(path)
    processed_text = []
    processed_text_with_scores = []
    try:
        image = cv2.imread(path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        results = reader.readtext(gray_image, detail=0)
        cleaned_text = " ".join(results)
        cleaned_text = re.sub(r'[^가-힣a-zA-Z\s]', '', cleaned_text)
        splitted_text = cleaned_text.split()
        print(path.split('/')[-1])
        print("추출된 단어:")
        print(splitted_text)
        def calculate_similarity(word1, word2):
            def separate_jamo(word):
                if not word:
                    return []
                base = ord('가')
                chosung = [
                    'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ',
                    'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
                ]
                jungsung = [
                    'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ',
                    'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ'
                ]
                jongsung = [
                    '', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ',
                    'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ',
                    'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
                ]
                result = []
                for char in word:
                    if '가' <= char <= '힣':
                        char_code = ord(char) - base
                        chosung_index = char_code // 588
                        jungsung_index = (char_code - 588 * chosung_index) // 28
                        jongsung_index = char_code - 588 * chosung_index - 28 * jungsung_index
                        result.append((chosung[chosung_index], jungsung[jungsung_index], jongsung[jongsung_index]))
                return result
            def calculate_jamo_similarity(jamo1, jamo2):
                if jamo1 == jamo2:
                    return 1
                if jamo1[1] == jamo2[1] and jamo1[0] != jamo2[0]:
                    return 0.5
                return 0
            jamo_list1 = separate_jamo(word1)
            jamo_list2 = separate_jamo(word2)
            total_similarity = 0
            for jamo1, jamo2 in zip(jamo_list1, jamo_list2):
                total_similarity += calculate_jamo_similarity(jamo1, jamo2)
            return total_similarity / max(len(jamo_list1), len(jamo_list2))
        for word in splitted_text:
            best_match = None
            best_similarity = 0
            for dict_word in dictList:
                similarity = calculate_similarity(word, dict_word)
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = dict_word
            if best_similarity >= 0.6:
                processed_text.append(best_match)
            processed_text_with_scores.append((best_match, best_similarity))
    except Exception as e:
        pass
    print("처리된 텍스트: ")
    print(processed_text)

    return processed_text