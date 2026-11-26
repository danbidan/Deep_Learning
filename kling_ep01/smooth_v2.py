"""Smooth test of EP.01 v2: 0.5s crossfades between scenes + motion interpolation to 48fps (free, post only).
Run from kling_ep01/: python3 smooth_v2.py
"""
import subprocess
SRC = "EP01_눈이먹고싶어_v2.mp4"
OUT = "EP01_눈이먹고싶어_v2_smooth.mp4"
DUR = [8, 5, 5, 6, 5, 6, 6, 4]  # scene lengths in the v2 episode (last = end card)
X = 0.5  # crossfade seconds
starts = [sum(DUR[:i]) for i in range(len(DUR))]
f = []
for i, (s, d) in enumerate(zip(starts, DUR)):
    f.append(f"[0:v]trim={s}:{s+d},setpts=PTS-STARTPTS[v{i}];[0:a]atrim={s}:{s+d},asetpts=PTS-STARTPTS[a{i}]")
vprev, aprev, length = "v0", "a0", DUR[0]
for i in range(1, len(DUR)):
    off = length - X
    f.append(f"[{vprev}][v{i}]xfade=transition=fade:duration={X}:offset={off}[vx{i}]")
    f.append(f"[{aprev}][a{i}]acrossfade=d={X}[ax{i}]")
    vprev, aprev, length = f"vx{i}", f"ax{i}", length + DUR[i] - X
f.append(f"[{vprev}]minterpolate=fps=48:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,format=yuv420p[v]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-filter_complex", ";".join(f),
                "-map", "[v]", "-map", f"[{aprev}]", "-c:v", "libx264", "-crf", "18",
                "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT], check=True)
print("wrote", OUT)
