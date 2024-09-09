# 🌿 2024 이화여대 대동제 : 부스 통합 안내 서비스 🌿

## 🎉 프로젝트 소개

#### 💚 [사이트 바로가기](https://www.liber-ewha.com/) 💚 <br>

2024 이화여대 대동제를 맞이해 '이화여대 멋쟁이 사자처럼 12기'가 (준)축제준비위원회과 협업하여 **부스 통합 안내 서비스**를 제작하였습니다.
<br/> **LiberEwha 홈페이지**는 311개의 부스를 포함해 대동제에 대한 모든 정보를 한번에 모아볼 수 있는 유일한 플랫폼으로써,
<br/> 대동제를 즐기는 벗들의 편의와 즐거움을 증진시키고, 부스를 운영하는 벗들에겐 부스 정보 관리 및 부스 홍보 효과를 제공합니다.
<br/>
<br>

## 🎉 기능

**LiberEwha 홈페이지**가 제공하는 기능은 다음과 같습니다.

1. 부스 위치 및 날짜별 조회 기능
2. 부스 이름 및 메뉴 검색 기능
3. 각 부스의 운영 일정, 위치 지도, 실시간 공지사항, 메뉴 및 품절 여부, 영업 상태 정보 제공
4. 부스 관리자가 부스 및 메뉴 관련 정보를 수정할 수 있는 기능
5. 관심 부스 및 메뉴 스크랩 기능
6. 부스 방명록을 통한 이용 후기 공유
7. 대동제 내 배리어프리 관련 정보 제공
8. (준)축제준비위원회 공지사항, 쓰레기통 및 그릇 반납 장소 안내, 주요 행사 일정 소개

<br>

## 🎉 백엔드 팀원 소개

<table align="center">
    <tr align="center">
        <td style="min-width: 150px;">
            <a href="https://github.com/julia-heo">
              <img src="https://avatars.githubusercontent.com/julia-heo" width="150" height="150" style="object-fit :cover">
            </a>
        </td>
        <td style="min-width: 150px;">
            <a href="https://github.com/y-won1209">
              <img src="https://avatars.githubusercontent.com/y-won1209" width="150" height="150" style="object-fit :cover">
            </a>
        </td>
        <td style="min-width: 150px;">
            <a href="https://github.com/binys21">
              <img src="https://avatars.githubusercontent.com/binys21" width="150" height="150" style="object-fit :cover">
            </a>
        </td>
    </tr>
    <tr align="center">
        <td>
            허채린<br/>
        </td>
        <td>
          심예원<br />
        </td>
        <td>
            이다빈<br />
        </td>
     </tr>
     <tr align="center">
        <td>
            로그인 / 회원가입<br />
            카카오 로그인<br />
            마이페이지<br />
            데이터 수합 페이지  <br />
            배포 / 서버 관리<br />
        </td>
        <td>
            부스 수정 페이지 <br />
            메뉴 수정 페이지 <br />
            공지 조회 페이지 <br />
            공지 등록/수정/삭제 <br />
            상설 부스 페이지  <br />
        </td>
        <td>
            메인 페이지 <br />
            검색 페이지 <br />
            부스 상세 페이지 <br />
            부스 스크랩 구현 <br />
            방명록 작성/수정/삭제 <br />
        </td>
    </tr>
</table>
<br/>

## 🎉 개발 기간

- ERD 설계 : 2024.03.26
- 초기 설정 및 EC2 배포 : 2024.03.28
- API 명세서 작성 및 R&R 정의 : 2024.04.04
- 축제 준비 위원회 공동 회의 : 2024.04.17
- API 개발 : 2024.04.05 ~ 2024.04.20
- 도메인 연결 및 HTTPS 설정 : 2024.04.24
- 데이터 입력 페이지 개발 : 2024.04.24 ~ 2024.04.28
- 부스/공연 관리자 계정 및 데이터 생성 : 2024.04.29
- 부스/공연 데이터 입력 시작: 2024.05.02
- 사이트 공개 : 2024.05.07


<br/>


## 🎉 기술 스택

언어 및 프레임워크 : <img src="https://img.shields.io/badge/python-3776AB?style=flat-square&logo=python&logoColor=white">  <img src="https://img.shields.io/badge/django-%23092E20.svg?style=flat-square&logo=django&logoColor=white">

데이터베이스 :  <img src="https://img.shields.io/badge/mysql-4479A1.svg?style=flat-square&logo=mysql&logoColor=white"> <img src="https://img.shields.io/badge/amazonrds-527FFF?style=flat-square&logo=amazonrds&logoColor=white">

배포 : <img src="https://img.shields.io/badge/amazonec2-FF9900?style=flat-square&logo=amazonec2&logoColor=white"> <img src="https://img.shields.io/badge/amazons3-569A31?style=flat-square&logo=amazons3&logoColor=white"> <img src="https://img.shields.io/badge/docker-2496ED?style=flat-square&logo=docker&logoColor=white"> <img src="https://img.shields.io/badge/nginx-009639?style=flat-square&logo=nginx&logoColor=white">

