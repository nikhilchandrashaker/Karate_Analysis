# Estimated Kick Biomechanics of Cobra Kai and Kickin’ It Fighters
### A rating-driven kinematic model of 28 fictional karate characters

## Abstract
We build a simple planar (side-view) biomechanical model for 28 characters from *Cobra Kai* (n = 19) and *Kickin’ It* (n = 9). Each character’s six editorial skill ratings (technique, speed, power, strategy, discipline, resolve) are mapped to joint angles, a kinetic-chain timing profile, an estimated peak foot speed, an impact index and a balance index. The Cobra Kai roster averages a higher foot speed (11.4 vs 10.9 m/s) and impact index (70 vs 59) than the Kickin’ It roster. The highest impact scores belong to Chozen Toguchi, Miguel Diaz, Tory Nichols. **These results follow from the mapping we chose and are not measurements.** The project is a visualization and a teaching toy, not a validated model.

## 1. Introduction
Both shows treat karate as central, but they portray it very differently: one as a drama with trained performers and long fight takes, the other as a family sitcom. The goal here is to put the two casts in the same quantitative frame by using the language of biomechanics: segment angles, centre of mass (COM), and proximal-to-distal sequencing in a kick.

## 2. Methods
### 2.1 Subjects and inputs
Each character has six ratings from 1 to 10 plus a "starting" and "peak" skill rating. All ratings are the author’s editorial judgments from general knowledge of the series. No footage was measured and no external dataset was used. Strategy and resolve are shown for context but are not used by the kick model.

### 2.2 Model
A 12-segment planar skeleton (head, trunk, two upper arms, two forearm+hand segments, two thighs, two shanks, two feet) is drawn at normalized body height (H = 1). Segment lengths use conventional anthropometric proportions (thigh 0.245 H, shank 0.246 H, upper arm 0.186 H, trunk 0.288 H). The pose is a front-leg kick from a single support leg. The COM uses Dempster-type segment mass fractions. These constants are textbook-style approximations and should be checked before any serious use.

| Quantity | Mapping |
|---|---|
| Hip flexion φ | 55 + 8 · technique (degrees) |
| Knee extension at impact | min(180, 118 + 6.2 · technique) (degrees) |
| Trunk lean | 6 + 0.22 (φ − 55) + 1.8 (10 − discipline) (degrees) |
| Peak foot speed v | 4.5 + 0.7 · speed + 0.3 · technique (m/s) |
| Impact index | (0.5 + 0.1 · power) · v², rescaled so the roster maximum is 100 |
| Chain peak lag Δ | 10 + 3.5 · technique (ms) between hip, knee and ankle peaks |
| Chain efficiency | 100 · (0.35 + 0.065 · technique) (percent) |
| Balance index | 100 · (1 − distance of COM from centre of support foot / 0.145 H), floored at 0 |

Joint angular velocities are drawn as Gaussian pulses (σ = 20 ms). Hip, knee and ankle peaks are separated by Δ, so a low-technique fighter shows overlapping peaks (poor sequencing).

