# Causal Influence and Attribution Methods as Edge Weights for Multi-Agent Event Graphs

Scope: methods that score how much an earlier event (message, tool output, document, step) causally affects a later LLM or agent output. Each method is judged on four things: whether it is interventional, its cost, the evidence that it is faithful, and how it handles redundancy and multi-step effects. Verification: every claim below was checked against the arXiv abstract page, the arXiv HTML full text, or the PDF text, unless it is marked "snippet-only". Search date is 2026-10-23.

## Q1. Context attribution: ContextCite and its follow-ups (AttriBoT, AT2, TracLLM, 2026 critiques)

### Takeaway
ContextCite and AttriBoT are both interventional. ContextCite fits a sparse linear surrogate to random ablations. AttriBoT approximates exact leave-one-out (LOO) on the teacher-forced response log-probability. Both are validated on open-weight models (Llama-3/3.1, Phi-3, Qwen2.5), and both suit edge weights from context segments to an output. AT2 learns an attention-based estimator from ablations, which brings the per-example cost below one forward pass. A key 2026 caveat is that these methods are unreliable when the context's content is already in the model's weights.

### Cited Findings
**ContextCite** (Cohen-Wang, Shah, Georgiev, Madry; arXiv 2409.00729, Sep 2024)
- Sources are mostly sentences. Ablation vectors are sampled uniformly over subsets of sources, and excluded sentences are removed from the context — [arXiv HTML](https://arxiv.org/html/2409.00729v2)
- Target: g(v) = logit of p_LM(R | Ablate(C, v), Q). This is the teacher-forced probability of the actual response R under the ablated context. The surrogate is a sparse linear model fit with Lasso (scikit-learn, alpha = 0.01), and its weights are the attribution scores — [arXiv HTML](https://arxiv.org/html/2409.00729v2)
- Budget: 32, 64, 128 or 256 ablations, i.e. that many forward passes per response. "ContextCite using just 32 context ablations consistently matches or outperforms the baselines" (LOO, attention, gradient norm, semantic similarity) on top-k log-prob drop (k = 1, 3, 5) and LDS (Spearman correlation) — [arXiv HTML](https://arxiv.org/html/2409.00729v2)
- Models: Llama-3-8B and Phi-3-mini, plus Llama-3-70B in the appendix. Datasets: TyDi QA, HotpotQA, CNN/DailyMail — [arXiv HTML](https://arxiv.org/html/2409.00729v2)
- Attention is competitive on Llama-3-8B but "not consistently reliable" on Phi-3-mini — [arXiv HTML](https://arxiv.org/html/2409.00729v2)
- Applications: verification, context pruning (better F1 on HotpotQA and NQ), and poisoning detection, where the injected prompt is the top source in more than 95% of cases. Reported failure cases: a partially successful optimization attack can mislead attribution, and a refusal was attributed to an unrelated sentence. The surrogate assumes sparsity and near-linearity, which the authors observed empirically but do not guarantee — [arXiv HTML](https://arxiv.org/html/2409.00729v2)

**AttriBoT** (Liu, Kandpal, Raffel; arXiv 2411.15102, ICLR 2025; code: github.com/r-three/AttriBoT)
- Target: exact LOO, i.e. the drop in response likelihood when one span is removed. The paper makes three observations, each with a matching trick:
  - About half of LOO FLOPs are redundant and can be removed with KV caching, which is lossless and gives a 2x speedup.
  - Hierarchical attribution works: paragraph-level LOO correlates with the sum of its sentence LOOs at R = 0.97 on HotpotQA with Llama 70B.
  - Same-family small proxies track the large model: Pearson correlation is 0.94 for an 8B proxy and 0.88 for a 1B proxy against Llama-3.1-70B LOO.
  - Source: [PDF](https://arxiv.org/pdf/2411.15102)
- Proxy-model pruning keeps only a fraction of sources, which are then re-scored with the target model. Recall of outlier sources reaches about 90% — [PDF](https://arxiv.org/pdf/2411.15102)
- Combined, the tricks give a ">300x speedup" with "only 10% drop in mAP" against exact LOO, which makes attribution "30x faster than generating" the response. AttriBoT is Pareto-better than attention weights, gradient norm, and ContextCite in the faithfulness vs GPU-seconds trade-off — [PDF](https://arxiv.org/pdf/2411.15102); [ICLR poster](https://iclr.cc/virtual/2025/poster/30669)
- Faithfulness metric: mAP at recovering the outlier LOO sources (found with a Generalized ESD test). Targets are Llama-3.1-70B-Instruct and Qwen2.5-72B-Instruct, with proxies down to 0.5B. Datasets: SQuAD 2.0, HotpotQA, QASPER — [PDF](https://arxiv.org/pdf/2411.15102)

**AT2, "Learning to Attribute with Attention"** (Cohen-Wang, Chuang, Madry; arXiv 2504.13752, Apr 2025; pip package `at2`)
- Features are per-(layer, head) attention weights from the generated tokens to each source. The method learns one coefficient per head by maximizing correlation with ablation effects on the logit-transformed response probability. Training ablations drop each source with p = 1/2 by zeroing attention. Training uses 2,000 examples x 32 ablations, roughly 64k forward passes, once per model — [arXiv HTML](https://arxiv.org/html/2504.13752)
- Inference costs less than one forward pass: "more than 2x faster than one forward pass" even when attention is recomputed. It performs comparably to ContextCite-style surrogates with 32–256 ablations and beats average attention and gradient norm. Average attention is poor on Phi-3.5-mini — [arXiv HTML](https://arxiv.org/html/2504.13752)
- Supports "thought attribution", i.e. attributing the final answer to intermediate reasoning sentences, on DeepSeek-R1-Distill-Qwen-7B. Other open models: Llama-3.1-8B-Instruct, Phi-3.5-mini — [arXiv HTML](https://arxiv.org/html/2504.13752)

**TracLLM** (Wang, Zou, Geng, Jia; arXiv 2506.04202, USENIX Security 2025)
- A generic context-traceback framework for long contexts. It argues that Shapley and similar methods are "sub-optimal" and/or costly at long context. It adds an informed-search algorithm for efficiency and ensembling plus denoising of contribution scores for accuracy — [arXiv abs](https://arxiv.org/abs/2506.04202)

**Critique: parametric overlap** (Trinh, Zhu, Szyller; arXiv 2607.23804, Jul 2026)
- Four "well-known" context attribution methods give "unfaithful attribution when the knowledge from the context also exists in the weights" and cannot separate in-context from in-weight contributions. The paper introduces the WMDP-Cyber++ benchmark and four metrics (BCS, CAC, APS, SSP) — [arXiv abs](https://arxiv.org/abs/2607.23804)

### Inferences
- For a SentryBench event graph, the most direct edge weight is the AttriBoT-style LOO score: Δ log p(actual later output | context without event e). It is exact, interventional, and cheap with KV caching and a hierarchical first pass over events then sub-spans. ContextCite with 32–64 ablations adds a little interaction robustness over pure LOO.
- AT2 is the cheapest option for online monitoring. It must be trained per model, but it is available for open models.
- An event whose content the model already knows, such as a fact, gets a low context-attribution score even if it was the proximate cause. Label such edges with care.

### Gaps
- The exact accuracy numbers for ContextCite and AT2 are only in figures and were not extracted. ContextCite's limitations appendix (C.4) was cut off in the fetch.
- Which four methods 2607.23804 tested was not verified.
- TracLLM's cost numbers, models, and results were not verified. A third-party summary's claim of O(K·e·log n) cost is unverified.

## Q2. Counterfactual ablation with teacher-forced log-probabilities of the actual later output, for agents and dialogues

### Takeaway
LOO on the teacher-forced log-probability of the realised output is the standard core of ContextCite, AttriBoT and AT2. In 2026 it was applied to agent settings: CausalArmor uses LOO at privileged tool-call decision points, and several trajectory papers use the same idea. Agent papers increasingly also use re-execution (rollout) counterfactuals, which capture downstream effects at much higher cost and with more variance.

### Cited Findings
- **CausalArmor** (Kim et al., Google; arXiv 2602.07918, ICML 2026): computes "leave-one-out ablation-based attributions at privileged decision points" and sanitizes only when an untrusted span, such as a tool output or retrieved document, has more attributable influence on the action than the user request. It adds retroactive CoT masking. Evaluated on AgentDojo and DoomArena. The abstract claims a theoretical bound that is exponentially small on selecting malicious actions — [arXiv abs](https://arxiv.org/abs/2602.07918)
- **C3** (Chen et al.; arXiv 2603.06859): substitutes one message at a decision point and continues the run to terminal reward, regenerating only downstream messages. With 4 continuations it reaches 0.69 rank correlation to a 16-continuation reference (two references agree at about 0.73), while a learned critic gets 0.29 — [arXiv abs](https://arxiv.org/abs/2603.06859). Note: v1 was titled "Contextual Counterfactual Credit Assignment…" and its HTML mentions "fixed-continuation replay" and a LOO baseline ([v1 HTML](https://arxiv.org/html/2603.06859v1), snippet-only). The current v4 abstract is titled "The Trace Is the State: Exact Credit Assignment for LLM Agent Teams" and names only terminal reward.
- **Snippet-only (not opened):** a long-horizon trajectory attribution benchmark defines component influence as the drop in mean token log-likelihood of the target output when the component is removed — [arXiv 2608.06909](https://arxiv.org/pdf/2608.06909). LOTAPO replaces a turn with a [DELETE] placeholder and measures the change in gold-answer log-likelihood — [arXiv 2607.13501](https://arxiv.org/pdf/2607.13501).

### Inferences
- There are two kinds of counterfactual, and they answer different questions:
  - **Teacher-forced (frozen downstream):** keep the later output fixed and ask how likely it would be without the event. This is cheap (one forward pass per ablation) and deterministic, but it measures only the direct effect of the event on that one output.
  - **Rollout (re-run downstream):** re-generate everything after the event and compare outcomes. This captures total effects through intermediate events, but it is stochastic and needs multiple samples.
- An event graph probably needs both: teacher-forced weights for edges, and rollout for validating "inflection points".
- Removing an event creates an out-of-distribution context, for example a dangling reference to a deleted tool call. Placeholder replacement (LOTAPO) is one mitigation.

### Gaps
- I found no verified paper that applies teacher-forced LOO across a full multi-agent dialogue graph with per-edge weights. The closest are CausalArmor (a single decision point) and the unverified 2608.06909.

## Q3. Shapley / kernel-SHAP over context segments or agents

### Takeaway
Shapley handles interactions and redundancy in principle, but it costs many more model calls. The 2025–2026 evidence suggests LOO is often enough to find bottleneck agents. Interaction-aware alternatives such as ProxySPEX and semantic Shapley reduce the cost. The Adaptive Accountability paper does use kernel-SHAP, but its agents are RL or controller agents, not LLMs.

### Cited Findings
- **Adaptive Accountability** (Alqithami; arXiv 2512.18561, v3 Mar 2026): uses "a Shapley-value-style responsibility rule… via a Monte-Carlo kernel-SHAP proxy with at most K coalition samples per event", with K = 32 and cost Õ(K·|E_t|) per round. Causal edges come from rolling multivariate Granger tests. A separate path-based responsibility uses discount β = 0.8, so that "proximal causes weigh more", and this is not reconciled with the Shapley definition. Agents are PPO, Q-learning or MPC, not LLMs. It reports 0.97 top-ranked attribution accuracy at a 10% Byzantine rate, with the ground-truth definition not visible in the fetched text — [arXiv HTML](https://arxiv.org/html/2512.18561v3); [abs](https://arxiv.org/abs/2512.18561)
- **Agents that Matter** (Lu, Huang, Lin, Su-In Lee; arXiv 2605.27621): "LOO identifies bottleneck agents as effectively as combinatorial methods at much lower computational cost". Different intervention protocols "induce distinct games", meaning the attribution depends on how an agent is removed. "Introspective LLM judges fail to faithfully approximate" ablation — [arXiv abs](https://arxiv.org/abs/2605.27621)
- **Semantic Cooperative Games / SLIC** (Jiang, Zhu, Zhu; arXiv 2607.18255): computes a Semantic Shapley Value from a single trajectory's semantic hypergraph, without re-running agent subsets. It is 93.3% cheaper than Monte Carlo Shapley on a medical benchmark. It provably reduces to classical Shapley under set-based, fully observable, order-independent conditions. Agreement with perturbation is reported only qualitatively — [arXiv abs](https://arxiv.org/abs/2607.18255)
- **ProxySPEX** (arXiv 2505.17495, NeurIPS 2025): fits gradient-boosted trees to masked LLM outputs and extracts sparse interactions. It reconstructs outputs about 20% more faithfully than marginal attribution and uses 10x fewer inferences than SPEX. SPEX needs about 2x10^4 inferences for order-5 interactions at n = 100 — [arXiv HTML](https://arxiv.org/html/2505.17495v2); [NeurIPS](https://neurips.cc/virtual/2025/poster/118659)
- **CAR** (Shah; arXiv 2606.08275): its budget-bounded Monte Carlo Shapley over agent steps recovers a planted two-step interaction (0.44, 0.45, ~0; efficiency sum 0.909 vs analytic 0.91) on synthetic SCMs — [arXiv abs](https://arxiv.org/abs/2606.08275)

### Inferences
- Under redundancy, where two events carry the same information, LOO gives both a weight near zero. Shapley splits the credit. Running a cheap LOO pass and adding Shapley or ProxySPEX only on the top-k candidate events is a reasonable hybrid, consistent with AttriBoT's prune-then-rescore idea.

### Gaps
- How the Adaptive Accountability paper defines its 0.97 accuracy was not visible. No LLM-agent experiments were found in that paper.

## Q4. Causal mediation: direct vs indirect effects through intermediate events

### Takeaway
I found no verified paper that formally decomposes LLM agent trajectories into natural direct and indirect effects. Agent work measures total effects by intervening and re-executing (CAR, C3, CausalFlow). Mediation analysis remains mostly an interpretability tool applied inside the model.

### Cited Findings
- **CAR** models a run as an SCM, applies do() to a step, and re-executes under the same stochastic policy. Every effect comes with confidence intervals. A "point-of-commitment rule" handles the confound that re-rolling downstream steps introduces — [arXiv abs](https://arxiv.org/abs/2606.08275). The search snippet said the rule picks the latest step whose effect interval excludes zero, but this was not confirmed on the abstract page.
- **Snippet-only:** CausalFlow (arXiv 2605.25338) computes Causal Responsibility Scores by step-level counterfactual intervention and validates them with minimal repairs — [arXiv HTML](https://arxiv.org/html/2605.25338)
- On Who&When, state-of-the-art step-level failure attribution accuracy is about 14% — [CAR abs](https://arxiv.org/abs/2606.08275)

### Inferences
- A graph-native decomposition looks feasible but unpublished. Take the teacher-forced effect of event A on output Y with intermediate event M frozen: that is a controlled direct effect. Take the rollout effect, where M is regenerated: that is the total effect. The difference approximates the indirect effect through M. This is a possible novel contribution for SentryBench.

### Gaps
- No verified paper reports natural direct and indirect effects for LLM pipelines. Mediation inside models (e.g., attention heads) was not pursued.

## Q5. Gradient, attention and approximation methods: agreement with exact ablation

### Takeaway
Raw attention and gradient norms are consistently less faithful to ablation than ablation-based methods, and their reliability depends on the model (attention works on Llama, not on Phi). Learned attention (AT2) and proxy-model LOO (AttriBoT) close most of the gap.

### Cited Findings
- ContextCite with 32 ablations matches or beats attention and gradient norm. Attention is unreliable on Phi-3-mini — [arXiv HTML](https://arxiv.org/html/2409.00729v2)
- AttriBoT is Pareto-dominant over attention weights (summed over all heads and layers) and over the Frobenius gradient norm, measured by mAP to exact LOO — [PDF](https://arxiv.org/pdf/2411.15102)
- AT2 outperforms average attention and gradient norm and matches ablation surrogates — [arXiv HTML](https://arxiv.org/html/2504.13752)
- Huang and Chan (arXiv 2601.03089, 2026) show that soft-perturbation faithfulness metrics can be inflated by how much information they retain, and propose π-Soft-NC and π-Soft-NS. Their Grad-ELLM is strong under π-Soft-NC, but no method dominates under π-Soft-NS. Models: Llama and Mistral — [arXiv abs](https://arxiv.org/abs/2601.03089)
- vStream (VLM) reports an LDS of 0.41 for attention rollout vs 0.72 for feature ablation (snippet-only) — [arXiv 2604.16587](https://arxiv.org/html/2604.16587v1)

### Gaps
- No verified study evaluates attribution patching or integrated gradients over context against exact ablation in agent settings. Per-method rankings in 2601.03089 were not extracted.

## Q6. Multi-agent-specific methods

### Takeaway
Counterfactual social influence is interventional but was designed for RL policies. NCB/BPD is not causal: it propagates LLM-judge agreement signs backward over a DAG. Activation deltas measure how far context shifts the model's internal state, as a detection signal, and are not attribution to a specific event.

### Cited Findings
- **Social influence** (Jaques et al.; arXiv 1810.08647, v4 2019): the intrinsic reward is the causal influence of an agent's action on other agents' actions, computed by simulating counterfactual actions. It is equivalent to rewarding mutual information between actions and uses learned models of other agents. The abstract does not state the KL form — [arXiv abs](https://arxiv.org/abs/1810.08647)
- **NCB / BPD** (Wu et al.; arXiv 2510.19420, v2 May 2026):
  - The conversation is unrolled into a temporal DAG. An external LLM judge assigns each edge a sign g ∈ {−1, 0, 1}. Judge agreement with humans was 98% for GPT-4o and 96% for DeepSeek-V3, on only 50 samples.
  - Terminal nodes are set to ±1 depending on agreement with the final answer. Scores propagate backward with S = P·S_next (P_ij = g/k), in one topological pass, as a signed PageRank variant.
  - Overhead is about 9–11% of runtime. Monitor accuracy is 90.7% (flat) and 93.3% (hierarchy), against 88.3% and 87.7% for G-Safeguard.
  - Removing backpropagation costs 6–8 points. The threshold ε = 1.5 was tuned on the evaluation setting.
  - Source: [arXiv HTML](https://arxiv.org/html/2510.19420v2)
- **Activation deltas / TaskTracker** (Abdelnabi et al.; arXiv 2406.00799, SaTML 2025): the difference in activations before and after processing external data. A linear probe detects task drift with near-perfect out-of-distribution ROC AUC. The dataset has 500K+ instances and covers six models — [arXiv abs](https://arxiv.org/abs/2406.00799)

### Inferences
- NCB's backward propagation over a DAG is a useful template for multi-step (second-order) aggregation. Replacing its judge signs with interventional edge weights such as LOO Δlog p would make it causal.
- Activation deltas could serve as a cheap per-event "how much did this event perturb state" node feature, but not as a causal edge weight.

### Gaps
- An Expert Systems 2026 paper on per-message counterfactual attribution (single-driver, mixed-driver, no-driver) was seen only in a snippet — [Wiley](https://onlinelibrary.wiley.com/doi/10.1111/exsy.70392)

## Q7. Failure modes and fixes

### Takeaway
The main failure modes are redundancy, interactions, distribution shift from ablation, overlap with parametric knowledge, cost, and intervention-protocol dependence. Each has a partial fix in the literature, but none is solved for multi-agent graphs.

### Cited Findings
- **Redundancy and interactions:** LOO is blind to interactions, and Shapley or interaction methods fix this at higher cost — [Agents that Matter](https://arxiv.org/abs/2605.27621); [ProxySPEX](https://arxiv.org/html/2505.17495v2); [CAR](https://arxiv.org/abs/2606.08275). ContextCite's sparse linear surrogate assumes approximately additive effects — [ContextCite](https://arxiv.org/html/2409.00729v2)
- **Parametric overlap:** attribution is unfaithful when the content is already in the model's weights — [2607.23804](https://arxiv.org/abs/2607.23804)
- **Cost:** KV caching, hierarchical pruning, and proxy models give a >300x speedup — [AttriBoT](https://arxiv.org/pdf/2411.15102). A learned attention estimator costs less than one forward pass — [AT2](https://arxiv.org/html/2504.13752). Shapley is costly at long context — [TracLLM](https://arxiv.org/abs/2506.04202)
- **Protocol dependence:** how an agent is removed changes the result ("distinct games"), and LLM judges do not track ablation — [Agents that Matter](https://arxiv.org/abs/2605.27621)
- **Adversarial robustness:** a partially successful optimization attack can mislead ContextCite — [ContextCite](https://arxiv.org/html/2409.00729v2)
- **Rollout variance:** re-running downstream steps adds stochastic confounds — [CAR](https://arxiv.org/abs/2606.08275). Two 16-continuation references agree at only about 0.73 — [C3](https://arxiv.org/abs/2603.06859)

### Inferences
- A recommended stack for SentryBench:
  1. Teacher-forced LOO Δlog p for every edge, accelerated AttriBoT-style.
  2. Shapley or interaction scores on the top-k edges, to handle redundancy.
  3. Rollout validation for second-order effects.
  4. Report the ablation protocol (delete vs placeholder) explicitly.

### Gaps
- No benchmark with ground-truth causal edge weights exists for multi-agent LLM graphs. One search-result mirror (Hugging Face) contained a prompt-injection instruction, which was ignored.
