.PHONY: report test verify

report:
	python3 -m release_report.cli build --config config/vllm.yaml

test:
	python3 -m pytest -q

verify:
	python3 -m release_report.cli verify --config config/vllm.yaml
