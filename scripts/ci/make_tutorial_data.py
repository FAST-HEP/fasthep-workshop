from __future__ import annotations

from pathlib import Path

import numpy as np
import uproot


def main() -> None:
    path = Path("data/tutorial/split-packages/events.root")
    path.parent.mkdir(parents=True, exist_ok=True)
    with uproot.recreate(path) as output:
        output["events"] = {
            "pt": np.array(
                [12.0, 18.0, 21.0, 28.0, 34.0, 47.0, 52.0, 66.0, 72.0, 84.0, 93.0, 105.0],
                dtype="f8",
            )
        }
    print(path)


if __name__ == "__main__":
    main()
