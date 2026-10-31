# Proposed experiment: notification summarization fine-tuning

Status: design only. No training run or improved model is claimed.

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

## Compute decision pending
Local inventory: GTX 1050 Ti, 4 GiB VRAM, approximately 16 GiB system RAM. Select a smaller trainable checkpoint and/or an available cloud GPU after compatibility and memory checks. No paid resource, unattended long training or new model download was started by this design step.
