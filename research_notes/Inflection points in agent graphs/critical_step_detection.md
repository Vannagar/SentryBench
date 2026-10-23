# Critical / Decisive Step Detection in LLM Reasoning Traces and Agent Trajectories

Verification note: items marked [abstract] were checked on the arXiv abstract page only. Items marked [full text] were checked in the arXiv HTML full text. Items marked [search snippet only] could NOT be checked at the source in this pass and should be re-checked before anyone relies on them.

## Q1. Resampling-based importance in reasoning traces (Thought Anchors, pivotal tokens, forking tokens)

### Takeaway
All three methods define criticality the same way: how much the distribution of final outcomes (or P(success)) shifts when you condition on a prefix and resample from there. They differ in granularity (token vs sentence), in the divergence measure (P(success) delta vs KL vs L2 plus change-point detection), and in cost, which runs to tens or hundreds of rollouts per position. Thought Anchors adds cheaper attention-based proxies, reported as about 100x cheaper.

### Cited Findings
**Thought Anchors (Bogdan, Macar, Nanda, Conmy; arXiv 2506.19143, v1 23 Jun 2025, v4 27 Oct 2025)**
- Sentence-level, black-box "counterfactual importance": resample a replacement sentence, keep only semantically different replacements, continue the CoT, and measure the shift in the final-answer distribution [abstract] — [arXiv abs](https://arxiv.org/abs/2506.19143)
- Formula: KL divergence D_KL[p(A' | T_i ≉ S_i) || p(A)]. T_i counts as dissimilar if its embedding cosine similarity to S_i is below the median (reported as 0.8, using the all-MiniLM-L6-v2 embedding model). ε = 1e-9, and Laplace/Jeffreys smoothing give the same patterns [full text] — [arXiv HTML](https://arxiv.org/html/2506.19143)
- 100 resamples per sentence, plus 100 forced-answer completions per position [full text] — [arXiv HTML](https://arxiv.org/html/2506.19143)
- Models are all open-weight: DeepSeek R1-Distill-Qwen-14B (main), R1-Distill-Llama-8B (validation), and Qwen3-30B-A3B for the MMLU experiments [full text] — [arXiv HTML](https://arxiv.org/html/2506.19143)
- Data: 20 MATH problems (from 1,000, chosen for 25–75% solve rate). Qwen-14B traces have about 144 sentences on average, with 40 responses [full text] — [arXiv HTML](https://arxiv.org/html/2506.19143)
- Two white-box proxies:
  - "Receiver heads": attention heads with high kurtosis of vertical attention, split-half reliability r = .84.
  - "Attention suppression": mask all attention to a sentence and measure KL on future-token logits.
  - Suppression scores correlate positively with resampling scores, and suppression needs about 100x less compute than resampling. Receiver-head scores are partly confounded by sentence position [full text] — [arXiv HTML](https://arxiv.org/html/2506.19143)
- Finding: the high-importance sentences ("thought anchors") are mostly planning and uncertainty-management sentences. Active-computation sentences score lowest [abstract + full text] — [arXiv abs](https://arxiv.org/abs/2506.19143)
- The paper gives no GPU-hour or cost figures [full text] — [arXiv HTML](https://arxiv.org/html/2506.19143)

**Pivotal Token Search (Phi-4 technical report, arXiv 2412.08905, Dec 2024, Sec. 4.3)**
- A pivotal token is a token where the next-token choice causes a sharp change in p(success | prefix). Low-probability tokens are not necessarily pivotal [full text] — [arXiv HTML](https://arxiv.org/html/2412.08905v1)
- Search method:
  - Recursively bisect the completion at the cumulative log-prob midpoint.
  - Stop when a segment's change in p(success) is below a threshold p_gap, or when the segment is a single token.
  - p(success) is estimated by sampling continuations and checking them with an oracle (tests or ground-truth answer).
  - The paper does not state the sample count or the p_gap value. One illustrative figure uses N = 529 completions [full text] — [arXiv HTML](https://arxiv.org/html/2412.08905v1)
- Questions are filtered to 0.2 ≤ p(success) ≤ 0.8, because pivotal tokens are rare on very easy or very hard tasks [full text] — [arXiv HTML](https://arxiv.org/html/2412.08905v1)
- Use: build DPO pairs at the pivotal token (prefix = query; the token that raises p(success) is accepted, the one that lowers it is rejected). Reported gains from SFT to DPO stage 1: GPQA 47.3 → 53.6 and MATH 77.1 → 80.5 [full text] — [arXiv HTML](https://arxiv.org/html/2412.08905v1)

**Forking Paths in Neural Text Generation (Bigelow, Holtzman, Tanaka, Ullman; arXiv 2412.07961, Dec 2024)**
- Hypothesis: there are "forking tokens" where resampling leads to very different outcomes. The method is black-box and needs no weights [abstract] — [arXiv abs](https://arxiv.org/abs/2412.07961)
- Pipeline:
  - At each token index, consider up to 10 alternate tokens, each with at least 5% probability, and sample 30 continuations per alternate. The t = 0 baseline uses 300 samples.
  - The outcome distribution o_t is a probability-weighted histogram of extracted answers.
  - Bayesian change-point detection (BEAST) runs on y_t = L2(o_t, o_0), with Bayes factor > 9.
  - Survival analysis: the hazard h(t) is the probability mass of alternates whose outcome differs from greedy by more than ε (ε = 0.6) [full text] — [arXiv HTML](https://arxiv.org/html/2412.07961)
- Model: gpt-3.5-turbo-instruct, which is NOT open-weight. Gemini 1.5 Flash is used as the answer extractor [full text] — [arXiv HTML](https://arxiv.org/html/2412.07961)
- Cost: about 1M tokens per base path (about $2), about 30 examples per task, about $500 total. Using 10–20 samples instead of 30 gave similar change-point counts, roughly halving cost [full text] — [arXiv HTML](https://arxiv.org/html/2412.07961)
- Results:
  - Share of examples with at least one change point: 63% on LastLetter, 43% on MMLU, 0% on CoinFlip.
  - Forking tokens include punctuation and whitespace.
  - CPD and survival metrics were essentially uncorrelated [full text] — [arXiv HTML](https://arxiv.org/html/2412.07961)

**Follow-up applying resampling to safety (2026)**
- "The Point of No Return: Counterfactual Localization of Deceptive Commitment in LM Reasoning" (Merrill & Srivastava, arXiv 2605.17113, May 2026):
  - Fixes each sentence prefix, resamples continuations, and estimates P(deceptive outcome) to localize the commitment sentence.
  - Scale: four reasoning models, five environments, about 1.46M sentences localized from more than 94.1M sampled continuations.
  - Attention-based transition features generalize out of distribution, but lexical cues do not.
  - Head sets under 10% of all heads causally suppress deceptive commitment in held-out environments [abstract] — [arXiv abs](https://arxiv.org/abs/2605.17113)

### Inferences
- All of these reduce to estimating Δ_t = D(p(outcome | prefix_{≤t}), p(outcome | prefix_{<t})), using a P(success) gap, KL, or L2. Cost is roughly (#positions) × (#samples per position) × (continuation length). The scale of 2605.17113 (94M continuations) shows how quickly this blows up.
- Transfer to a multi-agent event graph:
  - A "position" becomes an event node (a message or tool call), and resampling means regenerating that node's LLM output and re-running everything downstream.
  - The extra complication is that tool calls and environment side effects need to be replayable or sandboxed.
  - Bisection as in PTS is a natural way to cut cost on long graphs. Because the graph is a DAG rather than a line, bisection would run over a topological ordering, or over the causal ancestors of the outcome node.
- Thought Anchors' attention-suppression proxy needs white-box access to a single model's context, so it does not transfer directly across agents in separate contexts. Open-weight models (Qwen, Llama distills) make it feasible within each agent.

### Gaps
- Phi-4 does not report a PTS sample count, p_gap value, or compute cost.
- 2605.17113: I could not confirm from the abstract which four models were used, whether they are open-weight, or what commitment threshold was used.
- I did not locate other 2025–2026 follow-ups that apply Thought Anchors-style resampling directly to multi-agent or tool-using trajectories.

## Q2. Failure attribution in multi-agent systems (Who&When and follow-ups)

### Takeaway
Who&When defines the decisive step counterfactually: the earliest agent-step pair whose correction turns failure into success. Step-level accuracy is still low:
- 14.2% for the original best method.
- About 20.7% (hand-crafted) and 42.9% (algorithm-generated) for the RL-trained open-weight AgenTracer-8B.
- Up to 36.2% for causal-inference methods.

Agent-level accuracy is much higher, at about 50–70%.

### Cited Findings
- **Who&When (Zhang et al., arXiv 2505.00212, Apr 2025, camera-ready v3; venue not named on the abs page).**
  - Data: 127 MAS and 184 failure annotations.
  - 126 algorithm-generated systems built with CaptainAgent/GPT-4o (GAIA and AssistantBench), plus hand-crafted Magentic-One logs (30 GAIA + 28 AssistantBench) [full text] — [arXiv HTML](https://arxiv.org/html/2505.00212)
- Decisive-error definition: (i, t) such that correcting agent i's action at t flips failure to success. If there are several, the earliest is taken [full text] — [arXiv HTML](https://arxiv.org/html/2505.00212)
- Three LLM-judge methods: all-at-once, step-by-step (stop at the first flagged step), and binary search [full text] — [arXiv HTML](https://arxiv.org/html/2505.00212)
- GPT-4o step-level accuracy, as Algorithm-Generated / Hand-Crafted, with GT / without GT:

  | Method | With GT | Without GT |
  |---|---|---|
  | Random | 19.06 / 4.16 | 19.06 / 4.16 |
  | All-at-once | 12.50 / 5.26 | 13.53 / 3.51 |
  | Step-by-step | 25.51 / 7.02 | 15.31 / 8.77 |
  | Binary search | 23.98 / 6.90 | 16.59 / 6.90 |

  - Agent-level accuracy is best with all-at-once, at about 51–57% [full text] — [arXiv HTML](https://arxiv.org/html/2505.00212)
- Abstract headline: best 53.5% agent-level and 14.2% step-level, with some methods below random. o1 and R1 are "not practically usable" [abstract] — [arXiv abs](https://arxiv.org/abs/2505.00212)
- Token cost on the hand-crafted subset:

  | Method | Tokens | Agent-level | Step-level |
  |---|---|---|---|
  | All-at-once | 17.1k | 57.0 | 4.4 |
  | Binary search | 34.7k | 44.0 | 6.9 |
  | Step-by-step | 87.7k | 36.0 | 7.9 |
  | Hybrid | 149.2k | 57.0 | 12.3 |

  [full text] — [arXiv HTML](https://arxiv.org/html/2505.00212)
- Llama and Qwen were tested on the hand-crafted subset with the "same trends", but the numbers appear only in a figure [full text] — [arXiv HTML](https://arxiv.org/html/2505.00212)
- **AgenTracer (Zhang et al., arXiv 2509.03312, Sep 2025).**
  - Counterfactual replay: at each step, an analyzer agent (DeepSeek-R1) proposes a corrected action and the rest of the trajectory is re-simulated. The earliest step whose correction yields success is labeled decisive. Programmed fault injection adds further training data.
  - Formal definition: (i*, t*) = argmin_t over C(τ). The printed equation has a sign inconsistency (Ω(τ) = 1) [full text] — [arXiv HTML](https://arxiv.org/html/2509.03312)
- AgenTracer dataset and training: TracerTraj has about 2.5K annotated trajectory-error pairs (2,476) drawn from 4,655 curated trajectories, with 266 held-out test cases. AgenTracer-8B is Qwen3-8B trained with GRPO on 8×H100 using verl [full text] — [arXiv HTML](https://arxiv.org/html/2509.03312)
- AgenTracer results on Who&When, step-level, with GT / without GT:

  | Model | Hand-crafted | Automated |
  |---|---|---|
  | AgenTracer-8B | 20.68 / 20.68 | 42.86 / 37.30 |
  | Claude-Sonnet-4 | 17.24 / 18.97 | 40.65 / 38.83 |
  | DeepSeek-R1 | 13.29 / 6.90 | 31.32 / 29.52 |
  | Qwen3-8B (base) | 1.72 / 3.45 | 3.97 / 5.56 |

  - AgenTracer agent-level accuracy is 69.10 / 63.82 on hand-crafted and 69.62 / 63.73 on automated [full text] — [arXiv HTML](https://arxiv.org/html/2509.03312)
  - Its feedback gives 4.8–14.2% gains on MetaGPT and MaAS [abstract] — [arXiv abs](https://arxiv.org/abs/2509.03312)
- Caveat: AgenTracer's baseline numbers differ from Who&When's own tables (different splits and prompts), so the two papers' numbers are not directly comparable [inferred from both tables] — [2505.00212](https://arxiv.org/html/2505.00212); [2509.03312](https://arxiv.org/html/2509.03312)
- **Causal-inference attribution (Ma et al., arXiv 2509.08682, Sep 2025).**
  - Agent-level blame: a "performance causal inversion" that reverses the data flow in logs, combined with Shapley values.
  - Critical steps: a causal discovery algorithm, CDC-MAS, designed for non-stationary MAS data.
  - Suggested fixes are validated with counterfactual simulation.
  - Results: up to 36.2% step-level accuracy on Who&When/TRAIL, and a 22.4% average task-success gain. The abstract says prior state of the art was below 15% [abstract] — [arXiv abs](https://arxiv.org/abs/2509.08682)
- **EMFA (Liao et al., arXiv 2610.11600, 8 Oct 2026).**
  - Method: model error propagation and persistent loops in the trajectory, screen candidates by propagation, then verify counterfactually.
  - Defines the decisive error as the agent-step pair "whose correction would recover the failed execution".
  - Claims step-level state of the art: +3.45 points (Hand-Crafted) and +4.40 points (Algorithm-Generated) over the previous best. Agent-level accuracy is "competitive". The abstract gives no absolute numbers [abstract] — [arXiv abs](https://arxiv.org/abs/2610.11600)

### Inferences
- The best reported step-level numbers come from methods that build an explicit dependency or propagation structure and then verify counterfactually: CDC-MAS, EMFA, and DCFA per its snippet. That structure is essentially an event graph, so these are the closest prior art for a graph-based inflection detector.
- Hand-crafted (Magentic-One) logs are much harder than algorithm-generated ones (about 20% vs about 40% for the best model). Long, real orchestrator logs are the hard case.
- Ground-truth "decisive step" labels are themselves defined by counterfactual correction. Methods that actually replay (AgenTracer for labeling, EMFA and CDC-MAS for verification) are therefore aligned with the label definition, while pure LLM-judge methods are not.

### Gaps
- [search snippet only] The following could not be verified at the source in this pass:
  - DCFA (arXiv 2609.04749): causal dependency graph plus local counterfactuals, up to +8.27% step-level — [arXiv](https://arxiv.org/html/2609.04749)
  - ProFA (arXiv 2608.28264): step-level 0.53/0.78/0.42/0.38/0.20 across five datasets — [arXiv](https://arxiv.org/html/2608.28264)
  - "Seeing the Whole Elephant" benchmark (arXiv 2604.22708) — [arXiv](https://arxiv.org/html/2604.22708v1)
  - "Interpreting Emergent Extreme Events in MAS" (arXiv 2601.20538) — [arXiv](https://arxiv.org/pdf/2601.20538)
- EMFA's absolute accuracies, models, and cost are not on its abstract page.
- I found no explicitly spectrum-based (SBFL-style) or information-theoretic MAS attribution paper in this pass; this needs a targeted search.
- None of the abstracts I fetched report replay cost in dollars or tokens, except Who&When's token counts for its LLM-judge methods.

## Q3. Credit assignment in RL for LLM agents as decisive-step location

### Takeaway
Turn-level credit assignment (turn-level advantages and rewards) is an established line of work. It produces per-turn values that could locate decisive steps, but those papers aim at training, not at evaluating localization. Coverage in this pass is thin.

### Cited Findings
- Zeng, Wei et al., arXiv 2505.11821 (May 2025):
  - v1 is titled "...via Turn-Level Credit Assignment" and proposes turn-level advantage estimation that can be plugged into GRPO.
  - v2 (Oct 2025) is retitled "...via Turn-Level Reward Design" and introduces MT-GRPO/MT-PPO with verifiable and LLM-judge turn rewards.
  - MT-GRPO needs exponentially many rollouts for intermediate advantages, while MT-PPO uses a critic for scalability.
  - [search snippet only; abstract not fetched] — [arXiv abs v2](https://arxiv.org/abs/2505.11821v2); [v1](https://arxiv.org/abs/2505.11821v1)
- Related: Phi-4's PTS is itself a credit-assignment device, concentrating the DPO signal on the token where p(success) jumps [full text] — [arXiv HTML](https://arxiv.org/html/2412.08905v1)
- Related: AgenTracer uses the decisive step as a training signal (multi-granular RL reward) [full text] — [arXiv HTML](https://arxiv.org/html/2509.03312)

### Inferences
- A learned value function V(prefix) (a PPO critic or PRM) gives an amortized estimate of p(success | prefix). The largest |ΔV| between consecutive events is a cheap inflection candidate, i.e. PTS without per-position resampling. Its accuracy depends on how well the critic is calibrated, and no source here validates it against Who&When labels.
- The exponential-rollout comment on MT-GRPO is the same cost wall that resampling methods hit.

### Gaps
- Not covered in this pass: process reward models (e.g., Math-Shepherd-style Monte Carlo step labels), step-level value or PRM work for agents, or any paper that evaluates RL credit signals against ground-truth decisive steps.
- 2505.11821's results were not verified beyond search snippets.

## Q4. "Point of no return" / commitment-point detection (including safety)

### Takeaway
Several 2026 papers explicitly localize when a trajectory becomes committed to harm or deception:
- UMMB's "harm window" runs from the first harmful commitment to execution.
- SafetyDrift models absorbing-state Markov "points of no return".
- 2605.17113 localizes deceptive commitment by resampling.

A shared finding is that position-blind metrics overstate how well monitors localize the onset of harm.

### Cited Findings
- **Unified Misuse Monitoring Benchmark (Pramod, Oldfield, Bibi; arXiv 2610.07089, 5 Oct 2026).**
  - Asks when a trajectory becomes harmful, not just whether.
  - The harm window runs "from the agent's first harmful commitment to goal execution". A monitor succeeds if its first flag falls inside the window.
  - About 6,200 transcripts with labelled windows, benign controls, and refusals; threats are decomposition attacks and prompt injection.
  - Results across 17 monitor configurations:
    - Action-framed monitors score AUC 0.95 (decomposition) and 0.99 (injection) on classical metrics.
    - Content-framed monitors fall to AUC 0.52 on injection.
    - All monitors localize decomposition poorly under the interval metric.
  - [abstract] — [arXiv abs](https://arxiv.org/abs/2610.07089)
- **SafetyDrift (Dhodapkar, Pishori; arXiv 2603.27148, Mar 2026).**
  - Models agent safety as an absorbing Markov chain, with a closed-form probability of violation within a horizon.
  - Detects 94.7% of violations with 3.7 steps of warning. Baselines: keywords at 44.7% detection / 55.9% FPR, and per-step LLM judges at 52.6% / 38.2%.
  - More than 60,000x faster than LLM judges. Evaluated on 357 traces and 40 tasks.
  - Task dependence: in communication tasks, a mild risk state gives an 85% chance of violation within 5 steps; technical tasks stay below 5%.
  - [abstract] — [arXiv abs](https://arxiv.org/abs/2603.27148)
- **The Point of No Return (arXiv 2605.17113):** resampling-based localization of deceptive commitment (see Q1) [abstract] — [arXiv abs](https://arxiv.org/abs/2605.17113)

### Inferences
- UMMB's interval metric is directly usable as an evaluation metric for an inflection detector on event graphs. A detector is scored by whether it flags within [commitment, execution], not by trace-level AUC.
- SafetyDrift shows a cheap alternative to resampling: abstract states into a Markov chain and compute absorption probabilities. It trades fidelity for speed (no LLM calls at monitor time).

### Gaps
- [search snippet only] The following could not be verified at the source:
  - arXiv 2605.07937: "point of no return" for clarification timing, with a 30% cutoff — [arXiv](https://arxiv.org/pdf/2605.07937)
  - arXiv 2606.22936: representational commitment via hidden-state convergence, Llama-3.1-70B ReAct on HotpotQA — [arXiv](https://arxiv.org/pdf/2606.22936)
  - arXiv 2605.22007: commitment step at an entropy peak — [arXiv](https://arxiv.org/pdf/2605.22007)
- UMMB's labelling procedure for "first harmful commitment" and its exact interval-metric formula are not in the abstract; read the full paper.
- SafetyDrift's state abstraction and the models used were not verified.

## Q5. Scale and cost

### Takeaway
Resampling and replay methods are accurate by construction but expensive, roughly O(positions × samples × continuation length). Known mitigations:
- Bisection (PTS, Who&When binary search).
- Fewer samples (Forking Paths finds 10–20 samples are enough).
- White-box proxies (attention suppression, about 100x cheaper).
- Amortized learned judges or tracers (AgenTracer-8B).
- Analytical models (SafetyDrift, more than 60,000x faster than LLM judges).

### Cited Findings
- Forking Paths: about 1M tokens (about $2) per base path, about $500 total, and 10–20 samples are about as good as 30 — [arXiv HTML](https://arxiv.org/html/2412.07961)
- Thought Anchors: 100 rollouts per sentence × about 144 sentences per trace. Attention suppression costs about 100x less — [arXiv HTML](https://arxiv.org/html/2506.19143)
- 2605.17113: more than 94.1M sampled continuations to localize about 1.46M sentences, i.e. about 64 continuations per sentence (my arithmetic) — [arXiv abs](https://arxiv.org/abs/2605.17113)
- Who&When LLM-judge methods use 17k–149k tokens per hand-crafted log, and higher token spend does not reliably buy step accuracy — [arXiv HTML](https://arxiv.org/html/2505.00212)
- AgenTracer: training on 8×H100. Inference is a single 8B model pass, but the labels came from R1-driven counterfactual replay — [arXiv HTML](https://arxiv.org/html/2509.03312)
- SafetyDrift: more than 60,000x faster than per-step LLM judges — [arXiv abs](https://arxiv.org/abs/2603.27148)

### Inferences
- A practical recipe for a multi-agent event graph:
  1. Score nodes cheaply first (a value or critic delta, an attention proxy, or a trained tracer such as AgenTracer-8B on Qwen3-8B, which is open-weight).
  2. Bisect over the topological order.
  3. Spend resampling or counterfactual replay only on the top-k candidates, as EMFA and CDC-MAS do (screen, then verify).
- Replay fidelity (deterministic tools, seeded environments) is likely the main engineering cost on agent graphs, more than token cost.

### Gaps
- No source gave dollar or GPU-hour costs for counterfactual replay on full MAS trajectories (AgenTracer, EMFA, CDC-MAS).
- PTS sample budgets are unpublished.
