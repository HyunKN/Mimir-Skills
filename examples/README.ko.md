[English](README.md) | 한국어

# Examples Directory

이 디렉터리에는 다음을 함께 보여주는 end-to-end example이 들어갈 예정이다.

- trigger event
- canonical JSON decision record
- rendered Markdown summary
- 선택적인 memory candidate promotion

이 디렉터리의 example은 모두 공개 가능한 합성 샘플이어야 한다.

- 실제 secret, 내부 URL, credential, 비공개 incident 정보, raw sensitive log를 복사하지 않는다.
- example은 저장소 구조, schema, workflow를 설명하기 위한 용도로 사용한다.
- `examples/**/.ai/`는 실프로젝트 런타임 출력이 아니라 공개 가능한 샘플 데이터로 취급한다.
- 체크인된 Markdown summary는 파생 산출물이다. source record가 바뀌면 canonical JSON에서 다시 렌더한다.

각 example은 근거와 검증이 분명한 영향도 높은 변경을 다루어야 한다.

현재 example들:

- `windows-ci-timeout/`은 runtime 형태의 `.ai/records/` 구조 안에 canonical decision record 1개와 rendered Markdown summary 1개를 함께 보여준다.
- `cache-client-pin/`은 dependency/config trigger를 다루며, canonical decision record 1개와 JSON source에서 파생된 rendered Markdown summary 1개를 함께 보여준다.
