# Servco Ontology — Conversational Ledger

A running record of concepts, findings, decisions, and open questions from Roberto's ontology preparation work. Started 2026-08-18. Append as we go.

---

## 1. The Databricks Genie Ontology — conceptual model

**Two-layer architecture:**
- **Human-modeled layer** (Unity Catalog semantics): metric views, domains, Pages — defined, governed, certified.
- **Inferred layer**: snippets Genie One automatically extracts from existing assets and usage (queries, dashboards, Genie Agents), each carrying an authority score.

**Core objects** (per Naveen's framing, confirmed against docs):
- **Domains** — business-aligned organization layer; scoping/browsing mechanism. Pages live inside domains or subdomains. *Domain taxonomy = the permission model* (Pages inherit access from their domain; no per-Page grants).
- **Pages** — governed business concepts and terminology; authoritative source Genie One prioritizes over inferred context, with citation. Beta; UI-authored (Discover) or Genie Code (incl. bulk import from documents with dedup/conflict review). No public API yet. ⚠️ Page data: no CMK support, stored plain text, may replicate globally — no PII/sensitive content.
- **Metric views** — semantic layer for KPIs; SQL-authored UC securable objects. Most engineering-shaped surface today: DDL → git → review → CI.

**OntoRank** arbitrates competing definitions: weights source, author authority, usage frequency, ties to certified assets, freshness. **Certification** is a manual input into this ranking — a key control lever.

**Key implications:**
- Half the ontology learns from usage → *your query exhaust is now semantic input*. Sloppy but popular SQL accrues authority.
- Ontology ranks the most trusted *definition*; it does not verify the *computation* from it is correct. Reconciliation instinct still needed.
- Declarative shift: control what agents *conclude* (definitions + trust signals + graph structure) rather than what they *do* (queries, prompts).

## 2. DDD mapping (Roberto is studying Domain-Driven Design)

| DDD concept | Ontology counterpart |
|---|---|
| Ubiquitous language | Pages |
| Bounded contexts | Domains/subdomains; failures happen at boundaries where terms cross untranslated |
| Entities/aggregates | Metric views (computation + consistency boundary) |
| Core vs. generic subdomains | Which Pages to hand-author vs. bulk-extract |
| Context mapping (partnership, conformist…) | The "who certifies" question, played out in permission grants |

Live example: "TLE" = two different measures (Toyota-official vs. internal engagement proxy) wearing one name — a bounded-context collision the governed definition must resolve explicitly.

*(Terminology note: DDL = Data Definition Language — CREATE/ALTER/GRANT SQL. Not "Domain Design Language," though that's accidentally a good description of the ontology layer.)*

## 3. The sales intelligence skill — findings

- Org-catalog skill, v3.3 (July 2026), single SKILL.md, no author/owner metadata recorded. Prompt-only; entirely Claude-side — Genie never sees it. *(Exported for Roberto 8/18.)*
- **Governance gap flagged:** authoritative definitions with no owner field or changelog convention. Cheap fix: `author`/`owner` frontmatter convention for Servco skills.
- **Key principle: "The presence of the definition testifies to what broke without it."** The skill is a negative image of the endpoint's semantic gaps; every guardrail is a scar with a date on it.
- **Decomposition for migration:**
  - → *Ontology*: stock-type standard (New+Demo), LTV cohort definitions, TLE methodology (with proxy-vs-official distinction), ZIP-to-region crosswalk (as a UC reference table + explanatory Page), "Databricks is system of record."
  - → *Dies with data engineering fixes*: fan-out workarounds (multi-year join splitting) — don't enshrine bug workarounds in the semantic layer.
  - → *Stays in skill*: HST date defaults, dashboard structure, rendering rules, fallback behavior.
- **Discipline:** when a definition migrates into the ontology, delete the corresponding skill instruction — belt-and-suspenders muddies the testimony.
- Reconciliation tab (Databricks primary, Tableau spot-check only) = a manual authority ranking, pre-figuring what certification formalizes. Metric views shrink its job from "definition + computation agreement" to "computation agreement" — smaller surface, same instinct.

## 4. The Lani skill — findings

- Org-catalog skill (May 2026), also single-file, prompt-only. Agent persona for institutional knowledge capture: scheduling, 75-min structured interviews, synthesis, SharePoint filing, coverage reporting.
- **Data 360 domain map** (Customer, Vehicle, Parts, Service, People, Logistics, Finance 360) = *someone's existing draft of Servco's domain taxonomy*. Check alignment/conflict with the sales skill's implicit carving before the taxonomy conversation.
- Interview question bank includes natural bounded-context probes ("what would another department get wrong about this?").
- **SharePoint check (8/18, Roberto's account): the described `/Lani/` structure does not exist anywhere visible** — no KnowledgeBase folders, no CoverageTracker, no session outputs. Either the program never launched, or it lives behind permissions. → *No waiting inventory of validated definitions to promote into Pages.* If Lani spins up, design session-synthesis templates to emit Page-shaped output from the start.
- ⚠️ Flag for enablement program: Lani presents in first person as a colleague; AI-ness should stay unmistakably legible to participants for a trust-dependent program.

## 5. Claude-as-access-point — current audit (8/18)

**Reachable from this harness:** org skill catalog (readable, exportable); Sammy Genie MCP endpoints (question-shaped only); M365 (SharePoint/Outlook/Teams read + write), Slack, QuickBooks, Atlassian, Amperity; web; per-user memory.

**Not reachable:** the ontology's authoring surface. No enumeration of domains, no reading Page definitions, no metric-view DDL inspection, no OntoRank visibility beyond surfaced citations. Claude is a *consumer* of ontology conclusions, enforced at the protocol level.

**The inversion worth teaching:** governed data sits behind the narrowest interface (a question-shaped straw); ungoverned data sits behind the widest (SharePoint firehose). Explains why answers differ between surfaces — key AI-literacy point.

**Watch item:** when Databricks ships programmatic ontology access, which operations it exposes (read/enumerate vs. author vs. certify) determines whether harnesses graduate from client to co-author.

## 6. Strategic threads

- **The harness standoff:** everyone wants to be the surface on top of enterprise ontology; nobody wants to be the client. MCP has become the terrain of that fight (generous server implementations, reluctant clients). The durable asset is likely the governed semantic layer itself — definitions + accrued trust signals — not the harness.
- **Roberto's positioning:** a modest-but-stealthily-powerful runtime that fills gaps in enterprise ontologies (cross-platform reconciliation, transformations between governed definitions). Gap-fillers accumulate the most honest map of where the semantic layer breaks — which is the requirements doc for what to build next. Discipline: pipe stages must be deletable when gaps close (`sed` never tried to become the filesystem).

## 8. Official strategy — Tausif's "Strategic Direction" email (2026-08-12)

From Tausif Islam (Director, Data Visualization, Analytics and Automation) to the data team, CorrDyn + Databricks cc'd. Four pillars; Roberto named lead on 1 and 2.

1. **Genie One as LLM context layer** — common NL entry point spanning the governed catalog, existing governance/permissioning model determines access. *Roberto leads.* First priority: transition Sammy's capabilities from the Genie Agent implementation to Genie One + enterprise Metrics Views; deprecate standalone Genie Agents over time. Roberto also owns the accompanying enablement strategy/roadmap.
2. **Metrics Views as enterprise semantic layer** — define metrics once, reuse consistently; fixes "different numbers for the same metric." *Roberto leads, Iden Watanabe supporting.* Power users/analysts bring forward KPIs and flag inconsistent definitions; data team + business stakeholders + data stewards formalize. Positioned as a *derived product of the 360s* (360s = trusted foundation; built in parallel, no resource conflict).
3. **AI Gateway for MCP connectivity** — current MCP Server implementation acknowledged as proof-of-concept with high admin overhead, "not the architecture for enterprise scale." AI Gateway replaces it, applying existing governance/permissions/SSO; goal is extending governed context into external AI platforms (Claude, ChatGPT). *James Winegar (CorrDyn) driving rollout; Roberto continues user enablement on top once connectivity lands.*
4. **Databricks Apps for citizen development** — learning/enablement platform for now; AppSpaces + Genie App Builder expected to supersede as they mature. Alistair Thrussell (Databricks) training the Digital team + AutoRetail citizen-developer evaluators; Shawn Taras for AppDev alignment.

**Overlaps with this ledger's findings:**
- The Sammy → Genie One transition *is* the sales-skill decomposition (§3), now an assigned deliverable. The skill file = the migration requirements document.
- The "who certifies" question (§7) now has a process sketch: power-user intake → stakeholder/steward formalization. This routes certification intake through Roberto's enablement program — the two workstreams are officially one architecture.
- Sequencing concern resolved in principle: 360s carry the data-engineering prerequisites; metric views derive from them.
- The MCP inversion (§5) is officially acknowledged and slated for replacement via AI Gateway — watch-list item now has an owner (Winegar).
- Lani's Data 360 taxonomy (§4) mirrors the 360 project structure Tausif references — strengthens its status as a live draft of the domain carving.

**Gap flagged:** email is metric-views-first; Pages/Domains/Genie Ontology never mentioned by name. Qualitative semantics (TLE proxy-vs-official, stock-type conventions, terminology) have no explicit charter — scope for Roberto to claim or clarify with Tausif.

**Roberto's position (to raise):** push back on retaining the Sammy branding. In communications for the sections he owns, frame it as: *Sammy was part of the POC; going forward we use Genie One as the Databricks agentic harness for the Servco workspace.* Rationale aligns with the ledger's own discipline — the POC-era artifacts (Genie Agent implementation, admin-heavy MCP server, prompt-side definitions) are all being retired; carrying the brand forward blurs the line the migration is meant to draw. Note this diverges from Tausif's stated intent ("keep the Sammy name and user-facing experience"), so it needs an explicit conversation, not just different wording in Roberto's comms.

## 9. Action items / open questions

- [ ] **Raise Sammy branding position with Tausif** — POC framing vs. his stated brand-continuity intent; needs alignment before Roberto's enablement comms go out.
- [ ] **Claim or clarify ownership of qualitative semantics** (Pages/Domains/terminology) with Tausif — currently uncovered by the four pillars.
- [ ] Draft the Sammy → Genie One migration plan using the sales-skill decomposition (§3) as the requirements doc.
- [ ] Domain taxonomy conversation with Naveen + data governance — *before* any tooling. Inputs: Data 360 map, sales skill's implicit domains, Naveen's "Sales & Revenue" example.
- [ ] Design the power-user KPI intake process (per pillar 2) into the enablement program's power-user tier; define handoff to stakeholders/stewards for formalization. Coordinate with Iden Watanabe.
- [ ] Sequence ontology authoring against the 360 buildouts (identity linkage, de-duplicated fact model). Don't certify definitions over data that fans out.
- [ ] First authoring candidates, in order: stock-type Page (small, testable) → LTV cohort metric views → TLE Page (with proxy landmine defused) → geography reference table + Page.
- [ ] Track AI Gateway rollout (Winegar/CorrDyn) — audit which operations the new MCP surface exposes when it lands (read/enumerate vs. author vs. certify).
- [ ] Confirm with workspace admin who published the sales and Lani skills.
- [ ] Determine Lani program status (never launched vs. permissioned away).
- [ ] Skill hygiene proposals: owner/changelog frontmatter convention; decompose the sales skill per the Agent Skills spec (`references/`, `scripts/`) if it keeps growing.

## 10. Roberto's implementation plan — "Genie One and Metric Views Enablement Strategy" (v. 2026-08-25)

Roberto's proposal covering pillars 1–2 of Tausif's strategy. Rumelt kernel structure; **Jidoka** (quality built into the process) as guiding principle — meaning encoded in the most authoritative native layer, not corrected downstream in prompts/dashboards/apps.

**Operating model (layer → responsibility):** Data 360 models → stable primary tables (analytical contract; changes uncommon; program does NOT reopen data-model design). Metric views → KPI definitions/measures/dimensions/filters. Genie One → common entry point, discovery, governed access. Domains → business-domain boundaries for Data 360 assets. Pages → business-facing curation/navigation of subdomain context. Genie Agents → *bounded analytical configurations* with independent context, trusted assets, monitoring, benchmarks. *(Note: resolves the §8 gap — Domains/Pages now have an explicit charter within Roberto's scope.)*

**Five policies:** load-bearing KPIs first; meaning close to the data (Genie instructions stay concise/behavioral); business ownership paired with technical stewardship; prove quality before scaling; scale by domain via one proving slice.

**Eight-stage lifecycle:** Nominate → Prioritize → Define → Specify expected behavior (representative questions, expected answers, edge cases, failure modes *before* implementation) → Implement → Validate & publish → Evaluate & monitor → Certify/revise/retire.

**Failure triage rule:** metric semantics → fix the metric view; interpretation/source-selection → fix Genie configuration; escalate to primary table only on evidence the data contract itself is defective.

**Branding position (evolved from §8):** accept Sammy as user-facing default but constrain it architecturally (Genie One is the platform, never "Sammy Genie Space"; Sammy names the experience, not the architecture) + empirical exit ramp: if the brand anchors users to the old vehicle-deal agent's narrow capabilities, reposition or transition. Open question 6 puts brand durability formally on the record. → Sharper than blanket pushback: converts the disagreement into a testable hypothesis. *Gap: when/how the brand test runs is undefined — natural home is the proving-slice user review.*

**Key connections to earlier sections:**
- Lifecycle stage 4 = the "testimony" heuristic (§3) operationalized: the sales skill's ⚠️ guardrails are the pre-existing benchmark bank (stock-type = a benchmark question; fan-out patterns = regression tests). Proving-slice before/after test = the "does the ontology carry the weight" experiment.
- Boundaries section ("no parallel semantic registry or custom skills middleware when native primitives suffice") = clean line between Servco role and personal runtime project (§6); burden of proof sits with exhausting native primitives first.
- Tension to pre-empt: Tausif's email says standalone Genie Agents get *deprecated*; the operating model keeps Genie Agents as a permanent layer. Compatible readings (bounded configs *inside* Genie One vs. standalone), but needs one explicit sentence in the doc to close the misreading for the cc list.
- Recommended commitment: name the first proving slice — net new-vehicle units (stock-type KPI), sales domain: known disputes, documented expected behavior, mature model, existing production consumer.

**Doc's open questions mapped to ledger items:** Q4 (certification evidence) + Q5 (cross-domain KPI conflict ownership) sharpen the §7/§9 certification-authority item — note TLE is *already* a cross-context conflict, so Q5 likely bites during the first slice, not later. Q6 (brand durability) formalizes the §9 Sammy item. Q7 (Domains/Pages without making them proving-slice prerequisites) matches the §7 sequencing instinct. Q1–Q3 (instruction precedence, user-scoped vs. shared config, monitoring availability) are new — platform questions for Naveen/Databricks.

### Updated action items (supersedes/extends §9 where noted)

- [ ] Add one clarifying sentence to the doc: Genie Agents = bounded configurations within Genie One, superseding standalone implementations (pre-empts "deprecate" misreading).
- [ ] Define when/how the Sammy brand test runs — proposed: during proving-slice user review, with repositioning criteria agreed in advance. *(Sharpens §9 branding item; the doc's framing replaces blanket pushback.)*
- [ ] Commit to the first proving slice: net new-vehicle units (stock-type KPI), sales domain.
- [ ] Convert sales-skill guardrails into the stage-4 benchmark bank for the first slice.
- [ ] Take Q1–Q3 (workspace vs. agent instruction precedence, shareable config patterns, available monitoring/benchmark data) to Naveen/Databricks.
- [ ] Force early answer on Q5 (cross-domain conflict ownership) — TLE will surface it in slice one.

## 11. Strategy v3 — Genie Agents eliminated; all analytical behavior consolidated into Genie One (2026-08-25)

Roberto revised v2 with tracked changes + comments; Claude produced v3. **Supersedes §10's "Genie Agents as bounded configs inside Genie One" framing and the interim "domain subagents" compromise.**

**Final stance:** Genie Agents are removed from the strategy entirely (per Tausif's direction). All bounded analytical functionality — trusted assets, concise instructions, monitoring, benchmarks — folds into **Genie One itself as the single agent for analysis questions, scoped by domain**. Domain boundaries are context scoping within one agent, not separate agents. No new vocabulary ("subagent" considered and rejected) — avoids maintaining terminology against Databricks' product docs.

**Other v3 changes (from Roberto's tracked changes + comments):**
- "Strategy Kernel" → "Opportunities" (Diagnosis subheading dropped); "Guiding Policy" → "Guiding Strategy"
- Domain assets enumerated: Data 360 primary tables, domain-specific metric views, dashboards, Pages
- **Metric views made explicitly domain-specific** — built domain by domain, scoped to a domain's governed assets, never enterprise-wide in the abstract
- **Lifecycle intake routes through JSM**: nominations enter via the digital department's existing Jira intake (sample: REQ-751) and participate in that prioritization cadence
- Proving slice now six steps (Genie Agent connection step folded into metric-view implementation: "expose it through the domain's Genie One experience")
- Platform owner role merged into Data team role
- Open questions cut from 7 to 2: cross-domain KPI conflict ownership + Domains/Pages sequencing. (The removed platform questions — instruction precedence, config sharing, monitoring — live on in DGTL-14728, reframed in Genie One terms.)

**Jira alignment (same date):** DGTL-14611 epic rewritten to the enablement plan (summary: "Genie One & Metric Views Enablement (Sammy Transition)"); five Feature-level workstreams created under it — DGTL-14725 proving slice, 14726 benchmark bank, 14727 domain taxonomy, 14728 platform validation, 14729 governance. All descriptions now reflect the Genie One consolidation (zero "Genie Agent"/"subagent" references). Note: DGTL project hierarchy is Epic (L2) → Feature (L1) → Story (L0). Flagged for cleanup: POC-era backlog Features "Add Roadster/SFMC/ClarityKit Data to Sammy" (DGTL-14644/45/46) contradict the new model — re-scope or close as superseded.

## 12. Strategy v5–v6 — JSM as system of record; lifecycle split into build + evaluation intake (2026-08-26)

**v5 (from v4 comments):** JSM intake made explicit in two places — the lifecycle intro/close (each KPI's intake request carries it through every stage; JSM request = system of record for progress) and Quality & Evaluation (findings filed as intake requests, triaged in the same queue as nominations). Deliberate wording choice: doc names the process without citing REQ-751 (v4 dropped the sample-ticket reference); Jira keeps the citation since a linked sample earns its place there.

**v6 (clean revision, confirmed with Roberto):**
- **Lifecycle split — the big one.** Build lifecycle is now SIX stages (Nominate → Prioritize → Define → Specify expected behavior → Implement → Validate & publish). Former stages 7–8 (Evaluate & monitor; Certify/revise/retire) become **their own post-publish intake process**. Claude flagged the deletion as possibly accidental (doc's "eight-stage" lead-in and cross-references survived); Roberto confirmed deliberate and fixed the lead-ins himself.
- "First Proving Slice" heading → "First Phase" (body retains proving-slice language)
- Genie One described as "context-layer" — the word **"harness" dropped** from the doc's vocabulary
- "for all users, human or agents" → "for all users across the entire workspace"; "central problem" → "current problem"

**Jira sync to v6 (same date):** Epic approach rewritten around the six-stage build lifecycle + separate evaluation intake. 14725 renamed "First phase: first load-bearing KPI through the build lifecycle." 14726 reframed to serve both pre-publication validation and the post-publish evaluation queue. 14729 gained net-new scope: **design the evaluation intake process itself** (request type, queue, interop with build intake) — the v6 split created this work and nobody had owned it. 14727 cosmetic updates; 14728 untouched. POC-era "Add X Data to Sammy" Features (14644/45/46) still unresolved in the backlog.

**Platform observation — AI Gateway cutover in progress:** The direct Atlassian MCP connector disappeared mid-session (2026-08-26); all Jira reads/writes now route through **Databricks AI Gateway Hawaii Atlassian**, which worked cleanly (get/edit/search, no auth friction). Pillar 3 is live for Atlassian. Partial answer to the 14728 watch item: the gateway's Atlassian surface exposes full issue read/write. Still unknown: what the gateway will expose for the *ontology* surface (read/enumerate vs. author vs. certify). Related earlier finding: a "Databricks MCP Connector Helper" app (databricksapps.com) exists as transition-period scaffolding — connection diagnostics + identity/token checks — a textbook deletable gap-filler once the gateway handles identity federation natively.

---

*Ledger maintained across conversations; append new sections or amend as understanding evolves.*