<br/>


## 🎉 프로젝트 시작

```bash
git clone https://github.com/EWHA-LIKELION/12th-Ewha-Festival-Back.git
```

1. 프로젝트 디렉토리로 이동:

   ```bash
   cd 12th-Ewha-Festival-Back
   ```

2. 가상환경 설정 및 활성화:

   ```bash
   python -m venv venv
   source venv/bin/activate  # (Windows: `venv\Scripts\activate`)
   ```

3. 필수 패키지 설치:

   ```bash
   pip install -r requirements.txt
   ```

4. 환경 변수 설정:

   `.env` 파일을 생성하고 필요한 환경 변수를 설정합니다.
   ```
    DJANGO_ALLOWED_HOSTS=서버에서 허용할 호스트 목록
    DJANGO_SECRET_KEY=Django 프로젝트의 비밀 키
    
    DATABASE_NAME=데이터베이스 이름
    DATABASE_USER=데이터베이스 사용자 이름(root)
    DATABASE_PASSWORD=데이터베이스 비밀번호
    DATABASE_HOST=데이터베이스 호스트(127.0.0.1)
    DATABASE_PORT=3306
    
    AWS_S3_ACCESS_KEY_ID=AWS S3의 접근 키
    AWS_S3_SECRET_ACCESS_KEY=AWS S3의 비밀 접근 키
    AWS_STORAGE_BUCKET_NAME=AWS S3 버킷 이름
    
    KAKAO_CLIENT_ID=카카오 API 클라이언트 ID
    KAKAO_APP_ID=카카오 앱 ID
    KAKAO_CLIENT_SECRET_KEY=카카오 클라이언트 비밀 키
    KAKAO_REDIRECT_URI=카카오 리다이렉트 URI
    KAKAO_USERNAME=카카오 서비스 사용자 이름
    KAKAO_PASSWORD=카카오 서비스 비밀번호
   ```

6. 마이그레이션 및 서버 실행:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

7. 프로젝트에 접근:

   - 브라우저에서 `http://localhost:8000`으로 접속



</br>




## 🎉 커밋 컨벤션
`feat`: 새로운 기능 추가

`fix`: 버그 개선

`refactor`: 새로 추가된 기능은 없지만, 코드를 변경하는 경우

`chore`: 그 외 자잘한 수정

`docs`: 문서 수정

`test`: 테스트 코드
</br>


## 🎉 API 명세서

