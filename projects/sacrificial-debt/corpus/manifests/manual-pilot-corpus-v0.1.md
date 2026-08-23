# Sacrificial Debt Manual Pilot Corpus v0.1

Status: proposed pilot scope for Milestone 1 / issue #1  
Date: 2026-08-21  
Authority: `docs/design/source/FSPP_Sacrificial_Debt_Research_Program_Prospectus_v0.2.txt`

This manifest defines the first bounded source universe for the Sacrificial
Debt manual pilot. It does not create canonical source records and it does not
authorize ingestion of restricted or copyrighted source text into the public
repository.

## Pilot Shape

The pilot is Germany-first. Germany is the mechanism-discovery case; Britain,
Australia, and France remain required contrast cases, but their matched samples
are deferred until the German source families demonstrate that the mechanism can
be coded without concept inflation.

This sequencing follows the prospectus phase order:

- Phase 2: German pilot.
- Phase 3: contrast-case pilot.

The Germany-first pilot must not become a Koenigsberg confirmation exercise. It
must test whether Koenigsberg's Hitler-centered observation is isolated,
overweighted, contradicted, or only one part of a broader institutional and
comparative pattern.

## Anti-Confirmation Controls

The pilot must preserve these controls before any annotation packet is treated
as reference evidence:

- Koenigsberg-derived Hitler passages are capped as one source family, not the
  organizing spine of the corpus.
- Each confirming source family requires paired negative-evidence, rival, or
  contradiction targets.
- Jewish veteran and Jewish organizational sources are required, not optional,
  because they test whether demonstrated sacrifice could discharge accusation.
- Judenzaehlung materials must include both allegations of Jewish shirking and
  evidence contradicting those allegations.
- Nazi leadership and propaganda sources must be separated by actor and domain;
  Hitler rhetoric cannot stand in for Goebbels, Himmler/SS, institutional
  practice, public reception, or policy.
- Generic antisemitism, racial ideology, casualty rhetoric, or sacrifice praise
  must not be promoted to sacrificial-debt evidence unless the minimum evidence
  rule is met.
- At least one pilot finding must weaken, revise, or reject a hypothesis before
  expansion. If all hypotheses appear confirmed, the coding rules are too
  permissive.

## Tier Policy

| Tier | Pilot use | Publication implication |
|---|---|---|
| Tier 1 — Core interpretive | Small Germany mechanism-discovery sample, fully provenance-reviewed and manually coded. | Eligible for strongest claims only after review, observation lock, and reliability checks. |
| Tier 2 — Validation | Later matched contrast samples and robustness samples. | Supports recurrence, variation, and negative findings, not strongest causal claims alone. |
| Tier 3 — Search/reference | Bibliographic leads, concordance candidates, source-family inventories, literature pointers. | A hit is a lead, not coded evidence. |

## Germany Pilot Source Families

Target passage counts are planning ranges from the prospectus. They describe the
eventual manual coding target, not the number of source records required in the
first provenance seed.

