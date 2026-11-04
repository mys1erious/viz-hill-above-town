# The hill above town

A person and their dog sit on a hill above a small valley town at dusk. The sun goes down behind the ridge, the town turns its lights on one window at a time, a lit night train crosses the valley, and the stars come out. Everything is drawn in code with canvas 2D in one `index.html`: no images, no libraries, no image or video model.

Live: https://mys1erious.github.io/viz-hill-above-town/ (drag sideways or use the slider to set the time of day).

Our answer to the viral "cartoon dog on a hill at dusk" loop (x.com/_Gottalovezik/status/2116858838091473289), with our own characters and scene.

Open locally with `python3 -m http.server` in this folder. URL flags: `?clean` hides the UI, `?play` runs the 20 s self-playing timeline, `?t=<s>` freezes a moment, `?tod=0..1` pins the time of day.

Re-record: `node ../../../x-trend-ideas/_tools/record.mjs "http://127.0.0.1:<port>/<path>/?clean&play" tmp/silent.mp4 --seconds 20 --fps 30 --w 1080 --h 1350`, then mux the music bed (`video/bed.wav`, made by `music.py`, normalised to -14 LUFS) with ffmpeg.
