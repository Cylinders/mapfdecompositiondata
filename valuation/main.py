from pathlib import Path

from torch import Tensor
from typing import NamedTuple

from benchmark_format_parser import parse_map_from, parse_scenario_from
from bfs import shortest_path_bfs
from cutter import up_to_n_cuts
from inference import infer
from mapfaster_input_transform import encode_cuts
from selector import select_cut_fair
from structs import Agent, Grid, GridPath
import torch.nn.functional as F

class Problem(NamedTuple):
    map: Grid
    scenario: list[Agent]


def minimal_paths_for(agents: list[Agent], map: Grid) -> dict[Agent, GridPath]:
    return {
        agent: shortest_path_bfs(map, agent.start, agent.goal)
        for agent in agents
    }


def main():
    map = parse_map_from(Path("..\maps\Boston_0_256.map"))
    scenario = parse_scenario_from(Path("..\scenes\scen-even\Boston_0_256-even-20.scen"))

    p = Problem(map, scenario[:50])
    ccpd(p)

    return


type Cut = list[list[Agent]]
type CutOutput = list[list[float]]


def associate_cut_outputs(
        batch_cuts: list[Cut],
        output: Tensor,
) -> list[tuple[Cut, CutOutput]]:
    flat_outputs: list[list[float]] = output.detach().cpu().tolist()

    result: list[tuple[Cut, CutOutput]] = []
    i = 0

    for cut in batch_cuts:
        n_groups = len(cut)
        cut_output = flat_outputs[i:i + n_groups]
        result.append((cut, cut_output))
        i += n_groups

    assert i == len(flat_outputs)
    return result


def ccpd(p: Problem):
    paths = minimal_paths_for(p.scenario, p.map)

    # batch_cuts = epsilon_cut(2, scenario)
    batch_cuts: list[list[list[Agent]]] = up_to_n_cuts(20, p.scenario)
    # batch_cuts = no_cut(p.scenario)

    tensor: Tensor = encode_cuts(p.map, paths, batch_cuts)

    output = infer(tensor)
    print(F.softmax(output))

    cut_to_output = associate_cut_outputs(batch_cuts, output)

    print(select_cut_fair(cut_to_output)[1])

    return


if __name__ == "__main__":
    main()
