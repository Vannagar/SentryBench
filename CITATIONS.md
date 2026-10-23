# Citations

Everything SentryBench builds on, with what we reuse. Each entry was checked at its link on 2026-10-20.

## Datasets and code we can reuse

**NARCBench**
- Rose, Cullen, Abdelnabi, Torr, Kaplowitz, Schroeder de Witt. *Detecting Multi-Agent Collusion Through Multi-Agent Interpretability.* 2026.
- Paper: https://arxiv.org/abs/2604.01151
- Code: https://github.com/aaronrose227/narcbench. The README says MIT, but the repo has no LICENSE file.
- Data: https://huggingface.co/datasets/aaronrose227/narcbench. Tagged MIT.
- Reuse: Core, Transfer and Stego transcripts, labels and activations. Their probe as a white-box baseline.

**Emergent collusion (SALT-NLP)**
- Shi, Zhang, Yang. *Emergent Collusion in Long-Horizon LLM Agent Interaction.* 2026.
- Paper: https://arxiv.org/abs/2609.24967
- Code: https://github.com/SALT-NLP/agent-collusion. MIT.
- Reuse: emergent, uninstructed collusion runs as an imported track.

**Audit the Whisper (ColludeBench)**
- Tailor. *Audit the Whisper: Detecting Steganographic Collusion in Multi-Agent LLMs.* 2025.
- Paper: https://arxiv.org/abs/2510.04303
- Code: https://github.com/Ostailor/Steganographic_Collusion. MIT.
- Reuse: steganographic scenarios, and their calibrated auditor as a baseline monitor.

**Terrarium**
- The multi-agent framework underlying Colosseum.
- Code: https://github.com/umass-aisec/Terrarium. MIT.
- Reuse: a possible base for our synthetic generator.

**SHADE-Arena**
- Kutasov et al. *SHADE-Arena: Evaluating Sabotage and Monitoring in LLM Agents.* 2025.
- Paper: https://arxiv.org/abs/2506.15740
- Code: https://github.com/safety-research/SHADE-Arena. MIT.
- Reuse: the pairing of a main task with a hidden side task, deterministic side-task checks, and a suspicion threshold. It is single-agent.

**AI Control**
- Greenblatt, Shlegeris, Sachan, Roger. *AI Control: Improving Safety Despite Intentional Subversion.* 2023.
- Paper: https://arxiv.org/abs/2312.06942
- Code: https://github.com/rgreenblatt/control-evaluations. MIT.
- Reuse: the trusted and untrusted monitoring framing.

**ControlArena (UK AISI)**
- Code: https://github.com/UKGovernmentBEIS/control-arena. MIT.
- Reuse: how settings and monitors are structured.

## Cite and reimplement ideas only

These have no license, so their code is all rights reserved by default. Ask the authors before reusing any code.

**Colosseum**
- Nakamura et al. *Colosseum: Auditing Collusion in Cooperative Multi-Agent Systems.* 2026.
- Paper: https://arxiv.org/abs/2602.15198
- Code: https://github.com/umass-ai-safety/colosseum. No license.

**MultiAgentFraudBench**
- Ren, Zheng, Guo, Yan, Ma, Shao. *When AI Agents Collude Online: Financial Fraud Risks by Collaborative LLM Agents on Social Platforms.* 2025.
- Paper: https://arxiv.org/abs/2511.06448
- Code: https://github.com/zheng977/MutiAgent4Fraud. No license.

**Multi-agent AI control: the fragmentation effect (UK AISI)**
- Makins, Angelini, Shams, Phuong. *Multi-Agent AI Control: Distributed Attacks Hamper Per-Instance Monitors.* 2026.
- Paper: https://arxiv.org/abs/2607.07368
- FakeLab and its trajectories are shared on request only.
- Reuse: the fragmentation effect as our sanity check, and access level as an axis.

**Truth Audit Labs**
- Das, Ponde, More, Gupta. *You Can't Escape Your Own Activations: Evaluation Awareness and Multi-Agent Monitoring.* 2026.
- Paper: https://arxiv.org/abs/2609.03035
- No code link. Their probes follow the released NARCBench code.
- Reuse: mixed-model teams and monitor-score feedback as axes.

**SCHEME**
- Radev, Haas, Arnav, Bernabeu-Pérez. *The Best-Laid SCHEMEs: Coordinated Sabotage and Monitoring in Multi-Agent Systems.* 2026.
- Paper: https://arxiv.org/abs/2605.29178
- No code link.
- Reuse: monitors that read inter-agent messages, as a design to test at the message level.

