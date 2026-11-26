# EP.01 '눈이 먹고 싶어!' — Kling 생성 계획

- 비율 9:16 · 장면당 5초 · 7개 장면(생성 7건) · 1080p 기본 · 자막·효과음·내레이션 없음
- 모드: image-to-video (첫 프레임 고정, 일부 장면은 끝 프레임도 지정)
- 공통 스타일 문구(모든 프롬프트 끝에 붙임):
  `soft colored-pencil storybook illustration on grid paper, dashed stitch outlines, pastel cream palette, gentle snowfall, keep the exact character designs: white ermine-like creature with yellow knit scarf, brown raccoon-like creature with dark eye mask and red knit scarf. No text, no speech bubbles, no new characters.`

## 첫 프레임 준비 상태

| 장면 | 원본 | 첫 프레임 | 끝 프레임 |
|---|---|---|---|
| 1 첫눈 발견 | source/01_window.png 3컷 | frames/s1_first_* | – |
| 2 목도리 두르기 | source/02_scarf_room.png 전체 | frames/s2_first_9x16.png | – |
| 3 눈밭으로 출발 | source/03_running.png 2컷 | frames/s3_first_* | frames/s3_tail_* (4컷) |
| 4 눈이 먹고 싶어! | source/04_snow_tongue.png 1컷 | frames/s4_first_* | – |
| 5 철퍼덕 | source/04_snow_tongue.png 3컷 | frames/s5_first_* | frames/s5_tail_* (4컷) |
| 6 눈사람 만들기 | source/05_snowman_build.png 전체 | frames/s6_first_9x16.png | – |
| 7 에취! | source/06_sneeze.png 2컷 | frames/s7_first_* | frames/s7_tail_* (4컷) |

`*_panel.png`는 컷 원본(가로 약 2.3:1), `*_9x16.png`는 컷을 가운데 두고 위아래를 흐린 배경으로 채운 임시본이에요.
가로로 긴 컷은 9:16으로 자르면 캐릭터가 잘려서, 실제 생성 전에는 Kling 이미지 확장(아웃페인팅)으로
위아래 눈 풍경을 그려 채운 9:16 첫 프레임을 만드는 걸 권장해요(이미지 생성 크레딧이 장면당 1건 추가로 들어요).

## 장면별 동작 프롬프트 (5초, 카메라 움직임 1개)

1. **첫눈 발견** — The white creature lying on the windowsill cushion notices the falling snow, its eyes sparkle, it turns and gently shakes the sleepy brown raccoon, who rubs its eyes and yawns. Slow push-in. Snow drifts past the window, lantern glows warmly.
2. **목도리 두르기** — Both wrap their knit scarves around their necks in the cozy entryway; the raccoon's red scarf is far too long and keeps piling on the floor as it winds it, the white one giggles. Static camera, slight sway of the hanging coat.
3. **눈밭으로 출발** — They dash happily across the snowfield; the raccoon steps on its long trailing scarf, stumbles and wobbles, then recovers and keeps running with a big smile. Tracking side shot following them, small snow puffs at their feet.
4. **눈이 먹고 싶어!** — Both look up at the sky, open their mouths wide and stick out their tongues to catch falling snowflakes, blinking happily as flakes land. Slow tilt up toward the sky then back.
5. **철퍼덕** — A clump of snow drops from the branch above onto both their heads with a soft plop; they freeze, blink, sigh a little puff of breath, and look dizzy and deflated. Static camera, a few loose flakes keep falling.
6. **눈사람 만들기** — The white creature wraps the pink scarf around the small snowman's neck while the raccoon pats the snowman's head into shape; they both admire it. Gentle slow push-in, snow falling, warm window light.
7. **에취!** — The white creature shivers and lets out a big sneeze; the snowman's bucket-hat head pops off and rolls away across the snow; both freeze wide-eyed, staring. Static wide shot.
