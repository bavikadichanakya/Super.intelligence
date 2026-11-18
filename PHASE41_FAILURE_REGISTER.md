# SUPER.INTELLIGENCEEE — Phase 4.1 Failure Register & Legacy Defect Log
**Document ID:** SEC-P41-FLR-20261107  
**Status:** RECORDED & ACTIVE  
**Updated:** 2026-11-07  

---

## 1. Overview & Policy Compliance

In strict compliance with executive project rules, this register tracks all known defects and legacy test failures across the codebase. No tests have been silently ignored, skipped, or artificially modified to inflate pass rates.

- **Phase 4.1 Regressions Introduced:** 0
- **Phase 4.1 Pipeline Suite Pass Rate:** 100.0% (6/6 passing)
- **Phase 4.0 Intelligence Suite Pass Rate:** 100.0% (10/10 passing)
- **Legacy Test Suite Defect Count:** 5 (preserved verbatim in `tests/test_v2_tech_documentary.py`)

---

## 2. Comprehensive Inventory of Known Failures

The 5 failures in `tests/test_v2_tech_documentary.py` originated during the Phase 3.0 to Phase 3.5 engine refactor when component signatures evolved towards production configurability. They are cataloged below:

```
┌────┬─────────────────────────────────────────────────┬─────────────────┬───────────────────────────────┐
│ ID │ Test Name                                       │ Defect Type     │ Subsystem                     │
├────┼─────────────────────────────────────────────────┼─────────────────┼───────────────────────────────┤
│ 01 │ test_documentary_compositor_dispatch_types      │ TypeError       │ DocumentaryCompositor         │
│ 02 │ test_hud_telemetry_gauges_and_reticles          │ AttributeError  │ HUDTelemetryEngine            │
│ 03 │ test_terminal_animator_frame_rendering          │ TypeError       │ TerminalAnimator              │
│ 04 │ test_terminal_animator_syntax_coloring          │ AttributeError  │ TerminalAnimator              │
│ 05 │ test_vector_diagram_frame_rendering             │ TypeError       │ VectorDiagramEngine           │
└────┴─────────────────────────────────────────────────┴─────────────────┴───────────────────────────────┘
```

---

## 3. Individual Failure Records

### Defect #1: `test_documentary_compositor_dispatch_types`
- **Location:** `tests/test_v2_tech_documentary.py:161`
- **Component:** `creative/tech_documentary/scene_composition/documentary_compositor.py`
- **Invocation:** `compositor = DocumentaryCompositor(output_dir=self.temp_dir)`
- **Exception:** `TypeError: DocumentaryCompositor.__init__() got an unexpected keyword argument 'output_dir'`
- **Analysis:**  
  `DocumentaryCompositor.__init__` was designed to accept `config=None` and resolves output paths via `config.resolve_path("output/drafts/scenes")`. The legacy unit test attempted to pass `output_dir` directly as a parameter.
- **Impact on Production:**  
  None. The production pipeline (`UnifiedProductionPipeline` and `TechDocProducer`) instantiates `DocumentaryCompositor()` without `output_dir` arguments.
- **Scheduled Fix:**  
  Add `output_dir: Optional[Path | str] = None` to `DocumentaryCompositor.__init__` in Phase 4.2.

---

### Defect #2: `test_hud_telemetry_gauges_and_reticles`
- **Location:** `tests/test_v2_tech_documentary.py:114`
- **Component:** `creative/tech_documentary/motion_graphics/hud_telemetry.py`
- **Invocation:** `hud.draw_corner_reticles(draw, (50, 50, 450, 250), color=(0, 210, 255), length=16)`
- **Exception:** `AttributeError: 'HUDTelemetryEngine' object has no attribute 'draw_corner_reticles'`
- **Analysis:**  
  During Phase 3.5, HUDTelemetryEngine was refactored to eliminate low-level primitive calls in favor of composited full-plate renderings (`render_telemetry_plate()`). The helper function `draw_corner_reticles` was privatized/removed.
- **Impact on Production:**  
  None. Production uses `render_scene()` and `render_telemetry_plate()`.
- **Scheduled Fix:**  
  Expose a public backward-compatibility method `draw_corner_reticles()` in `HUDTelemetryEngine` in Phase 4.2.

---

### Defect #3: `test_terminal_animator_frame_rendering`
- **Location:** `tests/test_v2_tech_documentary.py:60`
- **Component:** `creative/tech_documentary/screen_demonstration/terminal_animator.py`
- **Invocation:** `animator.render_frame(..., output_lines=[...])`
- **Exception:** `TypeError: TerminalAnimator.render_frame() got an unexpected keyword argument 'output_lines'`
- **Analysis:**  
  The modern `TerminalAnimator.render_frame()` signature expects `command: str`, `execution_output: Optional[List[str]]`, and `theme: Optional[str]`. The legacy unit test used the parameter name `output_lines`.
- **Impact on Production:**  
  None. Production scene rendering calls `TerminalAnimator.render_terminal_screen()` which uses modern parameter names.
- **Scheduled Fix:**  
  Add `output_lines: Optional[List[str]] = None` keyword alias to `render_frame()` in Phase 4.2.

---

### Defect #4: `test_terminal_animator_syntax_coloring`
- **Location:** `tests/test_v2_tech_documentary.py:76`
- **Component:** `creative/tech_documentary/screen_demonstration/terminal_animator.py`
- **Invocation:** `c_info = animator._get_line_color("[INFO] Ready")`
- **Exception:** `AttributeError: 'TerminalAnimator' object has no attribute '_get_line_color'`
- **Analysis:**  
  Phase 3.5 introduced a token-based lexer (`_tokenize_line_tokens()`) replacing whole-line coloring heuristics. `_get_line_color` was removed as obsolete.
- **Impact on Production:**  
  None. Token-based highlighting functions properly during video generation.
- **Scheduled Fix:**  
  Re-add deprecated `_get_line_color(line: str)` helper to `TerminalAnimator` in Phase 4.2.

---

### Defect #5: `test_vector_diagram_frame_rendering`
- **Location:** `tests/test_v2_tech_documentary.py:96`
- **Component:** `creative/tech_documentary/technical_diagrams/vector_diagram_engine.py`
- **Invocation:** `engine.render_frame(..., stages=stages)`
- **Exception:** `TypeError: VectorDiagramEngine.render_frame() got an unexpected keyword argument 'stages'`
- **Analysis:**  
  `VectorDiagramEngine.render_frame()` was updated to accept `stages_data: Optional[List[Dict]]` or `nodes` and `edges`. The legacy test passed the argument name `stages`.
- **Impact on Production:**  
  None. Diagram scene composition maps data cleanly through `render_vector_diagram_plate()`.
- **Scheduled Fix:**  
  Add `stages: Optional[List[Dict]] = None` keyword alias to `render_frame()` in Phase 4.2.

---

## 4. Failure Register Verification Sign-Off

All 5 defects are completely isolated to legacy unit test signature mismatches in `tests/test_v2_tech_documentary.py`. They do NOT affect the modern unified production pipeline, which executes with 100% test passing and zero runtime errors.
