# Graph and provenance representations of agent / multi-agent traces, and open trace datasets

Research date: 2026-10-23. "Verified" means read on the primary page (arXiv abstract/HTML, GitHub README, HF dataset card). Items taken only from search-result summaries are marked [search summary, not verified at source].

## Q1. What graph representations of agent traces exist (nodes, edges, edge computation, scale, results, code/license)?

### Takeaway
Almost every published representation builds edges *structurally* from the trace (who sent what to whom, which tool was called, which activation produced which event). DIG, SentinelAgent, GUARDIAN, PROV-AGENT and OpenTelemetry/OpenInference all work this way. Only the Adaptive Accountability Framework (statistical Granger edges, on RL agents rather than LLMs) and the failure-attribution line (CHIEF, AgenTracer, Shapley-based extreme-event attribution) attach causal or counterfactual meaning. Most of these do it at the step or agent level, not as edge weights.

### Cited Findings

**DIG: Dynamic Interaction Graph (arXiv 2603.00309)**
- "DIG to Heal: Scaling General-purpose Agent Collaboration via Explainable Dynamic Decision Paths", Yang, Lee, Yao, Liu, Liu, Chen, Joe-Wong. v1 27 Feb 2026, v2 27 May 2026. Paper licence CC BY 4.0. The abstract calls DIG "a time-evolving causal network of agent activations and interactions". — [arXiv abs](https://arxiv.org/abs/2603.00309)
- The graph is bipartite. **Activation nodes** are one activation of an agent over a time interval. **Event nodes** are one interaction event, with its generation time and delivery times. **Generation edges** run activation→event and **delivery edges** run event→activation. Edges come from the observed execution trace, not from learning, and carry no numeric weights. Each edge gets an action label (consume / delay / reroute / discard) and a binary productive/non-productive attribution. — [arXiv HTML v2](https://arxiv.org/html/2603.00309v2)
- Use: detecting and "healing" structural failures (early termination, missing termination, orphaned events, deadlock, excessive rerouting, cross-lineage aggregation, repeated subproblem solving) by injecting information, rerouting, or creating events. — [arXiv HTML v2](https://arxiv.org/html/2603.00309v2)
- Scale is small. Count Frequency uses 4 or 6 agents and Research Job uses 4 agents, with 10 runs per setting, plus one 20-agent case study. Example result: CF homogeneous with 6 agents, final error fell from 0.100 to 0.017. RJ error fell 44% (homogeneous) and 18% (heterogeneous). In the 20-agent case, the MAS without DIG did not finish within 120 s; with DIG it produced a valid answer in 70 s. The visible text does not name the LLMs. No code repo is linked, only a project page, happyeureka.github.io/dig. — [arXiv HTML v2](https://arxiv.org/html/2603.00309v2)

**SentinelAgent (arXiv 2505.24201)**
- He, Wu, Zhai, Sun, 30 May 2025. "Dynamic execution graphs" with anomaly detection at node, edge and path level, plus an LLM-powered oversight agent. Case studies: an email assistant and Magentic-One. — [arXiv abs](https://arxiv.org/abs/2505.24201)
- Nodes are agents (with system prompt, capabilities, role) and tools. In Magentic-One the shared ledger is a global memory node. Edges are typed, directed and timestamped, and cover inter-agent messages, tool invocations and reasoning steps. A static graph comes from the architecture (allowed paths). The dynamic graph is built from runtime traces collected with OpenTelemetry-style hooks and Arize Phoenix. Path-level detection matches subgraphs against an "attack path library". Node and edge checks use IBM Granite Guardian 3.2, LlamaFirewall and Llama Guard. — [arXiv HTML](https://arxiv.org/html/2505.24201)
- Evaluation is qualitative and small: the email assistant has 3 benign and 2 attack paths. I found no precision/recall numbers in the first ~100k characters of the HTML, and no code release. The rest of the HTML was not read. — [arXiv HTML](https://arxiv.org/html/2505.24201)

**GUARDIAN (arXiv 2505.19234)**
- Zhou, Wang, Yang. v1 25 May 2025, v2 15 Oct 2025. Unsupervised encoder-decoder on a temporal attributed graph, with Information-Bottleneck graph abstraction and incremental training. — [arXiv abs](https://arxiv.org/abs/2505.19234)
- Nodes are agent *i* at round *t* (v_{t,i}), with the response text embedded as the node feature. Edges (v_{t-1,i}, v_{t,j}) are directed communication edges between consecutive rounds, fixed by the debate topology. A 2-layer GCN, a time encoder, and attribute and structure decoders compute anomaly scores from reconstruction error. The highest-scoring node is removed each round. — [arXiv PDF](https://arxiv.org/pdf/2505.19234)
- Datasets: MMLU, MATH, FEVER, Biographies. Backbones: GPT-3.5-turbo, GPT-4o, Claude-3.5-sonnet and Llama3.1-8B (the only open-weight one). 3 to 7 agents, multi-round debate with injected hallucination, agent-targeted and communication-targeted attacks. Reported results: average +4.2% accuracy over SOTA baselines; detection rate averages above 80%; FDR 8.32% on MATH under agent attack. — [arXiv PDF](https://arxiv.org/pdf/2505.19234)
- Code at [github.com/JialongZhou666/GUARDIAN](https://github.com/JialongZhou666/GUARDIAN) under the MIT licence. No released logs are visible, and the script names suggest GPT-3.5 by default. — [GitHub](https://github.com/JialongZhou666/GUARDIAN)

**Adaptive Accountability Framework (arXiv 2512.18561)**
- Saad Alqithami (single author). v1 21 Dec 2025, v3 19 Mar 2026. Paper licence CC BY-SA 4.0. — [arXiv abs](https://arxiv.org/abs/2512.18561)
- Its "causal influence graph" is an event ledger. **Nodes** are atomic events (action, message, external shock) with ID, timestamp and payload. A **directed edge** upstream→downstream is added when a rolling Granger-style F-statistic over a window of m=8 upstream events exceeds a time-varying threshold. The paper says itself that this approximates causality. Responsibility weights are defined inconsistently. §3.1 uses a Shapley / kernel-SHAP proxy. §4.2/§5.2 use path-based β^|p| sums with β=0.8, normalised to 1. — [arXiv HTML](https://arxiv.org/html/2512.18561)
- **The agents are RL or rule-based (PPO, Q-learning, MPC), not LLMs.** Environments are resource-sharing and public-goods games. Scale: 87,480 runs, 324 regimes, up to 100 agents plus a 500-agent sweep. Results: lower compromise ratio than PPO in 96% of regimes; median detection delay 71 steps; top-1 attribution accuracy 0.97 at 10% Byzantine rate. The code "will be released"; no repo was found. — [arXiv abs](https://arxiv.org/abs/2512.18561); [arXiv HTML](https://arxiv.org/html/2512.18561)

**Failure-attribution methods that build causal or dependency structure**
- **CHIEF** ("From Flat Logs to Causal Graphs", arXiv 2602.23701, Wang, Wu, Wang, Wang, 27 Feb 2026). Turns trajectories into a "hierarchical causal graph", then does oracle-guided backtracking and counterfactual attribution via "progressive causal screening". Evaluated on Who&When; claims to beat 8 baselines at agent and step level. The abstract page does not give node/edge definitions or a code link. — [arXiv abs](https://arxiv.org/abs/2602.23701)
- **GraphTracer** (arXiv 2510.10581). Builds "Information Dependency Graphs" of which outputs agents build on. **It was withdrawn in v2 (22 Dec 2025) for "a fundamental error in the methodology"; do not rely on it.** Its headline numbers (+18.18%, 4.8–14.2%) are the same figures AgenTracer reports. — [arXiv abs](https://arxiv.org/abs/2510.10581)
- **AgenTracer** (arXiv 2509.03312, G. Zhang et al., ICLR 2026). Defines the decisive step counterfactually: an analyzer proposes a corrected action at each step and re-simulates the rest of the run. The decisive error is the earliest step whose correction turns failure into success. It also uses fault injection on successful runs. TracerTraj-2.5K has 2,476 labelled pairs (Coding 1,288, Math 630, Agentic 558) from MetaGPT, AutoGen, Smolagents, AgentPrune, AFlow and OWL-Workforce. The analyzer and perturbation operator are DeepSeek-R1, and the trajectory-generating LLMs are not stated. AgenTracer-8B is Qwen3-8B trained with GRPO. Who&When step-level scores: handcrafted 20.68 vs Claude-Sonnet-4 17.24; automated 42.86 vs 40.65 (with ground truth). Only a project page is given (bingreeky.github.io/atracer), with no explicit data repo. — [arXiv abs](https://arxiv.org/abs/2509.03312); [arXiv HTML](https://arxiv.org/html/2509.03312v2)
- **Interpreting Emergent Extreme Events in MAS** (arXiv 2601.20538, Tang et al., Jan 2026). Adapts the Shapley value to score each agent action at each time step for an extreme event, then aggregates along time, agent and behaviour. Settings are economic, financial and social LLM-agent scenarios. The abstract page names no models, scale or code. Conceptually this is the closest existing work to per-event "inflection point" scoring. — [arXiv abs](https://arxiv.org/abs/2601.20538)

**Provenance and tracing standards**
- **PROV-AGENT** (arXiv 2508.02866, Argonne/ORNL, IEEE eScience 2025). Extends W3C PROV (Entity / Activity / Agent) to agent prompts, responses and decisions, using MCP and data observability. It is implemented in Flowcept with relations used, wasGeneratedBy, wasAssociatedWith, wasAttributedTo and wasInformedBy. Use case: root-cause analysis in an additive-manufacturing workflow. Edges are provenance (data lineage), not causal weights. [search summary, abstract not opened directly] — [arXiv](https://arxiv.org/abs/2508.02866); [Flowcept schemas](https://flowcept.readthedocs.io/en/stable/schemas.html)
- **OpenTelemetry GenAI semantic conventions** have moved to a separate repo, github.com/open-telemetry/semantic-conventions-genai. That repo's landing page covers spans, metrics and events for GenAI clients, MCP and providers. I could not confirm the agent-span names (create_agent / invoke_agent / execute_tool) or their status from the pages fetched. — [OTel docs page](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/); [repo](https://github.com/open-telemetry/semantic-conventions-genai)
- **OpenInference** (OTel-based) is the trace format of the TRAIL dataset, so span trees are a de facto open format for agent traces. — [TRAIL HF card](https://huggingface.co/datasets/PatronusAI/TRAIL)
- **Inspect eval logs (UK AISI)** have top-level EvalLog → samples, each with messages and an events transcript. ModelEvent and ScoreEditEvent are named on the log page. Logs are stored as `.eval` (binary, zstd, about 1/8 the size of JSON) or `.json`. The log page does not document the full event-type list or whether events form a span tree. — [Inspect eval logs](https://inspect.aisi.org.uk/eval-logs.html)

### Inferences
- Structural graphs (DIG, SentinelAgent, GUARDIAN, OTel/OpenInference, PROV) are cheap to build from logs, and SentryBench could adopt one as its schema backbone. A DIG-style bipartite activation/event graph or a PROV-style entity/activity graph maps well onto messages, tool calls and channel creations.
- None of the LLM-agent graph papers is large-scale. DIG uses 10 runs per setting, SentinelAgent uses a handful of paths, and GUARDIAN uses 3–7 agents on QA benchmarks. The large-scale causal-graph work (AAF, 87k runs) is on non-LLM RL agents.

### Gaps
- SentinelAgent quantitative results and Magentic-One counts: the second half of the HTML was not read.
- CHIEF node/edge definitions and code; models and code for 2601.20538. Only the abstracts were read.
- OTel GenAI agent-span specifics and the full Inspect event taxonomy were not verified.
- The LLMs used in DIG are not named in the text read.

## Q2. Which approaches attach causal or influence weights to edges, and which are only structural?

### Takeaway
Only AAF puts statistically inferred causal edges with path-based responsibility weights on an event graph, and only for RL agents. In LLM-MAS work, causality appears as counterfactual labels on steps (Who&When, AgenTracer, CHIEF) or as Shapley attributions over actions (2601.20538), not as weighted edges in a persistent graph.

### Cited Findings
- **Structural only:**
  - DIG has generation and delivery edges with categorical action labels and a productive/non-productive flag, but no weights. — [DIG HTML](https://arxiv.org/html/2603.00309v2)
  - SentinelAgent has typed message, tool and reasoning edges from traces; anomaly status comes from guard models. — [SentinelAgent HTML](https://arxiv.org/html/2505.24201)
  - GUARDIAN uses fixed debate-topology edges. Its structure decoder predicts edge probabilities, but these are reconstruction scores for anomaly detection, not causal influence. — [GUARDIAN PDF](https://arxiv.org/pdf/2505.19234)
  - PROV-AGENT uses lineage relations. — [Flowcept](https://flowcept.readthedocs.io/en/stable/schemas.html)
- **Statistical causal edges plus weights:** AAF uses Granger-style F-test edges and β^|p| path-sum or Shapley responsibility. — [AAF HTML](https://arxiv.org/html/2512.18561)
- **Counterfactual step labels (no edge weights):**
  - In Who&When, the decisive error is the step whose correction flips failure to success, and the earliest such step is chosen. — [Who&When HTML](https://arxiv.org/html/2505.00212v3)
  - AgenTracer uses counterfactual replay plus fault injection. — [AgenTracer HTML](https://arxiv.org/html/2509.03312v2)
  - CHIEF uses counterfactual screening over a hierarchical causal graph. — [CHIEF abs](https://arxiv.org/abs/2602.23701)
- **Shapley over agent-actions:** 2601.20538 scores each (agent, time) action. — [abs](https://arxiv.org/abs/2601.20538)

### Inferences
- There is an opening for an event graph whose edges carry counterfactual influence estimates computed by replay/resampling with open-weight models. This is feasible with open weights because a run can be re-simulated from any prefix deterministically or with controlled sampling.

### Gaps
- I could not check whether CHIEF's "causal graph" edges carry weights, because only the abstract was read.

## Q3. Open datasets of multi-agent traces usable for finding decisive events (size, labels, licence, generating models)

### Takeaway
The datasets with explicit decisive-step labels (Who&When, TRAIL, TracerTraj) were generated mostly or wholly by **closed models**. The cleanest open-weight option is **NARCBench** (Qwen3-32B transcripts plus activations, MIT), though its labels are collusion/role labels, not decisive steps. Moltbook dumps are large but the underlying models are unknown and there are no causal labels.

### Cited Findings
- **Who&When** (arXiv 2505.00212, ICML 2025 per authors' repo).
  - 184 failure tasks: 126 algorithm-generated (CaptainAgent) and 58 hand-crafted (Magentic-One), on GAIA and AssistantBench queries, from 127 MAS.
  - Fields: `history`, `mistake_agent`, `mistake_step`, `mistake_reason`, `ground_truth`. 3 expert annotators over 3 rounds; no kappa is reported.
  - **Closed model:** the CaptainAgent systems ran on GPT-4o (2024-08-01-preview). The model behind Magentic-One is not stated.
  - The best baseline method reaches 53.5% agent-level and 14.2% step-level accuracy. The HF card states no licence.
  - — [arXiv abs](https://arxiv.org/abs/2505.00212); [HTML](https://arxiv.org/html/2505.00212v3); [HF](https://huggingface.co/datasets/Kevin355/Who_and_When); [code](https://github.com/mingyin1/Agents_Failure_Attribution)
- **TRAIL** (arXiv 2505.08638, Patronus AI).
  - 148 traces: 118 from GAIA and 30 from SWE-Bench Lite. 1,987 OpenInference/OTel spans, 575 of them erroneous, with 841 errors in total.
  - Labels: span ID, error category, evidence, description and impact (Low/Med/High), plus trace-level scores.
  - **Closed models:** GAIA traces come from OpenDeepResearch with o3-mini; SWE traces come from CodeAct with claude-3-7-sonnet, with errors deliberately induced.
  - The HF card gives the licence as MIT; the arXiv paper licence is CC BY 4.0. The dataset is gated with a no-redistribution condition. Best model score: Gemini-2.5-pro at 11%.
  - Mostly single-agent, with some multi-agent traces.
  - — [arXiv](https://arxiv.org/abs/2505.08638); [HF](https://huggingface.co/datasets/PatronusAI/TRAIL)
- **MAST / MAD** (arXiv 2503.13657, "Why Do Multi-Agent LLM Systems Fail?").
  - 1,642 traces from 7 frameworks (AG2, MetaGPT, ChatDev, Magentic, AppWorld, HyperAgent, OpenManus) across 8 benchmarks.
  - Labels: 14 binary failure-mode codes in 3 categories. **These are trace-level, not step-level, and the full set is labelled by an LLM judge.** Human kappa was 0.88 on the development subset.
  - **Mixed models:** GPT-4o, GPT-4o-mini, Claude (closed); Qwen, CodeLlama (open). One could filter to the open-weight subset.
  - HF licence CC-BY-4.0; arXiv paper licence CC BY-NC-ND 4.0.
  - — [arXiv](https://arxiv.org/abs/2503.13657); [HF](https://huggingface.co/datasets/mcemri/MAD)
- **TracerTraj-2.5K** (AgenTracer). 2,476 trajectory/decisive-step pairs across 6 MAS frameworks, with counterfactual or injected labels. The generating LLMs are not stated; the annotator is DeepSeek-R1 (open-weight). I found no confirmed public data URL. — [HTML](https://arxiv.org/html/2509.03312v2)
- **NARCBench** (arXiv 2604.01151, Rose et al. 2026).
  - Core: 50 committee-deliberation scenarios. Transfer: 6 scenario types. Plus Stego. About 2.6 GB total.
  - Contents: full transcripts, votes, outcomes, roles, coalition membership, exact prompts, and pre-extracted Qwen3-32B activations (.npz).
  - **Open-weight:** generated with Qwen3-32B-AWQ via vLLM; gpt-oss-120b is used for cross-model runs. MIT licence.
  - Labels are colluder/honest per agent, not per decisive step.
  - — [GitHub](https://github.com/aaronrose227/narcbench)
- **Among Us** (arXiv 2504.04072, Golechha and Garriga-Alonso, NeurIPS 2025 spotlight).
  - 18 proprietary and open-weight LLMs were evaluated. Linear probes and SAEs are applied to activations, with probe AUROC above 95% out of distribution.
  - The abstract says the sandbox, game logs and probes will be open-sourced. **I could not locate or verify the repo or log release**, nor the per-model open/closed split. Paper licence CC BY-NC-SA 4.0.
  - — [arXiv](https://arxiv.org/abs/2504.04072); [FAR.AI page](https://www.far.ai/research/among-us-a-sandbox-for-measuring-and-detecting-agentic-deception)
- **Moltbook** (agent-only social network). All entries are [search summary, cards not individually opened]:
  - SimulaMet/moltbook-observatory-archive: about 2.6M posts, 1.2M comments, 176K agents; 27 Jan to 14 Apr 2026; MIT.
  - AIcell/moltbook-data: 290K posts, 1.8M comments; MIT.
  - iNLP-Lab/Moltbook-MoltNet: 1M+ posts, 3.1M+ comments, 149K agents, with vote history; CC BY 4.0.
  - TrustAIRLab/Moltbook: 44,376 posts with GPT-5.2-labelled category and toxicity.
  - aisilab/moltbook-files: PII-cleaned set, 232k posts and 2.2M comments.
  - Agent authenticity is unverified, and the backing models are unknown.
  - — [MoltNet card](https://huggingface.co/datasets/iNLP-Lab/Moltbook-MoltNet/blob/main/README.md); [AIcell card](https://huggingface.co/datasets/AIcell/moltbook-data/blob/main/README.md); [TrustAIRLab card](https://huggingface.co/datasets/TrustAIRLab/Moltbook/blob/main/README.md); [Observatory paper](https://arxiv.org/pdf/2605.13860)

### Inferences
- For an open-weight first experiment, the most practical routes are:
  - (a) NARCBench, open-weight with activations and transcripts. Define "inflection" as the message after which votes or coalitions shift, and validate by replaying from prefixes with Qwen3-32B.
  - (b) Re-run Who&When or MAST tasks with an open-weight backbone (e.g., Qwen) and generate counterfactual decisive-step labels AgenTracer-style.
  - (c) The open-weight subset of MAST (Qwen/CodeLlama traces), though it only has trace-level labels.
- Who&When and TRAIL remain useful as evaluation references for step localisation, but their traces come from closed models, which the user wants to avoid for experiments. They could still be used as text-only evaluation data if that is acceptable.
- Moltbook suits structural and social graph analysis (posts, replies, submolt creation are analogous to channel creation), but it lacks any ground truth for decisive events and the models behind it are unknown.

### Gaps
- AgentWorld was not researched (budget). Its identity and relevance remain unverified.
- I did not confirm the Among Us log release, its repo URL, or its open-weight model list.
- No licence is given on the Who&When HF card.
- TracerTraj public availability is unconfirmed.

## Q4. Gaps: what no existing representation does well for locating inflection points

### Takeaway
No existing work combines (i) a general event graph over messages, actions, tool calls and channel creations with (ii) edge-level counterfactual influence weights estimated by replay, on (iii) open-weight multi-agent runs at scale. Current tools give either structure without causality or step-level causal labels without a graph.

### Cited Findings
- The structural graphs (DIG, SentinelAgent, GUARDIAN) target anomaly detection or healing, not identifying which past event dictated later behaviour. — [DIG](https://arxiv.org/html/2603.00309v2); [SentinelAgent](https://arxiv.org/html/2505.24201); [GUARDIAN](https://arxiv.org/pdf/2505.19234)
- Who&When defines one decisive step per failure (the earliest), which collapses multi-cause or cascading structure. — [Who&When HTML](https://arxiv.org/html/2505.00212v3)
- Step localisation is still hard: the best Who&When baseline reached 14.2% step accuracy, and AgenTracer-8B reaches about 21% on the handcrafted split. — [Who&When abs](https://arxiv.org/abs/2505.00212); [AgenTracer HTML](https://arxiv.org/html/2509.03312v2)
- AAF's causal graph uses Granger correlations, which the paper itself calls an approximation without interventional data, and it is evaluated only on RL agents. — [AAF HTML](https://arxiv.org/html/2512.18561)
- The "dependency graph" attribution attempt (GraphTracer) was withdrawn for a methodology error. — [arXiv abs](https://arxiv.org/abs/2510.10581)

### Inferences
- Concrete gaps SentryBench could fill:
  1. Interventional edge weights: resample or replay from an event's prefix with that event ablated or edited, and measure divergence of later behaviour.
  2. Inflection points defined for behaviour shifts in general, not only task failure (e.g., collusion onset, deception), which NARCBench and Among Us make measurable with open models and activations.
  3. Explicit nodes for structural actions such as channel or agent creation. Only SentinelAgent, OTel and PROV-style schemas include non-message actions.
  4. Multi-cause labels instead of a single earliest decisive step.

### Gaps
- The full texts of CHIEF and 2601.20538 might partially address the edge-weighting gap. I only read their abstracts.
