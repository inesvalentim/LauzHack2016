# LauzHack2016
Submission to LauzHack 2016 by Inês, Corentin and Sharbat.

We realized that in recent times, people who rely a lot on Facebook for news get trapped in an 'echo chamber'. (https://techcrunch.com/2016/11/13/how-facebook-can-escape-the-echo-chamber/). Mark's been bashed for it and the TechCrunch guys suggested some solutions.

So we tried to nudge people a bit to break out of the bubble.

We scrape articles from a tad bit on the extreme side (using data published by Facebook last year). We learn key phrases from it and give a score to articles based on sentiment (using Microsoft Cognitive Services). 

We learn key phrases for each 'group' (Democrats and Republicans for the US elections) and using these, classify new articles on 'immigration' on the Blue-Red (Dem-Rep) axis, as well as on the positive-negative axis.

Hence, we create a web app which shows options to a user, of choosing an article on one side of the axis and another on the opposite end. Can we break out of the echo chamber?
