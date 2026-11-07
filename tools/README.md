# Weekly Instagram batch tooling

- engine.py: renders slides (1080x1350, Fraunces + Inter). Needs /home/claude/fonts/Fraunces-{400,500,600}.ttf and Inter-{Regular,Medium}.otf.
  Fonts: `npm pack @fontsource/fraunces`, convert the latin 400/500/600 .woff to .ttf with fontTools (flavor=None); Inter from /usr/share/fonts/opentype/inter.
- posts_week2_example.py: the 21 posts of 9-15 Nov as data (copy as the template for the next week).
- build.py: renders every post to posts/<CODE>/<CODE>-NN.jpg.
Pipeline: render -> git push main -> insert rows into Supabase ig_posts as 'draft' (project vhalqmegueqsgffmujcb) -> user approves -> status 'scheduled'. The ig-publish edge function + pg_cron publish them. Never rebuild the Meta app.
