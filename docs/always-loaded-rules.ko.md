[English](always-loaded-rules.md) | 한국어

# Always-Loaded Rules

## 목적

이 문서는 `decision-skills`의 compact always-loaded baseline이다.

의도적으로 짧게 유지한다.
큰 constitution 문서가 아니며, 더 깊은 workflow, spec, example, evaluation 문서를 대체하지도 않는다.

shared CLI run, future adapter, future entry surface가 저장소 workflow를 호출할 때, 최소한으로 항상 보여야 하는 규칙층으로 사용한다.

## 기본 규칙

1. output은 final truth가 아니라 draft로 취급한다.
2. 먼저 shared CLI surface를 우선한다:
   - `python -m decision_skills prepare-handoff`
   - `python -m decision_skills write-pr-rationale`
3. 사용자가 로컬 브랜치나 working-tree context에서 continuation summary를 원하면 `prepare-handoff`를 사용한다.
4. 사용자가 무엇이 바뀌었는지, 왜 바뀌었는지, 무엇이 검증되었는지, 무엇을 더 봐야 하는지를 설명하는 reviewer-facing text를 원하면 `write-pr-rationale`를 사용한다.
5. `capture-ci-investigation`은 더 좁은 best-effort investigation summary로만 사용한다. 아직 beta이며 root-cause certainty를 약속하지 않는다.
6. canonical decision record가 rendered summary나 workflow draft보다 우선한다.
7. 로컬 evidence로 묶을 수 없는 rationale, validation, confidence를 주장하지 않는다.
8. 로컬 branch context가 너무 얇다면 generic prose로 메우지 말고, 명시적 rationale 또는 evidence note를 추가한다.
9. secret, credential, raw sensitive log, 불필요한 private output은 저장하지 않는다.
10. validation이 없거나, 불완전하거나, 아직 uncertain하면 그대로 말한다.

## 경계

- 이 규칙층은 map-like하게 유지해야 한다.
- 자세한 workflow 동작은 `SKILL.md`, `docs/`, `spec/`, `examples/`, `evaluations/`에 둔다.
- future adapter가 이 baseline을 미러링하거나 embed할 수는 있지만, 조용히 따로 갈라지게 만들면 안 된다.
