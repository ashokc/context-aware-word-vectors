import json
from typing import Any, Union

import numpy as np
from transformers import AutoTokenizer, pipeline

__all__ = ["ContextAwareWordVectors"]


class NumpyFloatValuesEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, np.float32):
            return round(float(obj), 3)
        return json.JSONEncoder.default(self, obj)


class ContextAwareWordVectors:
    def __init__(self, model: str, framework: str = "tf") -> None:
        self.framework = framework
        self.model = model
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.feature_extractor = pipeline(
            model=model,
            framework=framework,
            tokenizer=self.tokenizer,
            task="feature-extraction",
        )

    def dot_product(self, v1: Any, v2: Any) -> Any:
        return round(np.dot(v1, v2), 3)

    def euclidean_distance(self, v1: Any, v2: Any) -> Any:
        return round(np.linalg.norm(v1 - v2), 3)

    def manhattan_distance(self, v1: Any, v2: Any) -> Any:
        return round(np.linalg.norm(v1 - v2, ord=1), 3)

    def run(
        self, samples: dict[str, dict[str, str]]
    ) -> dict[str, dict[str, Union[str, list[float]]]]:
        test_word_vector: dict[str, list[float]]
        results: dict[str, dict[str, Union[str, list[float]]]] = {}

        for test_word, sample in samples.items():
            results[test_word] = {}
            results["sentences"] = sample
            test_word_vector = {}
            for index, sentence in sample.items():
                tokens = self.tokenizer.tokenize(sentence)
                vectors = self.feature_extractor(sentence, return_tensors=True).numpy()
                test_word_location = [
                    i for i in range(len(tokens)) if test_word == tokens[i]
                ][0]
                test_word_vector[index] = vectors[
                    0, test_word_location + 1, :
                ]  # 0 is '[CLS]'
                magnitude = np.linalg.norm(test_word_vector[index])
                test_word_vector[index] = test_word_vector[index] / magnitude
            results[test_word]["dot_product"] = [
                self.dot_product(test_word_vector["1"], test_word_vector["2"]),
                self.dot_product(test_word_vector["2"], test_word_vector["3"]),
                self.dot_product(test_word_vector["3"], test_word_vector["1"]),
            ]
            results[test_word]["euclidean_distance"] = [
                self.euclidean_distance(test_word_vector["1"], test_word_vector["2"]),
                self.euclidean_distance(test_word_vector["2"], test_word_vector["3"]),
                self.euclidean_distance(test_word_vector["3"], test_word_vector["1"]),
            ]
            results[test_word]["manhattan_distance"] = [
                self.manhattan_distance(test_word_vector["1"], test_word_vector["2"]),
                self.manhattan_distance(test_word_vector["2"], test_word_vector["3"]),
                self.manhattan_distance(test_word_vector["3"], test_word_vector["1"]),
            ]
        return results


if __name__ == "__main__":
    with open("sentences.json", encoding="utf-8") as fp:
        samples = json.load(fp)
        context_aware_word_vectors = ContextAwareWordVectors(model="bert-base-uncased")
        results = context_aware_word_vectors.run(samples)
        print(json.dumps(results, indent=2, cls=NumpyFloatValuesEncoder))
