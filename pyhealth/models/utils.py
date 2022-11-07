from typing import List

import torch


def batch_to_multihot(label: List[List[int]], num_labels: int) -> torch.tensor:
    """Converts label to multihot format.

    Args:
        label: [batch size, *]
        num_labels: total number of labels

    Returns:
        multihot: [batch size, num_labels]
    """
    multihot = torch.zeros((len(label), num_labels))
    for i, l in enumerate(label):
        multihot[i, l] = 1
    return multihot


def get_last_visit(hidden_states, mask):
    """get the last visit from the sequence model
    INPUT:
        - hidden_states: [batch size, seq len, hidden_size]
        - mask: [batch size, seq len]
    OUTPUT:
        - last_visit: [batch size, hidden_size]

    EXAMPLE:
        - mask = [[1, 1, 1, 0, 0], [1, 1, 0, 0, 0]]
        - then output = torch.Tensor([[hidden_states[0, 2, :], hidden_states[1, 1, :]]])
    """
    last_visit = torch.sum(mask, 1) - 1
    last_visit = last_visit.unsqueeze(-1)
    last_visit = last_visit.expand(-1, hidden_states.shape[1] * hidden_states.shape[2])
    last_visit = torch.reshape(last_visit, hidden_states.shape)
    last_hidden_states = torch.gather(hidden_states, 1, last_visit)
    last_hidden_state = last_hidden_states[:, 0, :]
    return last_hidden_state