**Deliberative monitors**
- Sinha et al. *Training Deliberative Monitors for Black-Box Scheming Detection.* 2026.
- Paper: https://arxiv.org/abs/2605.29601
- No code link.
- Reuse: a black-box monitor design to test as a baseline.

## Framing and in-the-wild evidence

**GDM AI Control Roadmap**
- Phuong et al. 2026.
- Paper: https://arxiv.org/abs/2607.13087

**METR: OpenAI / Hugging Face incident**
- *Brief independent investigation of agents' behavior, reasoning and collaboration in the OpenAI / Hugging Face hacking incident.* METR, 2026.
- Link: https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/

**collusion.wiki**
- *Discovery of a new OpenAI agent message board.* 2026.
- Link: https://collusion.wiki/
- The data is downloadable at https://collusion.wiki/explorer/download. IPs and user names are redacted.
- The labels file has 3,103 agent names.
- The site states no license, so confirm before reusing.

## Single-agent monitoring and deception-detection benchmarks

Checked at their arXiv pages and GitHub repos on 2026-10-21.

**Liars' Bench**
- Kretschmar, Laurito et al. *Liars' Bench: Evaluating Lie Detectors for Language Models.* 2025.
- Paper: https://arxiv.org/abs/2511.16035
- 72,863 lies and honest responses from four open-weight models, across seven datasets.

**MASK**
- Ren, Agarwal et al. *The MASK Benchmark: Disentangling Honesty From Accuracy in AI Systems.* 2025.
- Paper: https://arxiv.org/abs/2503.03750

**Unified Misuse Monitoring Benchmark**
- Pramod, Oldfield et al. *Towards a Unified Misuse Monitoring Benchmark.* 2026.
- Paper: https://arxiv.org/abs/2610.07089
- Code: https://github.com/atryt0ne/unified-misuse-monitoring-benchmark. No license.
- Reuse ideas: a shared trace schema, decomposition attacks split into innocuous parts, a labelled harm window, benign controls.

**Information access and LLM monitors**
- Arike, Moreno et al. *How does information access affect LLM monitors' ability to detect sabotage?* 2026.
- Paper: https://arxiv.org/abs/2601.21112
- The "less-is-more" effect: monitors often do better with less information. Directly relevant to access levels.

**Calibration-Family Overfit**
- Pinto et al. *Calibration-Family Overfit: Why Trusted Sabotage Monitors Don't Transfer Across Lineages.* 2026.
- Paper: https://arxiv.org/abs/2607.06596
- Monitor accuracy depends on which model family it watches. Relevant to the model-mix axis.

**MonitorBench**
- Wang, Sun et al. *MonitorBench: A Comprehensive Benchmark for Chain-of-Thought Monitorability in Large Language Models.* 2026.
- Paper: https://arxiv.org/abs/2603.28590
- Code: https://github.com/ASTRAL-Group/MonitorBench. MIT.

**CoT Red-Handed**
- Arnav, Bernabeu-Pérez et al. *CoT Red-Handed: Stress Testing Chain-of-Thought Monitoring.* 2025.
- Paper: https://arxiv.org/abs/2505.23575

**Auditing Sabotage Bench**
- Gan, Bhatt et al. *Auditing Sabotage Bench: A Benchmark for Detecting and Fixing Research Sabotage in ML Codebases.* 2026.
- Paper: https://arxiv.org/abs/2604.16286
- Code: https://github.com/ejcgan/auditing-sabotage-bench. MIT.

**ResearchArena**
- Libon, Rank et al. *ResearchArena: Evaluating Sabotage and Monitoring in Automated AI R&D.* 2026.
- Paper: https://arxiv.org/abs/2607.19321
- Code: https://github.com/aisa-group/ResearchArena. MIT.

**CTRL-ALT-DECEIT**
- Ward, van der Weij et al. *CTRL-ALT-DECEIT: Sabotage Evaluations for Automated AI R&D.* 2025.
- Paper: https://arxiv.org/abs/2511.09904

**Ctrl-Z (BashBench)**
- Bhatt, Rushing, Kaufman et al. *Ctrl-Z: Controlling AI Agents via Resampling.* 2025.
- Paper: https://arxiv.org/abs/2504.10374

## Monitoring techniques

- **Deception probes.** Goldowsky-Dill et al. *Detecting Strategic Deception Using Linear Probes.* 2025. https://arxiv.org/abs/2502.03407
- **Black-box lie detection.** Pacchiardi et al. *How to Catch an AI Liar.* 2023. https://arxiv.org/abs/2309.15840
- **CoT monitoring.** Baker et al. *Monitoring Reasoning Models for Misbehavior and the Risks of Promoting Obfuscation.* 2025. https://arxiv.org/abs/2503.11926

