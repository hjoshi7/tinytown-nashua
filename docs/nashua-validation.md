# Nashua first-pass validation

This record covers the downtown map generated with the unmodified TinyTown renderer from upstream `e7146e2f210d245b5dc952b2f37f267ee20cb68b`.

## Map and build

- Center: 42.7615, -71.4670; requested extent: 1,600 × 1,600 metres.
- 2,253 buildings, 2,190 road/path pieces, 127 areas, and 148 points of interest.
- Actual OpenStreetMap data and a 96 × 96 USGS terrain grid; no substitute town or synthetic source map.
- Rebuilding with `tinytown.site.build(..., write=False)` exactly reproduced the committed scene.
- Scene SHA-256: `632eab1d54600ad81eef40bc3fcbf8c47956f5b2e2d78256c268d90c310c03e3`.
- `./town bake nashua --check`: passed, surfaces current and 287 streaming tiles current.
- `./town stage --target nashua`: passed. Correct Nashua title, site selection, and Nashua preview image; source/reference directories excluded from the staged output.
- Original `src/` and `tinytown/` source files are unchanged from upstream.

## Browser checks on Nashua

Tested in TinyTown's pinned private Chromium at 1440 × 1000 and 390 × 844, using the desktop and mobile quality profiles respectively. Opened the documented streaming link focused on the Nashua Public Library, waited for nearby detail, and checked real browser input.

| Profile | Resident detail tiles | Detail memory / budget | Coarse base + regions | Drag, zoom, day/night |
| --- | ---: | ---: | ---: | --- |
| desktop | 12 | 55.1 / 80 MiB | 62.8 MiB | Passed |
| mobile | 6 | 26.4 / 40 MiB | 35.0 MiB | Passed |

Both profiles rendered with the correct title, loaded nearby detail without reported streaming failures, and had no captured JavaScript exceptions. Screenshots were visually inspected. The README preview is an actual screenshot, not a concept image.

The headless checks took approximately 34 seconds to reach the initial scene while other build/regression work was running. This is not a controlled performance benchmark or a promise about other devices. Detail budgets exclude the coarse map, renderer allocations, decoding buffers, and textures outside that detail accounting.

## Existing regression tests

- Python unit suite: **250 tests passed**, including an explicit Nashua default-route check. The original Avon route assertion is now explicitly scoped to the Avon target.
- Node logic suite: **74 tests passed**.
- The broader upstream `viewer-browser.mjs` suite did **not** finish green. After restoring a missing polygon fixture, its rerun timed out at `checkLighting` with `Timed out: night transition finishes after waking`. That lighting check passed on the earlier run. This is a nondeterministic regression-run result, not a diagnosed or fixed upstream bug. Nashua’s separate desktop/mobile day/night, drag, zoom, and streaming checks passed. No whole-suite success is claimed.
- The sparse checkout initially omitted upstream golden-scene and polygon fixtures. Those files were restored unchanged for regression testing. A full checkout includes them.
- The runtime emits existing Python resource and Node module-type warnings; the renderer was not altered to suppress them.

## Limits and next steps

Buildings use upstream procedural appearances. Photo-informed blueprints have not been authored for Nashua yet. Geographic locations/footprints are grounded in the map, but facade details, inferred heights, trees, and street props are approximations.

Only downtown is generated. City-wide coverage and long-session memory growth have not been validated. Expand the map in measured steps and verify the municipal boundary before claiming entire-city coverage.

The shared streaming base is approximately 3.8 MiB compressed, with 24 landscape regions and 287 detail tiles. Total detailed-tile data is about 130 MiB, loaded selectively. The original-loader fallback surface file is 31,520,376 bytes; check the intended host's individual-file limit before attempting website deployment. This delivery publishes a GitHub repository and local preview, not a hosted public website.
