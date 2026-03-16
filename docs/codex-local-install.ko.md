[English](codex-local-install.md) | 한국어

# Codex 로컬 설치

## 목적

이 문서는 `decision-skills`의 첫 번째 runtime adapter를 설명한다.

remote registry, hosted installer, full multi-agent packaging을 약속하지 않으면서도, Codex에서 실제로 사용할 수 있는 로컬 install path를 제공한다.

이 Codex 경로가 Claude Code, Gemini CLI, Qwen Code, 그리고 shared CLI baseline과 어떤 관계인지 보려면 [Agent Support Levels](agent-support-levels.ko.md)를 참고한다.
future adapter와 shared CLI run에서 같이 보여야 하는 compact rule layer는 [Always-Loaded Rules](always-loaded-rules.ko.md)를 참고한다.

## 무엇이 설치되는가

installer는 현재 outward-facing workflow와 그 internal dependency를 `$CODEX_HOME/skills/` 아래로 복사한다:

- `prepare-handoff`
- `write-pr-rationale`
- `capture-ci-investigation`
- `handoff-context`
- `pr-rationale`
- `ci-rationale`
- `decision-capture`
- `decision-core`

또한 install 뒤에도 example과 evaluation reference가 계속 해석되고, 설치된 direct-use script가 shared `decision_skills` runtime package를 계속 import할 수 있도록, 공개 가능한 support asset을 `$CODEX_HOME/skills/decision-skills-support/` 아래로 복사한다.

## 설치

현재 outward-facing workflow 전체를 기본 Codex home에 설치:

```bash
python adapters/codex/scripts/install_codex_skills.py
```

선택한 workflow만 설치:

```bash
python adapters/codex/scripts/install_codex_skills.py --workflows prepare-handoff write-pr-rationale
```

특정 Codex home에 설치하고 기존 설치본을 교체:

```bash
python adapters/codex/scripts/install_codex_skills.py --codex-home ~/.codex --force
```

## Quick Start

설치 후에는 Codex에게 다음과 같이 직접 workflow 언어로 요청할 수 있다:

- `Prepare a handoff from my current changes.`
- `Write PR rationale for this branch.`
- `Summarize this CI failure as a bounded investigation note.`

그러면 Codex는 이런 prompt를 기준으로 설치된 workflow skill을 trigger할 수 있고, wrapper가 이미 direct draft generation을 지원하는 곳에서는 함께 설치된 script도 사용할 수 있다.

## 피드백 루프

실제 사용 뒤에는 [Adapter 피드백 루프](adapter-feedback-loop.ko.md)의 가벼운 검토 절차를 사용한다.

현재 목표는 설치된 workflow가 더 넓은 adapter 작업을 정당화할 만큼 빠르게 유용한 draft를 만드는지 배우는 것이지, 첫 adapter 경로가 이미 최종 형태라고 주장하는 것이 아니다.

## 현재 한계

- 이것은 Codex 전용 로컬 install path다.
- remote skill registry에 공개하는 방식은 아니다.
- 저장소의 모든 internal workflow를 설치하지는 않는다.
- output은 여전히 draft이며 human review가 필요하다.
- `capture-ci-investigation`은 여전히 더 좁은 beta wrapper이며, direct-use collector나 generator script는 아직 포함하지 않는다.
