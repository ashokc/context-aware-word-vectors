from typing import Any

import pytest

from context_aware_word_vectors.context_aware_word_vectors import (
    ContextAwareWordVectors,
    print_results,
)

measures1 = {"dot_product"}
measures2 = {"euclidean_distance", "manhattan_distance"}


def compare_values(results: Any) -> None:
    for test_word, result in results.items():
        for key, values in result.items():
            if key in measures1:
                assert values[1] > values[0], f"{test_word} Failed"
                assert values[1] > values[2], f"{test_word} Failed"

            if key in measures2:
                assert values[1] < values[0], f"{test_word} Failed"
                assert values[1] < values[2], f"{test_word} Failed"


@pytest.mark.all
@pytest.mark.pt
def test_with_pytorch(samples: dict[str, dict[str, str]]) -> None:
    context_aware_word_vectors = ContextAwareWordVectors(model="bert-base-uncased")
    results = context_aware_word_vectors.run(samples)
    compare_values(results)


@pytest.mark.all
@pytest.mark.tf
def test_with_tensorflow(samples: dict[str, dict[str, str]]) -> None:
    context_aware_word_vectors = ContextAwareWordVectors(
        model="bert-base-uncased", framework="tf"
    )
    results = context_aware_word_vectors.run(samples)
    compare_values(results)


@pytest.mark.all
def test_main() -> None:
    print_results()
