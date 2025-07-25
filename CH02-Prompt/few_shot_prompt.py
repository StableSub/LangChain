import os
import click
from dotenv import load_dotenv
from langchain_teddynote import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts.few_shot import FewShotPromptTemplate
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
os.environ["LANGCHAIN_PROJECT"] = "CH02-Prompt"

llm = ChatGoogleGenerativeAI (
    model="gemini-2.5-flash",
    temperature=0.4,
    api_key=os.getenv("GOOGLE_API_KEY")
)

examples1 = [
    {
        "question": "스티브 잡스와 아인슈타인 중 누가 더 오래 살았나요?",
        "answer": """이 질문에 추가 질문이 필요한가요: 예.
추가 질문: 스티브 잡스는 몇 살에 사망했나요?
중간 답변: 스티브 잡스는 56세에 사망했습니다.
추가 질문: 아인슈타인은 몇 살에 사망했나요?
중간 답변: 아인슈타인은 76세에 사망했습니다.
최종 답변은: 아인슈타인
        """,
            },
        {
            "question": "네이버의 창립자는 언제 태어났나요?",
            "answer": """이 질문에 추가 질문이 필요한가요: 예.
추가 질문: 네이버의 창립자는 누구인가요?
중간 답변: 네이버는 이해진에 의해 창립되었습니다.
추가 질문: 이해진은 언제 태어났나요?
중간 답변: 이해진은 1967년 6월 22일에 태어났습니다.
최종 답변은: 1967년 6월 22일
    """,
        },
        {
            "question": "율곡 이이의 어머니가 태어난 해의 통치하던 왕은 누구인가요?",
            "answer": """이 질문에 추가 질문이 필요한가요: 예.
추가 질문: 율곡 이이의 어머니는 누구인가요?
중간 답변: 율곡 이이의 어머니는 신사임당입니다.
추가 질문: 신사임당은 언제 태어났나요?
중간 답변: 신사임당은 1504년에 태어났습니다.
추가 질문: 1504년에 조선을 통치한 왕은 누구인가요?
중간 답변: 1504년에 조선을 통치한 왕은 연산군입니다.
최종 답변은: 연산군
    """,
        },
        {
            "question": "올드보이와 기생충의 감독이 같은 나라 출신인가요?",
            "answer": """이 질문에 추가 질문이 필요한가요: 예.
추가 질문: 올드보이의 감독은 누구인가요?
중간 답변: 올드보이의 감독은 박찬욱입니다.
추가 질문: 박찬욱은 어느 나라 출신인가요?
중간 답변: 박찬욱은 대한민국 출신입니다.
추가 질문: 기생충의 감독은 누구인가요?
중간 답변: 기생충의 감독은 봉준호입니다.
추가 질문: 봉준호는 어느 나라 출신인가요?
중간 답변: 봉준호는 대한민국 출신입니다.
최종 답변은: 예
    """,
        },
        ]
