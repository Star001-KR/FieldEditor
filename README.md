### FieldEditor

- 파이썬 GUI 를 이용해 게임에서 사용하는 필드 그룹 및 필드 타일 데이터를 수정하는 툴입니다.
    > Field List 영역 (화면 좌측)


        * 필드 그룹 클릭 후 Select Field 버튼을 통해 필드 그룹을 선택할 수 있습니다.
        * 상단의 상/하 화살표 버튼을 이용해 그룹의 순서를 변경할 수 있습니다.
        * Add Field 윗줄의 추가할 그룹 이름 입력 후 Add Field 버튼을 통해 그룹을 생성할 수 있습니다.
        * Del Field 버튼을 통해 선택중인 필드 그룹을 제거할 수 있습니다.

        
    > Field State 영역 (화면 중앙)


        * 상단의 좌/우 화살표 버튼을 이용해 그룹 선택을 변경할 수 있습니다.
        * Start / Goal 버튼을 통해 Start / Goal 설정 시작 및 종료 상태로 변경할 수 있습니다.
        * 필드의 상태는 버튼으로 구성되어 있고, Start / Goal 설정 시작 상태라면 버튼 클릭 시 Start / Goal 상태로 변경합니다.
        * Start / Goal 설정 시작 상태가 아니라면 Empty > Object > Monster > Empty 순서로 타일 타입을 변경합니다.
        * 하단의 Validate Check 를 통해 현재 작업중인 필드가 사용가능한 상태인지 확인할 수 있습니다. (True 일 경우 사용 가능)


    > Buttons 영역 (화면 우측)
        * Reset 버튼을 통해 툴을 처음 시작했던 상태로 필드 그룹 및 타일 상태를 되돌릴 수 있습니다. (저장을 했더라도 그 이전으로 돌릴 수 있습니다.)
        * Save 버튼을 통해 작업중인 정보를 데이터 테이블에 반영(저장) 할 수 있습니다.

- 파일 경로 안내
    > 샘플 데이터 테이블 경로 : Game/DataSheet/

    
    > 툴 실행용 파이썬 파일 경로 : Tool/FieldEditor/FieldEditor.py


    > 툴 모듈화에 사용한 패키지 파이썬 파일 경로 : Tool/FieldEditor/Package


        * common_function.py : 공통 함수를 관리하는 패키지 파이썬 파일
        * directory.py : 데이터 테이블 경로를 관리하고, OS 별로 대응하도록 구성한 파이썬 파일 (Mac, Windows 대응)
        * field_group.py : 툴 내부의 필드 그룹과 필드 타일 클래스를 정의하는 파이썬 파일
        * Enum_Common.py : 툴에서 사용하는 Enum 을 정리한 파이썬 파일
        * tool_manager.py : 툴에서 사용해야하는 기능적인 부분이 정의된 파이썬 파일
        * gui_mainScreen.py : tool_manager.py 에서 정의한 내용을 바탕으로 gui 를 통해 사용할 수 있도록 하는 파이썬 파일

- 사용 PIP 리스트
    > openpyxl (3.0.7) : 파이썬에서 엑셀 파일을 읽고 쓰는데 사용

- 사용 import 리스트
    > platform : 툴을 사용중인 OS 환경 체크에 사용


    > shutil : 테이블 데이터 파일 복사에 사용


    > os : 임시 파일 생성 및 제거에 사용


    > tkinter : gui 설계에 사용