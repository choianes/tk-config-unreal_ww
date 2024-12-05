import os
import sgtk

# HookBaseClass는 ShotGrid의 기본 Collector 기능을 상속받습니다.
HookBaseClass = sgtk.get_hook_baseclass()

class CustomCollector(HookBaseClass):
    def process_current_session(self, settings, parent_item):
        """
        현재 Maya 세션 및 관련 FBX 파일을 수집합니다.
        """
        # 현재 엔진 이름 확인 (Maya 엔진인지 검증)
        engine_name = self.parent.engine.name
        if engine_name != "tk-maya":
            self.logger.warning(f"이 Collector는 Maya에서만 동작합니다. 현재 엔진: {engine_name}")
            return

        # 현재 열려있는 Maya 파일 경로 가져오기
        current_file_path = self.parent.engine.current_file_path
        if not current_file_path:
            self.logger.warning("현재 Maya 세션이 저장되지 않았습니다. 세션 파일이 수집되지 않습니다.")
            return

        # Maya 세션 파일을 수집
        self._collect_maya_file(parent_item, current_file_path)

        # 같은 디렉토리에 있는 FBX 파일을 수집
        self._collect_fbx_files(parent_item, os.path.dirname(current_file_path))

    def _collect_maya_file(self, parent_item, file_path):
        """
        현재 Maya 세션 파일을 수집합니다.
        """
        # 파일명 추출
        file_name = os.path.basename(file_path)

        # Maya 파일 아이템 생성
        maya_item = parent_item.create_item(
            "maya.session",
            "Maya File",
            file_name
        )
        maya_item.properties["path"] = file_path

        # 추가 정보 로그
        self.logger.info(f"Maya 파일 수집 완료: {file_path}")

    def _collect_fbx_files(self, parent_item, directory):
        """
        현재 Maya 파일과 동일한 디렉토리에 있는 FBX 파일을 수집합니다.
        """
        if not os.path.isdir(directory):
            self.logger.warning(f"디렉토리 경로가 잘못되었습니다: {directory}")
            return

        # 디렉토리 내 FBX 파일 탐색
        for file_name in os.listdir(directory):
            if file_name.lower().endswith(".fbx"):
                fbx_path = os.path.join(directory, file_name)
                self._create_fbx_item(parent_item, fbx_path)

    def _create_fbx_item(self, parent_item, file_path):
        """
        FBX 파일 아이템을 생성하고 수집합니다.
        """
        # 파일명 추출
        file_name = os.path.basename(file_path)

        # FBX 파일 아이템 생성
        fbx_item = parent_item.create_item(
            "file.fbx",
            "FBX File",
            file_name
        )
        fbx_item.properties["path"] = file_path

        # 추가 정보 로그
        self.logger.info(f"FBX 파일 수집 완료: {file_path}")
