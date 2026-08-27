# Caption & Search Photo Gallery

A small CPU-only demo that combines two pretrained vision-language models to
make a folder of photos searchable with plain-English text.

## How it works

Every image in the `images` folder is run through **BLIP**
(`Salesforce/blip-image-captioning-base`), which writes a short caption
describing what's in it. Every image is also run through **CLIP**
(`openai/clip-vit-base-patch32`), which turns it into a 512-number vector
that captures its meaning rather than its pixels. When you type a search
query, CLIP turns that text into the same kind of vector, and the script
just measures how close it sits to each image's vector (cosine similarity).
The five closest images are the results. BLIP never sees the query at all —
it only supplies the caption shown next to each result, so you can sanity
check what the model actually saw in that photo.

Both models are the smallest "base" versions rather than the "large" ones,
specifically so this runs at a reasonable speed on a CPU with no GPU
involved.

## The dataset

25 everyday photos, mostly kids doing outdoor activities (climbing,
swimming, biking, playing in water) and dogs (running, playing, swimming).
Nothing exotic — cars, food scenes, or offices don't really appear here, so
queries about those wouldn't have anything good to find.

## abstract queries

The real test isn't typing "a dog," it's typing something that never names
the object directly and seeing whether CLIP still finds the right idea.
Three were tried here.

"Someone moving upward during an adventure" pulled back the man climbing a
mountain, the rock wall, the girl climbing a rock wall, and the girl
climbing a rope — four out of five results were genuinely about climbing,
even though the word "climb" never appeared in the query. One result ("two
boys in a room") clearly doesn't belong, which is a useful reminder that
with only 25 images, the fifth-place result doesn't have to be a good match
to make the top 5 — it just has to beat 21 other images.

"Young people enjoying their free time" is a vaguer query, and the results
were correspondingly broader: a boy eating pizza, kids climbing, a girl in
water, two boys in a room. All plausibly fit "kids having fun," but it's a
looser fit than the climbing query — the vaguer the phrase, the more images
can reasonably claim to match it, so the ranking gets less decisive.

"A fun moment with a companion" was the strongest result of the three: two
dogs playing, a dog catching what BLIP's caption garbled as a "frur" (almost
certainly a frisbee), two dogs running together, a couple sitting on a
bench, and a dog with its owner. Every single result involves two subjects
doing something together, which is exactly what "companion" was pointing
at, without the query ever saying "dog" or "two."

Overall, CLIP handled the abstract phrasing better than you might expect
for a model this small, especially when the query implied a concrete
action or interaction (climbing, playing together). It got noticeably
fuzzier on the vaguer, mood-based query. Two smaller things worth noting:
similarity scores across all three queries stayed clustered in a narrow
0.23-0.28 band, which is normal for CLIP but means the model wasn't hugely
confident about any single best answer here; and BLIP's captions had a
couple of garbled words ("frur," "frck") where it was clearly trying to say
"frisbee" — a known quirk of the "base" captioning model that the "large"
version usually gets right.

## Files

- `script.py` — the script itself
- `dataset/` — put your photos here
- `results.json` — every image's caption plus each query's top-5 results,
  written out after you run the script
