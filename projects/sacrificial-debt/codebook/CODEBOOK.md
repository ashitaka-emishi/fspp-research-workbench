# Sacrificial Debt Codebook v0.1.0

Status: controlled manual-pilot codebook.

This codebook defines the first stable coding rules for the Sacrificial Debt
manual pilot. It is locked for pilot annotation and validation, but it is not a
claim release, source approval, or finding about any historical case.

Do not expand categories because a model suggests them. Record proposed changes
in `DECISION_LOG.md`, preserve released identifiers, and version the codebook
before changing schema semantics or published record meaning.

## Scope

v0.1.0 covers the first manual pilot only:

- proposition-level annotation;
- observation before interpretation;
- the minimum debt evidence rule;
- emic, etic, mixed, and absent debt states;
- evidence strength;
- rhetoric, reception, and policy domain separation;
- rival explanations and negative evidence.

The Germany-first pilot is a mechanism-discovery sequence. It must not privilege
Koenigsberg-derived interpretation as a conclusion to be re-proved. Germany
annotations require the same source-coordinate, rival-explanation, and negative
evidence discipline as every future comparison case.

## Unit

The principal interpretive unit is the **proposition**.

A proposition may occupy part of a sentence, one sentence, or multiple
sentences, but it must resolve to exact stable source coordinates. A proposition
is not valid pilot evidence if it cannot be traced to a source, document,
segment, and recorded coordinates.

Do not treat whole documents, search hits, summaries, or model outputs as coded
propositions.

## Annotation State Order

Annotations move through a state machine:

1. `observation_draft`
2. `observation_reviewed`
3. `observation_locked`
4. `interpretation_draft`
5. `reference_reviewed`
6. `released`

Interpretive fields are forbidden before observation lock. Reference evidence
must not be promoted from observation to interpretation merely because the
proposition appears rhetorically important, appears in a canonical author, or
matches an expected theory pattern.

## Identification Layer

Code observable structure first:

- `collective_object`: the collective entity or identity at stake;
- `sacrificer_ids`: actors represented as sacrificing;
- `sacrifice_types`: sacrifice forms using the controlled vocabulary;
- `alleged_survivor_ids`: actors represented as spared, surviving, benefiting,
  or contributing less;
- `explicit_comparison`: `yes`, `no`, or `uncertain`;
- `moral_value_sacrifice`: textual values attached to sacrifice;
- `moral_value_survival`: textual values attached to survival, exemption, or
  lower contribution;
- `actor_ids`: speaker, writer, institution, or attributed actor;
- `audience`: addressed or implied audience when known;
- `date`: date or best supported date when known.

Identification may record asymmetry-relevant structure, but it does not by
itself establish Sacrificial Debt.

## Interpretation Layer

Interpret only after observation lock:

- sacrificial asymmetry;
- creditor and debtor actors;
- reciprocal obligation;
- debt status;
- debt and repayment language;
- equalization claim;
- essentialization status;
- dischargeability;
- sanction types;
- causal role;
- rival explanations;
- evidence strength.

Interpretation must remain reversible through review and adjudication. If a
field cannot be coded without changing the theory, stop and record the issue in
the decision log or a follow-up schema issue.

## Minimum Debt Evidence Rule

Code **strong** Sacrificial Debt evidence only when all three elements are
present:

A. identifiable prior or ongoing sacrifice;
B. explicit comparison with a less-sacrificing, spared, or benefiting actor;
C. normative implication that the second actor therefore owes, deserves less,
must contribute, must repay, or may legitimately be sanctioned.

Without C, evidence may support sacrificial asymmetry but not debt.

Do not infer debt merely from:

- hostility;
- casualties;
- persecution;
- generic sacrifice praise;
- resentment of nonparticipants;
- coercive severity;
- antisemitism or other prejudice without reciprocal-obligation logic;
- policy outcome without debt-framed evidence.

## Debt Status

Use these states:

- `absent`: no coded debt relation;
- `emic`: actors explicitly articulate owing, payment, balance, repayment,
  reciprocal obligation, deserved loss, or a close equivalent;
