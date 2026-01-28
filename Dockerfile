FROM python:3.11-slim

# 환경 변수: 모든 최적화 기능을 비활성화하여 호환성 극대화
ENV PIP_NO_BINARY=numpy
ENV NPY_DISABLE_CPU_FEATURES="AVX,AVX2,FMA,SSE4_1,SSE4_2,AVX512F"
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 빌드 필수 도구 설치 (slim 이미지 사용 시 필수)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# NumPy를 먼저 무조건 소스에서 빌드하여 설치 (v1.26.x 대역이 안정적입니다)
RUN pip install --no-cache-dir --force-reinstall "numpy<2.0.0"

# 나머지 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
RUN mkdir -p data/uploads data/outputs

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]