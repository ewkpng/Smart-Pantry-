# Smart Pantry

Smart Pantry is a Python/Tkinter household food-management prototype created for UTS 52685 Creative Coding. It brings inventory, expiry tracking, shopping recommendations, meal attendance and grocery budgeting into one local application.

## Core features

- Add, view, update and delete food inventory entries.
- Keep multiple batches of the same food separate using unique IDs and different expiry dates.
- Track expiry dates and generate food alerts.
- Organise food into Fridge / Fresh, Pantry and Frozen categories.
- Support both price-per-item and price-per-kilogram food.
- Create and manage a shopping list.
- Mark regular household foods and generate low-stock recommendations.
- Record persistent lunch and dinner responses for household members.
- Create meal-update messages that can be cleared without deleting the meal-board status.
- Set a weekly grocery budget and compare it with spending and estimated shopping-list costs.
- Automatically save and reload data using JSON.
- Use a basic Tkinter graphical interface.

## Requirements

- Python 3
- Tkinter

No pip packages are required. The project uses Python standard-library modules only.

## Run the project

### macOS

Open Terminal in the project folder and run:

```bash
python3 Smart_Pantry_Final.py
```

If VS Code Code Runner tries to use `python` and shows `command not found`, configure it to use `python3`.

### Windows

Run either:

```bash
python Smart_Pantry_Final.py
```

or:

```bash
py Smart_Pantry_Final.py
```

## Automatic saving

Smart Pantry creates `smart_pantry_data.json` beside the Python file when data is saved. This file contains inventory, shopping-list information, regular-item settings, meal plans, messages, budget values and ID counters.

The file is ignored by Git because it is user/runtime data. To reset Smart Pantry completely, close the program and delete `smart_pantry_data.json`.

## Repository structure

```text
Smart_Pantry_GitHub_Ready/
├── Smart_Pantry_Final.py       # final prototype
├── README.md                   # project and run instructions
├── TEST_RESULTS.txt            # final regression-test summary
├── .gitignore                  # ignores runtime/cache files
├── docs/
│   ├── MANUAL_TEST_CHECKLIST.md
│   └── 3_MINUTE_EXPLAINER_SCRIPT.txt
└── drafts/                     # earlier development milestones
```

## Current limitations

- Smart Pantry is a local single-device prototype, not a shared online application.
- The Tkinter interface is intentionally basic.
- Fridge and Fresh are currently combined into one category.
- Frozen foods do not separately track a bag/container and the number of portions inside it.
- Prices are entered manually rather than retrieved from stores.
- The program does not support simultaneous editing by multiple household members.

## Future development

Possible future improvements include separating Fresh and Fridge, adding more flexible measurement units such as grams, millilitres and portions, improving frozen-bag tracking, and eventually supporting shared/cloud data.


## Development drafts
Previous versions are grouped into `drafts/Week 1` through `drafts/Week 8`. See `drafts/Draft Guide.txt` for a short description of each milestone.
