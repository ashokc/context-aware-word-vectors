import pytest

from context_aware_word_vectors.context_aware_word_vectors import (
    ContextAwareWordVectors,
)


@pytest.mark.pt
def test_with_pytorch(samples: dict[str, dict[str, str]]) -> None:
    context_aware_word_vectors = ContextAwareWordVectors(model="bert-base-uncased")
    results = context_aware_word_vectors.run(samples)

    for test_word, result in results.items():
        assert result["dot_product"][1] > results["dot_product"][0]
        assert result["dot_product"][1] > results["dot_product"][2]

        for measure in ["euclidean_distance", "manhattan_distance"]:
            assert result[measure][1] < result[measure][0]
            assert result[measure][1] < result[measure][2]


@pytest.mark.tf
def test_with_tensorflow(samples: dict[str, dict[str, str]]) -> None:
    context_aware_word_vectors = ContextAwareWordVectors(
        model="bert-base-uncased", framework="tf"
    )
    results = context_aware_word_vectors.run(samples)

    for test_word, result in results.items():
        assert result["dot_product"][1] > result["dot_product"][0]
        assert result["dot_product"][1] > result["dot_product"][2]

        for measure in ["euclidean_distance", "manhattan_distance"]:
            assert result[measure][1] < result[measure][0]
            assert result[measure][1] < result[measure][2]
