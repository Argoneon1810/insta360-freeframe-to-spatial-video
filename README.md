# Insta360 FreeFrame to Spatial Video
## 개발이유
Insta360 Studio에서 FreeFrame Video를 크롭하지 않고 Equirectangular로 출력하고 싶었는데, 그런 기능이 없다는 것을 발견했습니다.

ffmpeg을 사용해서 변환할 수 있다는 사실은 이미 수 년 전부터 알려져 있었지만, 
쓸 때 마다 사용 례가 뻔한데 왜 딸깍으로 렌더링 할 수 있는 Wrapper 앱이 존재하지 않는지 의문이 들었습니다. 
더구나, 저는 ffmpeg에 익숙하지 않은지라, 그 순서에 민감한 명령어를 정확하게 기억하고 사용한다는 것은 그리 현실적인 옵션이 아니였습니다.

그래서 Gemini 3.1 Pro의 도움을 받아 만들었습니다. 
몇시간만에 만든 앱이라 선택 가능한 옵션이 별로 없지만, 차차 필요에 따라 개선해 나갈 계획입니다.

## 기능
- 두가지 모드를 지원합니다
  - 여러 비디오를 각각 변환하는 모드
  - 여러 비디오를 하나의 비디오로 병합하여 변환하는 모드 (이름 오름차순)
- FreeFrame Video는 한쪽 면 180도만 촬영하기 때문에, 비는 공간은 검은색으로 패딩하고 있습니다.

## 지원범위
- 현재로써는 Windows OS에서 nvidia nvenc h265를 사용하는 것을 전제로 하드코딩 되어 있습니다.
  - nvidia가 아닌 인코더 디코더와 Ubuntu OS 까지는 지원할 계획을 가지고 있습니다.
- 5.7K 화질 출력을 지원합니다.
  - nvenc의 화질 지원 한계는 8K까지로 알고 있지만, 제 경우 거기까지 높은 화질이 필요하지 않았기 때문에 5.7K로 하드코딩 되었습니다.
  - 원본 촬영물 화질에 비례한 프리셋과, 커스텀 화질을 지원하도록 확장할 계획입니다.
- FFMPEG와 MKVToolNIX가 PATH에 등록되어 있어야 합니다.
  - 두 툴을 호출할 수 있는지 확인한 후, 호출되지 않는다면 사용자에게 안내하는 기능을 지원할 계획입니다.
  - 또한, PATH 등록을 원치 않는 유저를 위해, 두 툴을 호출할 수 있는 커스텀 경로를 지정할 수 있도록 확장할 계획입니다.
 
## 실행 방법
1. 적당한 경로에서 터미널을 열고 다음 명령을 입력해 이 프로젝트를 클론하십시오. `git clone https://github.com/Argoneon1810/insta360-freeframe-to-spatial-video.git`
2. 다음 명령을 실행해 앱을 켜십시오 `python -m main`
3. 나머지는 GUI를 따라 사용하시면 됩니다.
   1. 사용하시면서 불편하신 점이 있으시다면 Issues에 올려 주세요.

---

(The translation below is created with Gemini 3.1 Pro, so there might be some misinterpretation. I will refine it later. For short, below is given for you as a hint.)

# Insta360 FreeFrame to Spatial Video
## Reason for Development
I wanted to export FreeFrame Video to Equirectangular format without cropping it in Insta360 Studio, but I discovered that such a feature didn't exist.

The fact that it can be converted using ffmpeg has been known for years, but I wondered why there wasn't a wrapper app that could render it with a simple click, especially since the use cases are so predictable every time.
Furthermore, since I am not familiar with ffmpeg, accurately remembering and using those order-sensitive commands was not a very realistic option for me.

So, I created this with the help of Gemini 3.1 Pro.
Since it's an app built in just a few hours, there aren't many selectable options available yet, but I plan to gradually improve it as needed.

## Features
- Supports two modes:
  - A mode to convert multiple videos individually.
  - A mode to merge and convert multiple videos into a single video (in ascending alphabetical order of their names).
- Since FreeFrame Video only captures a 180-degree field of view on one side, the empty space is padded with black.

## Supported Scope
- Currently, it is hardcoded on the premise of using NVIDIA nvenc h265 on Windows OS.
  - I plan to support non-NVIDIA encoders/decoders and Ubuntu OS in the future.
- Supports 5.7K resolution output.
  - I am aware that the resolution limit for nvenc is up to 8K, but since I didn't need such high resolution, it is hardcoded to 5.7K.
  - I plan to expand it to support presets proportional to the original footage's resolution and custom resolution settings.
- FFMPEG and MKVToolNIX must be registered in the system PATH.
  - I plan to add a feature that checks if both tools can be called and notifies the user if they cannot.
  - Additionally, for users who do not want to register them in the PATH, I plan to expand the app to allow specifying custom paths to call these two tools.
 
## How to Run
1. Open a terminal in an appropriate directory and enter the following command to clone this project: `git clone https://github.com/Argoneon1810/insta360-freeframe-to-spatial-video.git`
2. Run the following command to launch the app: `python -m main`
3. For the rest, just follow the GUI.
   1. If you experience any inconvenience while using it, please post it in the Issues section.