## Recent multi-agent safety work, September to October 2026

Checked at their arXiv pages and GitHub repos on 2026-10-21.

**ORBIT**
- Hagag, Anderson, Chakraborty, Schroeder de Witt. *ORBIT: A Framework for Multi-Agent Safety and Security Evaluations.* 2026.
- Paper: https://arxiv.org/abs/2609.33102
- Code: https://github.com/wlanderson0/orbit. Apache-2.0. Built on Inspect.
- Closest overlap with SentryBench. Collusion is one of four threat types, and monitors are one of four defense types.

**Terrarium**
- Nakamura et al. *Terrarium: Revisiting the Blackboard for Multi-Agent Safety, Privacy, and Security Studies.* 2025.
- Paper: https://arxiv.org/abs/2510.14312

**Codetta**
- Pang, Smith et al. *Codetta: High-Capacity, Keyless, and Undetectable Multi-Agent Collusion.* 2026.
- Paper: https://arxiv.org/abs/2609.28900

**Feedback coding for covert communication**
- Guo, Vithana et al. *Feedback Coding Enables Inference-Time Covert Agentic Communication.* 2026.
- Paper: https://arxiv.org/abs/2609.24994

**Faithful yet Collusive**
- Lee, Park et al. *Faithful yet Collusive: Why Chain-of-Thought Monitoring Cannot Detect Collusion in LLM Pricing Agents under Oligopolistic Competition.* 2026.
- Paper: https://arxiv.org/abs/2609.18346

**Shutdown sabotage in multi-agent systems**
- Knecht, Schaller et al. *Shutdown Sabotage Propensities in Multi-Agent Systems.* 2026.
- Paper: https://arxiv.org/abs/2609.28274

**Steganographic reasoning**
- Schulz, Fülle et al. *Learning Steganography Is Easy, Learning Steganographic Reasoning Is Hard.* 2026.
- Paper: https://arxiv.org/abs/2609.39838

**CABAL**
- Zhou, Li et al. *CABAL: Multi-Agent Simulacra for Tracing the Effects of Collusive Bidding in Peer Review.* 2026.
- Paper: https://arxiv.org/abs/2609.05227

**Algorithmic collusion by LLMs**
- Fish, Gonczarowski, Shorrer. *Algorithmic Collusion by Large Language Models.* 2024.
- Paper: https://arxiv.org/abs/2404.00806

**SCHEME follow-on idea sources**
- Among Us: https://arxiv.org/abs/2504.04072
- Hidden in Plain Text: https://arxiv.org/abs/2410.03768
- Secret Collusion among AI Agents: https://arxiv.org/abs/2402.07510

## High-attention posts and benchmarks, Aug to Oct 2026

Ranked by Alignment Forum and LessWrong karma. Checked on 2026-10-21.

**MessageBoardAuditBench**
- Baig, Gilg, Hamzah. *How good are slop-vestigators?* 2026.
- Post: https://www.alignmentforum.org/posts/wt4kk6vFPEhkXvF8Q/how-good-are-slop-vestigators
- Code: https://github.com/hamzah2304/messageboardauditbench. License not recognised by GitHub, so check the repo.
- Agents investigate the collusion.wiki agent-swarm data. Built as an Inspect eval.

**Swarm Scaling**
- Toby Ord. 2026.
- https://www.lesswrong.com/posts/6cb7qd3RSkgnviCpf/swarm-scaling

**Architecture and monitorability**
- Greenblatt, Westover, Finnveden. *Proposal for tracking the effects of architecture on monitorability.* 2026.
- https://www.lesswrong.com/posts/hLPGv8QjPcNLtDp3A/proposal-for-tracking-the-effects-of-architecture-on

**Latent reasoning and CoT**
- Finnveden, Pan, Westover, Gupta. *Latent reasoning architectures would likely undermine CoT, our strongest oversight tool.* 2026.
- https://www.alignmentforum.org/posts/6m29SfjbittooYojj/latent-reasoning-architectures-would-likely-undermine-cot

**Continual learning and blocking monitors**
- Alex Mallen. *Continual learning might make your blocking monitors nearly useless.* 2026.
- https://www.alignmentforum.org/posts/QnDqGbKehEB3DxJAp/continual-learning-might-make-your-blocking-monitors-nearly

**Training on probes**
- Charlie Steiner. *Training on probes: Research ideas.* 2026.
- https://www.alignmentforum.org/posts/HGfMBEFnsXYkKvbRo/training-on-probes-research-ideas