| Family ID | Source family | Target passages | Initial tier | Function | Inclusion requirement | Bias control |
|---|---:|---:|---|---|---|---|
| SD-GER-HITLER | Hitler writings, speeches, proclamations, wartime statements, political testaments, and source-critical conversation records | 20-30 | Tier 1 after provenance review | Test whether reciprocal moral accounting is recurrent or isolated in Hitler's political imagination. | Must span WWI recollection, sacrifice/Volksgemeinschaft language, anti-Jewish framing, and wartime radicalization where source reliability allows. | Capped as one family; cannot define the mechanism by itself. |
| SD-GER-JUDENZAEHLUNG | Judenzaehlung records, Reichstag/War Ministry debate, press/public allegations, and Jewish organizational responses | 15-20 | Tier 1 after provenance review | Test group-specific accusation of shirking and whether counterevidence was available. | Must include allegation records and contradiction/response records. | Required disconfirmation path for non-dischargeability and essentialization hypotheses. |
| SD-GER-JEWISH-VETERANS | Jewish veteran diaries, petitions, letters, memoirs, organizational records, and later persecution-status materials | 15-20 | Tier 1 after provenance review | Test whether demonstrated service could discharge accusation. | Must preserve Jewish actor perspective and service/belonging claims where sources permit. | Prevents reproducing perpetrator symbolic logic as total historical reality. |
| SD-GER-GOEBBELS | Goebbels diaries, speeches, newspaper articles, and total-war propaganda | 15-20 | Tier 1 or Tier 2 depending on source form | Test whether sacrifice/debt framing appears beyond Hitler and in propaganda/reception-oriented domains. | Must keep diary, speech, and press genres distinct. | Cannot be read as policy causation without separate evidence. |
| SD-GER-HIMMLER-SS | Himmler and SS speeches, ideological training, policy communications, and leadership statements | 10-15 | Tier 1 or Tier 2 depending on source form | Test links among German sacrifice, racial hierarchy, duty, destruction, and institutional collection. | Must distinguish ideological rhetoric from operational policy records. | Guards against treating violent policy severity as sacrificial-debt framing. |
| SD-GER-VETERANS-MEMORY | Veterans' associations, paramilitary organizations, memorial speeches, war monuments, commemorative publications | 10-15 | Tier 2 initially | Test failed sacrifice, memorialization, creditor constituencies, and postwar claims on the living. | Must include actor/audience/date metadata. | Checks whether sacrificial accounting is broader than Hitler but not automatically Nazi policy. |
| SD-GER-SOLDIER-HOMEFRONT | Soldiers' letters/diaries and home-front discourse comparing front suffering with spared, safe, profiteering, or shirking populations | 10-15 | Tier 2 initially | Test whether "our suffering/their survival" comparisons circulated outside elite statements. | Must preserve provenance, audience, and publication/editing status. | Prevents overreliance on elite/published rhetoric. |
| SD-GER-RIVALS-NEGATIVE | Sources supporting rival explanations or weakening sacrificial-debt hypotheses | Minimum 10 records/leads | Tier 1-3 depending on source | Maintain falsification as a corpus requirement, not an afterthought. | Must map to F1-F7 or a named rival explanation. | Mandatory before expansion or public claims. |

## Named Starting Leads

These are leads from the prospectus and design source map. They require
bibliographic verification before canonical source records are created.

| Lead ID | Candidate source or literature lead | Family | Planned use | Required verification before source record |
|---|---|---|---|---|
| LEAD-HITLER-MEIN-KAMPF | Adolf Hitler, `Mein Kampf` | SD-GER-HITLER | WWI recollection, sacrifice, nation/race, and alleged Jewish self-preservation claims. | Edition, translator if any, publication date, copyright/redistribution status, canonical coordinates. |
| LEAD-HITLER-SPEECHES | Hitler speeches/proclamations and wartime statements | SD-GER-HITLER | Test recurrence across time and audience. | Reliable edition/archive, date, audience, language, source criticism. |
| LEAD-KOENIGSBERG-SMH | Richard A. Koenigsberg, "The Sacrificial Meaning of the Holocaust" | SD-GER-HITLER / SD-GER-RIVALS-NEGATIVE | Generative observation and hypothesis source, not primary evidence for actor claims. | Publication venue/version, rights, exact quoted source coordinates, distinction between Koenigsberg interpretation and primary-source evidence. |
| LEAD-GEHERAN-COMRADES | Michael Geheran, `Comrades Betrayed` | SD-GER-JEWISH-VETERANS | Secondary guide to Jewish WWI veterans and non-dischargeability tests. | Edition, citation metadata, candidate primary sources referenced. |
| LEAD-GEHERAN-JUDENZAEHLUNG | Michael Geheran, "Judenzaehlung (Jewish Census)," 1914-1918-online | SD-GER-JUDENZAEHLUNG | Orientation to allegation/counterevidence context. | Stable URL, license, citation metadata, linked primary-source leads. |
| LEAD-GOEBBELS-DIARIES | Goebbels diaries and selected speeches/articles | SD-GER-GOEBBELS | Actor comparison beyond Hitler. | Edition, date coverage, translator/editor, rights, genre separation. |
| LEAD-HIMMLER-SPEECHES | Himmler/SS leadership speeches and training materials | SD-GER-HIMMLER-SS | Institutional/ideological comparison. | Archive/edition, audience, date, reliability, policy-vs-rhetoric domain. |
| LEAD-MOSSE-FALLEN | George L. Mosse, `Fallen Soldiers` | SD-GER-VETERANS-MEMORY / rivals | Context for cult of fallen soldiers and memorialization. | Edition and citation metadata; candidate primary-source leads. |
| LEAD-FRIEDLANDER | Saul Friedlaender, `Nazi Germany and the Jews` | SD-GER-RIVALS-NEGATIVE | Rival/neighboring redemptive antisemitism and historiographical guardrails. | Edition and cited primary-source leads. |
| LEAD-BARTOV | Omer Bartov works on the Eastern Front, brutalization, and Nazi violence | SD-GER-RIVALS-NEGATIVE | Rival explanations and scope limits. | Edition and exact relevance to rival explanation records. |
| LEAD-KERSHAW | Ian Kershaw Hitler biographies | SD-GER-HITLER / rivals | Hitler chronology, radicalization, and source-critical guidance. | Edition and primary-source coordinates. |
| LEAD-GERWARTH | Robert Gerwarth, `The Vanquished` | SD-GER-VETERANS-MEMORY / rivals | Failed sacrifice, postwar violence, and defeat context. | Edition and primary-source leads. |

