# Release Intelligence Agent Instructions

This repository implements the reproducible vLLM Release Intelligence and PDF Reporting pipeline requested by the repository owner. The source of truth is the official vLLM GitHub Release API and official documentation URLs in `config/vllm.yaml`.

The `release-report` CLI must fetch, analyze, render, and visually verify both PDF artifacts. Do not treat PDF creation as success unless `release-report verify` passes. Keep factual claims source-linked, separate stable/patch/post/RC releases, use cached raw API data for offline builds, and never persist tokens or sensitive request headers.