## 3. Results
| Fighter | Show | Toe height (% H) | Foot speed (m/s) | Impact | Balance | Chain eff. (%) | Growth |
|---|---|---|---|---|---|---|---|
| Chozen Toguchi | Cobra Kai | 96 | 13.1 | 100 | 63 | 100 | +1 |
| Miguel Diaz | Cobra Kai | 86 | 13.5 | 98 | 61 | 94 | +7 |
| Tory Nichols | Cobra Kai | 86 | 13.5 | 98 | 56 | 94 | +4 |
| Sensei Wolf | Cobra Kai | 86 | 12.8 | 95 | 63 | 94 | +0 |
| Robby Keene | Cobra Kai | 75 | 12.5 | 84 | 60 | 87 | +4 |
| Jack Brewer | Kickin’ It | 75 | 12.5 | 84 | 63 | 87 | +3 |
| John Kreese | Cobra Kai | 86 | 11.4 | 82 | 61 | 94 | +1 |
| Hawk | Cobra Kai | 63 | 12.2 | 80 | 59 | 80 | +5 |
| Axel Kovačević | Cobra Kai | 63 | 11.5 | 77 | 62 | 80 | +2 |
| Kim Crawford | Kickin’ It | 75 | 12.5 | 77 | 68 | 87 | +2 |
| Xander Stone | Cobra Kai | 75 | 12.5 | 77 | 63 | 87 | +0 |
| Bobby Wasabi | Kickin’ It | 75 | 11.8 | 75 | 68 | 87 | +1 |
| Johnny Lawrence | Cobra Kai | 75 | 11.1 | 72 | 63 | 87 | +1 |
| Terry Silver | Cobra Kai | 75 | 11.1 | 66 | 63 | 87 | +1 |
| Sensei Ty | Kickin’ It | 75 | 11.1 | 66 | 56 | 87 | +0 |
| Aisha Robinson | Cobra Kai | 63 | 11.5 | 65 | 62 | 80 | +3 |
| Zara Malik | Cobra Kai | 63 | 11.5 | 65 | 59 | 80 | +2 |
| Kyler | Cobra Kai | 51 | 10.5 | 64 | 62 | 74 | +1 |
| Daniel LaRusso | Cobra Kai | 75 | 11.1 | 61 | 70 | 87 | +2 |
| Samantha LaRusso | Cobra Kai | 63 | 11.5 | 59 | 72 | 80 | +4 |
| Jerry Martinez | Kickin’ It | 51 | 10.5 | 54 | 62 | 74 | +3 |
| Frank | Kickin’ It | 51 | 10.5 | 54 | 62 | 74 | +1 |
| Rudy Gillespie | Kickin’ It | 63 | 10.1 | 50 | 74 | 80 | +1 |
| Eddie Jones | Kickin’ It | 40 | 10.2 | 42 | 67 | 68 | +3 |
| Demetri | Cobra Kai | 51 | 9.8 | 39 | 70 | 74 | +5 |
| Milton Krupnick | Kickin’ It | 29 | 8.5 | 26 | 77 | 61 | +3 |
| Kenny Payne | Cobra Kai | 19 | 8.2 | 24 | 67 | 54 | +4 |
| Anthony LaRusso | Cobra Kai | 19 | 7.5 | 20 | 70 | 54 | +3 |

**Roster means.** Foot speed 11.4 (Cobra Kai) vs 10.9 (Kickin’ It). Impact 70 vs 59. Balance 63 vs 66. Chain efficiency 83% vs 78%.

**Highlights.** Highest impact: Chozen Toguchi (100), Miguel Diaz (98), Tory Nichols (98). Best balance: Milton Krupnick (77), Rudy Gillespie (74), Samantha LaRusso (72). Biggest rated growth: Miguel Diaz (+7), Hawk (+5), Demetri (+5).

Figures: `summary_matchups.png` (ten head-to-head models), `summary_roster.png` (speed vs impact for all 28), and one panel per fighter (`<name>.png`).

### 3.1 Case studies: documented fights
16 fights with a clear winner in published recaps were compared with the model. For each fight, P(A wins) = 1 / (1 + exp(−(mean rating A − mean rating B) / 1.5)).

| Episode | Fight | Winner | Model P(winner) | Called? |
|---|---|---|---|---|
| Cobra Kai S1E10 “Mercy” (final) | Miguel Diaz vs Robby Keene | Miguel Diaz | 58% | yes |
| Cobra Kai S4E10 “The Rise” (boys’ final) | Robby Keene vs Hawk | Hawk | 31% | no |
| Cobra Kai S4E10 “The Rise” | Robby Keene vs Demetri | Robby Keene | 66% | yes |
| Cobra Kai S4E10 “The Rise” (girls’ final) | Samantha LaRusso vs Tory Nichols | Tory Nichols | 69% | yes |
| Kickin’ It S1E1 “Wasabi Warriors” (cafeteria) | Jack Brewer vs Frank | Jack Brewer | 81% | yes |
| Kickin’ It S1E1 (tournament) | Frank vs Jack Brewer | Jack Brewer | 81% | yes |
| Cobra Kai S1E10 “Mercy” (semifinal) | Robby Keene vs Hawk | Robby Keene | 69% | yes |
| Cobra Kai S1E10 “Mercy” (quarterfinal) | Aisha Robinson vs Xander Stone | Xander Stone | 66% | yes |
| Cobra Kai S4E9 “The Fall” (quarterfinal) | Robby Keene vs Kenny Payne | Robby Keene | 89% | yes |
| Cobra Kai S4E9 “The Fall” (quarterfinal) | Kyler vs Hawk | Hawk | 58% | yes |
| Cobra Kai S2 school brawl | Demetri vs Hawk | Demetri | 53% | yes |
| Cobra Kai S1 cafeteria | Kyler vs Miguel Diaz | Miguel Diaz | 81% | yes |
| Cobra Kai S6 Sekai Taikai (girls’ final) | Tory Nichols vs Zara Malik | Tory Nichols | 81% | yes |
| Cobra Kai S6 Sekai Taikai (boys’ final) | Axel Kovačević vs Miguel Diaz | Miguel Diaz | 73% | yes |
| Cobra Kai S6 Sekai Taikai (sensei tiebreaker) | Johnny Lawrence vs Sensei Wolf | Johnny Lawrence | 29% | no |
| Kickin’ It S1E5 “Swords and Magic” | Jerry Martinez vs Kim Crawford | Kim Crawford | 84% | yes |