- `etic`: the researcher reconstructs creditor/debtor logic without explicit
  debt language;
- `mixed`: both explicit actor language and reconstructed logic are present.

Never treat emic and etic evidence as evidentially identical. Etic-only evidence
may be coded for pilot analysis when A+B+C are satisfied, but whether etic-only
chains can support strong published claims remains provisional and requires
human review before release.

## Evidence Strength

Use evidence strength conservatively:

- `weak`: relevant but incomplete, ambiguous, or useful mainly as a lead;
- `moderate`: supports a coded relation but lacks one or more conditions for
  strong debt evidence;
- `strong`: satisfies the A+B+C rule and is source-coordinate traceable;
- `decisive_for_mechanism`: reserved for reviewed evidence chains, not a single
  annotation by convenience.

`decisive_for_mechanism` is not a model confidence score. It requires human
review of support, contradiction, chronology, and rival explanations.

Human review is a quality-control gate, not an evidence-strength level by
itself. Review status records whether a qualified person has checked the
annotation, evidence chain, or claim. `decisive_for_mechanism` records the
evidentiary consequence after that review: the evidence is strong enough, in
context, to materially confirm, reject, narrow, or revise a mechanism claim.

## Evidence Domains

Keep evidence domains separate:

- `rhetoric`: claims, framing, propaganda, speeches, writing, imagery, or other
  ideological production;
- `reception`: audience uptake, circulation, response, adoption, resistance, or
  documented interpretation;
- `policy`: institutional process, administrative decision, law, enforcement,
  command structure, or implementation record.

Evidence in one domain does not automatically establish another. Rhetoric alone
does not prove reception. Rhetoric or reception alone does not prove policy
causation.

## Mechanism Components

The provisional mechanism remains a sequence to test, not a universal law:

- A: sacrificial mobilization;
- B: asymmetry and moral comparison;
- C: essentialization and political activation;
- D: coercive equalization and closure.

Cases may stall, branch, reverse, or fail to exhibit modules. Absence,
contradiction, and rival explanations are valid pilot outcomes.

## Negative Evidence and Rival Explanations

Negative evidence is first-class evidence. Record it when the source weakens,
qualifies, or contradicts the mechanism, including:

- successful discharge;
- veteran protection;
- contribution reclassification;
- expected rhetoric absent;
- coercion without debt;
- debt without coercion;
- explicit rejection;
- chronology contradiction;
- actor inconsistency;
- other documented counterevidence.

Absence claims require a documented search scope. "I did not find it" is not a
valid absence claim.

Rival explanations must remain available to the evidence chain and claim audit.
They are not footnotes to be removed after confirming evidence is found.

## Disqualification Rules

Do not code a proposition as strong Sacrificial Debt evidence when:

- the proposition lacks an identifiable sacrifice;
- the comparison is implicit, absent, or uncertain;
- the source lacks reciprocal-obligation, repayment, desert, contribution, or
  sanction logic;
- the proposition only records violence, prejudice, hatred, or coercion;
- the evidence comes from a Tier 3 lead without qualifying annotation and
  review;
- the inference depends on unstated researcher assumptions;
- source coordinates or provenance are missing.

## Historical Sensitivity

Perpetrator rhetoric is historical evidence, not moral endorsement. Do not
represent victims of violence as voluntary sacrificial participants. Do not
equate combat death with genocide. Do not turn Sacrificial Debt into a total
explanation of the Holocaust or of political violence.

Quotations and translated evidence must preserve provenance, context, and
original-language text when available.

## Provisional Items

The following remain provisional after v0.1.0 and require follow-up decisions:

- reliability thresholds for field-level publication readiness;
- whether strong etic-only evidence can support a published claim;
- the approval rule for `decisive_for_mechanism`;
- reception-evidence minimums by case and source family;
- policy-causation minimums beyond the current domain-separation rule;
- translation authority and display policy;
- source storage and external model-processing policy.
