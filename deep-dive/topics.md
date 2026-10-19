# Deep-Dive Topic Bank

Pull proposals from here (plus live trending searches). Skip anything marked DONE in LOG.md. Each entry: topic — the week's experiment in one line.

## Mechanistic interpretability
- Superposition & sparse autoencoders — train a tiny SAE on a small LM's activations, find interpretable features (Anthropic's "Toy Models of Superposition" + SAE papers)
- Induction heads & in-context learning — reproduce the induction-head phase change in a 2-layer transformer
- Circuit tracing / activation patching — locate the circuit for a simple task (IOI-style) in GPT-2 small with TransformerLens
- Logit lens & tuned lens — track how predictions form layer by layer

## Training dynamics
- Lottery ticket hypothesis — iterative magnitude pruning on a small CNN/transformer, find a winning ticket
- Double descent — sweep model width on a noisy dataset, reproduce the curve
- Edge of stability — track sharpness (top Hessian eigenvalue) during full-batch training
- muP / hyperparameter transfer — verify LR transfer across widths on a toy transformer
- Scaling laws in miniature — fit a loss-vs-compute power law across tiny model sizes
- Loss landscape geometry — mode connectivity: find a low-loss path between two independently trained models

## Architectures
- State space models (Mamba/S4) — implement a minimal selective SSM, race it against attention on long-range tasks
- Mixture of experts — build a small MoE layer, study routing collapse and load balancing
- Linear attention / the kernel view — implement 2–3 linear attention variants, measure the quality/speed trade
- Diffusion models from scratch — DDPM on MNIST/CIFAR, then distill to fewer steps
- Rotary embeddings & length extrapolation — train short, test long; compare RoPE scaling tricks (NTK, YaRN)

## Inference & systems
- Speculative decoding — implement draft-then-verify with two sizes of the same model family, measure real speedup
- KV cache internals — implement paged/quantized KV cache, measure memory vs. quality
- Quantization — GPTQ/AWQ-style weight quantization by hand on a small model, perplexity vs. bits curve
- FlashAttention from first principles — write a tiled attention kernel (Triton), verify IO savings
- Writing a tiny inference engine — greedy/beam/top-p sampling, batching, streaming, from raw weights

## Post-training & RL
- DPO vs. RLHF — derive DPO from the RLHF objective, run DPO on a small model with a toy preference set
- GRPO / RLVR — reinforcement learning on verifiable rewards (math/code) with a small model
- Reward hacking — build a deliberately gameable reward, watch a policy exploit it, then patch it
- Best-of-N & test-time compute — measure how sampling budget trades against model size

## Evaluation & alignment
- LLM-as-judge biases — measure position/length/self-preference bias systematically
- Calibration — reliability diagrams and temperature scaling for an LLM's stated confidence
- Contamination detection — n-gram and embedding-based leak checks on a benchmark

## Classics worth a week
- Variational autoencoders, properly — derive the ELBO, implement, study posterior collapse
- Normalizing flows — RealNVP on 2D toy densities, then images
- Energy-based models — contrastive divergence on toy data; connect to modern diffusion
- Neural ODEs — implement adjoint training, compare to ResNet on a small task
- Information bottleneck — reproduce (and critique) the compression-phase claims on a small net
- Hopfield networks → modern Hopfield → attention — the lineage, with code at each step

## Agents & memory
- Agent memory architectures — build a small memory layer (extraction, consolidation, retrieval) and evaluate it on a long-conversation benchmark
- Planning: tree search + LLMs — implement MCTS/ToT over a toy environment, measure vs. greedy
- World models — train a small world model (RSSM-style) on a gridworld, plan in latent space
- Multi-agent emergence — negotiation or signaling games between LLM agents

## Seeded ideas
(Ideas that came out of past weeks — append here during wrap-up.)