## Deferred Contrast-Case Families

The contrast cases are required for the research program but deferred from full
item selection until the German pilot answers whether the codebook can identify
mechanism modules without stretching.

| Case | Deferred family | Prospectus target | Purpose when activated | Gate before activation |
|---|---|---:|---|---|
| Britain | White-feather, shirker, conscientious-objector, and burden-sharing materials | 15-20 passages | Test individualized stigma and social coercion without fixed group debt. | German pilot can distinguish asymmetry, debt, and essentialization. |
| Australia | Conscription referendum and equality-of-sacrifice rhetoric | 15-20 passages | Clean contrast for explicit reciprocal burden-sharing language. | Codebook can separate debt language from ordinary patriotic obligation. |
| France | Blood-tax, embusque, war-industry exemption, and profiteer discourse | 15-20 passages | Test republican burden-sharing and resentment without the same racialized non-dischargeable debt pathway. | German pilot includes enough negative/rival evidence to avoid teleology. |

## Exclusions and Deferrals

- Ottoman, Italian, Japanese, Russian, and later civil-war/ethnic-conflict cases
  are explicitly deferred.
- Large-scale NLP, embeddings, frequency analysis, and model extraction are
  excluded until manual coding and reliability gates are met.
- Raw source text is excluded from this public repository unless rights review
  permits redistribution.
- Secondary literature may guide source discovery and rival explanations, but
  actor claims must resolve to primary-source coordinates before annotation.

## Go / No-Go Questions Before Expansion

The pilot may proceed to contrast-case item selection only after answering:

1. Can coders distinguish sacrificial debt from generic hostility, sacrifice
   praise, racial ideology, revenge, and distributive resentment?
2. Does the Germany sample contain repeated evidence of reciprocal moral
   accounting, or only isolated Koenigsberg-centered passages?
3. Do Jewish military service and Jewish organizational response materials
   provide a real test of dischargeability?
4. Does at least one F1-F7 falsification path weaken, revise, or reject a
   hypothesis?
5. Are Britain, Australia, and France still the right contrast functions after
   the German pilot, or should case selection be narrowed/revised?

## Follow-Up Issues

- Issue #2 locks the codebook v0.1 against this bounded pilot.
- Issue #3 creates seed source/provenance records from this manifest after
  bibliographic and rights verification.
- Issue #4 proves stable document/segment IDs on a tiny fixture subset.
- Issue #5 creates the first manual reference annotation packet only after
  source and segment records exist.

