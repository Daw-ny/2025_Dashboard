#######################################################
# packages
import numpy as np
import pandas as pd

#######################################################
# 혼합된 난자 수 보정하기
def nanja_count_settings(data):
    cri = [
        (data['혼합된 난자 수'] == data['파트너 정자와 혼합된 난자 수'] + data['기증자 정자와 혼합된 난자 수'] + data['확인되지 않은 혼합된 난자 수']) & ~(data['혼합된 난자 수'].isna()),
        (data['혼합된 난자 수'] > data['파트너 정자와 혼합된 난자 수'] + data['기증자 정자와 혼합된 난자 수'] + data['확인되지 않은 혼합된 난자 수']) & (data['정자 출처'] == '배우자 제공') & ~(data['혼합된 난자 수'].isna()),
        (data['혼합된 난자 수'] > data['파트너 정자와 혼합된 난자 수'] + data['기증자 정자와 혼합된 난자 수'] + data['확인되지 않은 혼합된 난자 수']) & (data['정자 출처'] == '기증 제공') & ~(data['혼합된 난자 수'].isna()),
        (data['혼합된 난자 수'] > data['파트너 정자와 혼합된 난자 수'] + data['기증자 정자와 혼합된 난자 수'] + data['확인되지 않은 혼합된 난자 수']) & (data['정자 출처'] == '미할당') & ~(data['혼합된 난자 수'].isna()),
    ]
    con1 = [
        data['파트너 정자와 혼합된 난자 수'],
        data['혼합된 난자 수'],
        0,
        0
    ]
    con2 = [
        data['기증자 정자와 혼합된 난자 수'],
        0,
        data['혼합된 난자 수'],
        0
    ]
    con3 = [
        0, 0, 0, data['혼합된 난자 수']
    ]
    data['파트너 정자와 혼합된 난자 수'] = np.select(cri, con1, default = data['파트너 정자와 혼합된 난자 수'])
    data['기증자 정자와 혼합된 난자 수'] = np.select(cri, con2, default = data['기증자 정자와 혼합된 난자 수'])
    data['확인되지 않은 혼합된 난자 수'] = np.select(cri, con3, default = data['확인되지 않은 혼합된 난자 수'])

    return data

# 수집 + 해동 = 저장 + 혼합 맞추기
# 수집 + 해동이 더 작은 경우 수집에 몰빵하기
def collect_nanja(data):
    cri = [
        data['해동 난자 수'] + data['수집된 신선 난자 수'] < data['저장된 신선 난자 수'] + data['혼합된 난자 수']
    ]
    con = [
        data['저장된 신선 난자 수'] + data['혼합된 난자 수']
    ]
    data['수집된 신선 난자 수'] = np.select(cri, con, default = data['수집된 신선 난자 수'])

    return data

# 배아 수 고치기
def egg_count_adj(data):

    data['총 생성 배아 수'] = np.where(data['미세주입된 난자 수'] < data['미세주입에서 생성된 배아 수'], data['미세주입된 난자 수'], data['총 생성 배아 수'])
    data['미세주입에서 생성된 배아 수'] = np.where(data['미세주입된 난자 수'] < data['미세주입에서 생성된 배아 수'], data['미세주입된 난자 수'], data['미세주입에서 생성된 배아 수'])

    return data

# 생성 + 해동 = 저장 + 혼합 맞추기
# 생성 + 해동이 더 작은 경우 수집에 몰빵하기
def collect_baea(data):
    cri = [
        (data['총 생성 배아 수'] + data['해동된 배아 수'] < data['저장된 배아 수'] + data['이식된 배아 수'])
    ]

    con = [
        data['저장된 배아 수'] + data['이식된 배아 수']
    ]

    data['총 생성 배아 수'] = np.select(cri, con, default = data['총 생성 배아 수'])

    return data

# PGS 관련 변수 합쳐놓기
def pgs_adj(data):

    data['PGS 시술 여부'][data['PGS 시술 여부'].isna()] = 0
    data['착상 전 유전 검사 사용 여부'][data['착상 전 유전 검사 사용 여부'].isna()] = 0

    cri = [
        (data['착상 전 유전 검사 사용 여부'] == 0) & (data['PGS 시술 여부'] == 0),
        (data['착상 전 유전 검사 사용 여부'] == 1) & (data['PGS 시술 여부'] == 0),
        (data['착상 전 유전 검사 사용 여부'] == 1) & (data['PGS 시술 여부'] == 1),
    ]

    con = [
        0, -1, 1
    ]
    
    data['PGS'] = np.select(cri, con, default = -999)

    return data