The model called 14 of 16 winners with a mean Brier score of 0.14 (a coin flip scores 0.25; lower is better). By show: 11 of 13 for *Cobra Kai* fights and 3 of 3 for *Kickin’ It* fights. The biggest miss is Johnny Lawrence over Sensei Wolf (the model gave the winner 29%). See `fight_examples.png`, and `fights.json` for the data.

**How these were analyzed.** Outcomes and key moments come from published recaps, plot summaries and some fan wikis, paraphrased here. No footage was measured. Fight results are scripted, so this tests whether the ratings track the story, not real combat. The ratings were set with knowledge of these outcomes, so this is not a blind test. Sixteen fights is a small sample, and only three are from *Kickin’ It* because its recaps rarely name winners. Some fights are group brawls, one outcome is implied by the tournament bracket, and one match (Jack vs Eddie in S1E5) was left out because it ended in a forfeit.

**Sources:** [Looper](https://looper.com/249279/why-cobra-kai-fans-have-a-problem-with-the-season-1-finale), [TV Tropes S1E10](https://tvtropes.org/pmwiki/pmwiki.php/Recap/CobraKaiS1E10Mercy), [TV Tropes S4E9](https://tvtropes.org/pmwiki/pmwiki.php/Recap/CobraKaiS4E9TheFall), [IMDb S4E10](https://imdb.com/title/tt14443266/plotsummary), [TV Acute S4E10](https://www.tvacute.com/cobra-kai-season-4-episode-10-recap), [The Cinemaholic](https://thecinemaholic.com/who-wins-the-boys-competition-in-cobra-kai-season-4-spoiler), [Screen Rant](https://screenrant.com/cobra-kai-season-4-ending-explained/), [SlashFilm](https://www.slashfilm.com/1770788/cobra-kai-season-6-part-3-sekai-taikai-tournament-winners), [Heroes Wiki](https://hero.fandom.com/wiki/Robby_Keene), [Antagonists Wiki](https://antagonists.fandom.com/wiki/Johnny_Lawrence), [Karate Kid Wiki (Demetri)](https://thekaratekid.fandom.com/wiki/Demetri_Alexopoulos), [Karate Kid Wiki (Bert)](https://thekaratekid.fandom.com/wiki/Bert), [Wikipedia Kickin’ It episodes](https://en.wikipedia.org/wiki/List_of_Kickin%27_It_episodes), [Kickin’ It Wiki](https://disneyskickinit.fandom.com/wiki/Swords_and_Magic).

## 4. Discussion
The model largely re-expresses the ratings: technique drives pose and sequencing, speed and technique drive foot speed, and power scales impact. Correlations between ratings and outputs are therefore built in and should not be read as findings about the shows. The more useful outputs are the cross-roster comparisons and the balance index, which comes from the pose geometry (kick height and lean) and so is not a direct copy of any single rating.

## 5. Limitations
- Ratings are subjective, and the characters are fictional. Fight scenes are performed by actors and stunt performers.
- The model is 2D, uses one kick type, and ignores arm contribution to power, ground reaction forces and opponent contact.
- Foot speeds and indices are illustrative units. They are not validated against motion capture or published kicking data.
- Segment constants are approximations from general knowledge, not checked against a source for this project.

## 6. Reproducibility
`bio.py` regenerates every figure from the character data in the dashboard (`karate-showdown.html`). Changing a rating there and rerunning updates all outputs.
