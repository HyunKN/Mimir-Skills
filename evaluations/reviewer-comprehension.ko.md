[English](reviewer-comprehension.md) | 한국어

# Reviewer Comprehension Evaluation

## 목적

이 평가는 rendered summary와 canonical record만으로 리뷰어가 변경 이유를 빠르게 이해할 수 있는지 확인하기 위한 것이다.

## 평가 대상 예시

다음 공개 가능한 합성 example 쌍 중 하나를 고른다.

- `../examples/windows-ci-timeout/.ai/records/reports/windows-ci-timeout-summary.md`
- `../examples/windows-ci-timeout/.ai/records/decisions/dec-20260311-ci-timeout-001.json`
- `../examples/cache-client-pin/.ai/records/reports/cache-client-pin-summary.md`
- `../examples/cache-client-pin/.ai/records/decisions/dec-20260312-cache-client-pin-001.json`

## 리뷰 질문

리뷰어 또는 평가자에게 다음 질문에 답하게 한다.

1. 무엇이 바뀌었는가?
2. 왜 바뀌었는가?
3. 어떤 evidence가 이 변경을 뒷받침하는가?
4. 무엇을 테스트했는가?
5. 아직 무엇을 주의해야 하는가?

## 통과 기준

원래 task transcript 없이도 다섯 질문에 답할 수 있으면 통과다.

## 실패 신호

다음과 같은 경우 평가는 약하거나 실패로 본다.

- summary가 실제 결정 이유를 가린다
- evidence가 너무 모호해서 주장을 뒷받침하지 못한다
- validation 결과가 없거나 불명확하다
- 남은 risk나 follow-up이 summary와 record 모두에서 빠져 있다

## 참고

- 먼저 Markdown summary를 읽고, 세부사항은 JSON record에서 확인한다.
- 목표는 장황함이 아니라 빠르고 신뢰할 수 있는 이해다.
