# Protocol: notification summarization fine-tuning

Status: pilot training completed on a free Colab Tesla T4. See the
[results](finetuning-results.md). No general quality improvement is claimed.

## Research question
Does supervised fine-tuning with LoRA improve concise Portuguese notification summaries compared with the same pretrained checkpoint and prompt, without increasing unsupported facts?

## Data
Use phbg/smart-notifications-synthetic with a recorded immutable Hub revision. Preserve existing train/validation/test separation. Because procedural templates can cross these splits, add an independently authored challenge set with held-out scenarios and wording, reviewed by the project author, before selecting a model. Do not use challenge outcomes for prompt or hyperparameter tuning. Record provenance and rights; omit private notifications.

## Experiment arms
1. Pretrained checkpoint with the existing task prompt.
2. The same checkpoint with the task prompt plus a trained LoRA adapter.
Keep generation settings, input limits and evaluation examples identical. Record model revision, tokenizer, chat template, training seed, package versions, GPU and peak memory. Check compatibility and one training step before a complete run. Use the original trainable checkpoint, not the Android .litertlm binary.

## Evaluation
Report target-word-limit compliance; preservation of current entities, dates and deadlines; incorrect use of superseded facts; unsupported factual additions; and empty/truncated output. Combine deterministic checks with blinded human review of semantic correctness. Report sample counts and uncertainty; ROUGE alone is insufficient. Compare latency/memory under the same runtime, excluding loading from inference timing. A decrease in training loss alone is not evidence of better summaries.

## Publication
Publish the trained adapter, adapter config, base-model revision, training script/config, dataset revision, evaluation protocol and results, including negative results. Label it as supervised fine-tuning of the named upstream model, not a foundation model trained from scratch. A failed quality comparison can still document a real experiment, but must not be marketed as an improvement.

## Android deployment is a separate gate
Merge/convert/quantize only through a supported architecture/export path. Repeat quality and device tests after conversion; do not replace the working PoC model merely because training completed. Compatibility with LiteRT-LM 0.17.0 must be verified rather than assumed.

## Compute decision
Local inventory: GTX 1050 Ti, 4 GiB VRAM, approximately 16 GiB system RAM. The pilot therefore used `google/gemma-3-1b-it` with QLoRA on a free Colab Tesla T4. No paid compute was used. The execution ran for 64 steps and exported the adapter, configuration and before/after generations.