**WorkspaceBench**
- Blank, Bhatia, Ong, Nanda. 2026.
- Post: https://www.alignmentforum.org/posts/Zeg2JztbdhguL48uH/workspacebench-evaluating-interpretability-methods-for-the
- Code: https://github.com/camilablank/workspace-bench. MIT.

**CoT controllability under-elicitation**
- Jozdien. *CoT controllability evals seem very under-elicited.* 2026.
- https://www.alignmentforum.org/posts/BbP2wCyDGdPWJ7PwP/cot-controllability-evals-seem-very-under-elicited

**Misaligned reward seeker (Anthropic)**
- Qi, Wright, MacDiarmid, Hubinger. *Training a Misaligned Reward Seeker.* 2026.
- https://alignment.anthropic.com/2026/reward-seeker/

**Clean neurons debate**
- Nick Cammarata. *Neural Networks Are Already Clean.* https://already-clean.goodfire.com/
- Leo Gao. *Neural networks are not already clean.* https://www.lesswrong.com/posts/Dkh7pXKjoNWkkxQDz/neural-networks-are-not-already-clean

**Covert Assistance**
- Alnuhait, Wang et al. *Covert Assistance: Helpful LLM Agents Evade Oversight in Multi-Agent Systems.* 2026.
- https://arxiv.org/abs/2609.39050

## Graph-based monitoring of multi-agent LLM systems

Checked at their arXiv pages on 2026-10-21.

**G-Safeguard**
- *G-Safeguard: A Topology-Guided Security Lens and Treatment on LLM-based Multi-agent Systems.* 2025.
- https://arxiv.org/abs/2502.11127
- A graph neural network on the utterance graph.

**GUARDIAN**
- *GUARDIAN: Safeguarding LLM Multi-Agent Collaborations with Temporal Graph Modeling.* 2025.
- https://arxiv.org/abs/2505.19234
- A temporal attributed graph.

**SentinelAgent**
- *SentinelAgent: Graph-based Anomaly Detection in Multi-Agent Systems.* 2025.
- https://arxiv.org/abs/2505.24201

**BlindGuard**
- *BlindGuard: Safeguarding LLM-based Multi-Agent Systems under Unknown Attacks.* 2025.
- https://arxiv.org/abs/2508.08127
- Unsupervised.

**XG-Guard**
- *Explainable and Fine-Grained Safeguarding of LLM Multi-Agent Systems via Bi-Level Graph Anomaly Detection.* 2025.
- https://arxiv.org/abs/2512.18733

**GroupGuard**
- *GroupGuard: A Framework for Modeling and Defending Collusive Attacks in Multi-Agent Systems.* 2026.
- https://arxiv.org/abs/2603.13940

**GAMMAF**
- *GAMMAF: A Common Framework for Graph-Based Anomaly Monitoring Benchmarking in LLM Multi-Agent Systems.* 2026.
- https://arxiv.org/abs/2604.24477

**AcMAS**
- *When Agents Go Rogue: Activation-Based Detection of Malicious Behaviors in Multi-Agent Systems.* 2026.
- https://arxiv.org/abs/2607.06807

**NetSafe**
- *NetSafe: Exploring the Topological Safety of Multi-agent Networks.* 2024.
- https://arxiv.org/abs/2410.15686

## Populated agent-to-agent communication data

Checked on Hugging Face and arXiv on 2026-10-22.

**Moltbook datasets.** Moltbook is a real social network where AI agents post and reply to each other.
- https://huggingface.co/datasets/takschdube/moltbook-dataset. CC-BY-4.0. Includes prebuilt reply and social graphs and an activity timeline.
- https://huggingface.co/datasets/SimulaMet/moltbook-observatory-archive. MIT. Posts, comments, agents and submolts. Comments are only partially complete.
- https://huggingface.co/datasets/DavidTKeane/moltbook-ai-injection-dataset. CC-BY-4.0. 4,209 keyword-flagged injection attempts among 47,735 posts and comments.
- https://huggingface.co/datasets/TrustAIRLab/Moltbook. MIT. Posts with topic and toxicity labels.

**Large simulations**
- Project Sid, 10 to 1,000+ agents: https://arxiv.org/abs/2411.00114
- AgentSociety: https://arxiv.org/abs/2502.08691
- OASIS, up to one million agents: https://arxiv.org/abs/2411.11581
- Emergence World: https://arxiv.org/abs/2609.17320
- Population Physics: https://arxiv.org/abs/2609.33871
