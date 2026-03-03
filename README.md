# RaceTrac Agent Demo Bundle

This repository is a Databricks Asset Bundle that demonstrates multiple agent bricks for a RaceTrac-focused demo:

- Knowledge Assistant (RAG-style pump operations and maintenance enablement)
- Information Extraction (pump incident and breakdown signal extraction)
- Genie-style NL-to-SQL query generation for pump maintenance and fuel pricing
- Supervisor orchestration across all pump-focused bricks

The default Unity Catalog targets are:

- Catalog: `reggie_pierce`
- Schema: `racetrac_agent_demo`

## Repository Layout

- `databricks.yml`: bundle configuration and targets
- `resources/`: bundle resources (schemas and demo job workflow)
- `packages/common`: shared code and demo data generation helpers
- `packages/knowledge_assistant`: RAG-style retrieval brick
- `packages/info_extractor`: unstructured text to structured signal brick
- `packages/genie_space`: natural-language to SQL brick
- `packages/genie_space/src/genie_space/provisioning.py`: Genie space setup payload helper
- `packages/supervisor`: orchestration brick that composes outputs
- `packages/notebooks/notebooks`: demo notebooks and dummy data setup

## Demo Story (meeting aligned)

Recommended sequence for live demo:

1. Run `00_setup_catalog_schema.py` and `01_generate_dummy_data.py`
2. Lead with `02_demo_knowledge_assistant.py` (developer-team first)
3. Run `04_prepare_genie_views.py` to build `ai_forecast` Genie views
4. Pivot to `04_demo_genie_space.py` for operations and BI stakeholders
5. Close with `05_demo_supervisor.py` showing multi-brick orchestration

## Bundle Commands

Validate:

```bash
databricks bundle validate
```

Deploy:

```bash
databricks bundle deploy -t dev
```

Populate dummy data only:

```bash
databricks bundle run racetrac_dummy_data_prep -t dev
```

Run full demo workflow job:

```bash
databricks bundle run racetrac_agent_bricks_demo -t dev
```

## Pixi Tasks

Deploy bundle:

```bash
pixi run bundle-deploy
```

Deploy bundle and ensure dummy data is prepared first:

```bash
pixi run bundle-deploy-with-dummy-data
```

Run full demo with dummy data prep:

```bash
pixi run bundle-run-demo
```
