# 베이스 이미지 선택
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# libgomp1
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get -y install curl
RUN apt-get install libgomp1

# Poetry에서 변환한 requirements.txt 복사
COPY requirements.txt .

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 포트 설정 (Dash 앱 기본 포트는 8050)
EXPOSE 8050

# Gunicorn 실행 명령
CMD ["gunicorn", "-b", "0.0.0.0:8050", "app:server"]