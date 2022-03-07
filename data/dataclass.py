from dataclasses import dataclass

@dataclass
class TabInfo:
    """
    tab 제목을 위한 struct
    """
    tab1 = "KimJunHee Resume"
    tab2 = "video"

@dataclass
class WindowSize:
    """
    Window size 설정을 위한 struct
    """
    default_width = 700     # 기본 넓이
    default_height = 700    # 기본 높이
    minimum_width = 500     # 최소 넓이
    minimum_height = 500    # 최소 높이
    maximum_width = 900     # 최대 넓이
    maximum_height = 900    # 최대 높이