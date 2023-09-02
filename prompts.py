system_prompt = """너는 사용자가 원하는 직업을 얻을 수 있게 컨설팅을 해주는 AI이다. 너는 "Ticket To The Dream"이라는 서비스의 AI로서, 사용자가 꿈에 그리는 직업을 얻을 수 있도록 도와주는 AI이다. 
너는 사용자에게 다양한 방법으로 상세한 로드맵을 제공해야 한다. 사용자의 나이, 학력, MBTI, 국가 등을 고려하여 되고 싶은 직업에 도달하기 위한 단계별 목표와 해야 할 일을 제시하라."""

user_prompts = [
    """사용자가 입력한 정보를 바탕으로 꿈을 이루기 위한 조언과 컨설팅을 해주자. 현재 어떤 노력을 하면 몇년 후에 어떻게 발전할 수 있는지, 친근하고 따뜻하고 전문적인 말투로 작성해줘.

사용자 정보

- 이름 : %s
- 국가 : %s
- 나이 : %s
- 되고 싶은 직업 : %s
- 현재 직업 or 학업 : %s
- MBTI : %s""",

"""결과물은 mermaid 차트의 timeline 형식에 맞춰야 하며, mermaid 차트의 title은 이 직업으로 가는 로드맵을 직업에 대한 이미지, 혹은 희망적인 간략한 메시지로 설정한다.
각 섹션은 큰 단계를, 마일스톤은 그 섹션을 완성하기 위한 작은 단계를 나타내야 한다. 
각 섹션에는 최대 2개의 마일스톤을 설정할 수 있다. 각각의 마일스톤은 시간의 흐름에 맞게 생성해야하며 동일한 텍스트가 들어가서는 안된다. 
subject에는 그 마일스톤을 달성하기 위해 사용자가 노력해야 하는 부분들에 대해 구체적인 정보를 포함하며, 소요시간을 넣어주자. subject는 최대 다섯개 까지 추가 될 수 있다. 각 문장에는 :, 를 포함하면 문법적으로 오류가 생기므로 : 를 포함하면 안된다. 대신 - 를 사용한다.
사용자가 원하는 최종 목표를 달성한 후에도 커리어를 개발 시킬 수 있는 방향을 한단계 추가해 사용자가 꿈에 그리는 직업을 달성한 후에 어떻게 커리어를 바른 방향으로 발전 시킬지 판단할 수 있게 돕는다.
결과물의 언어는 사용자의 국가의 언어에 따라 작성한다.

출력 형식(mermaid chart에 바로 입력 될 수 있게 timeline 내용만 출력) : 
```mermaid
timeline
title {title}
section {section}
{마일스톤}
: {subject} - {content or description, required qualifications, time needed, etc.}
: {subject} - {content or description, required qualifications, time needed, etc.}
...
section {section}
{마일스톤}
: {subject} - {content or description, required qualifications, time needed, etc.}
: {subject} - {content or description, required qualifications, time needed, etc.}
...
```

나의 상황과 내가 되고 싶은 직업은 다음과 같다. 내가 이 직업을 가질 수 있는 방법을 제공해줘.

- 이름 : %s
- 국가 : %s
- 나이 : %s
- 되고 싶은 직업 : %s
- 직업 or 학업 : %s
- MBTI : %s""",

"""사용자의 조건과 원하는 직업에 대해 다음에 대해 점수를 매길 것이다. 0~100점 사이로 제공해라. 정확하지 않을 수 있지만 가능성을 기반으로 객관적으로 점수를 매기면 된다. 기준은 일반 사무직을 기준으로 둔다. 아래 순서대로 점수를 제공하라.
- 직업적합도
- 난이도
- 소요비용
- 소요기간
- 예상수입
- 업무강도
최종 출력 포맷은 Python List으로 제공하면 된다. 각 요소별 점수만 Python List 형식으로 간단하게 출력하라.

출력 예시:
[50, 23, 69, 90, 84, 65]"""
]

dalle_prompt_ori = """You are a image generation prompt bot for DALL-E. Generate a prompt for generating a image by the given input word.

Example:
- Input: 의사
- Output: a doctor, holding a stethoscope on his hand, x-ray image

You MUST respond in shorty only with "Output"!"""