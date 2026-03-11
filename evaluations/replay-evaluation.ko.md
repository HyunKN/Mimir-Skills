[English](replay-evaluation.md) | 한국어

# Replay Evaluation

## 목적

이 평가는 새로운 에이전트가 원래 맥락을 다시 추적하지 않고도 저장된 decision artifact만으로 작업을 이어갈 수 있는지 확인하기 위한 것이다.

## 평가 대상 예시

다음 공개 가능한 합성 example 쌍 중 하나를 고른다.

- `../examples/windows-ci-timeout/.ai/records/decisions/dec-20260311-ci-timeout-001.json`
- `../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md`
- `../examples/cache-client-pin/.ai/records/decisions/dec-20260312-cache-client-pin-001.json`
- `../examples/cache-client-pin/.ai/records/reports/cache-client-pin-summary.md`

## 평가자 지침

새 에이전트에게 선택한 example record와 rendered summary만 제공한다.
원래 대화나 숨겨진 구현 메모는 제공하지 않는다.

다음 질문에 답하게 한다.

1. 어떤 결정이 내려졌는가?
2. 왜 그 옵션이 다른 대안보다 선택되었는가?
3. 어떤 파일 또는 workflow 영역이 영향을 받았는가?
4. 어떤 검증이 수행되었는가?
5. 어떤 위험이 남아 있는가?
6. 다음에는 무엇을 해야 하는가?

## 통과 기준

다음 항목을 에이전트가 정확히 복원할 수 있으면 통과다.

- 선택된 변경
- 이를 뒷받침하는 evidence
- 영향받은 경로
- validation 결과
- 남은 risk
- follow-up task

## 실패 신호

다음과 같은 경우 평가는 약하거나 실패로 본다.

- record에 없는 evidence를 꾸며낸다
- 영향받은 경로를 식별하지 못한다
- 남은 risk나 follow-up을 놓친다
- 선택된 옵션과 기각된 대안을 혼동한다

## 참고

- 이 평가는 공개 가능한 합성 example을 기준으로 설계되었다.
- canonical JSON이 바뀌었다면 먼저 validator를 실행한다.
