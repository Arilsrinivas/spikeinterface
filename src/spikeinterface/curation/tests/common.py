from __future__ import annotations

import pytest
from pathlib import Path

from spikeinterface.core import generate_ground_truth_recording, start_sorting_result
from spikeinterface.qualitymetrics import compute_quality_metrics

if hasattr(pytest, "global_test_folder"):
    cache_folder = pytest.global_test_folder / "curation"
else:
    cache_folder = Path("cache_folder") / "curation"


job_kwargs = dict(n_jobs=-1)
def make_sorting_result(sparse=True):
    recording, sorting = generate_ground_truth_recording(
        durations=[300.0],
        sampling_frequency=30000.0,
        num_channels=4,
        num_units=5,
        generate_sorting_kwargs=dict(firing_rates=20.0, refractory_period_ms=4.0),
        noise_kwargs=dict(noise_level=5.0, strategy="on_the_fly"),
        seed=2205,
    )

    sorting_result = start_sorting_result(sorting=sorting, recording=recording, format="memory",  sparse=sparse)
    sorting_result.select_random_spikes()
    sorting_result.compute("waveforms", **job_kwargs)
    sorting_result.compute("templates")
    sorting_result.compute("noise_levels")
    # sorting_result.compute("principal_components")
    # sorting_result.compute("template_similarity")
    # sorting_result.compute("quality_metrics", metric_names=["snr"])

    return sorting_result


@pytest.fixture(scope="module")
def sorting_result_for_curation():
    return make_sorting_result(sparse=True)


if __name__ == "__main__":
    sorting_result = make_sorting_result(sparse=False)
    print(sorting_result)