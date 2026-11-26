"""Assemble EP.01 v2: trim/normalize clips, burn Korean subtitles, add end card, concat.

Run from kling_ep01/: python3 assemble_v2.py
Inputs: videos/s1_v2_full.mp4, videos/s2.mp4, videos/v2/s3..s7.mp4
Output: EP01_눈이먹고싶어_v2.mp4
"""
import os
import subprocess
import tempfile

FONT = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
W, H, FPS = 1080, 1920, 24
BROWN = "0x6b4a3a"

# (source, start, duration, [(text, t_in, t_out), ...])
CLIPS = [
    ("videos/s1_v2_full.mp4", 2.0, 8.0, [("우와! 하늘에서 솜사탕이 내려!", 0.8, 4.8)]),
    ("videos/s2.mp4", 0.0, 5.0, []),
    ("videos/v2/s3.mp4", 0.0, 5.0, []),
    ("videos/v2/s4.mp4", 0.0, 6.0, [("……아무 맛도 안 나.", 3.4, 6.0)]),
    ("videos/v2/s5.mp4", 0.0, 5.0, [("이제 안 춥지?", 2.4, 5.0)]),
    ("videos/v2/s6.mp4", 0.0, 6.0, [("에… 에… 에취!!!", 0.2, 2.6)]),
    ("videos/v2/s7.mp4", 0.0, 6.0, [("우와… 달다!", 1.2, 3.4), ("이게 진짜 맛있네!", 3.6, 6.0)]),
]
END_SECONDS = 4.0
END_LINES = [("눈은 달지 않았지만,", 0.40, 64), ("오늘 하루는 참 달콤했어.", 0.46, 64), ("몽글로리 아지트 ♡", 0.58, 72)]


def run(cmd):
    subprocess.run(cmd, check=True)


def textfile(tmp, text):
    fd, path = tempfile.mkstemp(dir=tmp, suffix=".txt")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def subtitle_filter(tmp, text, t_in, t_out):
    tf = textfile(tmp, text)
    return (f"drawtext=fontfile={FONT}:textfile={tf}:fontsize=62:fontcolor=white:"
            f"borderw=6:bordercolor={BROWN}:x=(w-tw)/2:y=h*0.80:"
            f"enable='between(t,{t_in},{t_out})'")


def main():
    tmp = tempfile.mkdtemp()
    parts = []
    for i, (src, ss, dur, subs) in enumerate(CLIPS, 1):
        vf = [f"scale={W}:{H}:force_original_aspect_ratio=increase", f"crop={W}:{H}", "setsar=1", f"fps={FPS}"]
        vf += [subtitle_filter(tmp, *s) for s in subs]
        out = os.path.join(tmp, f"p{i}.mp4")
        run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-t", str(dur), "-i", src,
             "-vf", ",".join(vf), "-af", "aresample=44100,aformat=channel_layouts=stereo",
             "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", out])
        parts.append(out)

    # End card: freeze last frame of the final clip, soften it, overlay the closing lines.
    last_src, last_ss, last_dur, _ = CLIPS[-1]
    still = os.path.join(tmp, "last.png")
    run(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.1", "-i", last_src, "-frames:v", "1", still])
    draws = []
    for text, y, size in END_LINES:
        tf = textfile(tmp, text)
        draws.append(f"drawtext=fontfile={FONT}:textfile={tf}:fontsize={size}:fontcolor={BROWN}:"
                     f"borderw=4:bordercolor=white:x=(w-tw)/2:y=h*{y}:alpha='min(1,t/0.8)'")
    end = os.path.join(tmp, "end.mp4")
    vf = (f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,fps={FPS},"
          f"boxblur=8:1,"
          f"drawbox=x=0:y=0:w=iw:h=ih:color=0xfff6ea@0.45:t=fill," + ",".join(draws) +
          f",fade=t=out:st={END_SECONDS - 0.8}:d=0.8")
    run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", str(END_SECONDS), "-i", still,
         "-f", "lavfi", "-t", str(END_SECONDS), "-i", "anullsrc=r=44100:cl=stereo",
         "-vf", vf, "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-shortest", end])
    parts.append(end)

    n = len(parts)
    inputs = sum((["-i", p] for p in parts), [])
    chain = "".join(f"[{k}:v][{k}:a]" for k in range(n))
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex",
         f"{chain}concat=n={n}:v=1:a=1[v][a]", "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
         "-movflags", "+faststart", "EP01_눈이먹고싶어_v2.mp4"])
    print("wrote EP01_눈이먹고싶어_v2.mp4")


if __name__ == "__main__":
    main()
