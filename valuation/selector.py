from structs import Agent

type Cut = list[list[Agent]]
type CutEvaluation = list[list[float]]


# fair
def select_cut_fair(
        cut_outputs: list[tuple[Cut, CutEvaluation]],
) -> tuple[Cut, CutEvaluation]:
    if not cut_outputs:
        raise ValueError("cut_outputs must not be empty")

    def cut_score(item: tuple[Cut, CutEvaluation]) -> tuple[float, float, float]:
        cut, evaluation = item

        if len(cut) != len(evaluation):
            raise ValueError("cut and evaluation must have same number of groups")

        # best score available for each group across algorithms
        group_best: list[float] = []

        for group, outputs in zip(cut, evaluation):
            if not group:
                raise ValueError("cut contains empty group")
            if not outputs:
                raise ValueError("evaluation contains empty output list")

            group_best.append(max(outputs))

        # 1. maximize worst group
        # 2. maximize average group quality
        # 3. maximize total quality
        return (
            min(group_best),
            sum(group_best) / len(group_best),
            sum(group_best),
        )

    return max(cut_outputs, key=cut_score)


# avg
def select_cut_avg(
        cut_outputs: list[tuple[Cut, CutEvaluation]],
) -> tuple[Cut, CutEvaluation]:
    assert cut_outputs

    def cut_score(item: tuple[Cut, CutEvaluation]) -> float:
        cut, output = item
        assert len(cut) == len(output)
        assert output

        scores: list[float] = [max(nodes) for nodes in output]
        return sum(scores) / len(scores)

    return max(cut_outputs, key=cut_score)