examples2 = [
    {
        "instruction": "당신은 회의록 작성 전문가 입니다. 주어진 정보를 바탕으로 회의록을 작성해 주세요",
        "input": "2023년 12월 25일, XYZ 회사의 마케팅 전략 회의가 오후 3시에 시작되었다. 회의에는 마케팅 팀장인 김수진, 디지털 마케팅 담당자인 박지민, 소셜 미디어 관리자인 이준호가 참석했다. 회의의 주요 목적은 2024년 상반기 마케팅 전략을 수립하고, 새로운 소셜 미디어 캠페인에 대한 아이디어를 논의하는 것이었다. 팀장인 김수진은 최근 시장 동향에 대한 간략한 개요를 제공했으며, 이어서 각 팀원이 자신의 분야에서의 전략적 아이디어를 발표했다.",
        "answer": """
회의록: XYZ 회사 마케팅 전략 회의
일시: 2023년 12월 25일
장소: XYZ 회사 회의실
참석자: 김수진 (마케팅 팀장), 박지민 (디지털 마케팅 담당자), 이준호 (소셜 미디어 관리자)

1. 개회
   - 회의는 김수진 팀장의 개회사로 시작됨.
   - 회의의 목적은 2024년 상반기 마케팅 전략 수립 및 새로운 소셜 미디어 캠페인 아이디어 논의.

2. 시장 동향 개요 (김수진)
   - 김수진 팀장은 최근 시장 동향에 대한 분석을 제시.
   - 소비자 행동 변화와 경쟁사 전략에 대한 통찰 공유.

3. 디지털 마케팅 전략 (박지민)
   - 박지민은 디지털 마케팅 전략에 대해 발표.
   - 온라인 광고와 SEO 최적화 방안에 중점을 둠.

4. 소셜 미디어 캠페인 (이준호)
   - 이준호는 새로운 소셜 미디어 캠페인에 대한 아이디어를 제안.
   - 인플루언서 마케팅과 콘텐츠 전략에 대한 계획을 설명함.

5. 종합 논의
   - 팀원들 간의 아이디어 공유 및 토론.
   - 각 전략에 대한 예산 및 자원 배분에 대해 논의.

6. 마무리
   - 다음 회의 날짜 및 시간 확정.
   - 회의록 정리 및 배포는 박지민 담당.
""",
    },
    {
        "instruction": "당신은 요약 전문가 입니다. 다음 주어진 정보를 바탕으로 내용을 요약해 주세요",
        "input": "이 문서는 '지속 가능한 도시 개발을 위한 전략'에 대한 20페이지 분량의 보고서입니다. 보고서는 지속 가능한 도시 개발의 중요성, 현재 도시화의 문제점, 그리고 도시 개발을 지속 가능하게 만들기 위한 다양한 전략을 포괄적으로 다루고 있습니다. 이 보고서는 또한 성공적인 지속 가능한 도시 개발 사례를 여러 국가에서 소개하고, 이러한 사례들을 통해 얻은 교훈을 요약하고 있습니다.",
        "answer": """
문서 요약: 지속 가능한 도시 개발을 위한 전략 보고서

- 중요성: 지속 가능한 도시 개발이 필수적인 이유와 그에 따른 사회적, 경제적, 환경적 이익을 강조.
- 현 문제점: 현재의 도시화 과정에서 발생하는 주요 문제점들, 예를 들어 환경 오염, 자원 고갈, 불평등 증가 등을 분석.
- 전략: 지속 가능한 도시 개발을 달성하기 위한 다양한 전략 제시. 이에는 친환경 건축, 대중교통 개선, 에너지 효율성 증대, 지역사회 참여 강화 등이 포함됨.
- 사례 연구: 전 세계 여러 도시의 성공적인 지속 가능한 개발 사례를 소개. 예를 들어, 덴마크의 코펜하겐, 일본의 요코하마 등의 사례를 통해 실현 가능한 전략들을 설명.
- 교훈: 이러한 사례들에서 얻은 주요 교훈을 요약. 강조된 교훈에는 다각적 접근의 중요성, 지역사회와의 협력, 장기적 계획의 필요성 등이 포함됨.

이 보고서는 지속 가능한 도시 개발이 어떻게 현실적이고 효과적인 형태로 이루어질 수 있는지에 대한 심도 있는 분석을 제공합니다.
""",
    },
    {
        "instruction": "당신은 문장 교정 전문가 입니다. 다음 주어진 문장을 교정해 주세요",
        "input": "우리 회사는 새로운 마케팅 전략을 도입하려고 한다. 이를 통해 고객과의 소통이 더 효과적이 될 것이다.",
        "answer": "본 회사는 새로운 마케팅 전략을 도입함으로써, 고객과의 소통을 보다 효과적으로 개선할 수 있을 것으로 기대된다.",
    },
]


@click.group()
def cli():
    pass

@cli.command()
def sol1(): #FewShotPromptTemplate을 이용하여 예제를 직접 제공하여 문제 해결 방법을 유도

    example_prompt = PromptTemplate.from_template(
        "Question:\n{question}\nAnswer:\n{answer}"
    )
    print(example_prompt.format(**examples1[0]))
    prompt = FewShotPromptTemplate(
        examples = examples1,
        example_prompt = example_prompt,
        suffix = "Question:\n{question}\nAwnser:",
        input_variables=["question"],
    )
    chain = prompt | llm | StrOutputParser()
    for token in chain.stream({"question": "구글이 창림된 연도에 빌게이츠의 나이는?"}):
        print(token, end="", flush=True)

@cli.command()
def sol2(): # 예제가 많아질 경우 프롬프트에 포함할 예제를 선택하는 방법
    from langchain_core.example_selectors import (
        MaxMarginalRelevanceExampleSelector,
        SemanticSimilarityExampleSelector
    )
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    from langchain_chroma import Chroma
    
    chroma = Chroma("example_selector", GoogleGenerativeAIEmbeddings(model="models/embedding-001")) # 벡터 DB 생성

    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples1, # 선택 가능한 예시 목록
        GoogleGenerativeAIEmbeddings(model="models/embedding-001"), # 의미적 유사성을 측정하는 데 사용되는 임베딩을 생성하는 임베딩 클래스
        Chroma, # 임베딩을 저장하고 유사성 검색을 수행하는 데 사용되는 벡터 스토어 클래스
        k=1 # 생성할 예시의 수
    )
    
    question = "Google이 창립된 연도에 Bill Gates의 나이는 몇 살인가요?"
    
    selected_examples = example_selector.select_examples({"question": question})
        
    print(f"입력에 가장 유사한 예시:\n{question}\n")
    for example in selected_examples:
        print(f'question:\n{example["question"]}')
        print(f'answer:\n{example["answer"]}')
    
    example_prompt = PromptTemplate.from_template(
        "Question:\n{question}\nAnswer:\n{answer}"
    )
    
    prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        suffix= "Question:\n{question}\nAnswer:",
        input_variables=["question"],
    )

    chain = prompt | llm | StrOutputParser()
    
    for token in chain.invoke({"question" : question}):
        print(token, end="", flush=True)
    
