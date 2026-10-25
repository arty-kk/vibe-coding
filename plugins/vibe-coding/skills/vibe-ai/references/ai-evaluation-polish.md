# Improve AI Evaluation

## Operation

Implement the requested change and verify its directly affected behavior.

## Goal

Improve evaluation of the selected AI behavior with valid datasets, calibrated scoring and interpretable release criteria.

## Domain rules

- Fix task and data validity before adding more metrics or model-judge complexity.
- Version dataset, preprocessing, prompts, model/settings, scorers, rubrics, thresholds, and reports as one evaluation lineage.
- Use deterministic checks for verifiable properties and calibrated human/judge scoring only for genuinely semantic properties.
- Add risk slices and regression cases from real failure modes while keeping a protected release set separate from iterative development.
- Make the release gate interpretable: name blocking failures, uncertainty, allowed variance, and override owner.

## Validation

- Re-run the same versioned evaluation and verify reproducibility or report measured stochastic variance.
- Validate scorer/judge behavior against labelled cases and report disagreement by slice/failure class.
- Run paired baseline/candidate comparison with uncertainty, latency, cost, and safety evidence; list private/online gates separately.

Start with labelled examples on which the existing scorer/judge disagrees with the accepted decision contract. Repair the dataset/scoring boundary, test known acceptable and unacceptable outputs, then rerun a fixed paired candidate/baseline set. Keep training/tuning data separate from release evidence. If a required slice still fails, correct that owner or retain the gate; once the selected evaluation contract is supported, finish Patch Checking.
