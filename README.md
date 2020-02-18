# 🥇🥈🥉dailympic🥉🥈🥇

🏌️‍♀️🏄‍♂️🏊‍♂️🚴‍♀️⚽🏀🏐🏈🏉🎱🎳🥌⛳⛸🤿🛶🎿🏒🥍🏓🏸🥋🥊

생활 체육 수업/코칭 매칭 플랫폼 데일림픽

- Django
- JQuery + bootstrap
- MySQL + AWS RDS
- AWS EC2 + nginx + Apache

[Dailympic](http://dailympic.com) ⓒ 2020

## Notice
- DB 처음 생성 시, Board 객체 먼저 생성필요
<br>&nbsp;&nbsp;- 공지사항 게시판 객체 : 게시판 이름-공지사항 / 게시판 고유값-notice
<br>&nbsp;&nbsp;- 자주 묻는 질문 게시판 객체 :
게시판 이름-자주 묻는 질문 / 게시판 고유값-FAQ
<br>&nbsp;&nbsp;- 고객센터 게시판 객체 : 게시판 이름-고객센터 / 게시판 고유값-customer

## Packages to be installed manually
- 이하의 패키지들은 `pip install -r requirements.txt`로 자동 설치되지 않으므로 직접 별도로 설치해야 함.
- django-alluserboard==0.2 : 'django-alluserboard-0.2.tar.gz' 파일을 직접 다운 받은 후, `pip install django-alluserboard-0.2.tar.gz` 명령어를 통해 설치. 
- mysqlclient==1.4.6 : https://stackoverflow.com/questions/42152729/error-installing-mysqlclient-on-ubuntu-16-04-using-pip-and-python-3-6 참고. (ubuntu 환경)
- django-suit==2.0a1 : `pip install https://github.com/darklow/django-suit/tarball/v2` 명령어 사용.