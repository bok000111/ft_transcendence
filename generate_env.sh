#!/bin/bash

chars='abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'

# 랜덤한 문자열을 생성하는 함수
random_string() {
    LC_ALL=C tr -dc "$chars" < /dev/urandom | head -c "$1"
}

# 파일 이름을 첫 번째 인자로 받음
filename="$1"

# 파일 이름이 제공되지 않은 경우 처리
if [ -z "$filename" ]; then
    echo "파일 이름을 제공해주세요."
    exit 1
fi

# 파일 존재 여부 확인
if [ ! -f "$filename" ]; then
    echo "$filename 파일이 존재하지 않습니다."
    exit 1
fi

# 파일을 한 줄씩 읽어서 처리
while IFS='=' read -r key value; do
    # $key와 $value 변수에 각 줄의 키-값 쌍이 할당됨

    # 주석 또는 빈 줄인 경우 무시
    if [[ "$key" == \#* ]] || [ -z "$key" ]; then
        continue
    fi

    # value 문자열에 환경 변수가 포함된 경우 치환
    if [[ "$value" == *\$* ]]; then
        value=$(eval echo "$value")
    fi

    # value 문자열에 명령어 실행이 포함된 경우 실행 결과로 치환
    if [[ "$value" == *\$\(* ]]; then
        value=$(eval "$value")
    fi

    # 특정 키에 따라 값을 변경하는 예시 (DJANGO_SECRET_KEY 예시)
    if [ "$key" = "DJANGO_SECRET_KEY" ]; then
        value=$(random_string 50)
    fi

    # 결과 출력
    echo "$key=$value"

done < "$filename"
