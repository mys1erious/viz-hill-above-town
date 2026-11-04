# Soft lo-fi bed for the 20 s video, pure stdlib: pad chords, plucked notes, wind, crickets after dark.
import math, random, struct, wave, sys
SR, DUR = 44100, 16.0
N = int(SR * DUR)
random.seed(473289)
TAU = 2 * math.pi
CH = [  # (start, notes Hz) Fmaj7, Em7, Dm7, Cmaj7
    (0, [87.31, 174.61, 220.0, 261.63, 329.63]),
    (4, [82.41, 164.81, 196.0, 246.94, 293.66]),
    (8, [73.42, 146.83, 174.61, 220.0, 261.63]),
    (12, [65.41, 130.81, 164.81, 196.0, 246.94]),
]
MEL = [(0.3, 659.25), (1.0, 523.25), (1.7, 440.0), (2.8, 392.0), (4.2, 493.88), (4.9, 392.0), (5.6, 329.63), (6.8, 587.33),
       (8.2, 440.0), (8.9, 349.23), (9.6, 523.25), (10.9, 440.0), (12.2, 1318.5), (12.25, 659.25), (12.9, 392.0), (13.6, 493.88), (14.6, 523.25)]
def env_chord(t, s):  # 1.2 s crossfades
    a = min(1, max(0, (t - s + 0.6) / 1.2)); b = min(1, max(0, (s + 4.6 - t) / 1.2)) if s < 12 else 1
    return a * b
L = [0.0] * N; R = [0.0] * N
lp = 0.0; lp2 = 0.0
for i in range(N):
    t = i / SR
    pad = 0.0
    for s, notes in CH:
        e = env_chord(t, s)
        if e <= 0: continue
        for k, f in enumerate(notes):
            amp = 0.5 if k == 0 else 0.22
            pad += e * amp * (math.sin(TAU * f * t) + 0.6 * math.sin(TAU * (f + 0.7) * t + k) + 0.15 * math.sin(TAU * 2 * f * t))
    pad *= 0.16 * (0.85 + 0.15 * math.sin(TAU * 0.25 * t)) * min(1, t / 0.4)
    pl = 0.0
    for t0, f in MEL:
        d = t - t0
        if 0 <= d < 4:
            pl += math.exp(-2.2 * d) * (math.sin(TAU * f * d) + 0.35 * math.sin(TAU * 2 * f * d) * math.exp(-3 * d) + 0.1 * math.sin(TAU * 3 * f * d) * math.exp(-5 * d)) * min(1, d / 0.004)
    pl *= 0.22
    # wind: low-passed noise with gusts
    n = random.uniform(-1, 1); lp += 0.015 * (n - lp); lp2 += 0.03 * (lp - lp2)
    wind = lp2 * 1.6 * (0.55 + 0.45 * math.sin(TAU * 0.09 * t + 1.3))
    # crickets after dark: 4.3 kHz chirps, three pulses each
    cr = 0.0; ce = min(1, max(0, (t - 5.5) / 3))
    if ce > 0:
        for f0, rate, ph, pan in ((4300, 1.3, 0.0, 0), (4650, 1.1, 0.37, 1)):
            u = (t * rate + ph) % 1
            if u < 0.18 and math.sin(TAU * 26 * t) > 0.2:
                cr += ce * 0.03 * math.sin(TAU * f0 * t)
    # a distant train horn as the train crosses the valley (two-note chord, soft attack)
    hn = 0.0; d = t - 2.2
    if 0 <= d < 2.6:
        he = min(1, d / 0.25) * min(1, max(0, (2.6 - d) / 0.9))
        for f in (311.13, 369.99):
            hn += he * sum(math.sin(TAU * f * k * t) / k for k in range(1, 6))
        hn *= 0.05
    l = pad + pl * 0.9 + wind + cr + hn * 0.8
    r = pad + pl * 1.0 + wind * 0.9 + cr + hn
    fade = min(1, (DUR - t) / 1.5)
    L[i] = l * fade; R[i] = r * fade
out = sys.argv[1]
w = wave.open(out, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
peak = max(max(abs(x) for x in L), max(abs(x) for x in R)) or 1
w.writeframes(b''.join(struct.pack('<hh', int(L[i] / peak * 0.8 * 32767), int(R[i] / peak * 0.8 * 32767)) for i in range(N)))
w.close(); print('wrote', out, 'peak', round(peak, 3))