# PGD 관련 변수 합쳐놓기
def pgd_adj(data):

    data['PGD 시술 여부'][data['PGD 시술 여부'].isna()] = 0
    data['착상 전 유전 진단 사용 여부'][data['착상 전 유전 진단 사용 여부'].isna()] = 0

    cri = [
        (data['착상 전 유전 진단 사용 여부'] == 0) & (data['PGD 시술 여부'] == 0),
        (data['착상 전 유전 진단 사용 여부'] == 1) & (data['PGD 시술 여부'] == 0),
        (data['착상 전 유전 진단 사용 여부'] == 1) & (data['PGD 시술 여부'] == 1),
    ]

    con = [
        0, -1, 1
    ]
    
    data['PGD'] = np.select(cri, con, default = -999)

    return data

# DI와 IVF
def sisul_type_adj(data):

    cri = [
        (data['시술 유형'] == 'DI'),
        (data['시술 유형'] == 'IVF') & (data['난자 출처'] == '기증 제공'),
        (data['시술 유형'] == 'IVF') & (data['정자 출처'].isin(['기증 제공', '배우자 및 기증 제공'])),
    ]

    con = [
        1, 1, 1
    ]

    data['DI시술방법'] = np.select(cri, con, default=0)
    data['IVF시술방법'] = np.where(data['시술 유형'] == 'IVF', 1, 0)

    return data

# 난자출처에 따른 해당 주기의 난자 주인 나이를 설명
def nanja_own_age(data):
    cri = [
        data['난자 출처'] == '본인 제공',
        data['난자 출처'] == '알 수 없음',
        data['난자 출처'] == '기증 제공',
    ]

    con = [
        data['시술 당시 나이'],
        data['시술 당시 나이'],
        data['난자 기증자 나이']
    ]

    data['해당 주기 난자 주인 나이'] = np.select(cri, con, default = np.nan)

    return data

# 해당 주기 난자 주인 나이 매핑, 나이가 많을수록 낮은 값을 책정
def nanja_level_mapping(data):
    cri = [
        data['해당 주기 난자 주인 나이'] == '만18-34세',
        data['해당 주기 난자 주인 나이'] == '만45-50세',
        data['해당 주기 난자 주인 나이'] == '만35-37세',
        data['해당 주기 난자 주인 나이'] == '만38-39세',
        data['해당 주기 난자 주인 나이'] == '만21-25세',
        data['해당 주기 난자 주인 나이'] == '만40-42세',
        data['해당 주기 난자 주인 나이'] == '만43-44세',
        data['해당 주기 난자 주인 나이'] == '만31-35세',
        data['해당 주기 난자 주인 나이'] == '만26-30세',
        data['해당 주기 난자 주인 나이'] == '만20세 이하',
        data['해당 주기 난자 주인 나이'] == '알 수 없음'
    ]

    con = [
        6, 1, 5, 4, 6, 3, 2, 6, 6, 6, 0
    ]
    data['해당 주기 난자 주인 나이'] = np.select(cri, con, default = data['해당 주기 난자 주인 나이'])
    return data

