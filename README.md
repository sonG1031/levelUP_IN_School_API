# 학교에서 레벨업 API (levelUP IN School API)

### 가상환경
> ~/venvs> python3 -m venv swcontest  
> python -m venv는 파이썬 모듈 중 venv라는 모듈을 사용한다는 의미, 그 뒤는 가상환경 이름  
> > cd venvs/swcontest/bin  
> > source activate (가상환경 활성화)  
> > deactivate (가상환경 비활성화)
> > ***
> > [/Users/pulledsub/.zshrc] (가상환경 간편활성화)  
> > alias swcontest='export FLASK_APP=api;export FLASK_DEBUG=true;cd /Users/pulledsub/projects/levelUP_IN_School_API;source /Users/pulledsub/venvs/swcontest/bin/activate'

### 서버실행
> 플라스크 서버를 실행하려면 반드시 FLASK_APP 환경 변수에 플라스크 애플리케이션을 설정  
> export FLASK_APP=api;export FLASK_DEBUG=true; 

### pip install List
> pip install flask  
> pip install flask-migrate  
> pip install bcrypt  
> pip install pyjwt  
> pip install email_validator

### 기억해둘것
> ORM은 데이터베이스에 데이터를 저장하는 테이블을 파이썬 클래스로 만들어 관리하는 기술로 이해해도 좋다.  
> [ORM 적용]  
> db 객체를 create_app 함수 안에서 생성하면 블루프린트와 같은 다른 모듈에서 사용할수 없기 때문에 db, migrate와 같은 객체를 create_app 함수 밖에 생성하고, 해당 객체를 앱에 등록할 때는 create_app 함수에서 init_app 함수를 통해 진행한다.  
***
> flask db init 명령으로 데이터베이스를 초기화  
> flask db init 명령은 데이터베이스를 관리하는 초기 파일들을 다음처럼 migrations 디렉터리에 자동으로 생성한다.  
> flask db migrate : 모델을 새로 생성하거나 변경할 때 사용 (실행하면 작업파일이 생성된다.)  
> flask db upgrade : 모델의 변경 내용을 실제 데이터베이스에 적용할 때 사용 (위에서 생성된 작업파일을 실행하여 데이터베이스를 변경한다.)  
> 모델 클래스는 db.Model 클래스를 상속하여 만들어야 한다.  
>  모델을 서로 연결할 때에는 위와 같이 db.ForeignKey를 사용.  
> 데이터베이스에서는 기존 모델과 연결된 속성을 외부 키(foreign key)라고 한다.