@cli.command()
def sol3():
    from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
    from langchain_core.example_selectors import (
        SemanticSimilarityExampleSelector,
    )
    from langchain_chroma import Chroma
    from langchain_google_genai import GoogleGenerativeAIEmbeddings

    chroma = Chroma("fewshot_chat", GoogleGenerativeAIEmbeddings(model="models/embedding-001"))

    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{instruction}:\n{input}"),
            ("ai", "{answer}"),
        ]
    )
    
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples2,
        GoogleGenerativeAIEmbeddings(model="models/embedding-001"),
        Chroma,
        k=1
    )
    
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
    )

    question = {
    "instruction": "회의록을 작성해 주세요",
    "input": "2023년 12월 26일, ABC 기술 회사의 제품 개발 팀은 새로운 모바일 애플리케이션 프로젝트에 대한 주간 진행 상황 회의를 가졌다. 이 회의에는 프로젝트 매니저인 최현수, 주요 개발자인 황지연, UI/UX 디자이너인 김태영이 참석했다. 회의의 주요 목적은 프로젝트의 현재 진행 상황을 검토하고, 다가오는 마일스톤에 대한 계획을 수립하는 것이었다. 각 팀원은 자신의 작업 영역에 대한 업데이트를 제공했고, 팀은 다음 주까지의 목표를 설정했다.",
    }

    final_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant.",
            ),
            few_shot_prompt,
            ("human", "{instruction}\n{input}"),
        ]
    )

    chain = final_prompt | llm | StrOutputParser()

    for token in chain.invoke(question):
        print(token, end="", flush=True)

@cli.command()
def sol4(): # 유사도 문제 해결
    from langchain_teddynote.prompts import CustomExampleSelector
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
    from langchain_core.example_selectors import (
        SemanticSimilarityExampleSelector,
    )
    from langchain_chroma import Chroma
    from langchain_google_genai import GoogleGenerativeAIEmbeddings

    custom_selector = CustomExampleSelector(examples2, GoogleGenerativeAIEmbeddings(model="models/embedding-001"))

    custom_selector.select_examples({"instruction": "다음 문장을 교정 작성해 주세요"})
    
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{instruction}:\n{input}"),
            ("ai", "{answer}"),
        ]
    )

    custom_fewshot_prompt = FewShotChatMessagePromptTemplate(
        example_selector=custom_selector,  # 커스텀 예제 선택기 사용
        example_prompt=example_prompt,  # 예제 프롬프트 사용
    )

    custom_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant.",
            ),
            custom_fewshot_prompt,
            ("human", "{instruction}\n{input}"),
        ]
    )
    
    chain = custom_prompt | llm | StrOutputParser()
    
    question = {
        "instruction": "회의록을 작성해 주세요",
        "input": "2023년 12월 26일, ABC 기술 회사의 제품 개발 팀은 새로운 모바일 애플리케이션 프로젝트에 대한 주간 진행 상황 회의를 가졌다. 이 회의에는 프로젝트 매니저인 최현수, 주요 개발자인 황지연, UI/UX 디자이너인 김태영이 참석했다. 회의의 주요 목적은 프로젝트의 현재 진행 상황을 검토하고, 다가오는 마일스톤에 대한 계획을 수립하는 것이었다. 각 팀원은 자신의 작업 영역에 대한 업데이트를 제공했고, 팀은 다음 주까지의 목표를 설정했다.",
    }
    
    for token in chain.invoke(question):
        print(token, end="", flush=True)

    question = {
        "instruction": "문서를 요약해 주세요",
        "input": "이 문서는 '2023년 글로벌 경제 전망'에 관한 30페이지에 달하는 상세한 보고서입니다. 보고서는 세계 경제의 현재 상태, 주요 국가들의 경제 성장률, 글로벌 무역 동향, 그리고 다가오는 해에 대한 경제 예측을 다룹니다. 이 보고서는 또한 다양한 경제적, 정치적, 환경적 요인들이 세계 경제에 미칠 영향을 분석하고 있습니다.",
    }
    for token in chain.invoke(question):
        print(token, end="", flush=True)

    question = {
        "instruction": "문장을 교정해 주세요",
        "input": "회사는 올해 매출이 증가할 것으로 예상한다. 새로운 전략이 잘 작동하고 있다.",
    }
    for token in chain.invoke(question):
        print(token, end="", flush=True)
        
cli()