def preprocessing(df):
    df['확인되지 않은 혼합된 난자 수'] = 0

    # 혼합된 난자 불일치 변경
    df = nanja_count_settings(df)

    # 해동, 수집, 저장, 혼합에 관해 수식에 맞는 값으로 적용
    df = collect_nanja(df)

    # 총 배아수를 넘는 숫자 보정
    df = egg_count_adj(df)

    # 생성, 해동, 이식, 저장 배아수 조정
    df = collect_baea(df)

    df['정자 출처'] = np.where((df['파트너 정자와 혼합된 난자 수'] > 0) & (df['기증자 정자와 혼합된 난자 수'] > 0), '배우자 및 기증 제공', df['정자 출처'])

    # ICSI를 적용하지 않은 배아에 대한 파생 변수
    df['IVF에서 생성된 배아 수'] = df['총 생성 배아 수'] - df['미세주입에서 생성된 배아 수']

    df['IVF 배아 이식 수'] = df['이식된 배아 수'] - df['미세주입 배아 이식 수']

    df['IVF 후 저장된 배아 수'] = df['저장된 배아 수'] - df['미세주입 후 저장된 배아 수']

    # 폐기된 배아 수
    df['폐기된 배아 수'] = df['총 생성 배아 수'] + df['해동된 배아 수'] - (df['저장된 배아 수'] + df['이식된 배아 수'])

    # 배아 생성 실패 난자 수
    df['미세주입 배아 실패 수'] = df['미세주입된 난자 수'] - df['미세주입에서 생성된 배아 수']

    df['IVF 배아 실패 수'] = df['혼합된 난자 수'] - df['미세주입된 난자 수'] - df['IVF에서 생성된 배아 수']
    
    df = pgs_adj(df)

    # PGD 변수 합치기
    df = pgd_adj(df)

    # 시술 타입 대분류 공통적인 특징 보정
    df = sisul_type_adj(df)

    # 난자의 주인에 대한 나이 생성 (본인난자 사용하면 본인, 기증자 난자 사용하면 기증자 나이)
    df = nanja_own_age(df)

    # 해당 주기의 난자 주인 나이를 일치하기 위한 매핑 방법
    df = nanja_level_mapping(df)

    # 싹다 -999로 채워 EDA 하는 경우에 -999를 보면 Missing임을 알수있도록
    df = df.fillna('-999')

    # # 겹치는 Column과 상수 Column 제거
    # constant_columns = df.nunique() == 1
    # columns_to_drop = df.columns[constant_columns]

    # df = df.drop(columns=columns_to_drop)

    # 배란 유도 유형의 종류가 단 1건씩 두 종류만 존재해 배제 결정
    df = df.drop(columns='배란 유도 유형')

    # 나이 컬럼 처리
    df['정자 기증자 나이'] = df['정자 기증자 나이'].replace("-999", "알 수 없음")
    df['난자 기증자 나이'] = df['난자 기증자 나이'].replace("-999", "알 수 없음")

    # 나이가 높을수록 낮은 값을 책정
    age_mapping = {
        "만18-34세" : 1024,
        "만35-37세" : 512,
        "만38-39세" : 256,
        "만40-42세" : 128,
        "만43-44세" : 32,
        "만45-50세" : 4,
        "알 수 없음" : -999,
    }
    df["시술 당시 나이"] = df["시술 당시 나이"].map(age_mapping)

    age_mapping = {
        "만20세 이하" : 1024,
        "만21-25세" : 512,
        "만26-30세" : 128,
        "만31-35세" : 16,
        "알 수 없음" : -999,
    }

    df["난자 기증자 나이"] = df["난자 기증자 나이"].map(age_mapping)

    age_mapping = {
        "만20세 이하" : 1024,
        "만21-25세" : 512,
        "만26-30세" : 256,
        "만31-35세" : 128,
        "만36-40세" : 16,
        "만41-45세" : 4,
        "알 수 없음" : -999,
    }

    df["정자 기증자 나이"] = df["정자 기증자 나이"].map(age_mapping)

    # 시술 유형 처리
    mapping = {
        "DI" : -100,
        "IVF" : 100
    }
    df["시술 유형"] = df["시술 유형"].map(mapping)


    # 횟수 처리
    mapping = {
        "0회": 0, "1회": 1, "2회": 2, "3회": 3, "4회": 4, "5회": 5,
        "6회 이상": 20, '-999' : -999
    }
    # 6회 이상이라는 말에 의미를 담기 위해서 20로 매핑함.

    # 클리닉 횟수 관련
    df["총 시술 횟수"] = df["총 시술 횟수"].map(mapping)

    df["DI 시술 횟수"] = df["DI 시술 횟수"].map(mapping)

    df["IVF 시술 횟수"] = df["IVF 시술 횟수"].map(mapping)

    df["클리닉 내 총 시술 횟수"] = df["클리닉 내 총 시술 횟수"].map(mapping)

    # 임신 횟수 관련 
    df["총 임신 횟수"] = df["총 임신 횟수"].map(mapping)

    df["IVF 임신 횟수"] = df["IVF 임신 횟수"].map(mapping)

    df["DI 임신 횟수"] = df["DI 임신 횟수"].map(mapping)

    # 출산 횟수 관련 
    df["총 출산 횟수"] = df["총 출산 횟수"].map(mapping)

    df["IVF 출산 횟수"] = df["IVF 출산 횟수"].map(mapping)

    df["DI 출산 횟수"] = df["DI 출산 횟수"].map(mapping)

    # 코드가 뒤로 갈수록 나이가 많은 분들이 시술을 받는 경향을 받아, 선형적으로 구성, 연도인지는 모르겠으나, 현 연도로 오는만큼, 나이가 많은 사람이 임신을 하는 경우가 많다는 것을 확인
    code_to_year = {
        'TRXQMD' : 1,
        'TRZKPL' : 2,
        'TRVNRY' : 3,
        'TRJXFG' : 4,
        'TRYBLT' : 5,
        'TRCMWS' : 6,
        'TRDQAZ' : 7,
    }

    df['시술 시기 코드'] = df['시술 시기 코드'].map(code_to_year)

    # 난자 출처 매핑
    mapping = {
        "본인 제공" : 1,
        "기증 제공" : -1,
        "알 수 없음" : 1, # DI의 경우 99프로 이상이 본인의 난자와 수정하는 과정임.
    }
    df['난자 출처'] = df['난자 출처'].map(mapping)

    # 정자 출처 매핑
    mapping = {
        "배우자 제공" : 1,
        "기증 제공" : -1,
        "배우자 및 기증 제공" : 0,
        "미할당" : -999,
    }

    df['정자 출처'] = df['정자 출처'].map(mapping)

    # 특정 시술 유형의 :과 _를 없애어, 이상을 없앰.
    df['특정 시술 유형'] =df['특정 시술 유형'].str.replace(r'\s+', '', regex=True).str.replace(":", "_")

    # 특정 시술 유형 onehot
    for i in ['ICSI', 'IUI', 'ICI', 'GIFT', 'FER', 'GenericDI', 'IVI', 'BLASTOCYST', 'AH', 'Unknown', 'IVF', '-999', 'ICSI_ICSI', 'IVF_IVF', 'ICSI_Unknown', 'BLASTOCYST_IVF', 'IVF_Unknown', 'ICSI/BLASTOCYST', 'IVF/BLASTOCYST', 'ICSI/AH', 'IVF/AH', 'ICSI/BLASTOCYST_IVF/BLASTOCYST']:
        df['특시유_' + i] = np.where(df['특정 시술 유형'].str.contains(i, regex=False), 1, 0)

    # 배아 생성 주요 이유 onehot
    for i in ['-999', '기증용', '난자 저장용', '배아 저장용', '연구용', '현재 시술용']:
        df['배생이_' + i] = np.where(df['배아 생성 주요 이유'].str.contains(i), 1, 0)

    df = df.drop(columns = ['배아 생성 주요 이유'])

    # Int화
    df['착상 전 유전 진단 사용 여부'] = df['착상 전 유전 진단 사용 여부'].astype(int)
    df['착상 전 유전 검사 사용 여부'] = df['착상 전 유전 검사 사용 여부'].astype(int)
    df['임신 시도 또는 마지막 임신 경과 연수'] = df['임신 시도 또는 마지막 임신 경과 연수'].astype(int)
    df['단일 배아 이식 여부'] = df['단일 배아 이식 여부'].astype(int)

    # 시술유형에 따른 결측치 대체매핑 -> DI인 경우와 IVF인 경우에 의미가 다름.
    df.loc[(df['시술 유형'] == 100) & (df['착상 전 유전 검사 사용 여부'] == '-999'), '착상 전 유전 검사 사용 여부'] = 0

    df.loc[(df['시술 유형'] == 100) & (df['PGD 시술 여부'] == '-999'), 'PGD 시술 여부'] = 0
    df.loc[(df['시술 유형'] == 100) & (df['PGS 시술 여부'] == '-999'), 'PGS 시술 여부'] = 0

    df.loc[(df['시술 유형'] == 100) & (df['난자 채취 경과일'] == '-999'), '난자 채취 경과일'] = 0
    df.loc[(df['시술 유형'] == 100) & (df['난자 해동 경과일'] == '-999'), '난자 해동 경과일'] = 0
    df.loc[(df['시술 유형'] == 100) & (df['난자 혼합 경과일'] == '-999'), '난자 혼합 경과일'] = 0
    df.loc[(df['시술 유형'] == 100) & (df['배아 이식 경과일'] == '-999'), '배아 이식 경과일'] = 0
    df.loc[(df['시술 유형'] == 100) & (df['배아 해동 경과일'] == '-999'), '배아 해동 경과일'] = 0

    # str인 것들을 다 int화
    col = [
        "총 생성 배아 수", "미세주입된 난자 수", "미세주입에서 생성된 배아 수", "이식된 배아 수",
        "미세주입 배아 이식 수", "저장된 배아 수", "미세주입 후 저장된 배아 수", "해동된 배아 수",
        "해동 난자 수", "수집된 신선 난자 수", "저장된 신선 난자 수", "혼합된 난자 수",
        "파트너 정자와 혼합된 난자 수", "기증자 정자와 혼합된 난자 수", "동결 배아 사용 여부",
        "신선 배아 사용 여부", "기증 배아 사용 여부", "대리모 여부", "PGD 시술 여부",
        "PGS 시술 여부", "난자 채취 경과일", "난자 해동 경과일", "난자 혼합 경과일",
        "배아 이식 경과일", "배아 해동 경과일",  'IVF에서 생성된 배아 수', 'IVF 배아 이식 수',
        'IVF 후 저장된 배아 수', '폐기된 배아 수', '미세주입 배아 실패 수', 'IVF 배아 실패 수']
    df[col] = df[col].astype(int)

    # 횟수로부터, 경험의 여부 변수를 도축
    df['임신 경험 여부'] = df['총 임신 횟수'].apply(lambda x: 1 if x > 0 else 0)
    df['출산 경험 여부'] = df['총 출산 횟수'].apply(lambda x: 1 if x > 0 else 0)
    df['시술 경험 여부'] = df['총 시술 횟수'].apply(lambda x: 1 if x > 0 else 0)


    df['나이_X_이식수'] = df['시술 당시 나이'] * df['이식된 배아 수']

    df['배란자극_X_이식배아수'] = df['배란 자극 여부'].astype(int) * df['이식된 배아 수'] # 배란자극을 한 배아는 뭔가 다를까

    # 남은 배아수
    df['잉여_배아_수'] = df['총 생성 배아 수'] - df['이식된 배아 수']

    # 실제 1만 이식하는 경우
    df['단일_배아_이식_여부_수정'] = df['이식된 배아 수'].apply(lambda x: 1 if x == 1 else 0)

    # 클리닉 외에 시술이 있는지
    df['클리닉 외 시술 여부'] = (df['총 시술 횟수'] - df['클리닉 내 총 시술 횟수']) > 0

    # 생성된 배아수와 이식된 배아수의 비율
    df['이식률'] = np.where(
        df['총 생성 배아 수'] > 0,
        df['이식된 배아 수'] / df['총 생성 배아 수'] * 100,
    -999)

    # 미세주입된 난자와 그로부터 생성된 배아수의 비율
    df['수정률'] = np.where(
        df['미세주입된 난자 수'] > 0,
        df['미세주입에서 생성된 배아 수'] / df['미세주입된 난자 수'] * 100,
    -999)


    # 각 행의 경과일 합계를 새로운 컬럼으로 생성
    elapsed_days_columns = [
        '난자 채취 경과일',
        '난자 해동 경과일',
        '난자 혼합 경과일',
        '배아 이식 경과일',
        '배아 해동 경과일'
    ]

    df['총 경과일 합계'] = df[elapsed_days_columns].sum(axis=1, numeric_only=True)

    # 임신실패 횟수 관련 
    df["총 임신 실패 횟수"] = df["총 임신 횟수"] - df["총 시술 횟수"]

    df["IVF 임신 실패 횟수"] = df["IVF 임신 횟수"] - df["IVF 시술 횟수"]

    df["DI 임신 실패 횟수"] = df["DI 임신 횟수"] - df["DI 시술 횟수"]

    # 유산 횟수 컬럼
    df['총 유산 횟수'] = df['총 임신 횟수'] - df['총 출산 횟수']
    df['IVF 유산 횟수'] = df['IVF 임신 횟수'] - df['IVF 출산 횟수']
    df['DI 유산 횟수'] = df['DI 임신 횟수'] - df['DI 출산 횟수']

    # 난자와 정자의 기증자 나이에 따라 다를 수 있을 것이다.
    df['기증자 나이 합산'] = df['난자 기증자 나이'] + df['정자 기증자 나이']

    # 미세 주입 성공률 -> 난자 미세주입 후 생성 된 배아수에 대한 정보
    df['미세 주입 성공률'] = np.where(
        df['미세주입된 난자 수'] > 0,
        df['미세주입에서 생성된 배아 수'] / df['미세주입된 난자 수'] * 100,
        0
    )

    # 난자 채취 이후 경과일
    df['난자 채취 이후 경과일'] = df['난자 채취 경과일'] + df['배아 이식 경과일']

    # 난자 출처 + 정자 출처
    df['배아 출처'] = df['난자 출처'].astype(str) + df['정자 출처'].astype(str)

    where_mapping = {
        '11' : 1,
        '1-1' : 2,
        '-11' : 3,
        '-1-1' : 4,
        '1-999' : 5,
        '10' : 6,
        '-1-999': 7,
        '-10' : 8
    }

    df['배아 출처'] = df['배아 출처'].map(where_mapping)

    # 특정 시술 유형 카테고리 리스트
    categories = ['ICSI', 'IUI', 'ICI', 'GIFT', 'FER', 'GenericDI', 'IVI', 'BLASTOCYST', 'AH', 'Unknown', 'IVF', '-999', 'ICSI_ICSI', 'IVF_IVF', 'ICSI_Unknown', 'BLASTOCYST_IVF', 'IVF_Unknown', 'ICSI/BLASTOCYST', 'IVF/BLASTOCYST', 'ICSI/AH', 'IVF/AH', 'ICSI/BLASTOCYST_IVF/BLASTOCYST']

    df['특정 시술 유형 (합산 유형)'] = df[[f'특시유_{cat}' for cat in categories]].sum(axis=1)

    # 유전검사를 많이 했는지에 대한 여부를 합산으로 표현
    col = [
    '착상 전 유전 검사 사용 여부',
    '착상 전 유전 진단 사용 여부',
    'PGD 시술 여부',
    'PGS 시술 여부'
    ]

    df['유전검사 (합산통합)'] = df[col].sum(axis=1)

    # 불임원인이 많은지에 대한 여부를 합산으로 표현
    col = [ '남성 주 불임 원인',
    '남성 부 불임 원인',
    '여성 주 불임 원인',
    '여성 부 불임 원인',
    '부부 주 불임 원인',
    '부부 부 불임 원인',
    '불명확 불임 원인',
    '불임 원인 - 난관 질환',
    '불임 원인 - 남성 요인',
    '불임 원인 - 배란 장애',
    '불임 원인 - 자궁경부 문제',
    '불임 원인 - 자궁내막증',
    '불임 원인 - 정자 농도',
    '불임 원인 - 정자 면역학적 요인',
    '불임 원인 - 정자 운동성',
    '불임 원인 - 정자 형태']

    df['불임원인 (합산통합)'] = df[col].sum(axis=1)

    # 모든 남성 원인을 모아 한컬럼으로
    def men_cause(data):

        cri = [
            data['남성 주 불임 원인'] == 1,
            data['남성 부 불임 원인'] == 1,
            data['불임 원인 - 정자 농도'] == 1,
            data['불임 원인 - 정자 면역학적 요인'] == 1,
            data['불임 원인 - 정자 운동성'] == 1,
            data['불임 원인 - 정자 형태'] == 1,
            data['불임 원인 - 남성 요인'] == 1,
        ]

        con = [
            1, 1, 1, 1, 1, 1, 1
        ]

        data['남성 불임 요인'] = np.select(cri, con, default = 0)

        return data
    df = men_cause(df)

    # 모든 여성 원인을 모아 한컬럼으로
    def woman_cause(data):

        cri = [
            data['여성 주 불임 원인'] == 1,
            data['여성 부 불임 원인'] == 1,
            data['불임 원인 - 정자 농도'] == 1,
            data['불임 원인 - 난관 질환'] == 1,
            data['불임 원인 - 배란 장애'] == 1,
            data['불임 원인 - 자궁경부 문제'] == 1,
            data['불임 원인 - 자궁내막증'] == 1,
        ]

        con = [
            1, 1, 1, 1, 1, 1, 1
        ]

        data['여성 불임 요인'] = np.select(cri, con, default = 0)

        return data
    df = woman_cause(df)

    # IVF와 ICSI에서 가장 확률이 높았던 조건들
    def IVF_ICSI_best_condition(data):
        cri = [
            (data['특시유_IVF'] == 1) & (data['이식된 배아 수'] > 1) & (data['배아 이식 경과일'] == 5) & (data['해당 주기 난자 주인 나이'] == 6) & (data['배란 자극 여부'] == 1), 
            (data['특시유_ICSI'] == 1) & (data['이식된 배아 수'] > 1) & (data['배아 이식 경과일'] == 5) & (data['해당 주기 난자 주인 나이'] == 6) & (data['남성 불임 요인'] == 0)
        ]
        con = [
            1, 1
        ]
        data['IVF_ICSI_최상조건'] = np.select(cri, con, default=0)
        return data
    df = IVF_ICSI_best_condition(df)

    return df