| **Method** | **Description**                      | **URI**                                                      |
|------------|--------------------------------------|--------------------------------------------------------------|
| POST       | [회원가입](https://freckle-baritone-cbb.notion.site/3b75b67c8d3b4390ba265df518a8b102?pvs=4)                              | `/accounts/signup/`                                           |
| POST       | [로그인](https://freckle-baritone-cbb.notion.site/8875c7e979e046fa8ad7000cf0a473be?pvs=4)                                | `/accounts/login/`                                            |
| GET        | [아이디 중복 여부](https://freckle-baritone-cbb.notion.site/df252dfbb93d4d8eb666551988a1f287?pvs=4)                       | `/accounts/duplicate`                                         |
| GET        | [카톡 로그인](https://freckle-baritone-cbb.notion.site/458f018dbcb0461b998c201a16fa2061?pvs=4)                            | 도메인`/accounts/kakao/`                                      |
| GET        | [카톡 리다이렉트](https://freckle-baritone-cbb.notion.site/97a5ca458dd7404b834a36f745c472bb?pvs=4)                        | 도메인`/accounts/kakao/callback/?code=인증코드`              |
| POST       | [카톡 회원가입 후 닉네임 입력](https://freckle-baritone-cbb.notion.site/b9adc29d193547bb9446ae2dcb0298b6?pvs=4)           | `/accounts/kakao/nickname/`                                   |
| GET        | [프로필 조회](https://freckle-baritone-cbb.notion.site/3a223439d9e14435afea576ee11ae326?pvs=4)                            | `/accounts/`                                                  |
| GET        | [스크랩한 부스 목록 조회, 필터링](https://freckle-baritone-cbb.notion.site/ccd906b488804171b4786ce0b829d2c3?pvs=4)        | `/accounts/likes/?type=부스&page=1`                          |
| GET        | [홈화면](https://freckle-baritone-cbb.notion.site/46e77d66b2014f31a6e48356878d438e?pvs=4)                                | `/booths/home`                                                |
| GET        | [부스 목록 필터링](https://freckle-baritone-cbb.notion.site/ddb36f18cddb4cb09926f670e7702e8f?pvs=4)                       | `/booths/?type=부스&day=int&college=char&page=int`            |
| GET        | [부스 검색](https://freckle-baritone-cbb.notion.site/8527987e243a4da9801a04cdbc5b3061?pvs=4)                              | `/booths/search/?keyword=char&type=부스&page=1`              |
| GET        | [부스 상세 조회](https://freckle-baritone-cbb.notion.site/818b7d93feae423f99e226a8018fce49?pvs=4)                         | `/booths/<int:pk>/`                                           |
| GET        | [부스 댓글 조회](https://freckle-baritone-cbb.notion.site/27258565bdcd4947877e60cb386e6161?pvs=4)                       | `/booths/<int:pk>/comments/`                                  |
| PATCH      | [부스 스크랩 여부 변경](https://freckle-baritone-cbb.notion.site/e85b1a04744b487ba5f7c3f91ac38b22?pvs=4)                  | `/booths/<int:pk>/likes/`                                     |
| PATCH      | [메뉴 스크랩 여부 변경](https://freckle-baritone-cbb.notion.site/5d4121cddba2496bb11892e1c078c310?pvs=4)                  | `/booths/<int:pk>/menu/`                                      |
| POST       | [부스 댓글 작성](https://freckle-baritone-cbb.notion.site/3372d9038ff9493494a6bddbea0f47b1?pvs=4)                         | `/booths/<int:pk>/comments/`                                  |
| PATCH      | [부스 댓글 수정](https://freckle-baritone-cbb.notion.site/fc36d576f50f4880a13165c4b14a1ff9?pvs=4)                         | `/booths/comments/<int:comment_pk>/`                          |
| DELETE     | [부스 댓글 삭제](https://freckle-baritone-cbb.notion.site/e603657f276545f2bf6d3d38ad9ea425?pvs=4)                         | `/booths/comments/<int:comment_pk>/`                          |
| PATCH      | [내 부스 정보 수정](https://freckle-baritone-cbb.notion.site/880886e79b5d4fdaa1aa47f6e41e4177?pvs=4)                     | `/manages/<int:pk>/`                                          |
| GET        | [내 메뉴 목록 조회](https://freckle-baritone-cbb.notion.site/2735071db61a4f59879481fa154a51cb?pvs=4)                     | `/manages/<int:pk>/menus/`                                    |
| GET        | [내 메뉴 조회](https://freckle-baritone-cbb.notion.site/c254a20187af449b90b2ed8fff90a629?pvs=4)                          | `/manages/<int:pk>/menus/<int:menu_pk>/`                      |
| POST       | [내 메뉴 추가](https://freckle-baritone-cbb.notion.site/3ae173712e5449f883002a1b247419bf?pvs=4)                          | `/manages/<int:pk>/menus/`                                    |
| DELETE     | [내 메뉴 삭제](https://freckle-baritone-cbb.notion.site/bc02d2f4a2e140e3a1173686693f09a7?pvs=4)                          | `/manages/<int:pk>/menus/<int:menu_pk>/`                      |
| PATCH      | [내 메뉴 정보 수정](https://freckle-baritone-cbb.notion.site/2da04e9bd9cc4b5596ae010c8caac60f?pvs=4)                     | `/manages/<int:pk>/menus/<int:menu_pk>/`                      |
| GET        | [TF 공지 목록 조회](https://freckle-baritone-cbb.notion.site/TF-82c4afc7753840e983aed5a8b279192e?pvs=4)                     | `/notices/?page=int`                                          |
| POST       | [TF 공지 작성](https://freckle-baritone-cbb.notion.site/TF-dd5decfce7044d61a1210202bf85ae7e?pvs=4)                          | `/notices/`                                                   |
| GET        | [TF 공지 상세 조회](https://freckle-baritone-cbb.notion.site/TF-d543ba8146a54f32a2509587c14cdfc7?pvs=4)                     | `/notices/<int:pk>/`                                          |
| PUT        | [TF 공지 수정](https://freckle-baritone-cbb.notion.site/TF-17050ef361c5442293fc3d2ad358a2c9?pvs=4)                          | `/notices/<int:pk>/`                                          |
| DELETE     | [TF 공지 삭제](https://freckle-baritone-cbb.notion.site/TF-acac59066f794278bc69c0182d05553d?pvs=4)                          | `/notices/<int:pk>/`                                          |
| GET        | [TF 부스 목록 조회](https://freckle-baritone-cbb.notion.site/TF-b5699a0e489442b6833c791ccf8e7b5f?pvs=4)                     | `/notices/event/`                                             |
| GET        | [TF 부스 상세조회](https://freckle-baritone-cbb.notion.site/TF-59fc2e279ef141ecaa2dcbc127aa3ce2?pvs=4                      | `/notices/event/<int:pk>/`                                    |
| PATCH      | [TF 부스 수정](https://freckle-baritone-cbb.notion.site/TF-59e29115d9644e7e9faa8f3fc9fa5195?pvs=4)                          | `/notices/event/<int:pk>/`                                    |
| -          | 데이터수합용 로그인                    | `/collects/login/`                                            |
| -          | 데이터수합용 수정 페이지               | `/collects/detail/`                                           |

