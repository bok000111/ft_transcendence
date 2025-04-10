# 🏓 ft_transcendence - 탁구 게임 웹 서비스

<div align=center>
<img width="300" alt="capture1" src="https://github.com/user-attachments/assets/84c77494-61c8-408d-8eed-e15c230648a8" />
<img width="300" alt="capture2" src="https://github.com/user-attachments/assets/6afc10f0-a6c8-46fe-8f4d-dab2c5dd1b3c" />
<img width="300" alt="capture3" src="https://github.com/user-attachments/assets/54f18b6a-4a5a-4825-b4cb-2838fc0c5ebd" />
<img width="300" alt="capture4" src="https://github.com/user-attachments/assets/e487e54a-1359-4074-a9d1-7bc8b55c1c4e" />
<img width="300" alt="capture5" src="https://github.com/user-attachments/assets/0d61f26a-a354-4643-9017-194d8b3c0325" />
<img width="300" alt="capture6" src="https://github.com/user-attachments/assets/500cde2e-a400-4ffb-a68c-e1417c0e19d0" />
<img width="300" alt="capture7" src="https://github.com/user-attachments/assets/e176e117-367a-48ba-8b30-7aba28a4e8b9" />
<img width="300" alt="capture8" src="https://github.com/user-attachments/assets/33a296f3-0ec7-4101-a89e-36a8bd954d12" />
<img width="300" alt="capture9" src="https://github.com/user-attachments/assets/9f2fcd7c-39f9-4009-87d7-dedb2d84fff4" />
<img width="300" alt="capture10" src="https://github.com/user-attachments/assets/10e2af81-883b-4ccd-9c42-fb94925d1a4b" />
<img width="300" alt="capture11" src="https://github.com/user-attachments/assets/8d8bd575-daff-47c1-9af7-6445a015c996" />

</div>


## 💬 프로젝트 소개
-------------------

<blockquote>Real-time Multiplayer Pong Game with OAuth, Blockchain, 2FA and JWT</blockquote>
<br>

- 웹소켓을 기반으로 한 탁구 게임 서비스로 원격 환경에서 플레이 가능합니다. </br>
- 똑똑한 AI 봇을 상대로 즐길 수 있습니다. </br>
- 토너먼트 기능을 통해 여러 사용자와 함께 토너먼트 대진으로 플레이 가능합니다. </br>
- 친구들과 2:2 팀 게임 진행이 가능합니다. </br>
- 같은 PC로도 친구들과 탁구 게임을 즐길 수 있습니다. </br>

## 🖥️ 개발 기간
- 2024.03.30 ~ 2024.07.11
- 2024.03.30 start
- 2024.06.04 team building
- 2024.07.07 1st try(failed)
- 2024.07.11 passed

## ⚙️ 개발 환경
- Frontend: JavaScript
- Backend: Python, Django
- DataBase: Redis, postgresql
- Blockchain: solidity
- Docker
- nginx

## 🧑‍🤝‍🧑 개발자 소개 및 역할
- ⭐ 복준석(jbok): Backend, Frontend, DevOps
- 강민관(mingkang): Backend, Design
- 도준웅(jdoh): Frontend
- 송선우(sunwsong): Backend, Blockchain
- 이창현(changhyl): Frontend

*******************
## ⛩️ 프로젝트 구조
-------------------
컨테이너 구조
```mermaid
graph TB;
    A[ft_transcendence]
    subgraph docker-compose
        direction LR
        B[nginx]
        C[django]
        D[redis]
        E[postgres]
        F[hardhat]
    end

    A --> docker-compose
    B --> C
    C --> D
    C --> E
    C --> F
```
