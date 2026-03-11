[English](CONTRIBUTING.md) | 한국어

# Contributing

`decision-skills`에 기여해주셔서 감사합니다.

이 저장소는 문서 우선 프로젝트입니다. 기여는 decision record, example, skill, evaluation asset를 더 이해하기 쉽고, 검증 가능하며, 재사용 가능하게 만드는 방향이어야 합니다.

## 좋은 첫 기여 유형

- 공개 문서를 개선하거나 terminology를 더 명확히 하기
- 기존 example을 깨지 않으면서 spec을 확장하기
- 공개 가능한 synthetic example 추가하기
- 보안 표면을 넓히지 않으면서 validator 또는 renderer 동작 개선하기
- evaluation prompt나 reviewer guidance 추가하기
- skill instruction이나 reference 다듬기

## 변경 전에 할 일

1. [README.ko.md](README.ko.md), [SECURITY.ko.md](SECURITY.ko.md), [docs/project-one-pager.ko.md](docs/project-one-pager.ko.md)를 읽는다.
2. example, skill, script를 바꾸기 전에는 관련 spec을 먼저 확인한다.
3. 저장소 전체를 크게 뒤집기보다 작고 리뷰 가능한 변경을 우선한다.

## 저장소 규칙

- canonical decision record는 JSON으로 유지한다.
- Markdown summary는 source of truth가 아니라 파생 산출물로 취급한다.
- example은 공개 가능한 synthetic sample로 유지한다.
- secret, 내부 URL, 비공개 incident 정보, raw sensitive log를 추가하지 않는다.
- `.workspace/`는 로컬에 두고 GitHub 공개 범위에서 제외한다.
- JSON key, schema field name, file path는 영어를 유지한다.

## 언어 규칙

- 의미 기준 원문은 English 파일이다.
- 공개 매뉴얼과 개발 문서는 그 문서 종류가 이미 이중 언어라면 Korean 동반 문서를 유지한다.
- English 원문이 바뀌면 Korean 동반 문서도 직접 번역 형태로 함께 갱신한다.
- 두 언어에서 섹션 순서와 링크 구조를 맞춘다.

## Scripts And Hooks

- hook보다 bounded script를 먼저 선호한다.
- 새 자동화는 local-first, reviewable, safe-by-default여야 한다.
- 기본적으로 network-dependent automation, remote installer, secret-dependent behavior를 추가하지 않는다.
- v0.1에서는 draft decision record에 대해 blocking pre-save hook을 추가하지 않는다.
- 미래에 hook을 제안한다면, 좁은 범위로 두고, 명시적이며, 가능하면 warning-only이거나 finalization 단계에 묶인 형태를 선호한다.

## Examples And Evaluations

- 새 example에는 `.ai/records/decisions/` 아래 canonical JSON decision record가 포함되어야 한다.
- summary를 포함한다면 JSON record에서 렌더하거나, 적어도 JSON source에서 파생된 산출물임이 분명해야 한다.
- 새 example이 workflow coverage를 실질적으로 넓힌다면 evaluation 문서도 함께 업데이트한다.

## Validation Checklist

기여를 열기 전에 변경에 맞는 검증을 실행한다.

- 공개 example end-to-end 검증: `python scripts/verify_examples.py`
- canonical record 검증: `python skills/decision-core/scripts/validate_decision_record.py <path>`
- summary 렌더링: `python skills/decision-capture/scripts/render_summary.py <record-path> --output <summary-path>`
- 수정한 이중 언어 문서 쌍을 다시 읽고 Korean 파일이 English 원문을 그대로 반영하는지 확인한다

새 기능이 들어오면 그 기능이 동작함을 입증하는 가장 작은 검사를 CI에 추가한다. 기본적으로 관련 없는 검사까지 한꺼번에 넓히지는 않는다.

## Security Reporting

기여 과정에서 보안 문제를 발견했다면, 민감한 내용을 공개 issue로 올리기보다 [SECURITY.ko.md](SECURITY.ko.md)를 따른다.
