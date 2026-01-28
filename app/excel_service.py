import pandas as pd


HEADERS = [
    "고객번호",
    "레인보우포인트",
    "소멸예정포인트",
    "국내음성통화량",
    "데이터이용량",
    "문자메시지이용량",
    "요금제",
    "요금항목",
    "금액",
]


def process_excel(input_path, output_path, prefix):
    # Sheet1 읽기
    df = pd.read_excel(input_path, sheet_name=0)

    # 👉 A:I 컬럼만 사용 (엑셀 수식과 동일)
    df = df.iloc[:, :9]

    col_a = df.iloc[:, 0].astype(str)

    # 접두어 필터
    filtered = df[col_a.str.startswith(prefix, na=False)]

    # A열 기준 중복 제거 (행 전체 유지)
    filtered_unique = filtered.drop_duplicates(subset=[df.columns[0]])

    # 헤더 적용
    filtered_unique.columns = HEADERS

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Sheet1", index=False)
        filtered_unique.to_excel(writer, sheet_name="Sheet2", index=False)

    return filtered_unique.fillna("").values.tolist()
