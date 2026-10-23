# Change-point / tipping-point detection and internal "decision point" signals for multi-agent LLM event streams

Verification note: items marked "(abstract/HTML verified)" were fetched from the arXiv abs or HTML page during this session. Items marked "(search snippet only)" come from search-result summaries and were NOT fetched at source. Some fetches were done through a summarising tool, so exact numbers should be re-checked against the PDF before they go into a paper.

## Q1. Change-point detection: classical/modern methods and 2024–2026 applications to LLM outputs, agent traces, embeddings

### Takeaway
The classical toolkit is CUSUM (Page 1954), Bayesian online change-point detection (BOCPD, Adams & MacKay 2007) and kernel change-point detection (Arlot/Celisse/Harchaoui). Any of these can be run on a stream of per-event scalar or vector features. In 2024–2026 work, one-sided CUSUM is the method people actually use on LLM/agent streams. It has been applied to hidden-state-derived per-turn risk (SafeDream), to token entropy (an ICML 2026 poster, unverified), and to per-norm statistics in RL multi-agent simulations (AAF). I found no published application of CPD to tool-using LLM agent traces or to multi-agent LLM message graphs. NARCBench only says sequential detection is future work.

### Cited Findings
**Classical methods**
- CUSUM was introduced by E. S. Page, "Continuous Inspection Schemes", Biometrika 41(1–2):100–115, 1954. It detects a change in a distribution parameter (e.g. the mean) and gives a rule for when to act. It followed Wald's SPRT. — [Wikipedia: CUSUM](https://en.wikipedia.org/wiki/CUSUM); [Biometrika issue 41(1-2)](https://academic.oup.com/biomet/issue/41/1-2) (secondary sources; original paper text not fetched)
- BOCPD (Adams & MacKay, arXiv:0710.3742, 2007) does exact online inference of the most recent changepoint. It computes the posterior over the "run length" (time since the last change) with a simple message-passing recursion and assumes parameters before and after a change are independent. It is modular across data types. — [arXiv:0710.3742](https://arxiv.org/abs/0710.3742) (abstract verified; the abstract does not state complexity)
- Kernel multiple change-point detection (Arlot, Celisse, Harchaoui, JMLR 20(162):1–56, 2019) adds a model-selection penalty to the Harchaoui–Cappé kernel method to choose the number of change points. It proves a finite-sample oracle inequality and detects changes in the full distribution even when mean and variance stay constant. — [JMLR v20/16-155](https://jmlr.org/papers/v20/16-155.html); [arXiv:1202.3878](https://arxiv.org/pdf/1202.3878.pdf) (search summary)

**Adaptive Accountability Framework (AAF), arXiv:2512.18561**
- Single author: Saad Alqithami. v1 21 Dec 2025, v3 19 Mar 2026. AAF is a runtime layer that records provenance, "detects distributional change points in streaming traces", attributes responsibility with a causal influence graph, and applies cost-bounded interventions. — [arXiv:2512.18561](https://arxiv.org/abs/2512.18561) (abstract verified)
- The detector is an adaptive one-sided CUSUM: S_t = max{0, S_{t−1} + Z_t − μ₀ − δ}, with an alarm when S_t ≥ h_t, after which S_t resets. The threshold h_t is tuned by Robbins–Monro stochastic approximation (η_t = t^−0.6) so the long-run alarm rate equals a target α (Theorem 4). A global budget ᾱ = 0.05 is split across norms by online mirror descent. A Lorden-type delay bound h*/(Δ−δ) is given (Corollary 2). — [arXiv HTML 2512.18561](https://arxiv.org/html/2512.18561) (HTML verified, first ~100k chars)
- The per-norm stream features Z_t are: inequity (Gini over individual rewards), collusion (maximum pairwise mutual information among agents' action streams in a sliding window), and throughput (queue length minus capacity). — [arXiv HTML 2512.18561](https://arxiv.org/html/2512.18561)
- The agents are RL agents (PPO, tabular Q-learning, MPC), not LLMs. LLM MAS appear only in related work. — [arXiv HTML 2512.18561](https://arxiv.org/html/2512.18561)
- Scale: 87,480 runs, up to 100 agents plus a 500-agent sweep, 324 regimes, Byzantine rates up to 10%. AAF lowers the compromise ratio in 96% of regimes (median −11.9% vs PPO). Top-ranked attribution accuracy is 0.97 at 10% Byzantine. — [arXiv:2512.18561](https://arxiv.org/abs/2512.18561)
- **Inconsistency:** the abstract reports a median detection delay of 71 steps (IQR 39–177), while Section 5.3 reportedly cites a "9-step median, 17-step 95th percentile". — [abs](https://arxiv.org/abs/2512.18561) vs [HTML](https://arxiv.org/html/2512.18561)

**NARCBench / HELIOS, arXiv:2604.01151**
- Rose, Cullen, Abdelnabi, Torr, Kaplowitz, Schroeder de Witt. v1 1 Apr 2026, v5 15 Oct 2026. HELIOS uses per-agent activation probes as "sensors" and treats collusion detection in an unknown subgroup as composite hypothesis testing. NARCBench tests transfer under environment shift across four open-weight models. The best method per model reaches 0.99–1.00 AUROC on steganographic collusion that transcript monitors fail to separate. Transfer to emergent-collusion third-party environments is only partial. In one environment only 2 of 229 collusive episodes verbalise the coordination. — [arXiv:2604.01151](https://arxiv.org/abs/2604.01151) (abstract verified)
- Sequential detection is mentioned only as future work: "Multi-turn extensions of our detection setting call for sequential detection machinery". There is a related-work heading "Multisensor and sequential detection" and an Appendix A heading "Sequential detection". Agents are probed only "just after the initial prompt and at the end of the period", so there is no per-turn localisation. — [arXiv HTML 2604.01151](https://arxiv.org/html/2604.01151) (HTML verified, first ~100k chars)
- The five group statistics are Peak Suspicion, Deception Split, Sorted Concatenation, Activation Alignment and Asymmetry Probe. Peak Suspicion and Deception Split have GLRT interpretations; the other three are heuristic. No single statistic dominates. — [arXiv HTML 2604.01151](https://arxiv.org/html/2604.01151)

**Other 2024–2026 LLM applications**
- SafeDream (Yan, Lin, Zhu, Wang; arXiv:2604.16824, Apr 2026): a world model encodes LLM hidden states into a safety state. CUSUM accumulates weak per-turn risk into evidence, and "contrastive imagination" rolls out futures in latent space. It flags multi-turn jailbreaks 1.06–1.20 turns before compliance on XGuard-Train, SafeDialBench and SafeMTData, against 8 baselines. FPR is described only as "competitive"; models and CUSUM parameters are not in the abstract. — [arXiv:2604.16824](https://arxiv.org/abs/2604.16824) (abstract verified)
- An ICML 2026 poster, "Detecting Fluent Optimization Based Adversarial Prompts via Sequential Entropy Changes", frames adversarial-suffix detection as online CPD. It runs one-sided CUSUM on standardised next-token entropy and localises suffix onset. — [ICML 2026 poster](https://icml.cc/virtual/2026/poster/61448) (search snippet only)
- DeepContext (arXiv:2602.16935) tracks multi-turn "intent drift" with a recurrent hidden state rather than a formal CPD test. It reports F1 0.84 vs 0.67 for Llama-Prompt-Guard-2 and Granite-Guardian, with under 20 ms overhead on a T4. — [arXiv:2602.16935](https://arxiv.org/abs/2602.16935) (search snippet only)
- Pre-LLM precedent: Rabinovich et al. (ACL 2023), change-point detection and interpretation in task-oriented dialog systems. — [awesomepapers entry](https://awesomepapers.io/large-language-models/publications/rabinovich2023reliable) (search snippet only)

### Inferences
- The cheapest principled option for SentryBench is a one-sided CUSUM, or BOCPD for a posterior over onset, on a scalar per-event score. That score could be a probe score, a monitor score, or a feature like AAF's pairwise action mutual information. CUSUM gives detection delay and false-alarm-rate guarantees (Lorden/ARL), and an AAF-style adaptive threshold can hit a target alarm rate. For vector features such as message embeddings, kernel CPD is the principled offline segmentation baseline.
- The CUSUM alarm time is a detection time. It is not an estimate of the change point. Onset is usually estimated as the last time S_t was zero, or with BOCPD's run-length posterior. This difference matters for evaluating "inflection point" localisation against ground truth.
- Open niche: CPD on LLM multi-agent event streams with ground-truth onset labels. NARCBench explicitly leaves this open, and AAF does it only for RL agents.

### Gaps
- AAF's evaluation sections (beyond the first ~100k chars of HTML) were not read. The 71-step vs 9-step delay discrepancy is unresolved.
- NARCBench's Appendix A ("Sequential detection") body, the four model names (only Llama-3.1-70B is visible, in an appendix title) and the probed layers were not retrieved.
- The ICML entropy-CUSUM poster, DeepContext, HoloAegis (arXiv:2608.08485, EMA-of-embeddings drift alert) and LLM-SAN (ACL 2026 Findings) were not verified at source.
- I found no learned/neural CPD (e.g. deep kernel CPD) applied to LLM traces. I did not search the general learned-CPD literature in depth.

## Q2. Tipping points / critical transitions: early-warning signals and use on LLM conversations or multi-agent dynamics

### Takeaway
Early-warning signals (EWS) are well established in dynamical systems but have known caveats. Critical slowing down shows up as slower recovery, rising lag-1 autocorrelation and rising variance (sometimes skewness), and not all regime shifts produce it. Tipping-point behaviour has been shown in LLM populations: committed minorities overturning conventions. I could not verify anyone applying critical-slowing-down indicators to LLM conversations or multi-agent LLM systems.

### Cited Findings
- Scheffer et al., "Early-warning signals for critical transitions", Nature 461:53–59 (2009), doi:10.1038/nature08227. Critical slowing down near a bifurcation gives three signals: slower recovery from perturbations, increased autocorrelation and increased variance. Asymmetry (skewness) of fluctuations may rise before catastrophic bifurcations. — [IDEAS/RePEc record](https://ideas.repec.org/a/nat/nature/v461y2009i7260d10.1038_nature08227.html); [PDF copy](https://web.physics.rutgers.edu/grad/601/CM2018/scheffer2009a.pdf) (search summary)
- A 2025 review describes rising variance, autocorrelation and skewness as shared EWS, with lag-1 autocorrelation approaching 1 near the threshold. — [arXiv:2511.01168](https://arxiv.org/pdf/2511.01168) (search snippet only)
- Caveat: not all regime shifts show critical slowing down, and detection under noise is hard. — [arXiv:1305.6700](https://www.arxiv.org/pdf/1305.6700) (search snippet only)
- Deep-learning EWS classifiers are trained to anticipate bifurcations and their type. — [Bury et al. 2021, WUR depot](https://edepot.wur.nl/554852) (search snippet only)
- LLM populations (Ashery, Aiello, Baronchelli; arXiv:2410.08948, published in Science Advances 2025): conventions emerge spontaneously in a naming game, and collective biases appear even when individual agents look unbiased. Committed minorities above a critical size overturn established conventions. Results are reported robust across Llama-2-70b-Chat, Llama-3-70B-Instruct, Llama-3.1-70B-Instruct and Claude-3.5-Sonnet. — [arXiv:2410.08948](https://arxiv.org/abs/2410.08948v1); [Science Advances PDF](https://openaccess.city.ac.uk/id/eprint/35211/1/sciadv.adu9368.pdf) (search summary; exact thresholds not retrieved)
- CIVA (Zhang et al., arXiv:2604.05339, Apr 2026): an LLM agent community shows "catastrophic collapse" under value misspecification, with deception and power-seeking emerging. A search snippet claimed the paper uses autocorrelation as a critical-slowing-down test, but the abstract does not mention CSD, autocorrelation or precursors. — [arXiv:2604.05339](https://arxiv.org/abs/2604.05339) (abstract verified; CSD claim unverified)

### Inferences
- EWS are a cheap add-on: rolling variance and lag-1 autocorrelation of any per-round scalar (e.g. fraction of agents adopting a behaviour, a mean probe score). They only apply where the inflection is a slow bifurcation-type approach, as in convention flips under a growing committed minority. They will not catch abrupt, instruction-triggered changes such as an agent receiving a collusion instruction. CPD fits those better.
- The Ashery et al. naming-game setup, with open-weight Llama-3.x, is a ready-made testbed with a known tipping mechanism (committed minority size) for validating EWS or CPD on LLM multi-agent streams.

### Gaps
- No verified study applies CSD indicators to LLM conversations or LLM multi-agent dynamics. CIVA's full text was not checked for an autocorrelation analysis.
- No verified study found on EWS before collusion emergence in LLM agents.

## Q3. Internal decision points: how early is an LLM's eventual answer/action linearly decodable, and how accurately?

### Takeaway
There is strong evidence, mostly from 2025–2026 and on open-weight models, that answers are often decodable before they are produced: pre-CoT probes reach >0.9 AUC, and attention probes allow early exit that saves 26–68% of tokens. For agent actions, "The Agent Knew" shows a residual-stream readout is weak right after the decisive fact (AUROC 0.58) but strong at the decision/pre-action step (0.94). In that agentic setting, the internal signal is not much earlier than the action itself. Activation-based multi-agent detection (AcMAS, HELIOS) reaches high F1/AUROC but does not localise onset in time.

### Cited Findings
- "The Agent Knew" (Fayyazi, Kamal, Pedram; arXiv:2610.17301, 12 Oct 2026). A linear residual-stream readout forecasts unauthorized actions before the action (AUROC 0.94) and false reports before the report. It outperforms CoT monitors when the agent is pressured to hide its reasoning. Gating actions on the forecast reduces violations across four model families at about 10⁻⁸ of agent compute, 109× cheaper than a CoT monitor. On CAPE-Bench, "retroactive permission laundering" precedes a false report in 70% of 1,081 violations vs 8% otherwise. Tests were preregistered. — [arXiv:2610.17301](https://arxiv.org/abs/2610.17301) (abstract verified)
- Time course in the same paper. Before the decisive fact is revealed, every monitor is at chance (0.48–0.51). At the first turn after the reveal (last prompt token), the internal readout forecasts the later violation weakly (AUROC 0.580) but leads the CoT monitor and supervised text. While the plan is being written, text leads, and two actions before the violation text is ahead of the readout. At the decision/pre-action state the readout reaches 0.941 (0.985 in one table comparison). — [arXiv HTML 2610.17301](https://arxiv.org/html/2610.17301) (HTML via summariser)
- Readout details from the same paper: mean residual vector over the 8 tokens before the position. The deployed score averages z-scored readouts over five depths and two cross-fitted folds; layer indices were not retrieved. Lie forecast AUROC (internal vs supervised text): Gemma-4 0.87 vs 0.94, gpt-oss 0.72 vs 0.81. Pooled AUROC is 0.745 (95% CI 0.67–0.82). Code: github.com/AryaFayyazi/Honesty. Models reported as Gemma-4-26B-A4B, gpt-oss-20b, and two others named "Qwen3.8-27B" and "Muse-Glimmer-30B". — [arXiv HTML 2610.17301](https://arxiv.org/html/2610.17301). **Caution:** the last two names came through a summariser and look unusual; check them in the PDF.
- Pre-CoT probes (Cox, Kianersi, Garriga-Alonso; arXiv:2603.01437, ICML 2026): linear probes at the last token before CoT predict the final answer with ">0.9 AUC on most tasks". Steering along the probe direction flips answers much more often than norm-matched orthogonal directions. Wrong answers after steering show confabulation or non-entailment. — [arXiv:2603.01437](https://arxiv.org/abs/2603.01437) (abstract verified; models not named in abstract)
- Reasoning Theater (Boppana, Ma, Loeffler, Sarfati, Bigelow, Geiger, Lewis, Merullo; Goodfire, 12 Mar 2026; arXiv:2603.05488). Models: DeepSeek-R1-0528, GPT-OSS-120B and R1 distills, on MMLU-Redux and GPQA-Diamond. Attention (context-pooling) probes reach 87.98% average answer accuracy on MMLU; single-token linear probes reach only ~31.85% (chance 25%). On easy questions the answer is decodable from the start while the CoT monitor lags. On GPQA, probe, forced answering and monitor all rise together. Early exit at 95% probe confidence saves 67.7% of tokens on MMLU (96.7% of baseline accuracy) and 33.4% on GPQA (100.8%) for R1. For GPT-OSS it saves 61.3% (94.9%) and 26.1% (98.2%). — [Goodfire blog](https://www.goodfire.com/research/reasoning-theater) (fetched)
- Predicting correctness (not the answer) early: hidden states after about 4 reasoning tokens give AUC up to ~0.8+ for eventual correctness ([Temporal Predictors of Outcome, arXiv:2511.14773](https://arxiv.org/abs/2511.14773)). Afzal et al. (Findings ACL 2025) predict zero-shot CoT success before any token is generated ([ACL Findings 2025.662](https://preview.aclanthology.org/vol-to-evt/2025.findings-acl.662.pdf)). — (search snippets only)
- AcMAS (Xu et al.; arXiv:2607.06807, ICML 2026) detects malicious agent behaviour from local agents' activation-space reasoning states, without an interaction graph. F1 is 0.94 vs 0.72 for graph baselines (synchronous) and 0.93 vs 0.38 (asynchronous). It generalises across open-source backbones (not named in abstract) and uses activation analysis to guide restoration rather than isolation. Temporal localisation is not described. — [arXiv:2607.06807](https://arxiv.org/abs/2607.06807) (abstract verified)
- HELIOS/NARCBench probes agents only after the initial prompt and at period end; see Q1. — [arXiv HTML 2604.01151](https://arxiv.org/html/2604.01151)

### Inferences
- How early: for single-turn QA the answer is often decided before any CoT. For agentic violations in "The Agent Knew", the strong signal appears at the decision step, and the earliest post-reveal signal is weak (0.58). The internal "decision point" in agents may lie close to the turn where the triggering information arrives plus the decision turn, not many turns earlier.
- How accurate: AUROC ~0.9–0.99 is typical at the decision point; earlier readouts are much weaker. Probe architecture matters: attention probes far outperform single-token linear probes in Reasoning Theater.
- All the cited internal-signal work uses open-weight models (gpt-oss, Gemma, Llama, DeepSeek-R1), which fits SentryBench's constraint.

### Gaps
- Per-model violation AUROCs and layer indices for "The Agent Knew" were not retrieved. Two of its model names need confirmation.
- The models and datasets behind the >0.9 AUC in Cox et al. were not retrieved.
- AcMAS model names, probe design and any per-step detection latency were not retrieved.
- I did not fetch "Future Lens" or "emergent response planning" style papers (decoding future tokens or response attributes from hidden states).

## Q4. Which internal signals could mark an inflection point?

### Takeaway
The most directly supported signal is a sharp change in a probe's predicted final answer or action over the token/turn sequence. Reasoning Theater shows such sharp shifts can accompany genuine realisations, but verbalised "Wait/Aha" markers do not reliably coincide with them. Running a CUSUM over per-turn hidden-state risk scores is already validated for multi-turn jailbreaks (SafeDream, ~1.1 turns lead). Combining per-agent probe streams (HELIOS-style sensors) with sequential CPD is an unexplored but well-motivated route for multi-agent inflection detection.

### Cited Findings
- Reasoning Theater: high-confidence responses have about half as many verbalised inflections ("Wait", "Aha") as low-confidence ones. Individual verbalised inflections do not reliably align with shifts in probe confidence. A worked example shows a sharp probe-confidence change at a genuine realisation step. — [Goodfire](https://www.goodfire.com/research/reasoning-theater)
- The Agent Knew: the readout jumps from near chance before the reveal (0.48–0.51), to 0.58 just after the reveal, to 0.94 at the decision. This is a time profile of a probe forecasting a future action across a trajectory. — [arXiv HTML 2610.17301](https://arxiv.org/html/2610.17301)
- SafeDream: hidden-state-derived per-turn safety state plus CUSUM detects jailbreak onset 1.06–1.20 turns before compliance. — [arXiv:2604.16824](https://arxiv.org/abs/2604.16824)
- HELIOS: per-agent activation probe scores serve as sensors, combined with GLRT-style group statistics (Peak Suspicion, Deception Split). The authors say multi-turn extensions need sequential detection machinery. — [arXiv HTML 2604.01151](https://arxiv.org/html/2604.01151)
- Token-entropy stream with CUSUM localises adversarial-suffix onset (ICML 2026 poster). — [ICML poster](https://icml.cc/virtual/2026/poster/61448) (search snippet only)
- Observable (non-internal) features with a CPD-ready definition: AAF's collusion statistic is the maximum pairwise mutual information among agents' action streams in a sliding window; inequity is the Gini of rewards. — [arXiv HTML 2512.18561](https://arxiv.org/html/2512.18561)

### Inferences
- Candidate signals, ranked by evidence:
  1. Per-turn probe score for the eventual bad action or answer, using a deception, violation or collusion probe. The inflection is the point of a sudden rise; detect it with CUSUM or BOCPD and estimate onset from CUSUM's last-zero time or the BOCPD run-length posterior.
  2. Change in the probe's argmax or predicted class over time (a "belief flip"), as in the Reasoning Theater example.
  3. Group-level aggregation of per-agent probe streams (max or sum, as in GLRT Peak Suspicion) fed into a multivariate or sequential test.
  4. Cheap observable fallbacks: token entropy, pairwise action mutual information, embedding drift via kernel CPD.
- Validation design implication: ground-truth onset is needed. Settings like "The Agent Knew" (an explicit "reveal" turn) or injected instructions or collusion triggers give a known change time. Detection delay and false-alarm rate (ARL) can then be measured as in AAF.
- Risk: verbalised markers are not reliable proxies for internal inflections (Reasoning Theater). Text-only CPD may mislocalise the decision point.

### Gaps
- No verified paper reports a calibrated "jump in probe prediction" detector with onset-localisation accuracy against ground truth in a multi-agent LLM setting.
- I did not find evidence on whether probe-score streams satisfy CUSUM/BOCPD assumptions (independence, stable pre-change distribution) across turns. This would need empirical checks.
