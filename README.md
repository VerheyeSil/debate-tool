# debate-tool

Simulate Dutch political debates between LLM agents. Each agent represents a
party and argues from that party's documented core values and policies, while a
moderator agent (the *voorzitter*) leads the debate like in the Tweede Kamer.

The long-term goal is to compare these "policy-pure" AI debates with real
Tweede Kamer debates, to see where real debates drift away from substance.

The debate itself is in Dutch.

## Features

- Moderator agent that introduces the topic, gives each party the floor and
  summarises the main disagreements at the end
- Party agents built from per-party data files (core values, key policies,
  optional election programme text and extra positions)
- Every participant hears the whole debate, so parties can respond to each
  other and the moderator summarises what was actually said
- Responses stream live to the terminal, with each speaker's name in bold
- Bundled party data for **GroenLinks** and **VVD**

## Not implemented yet

- More parties (PvdA, CDA, D66, ...): only GroenLinks and VVD have data
- The `verkiezingsprogramma.txt` and `standpunten.txt` files are still empty
- Retrieval (RAG) over full party documents; only the first 2000 characters of
  the election programme are used
- Comparing simulated debates with real Tweede Kamer debates
- Debate quality metrics and saving transcripts to a file
- Command-line options: the topic, parties and number of rounds are set in
  `src/debate_tool/cli.py`

## Setup

Requires Python 3.10+ and an [OpenAI API key](https://platform.openai.com/api-keys).

```bash
git clone https://github.com/VerheyeSil/debate-tool.git
cd debate-tool
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
cp .env.example .env             # then put your key in .env
```

## Usage

```bash
debate-tool
# or
python -m debate_tool
```

This runs one round of a debate between GroenLinks and VVD on
*"Moet Nederland een vermogensbelasting invoeren?"* using `gpt-4o-mini`.

To change the debate, edit the constants at the top of `src/debate_tool/cli.py`:

```python
TOPIC = "Moet Nederland een vermogensbelasting invoeren?"
PARTIES = ["GroenLinks", "VVD"]
```

and `num_rounds` in the `run_debate(...)` call.

### Adding a party

Create a folder `src/debate_tool/data/parties/<party_name>/` (lowercase, spaces
as underscores) with:

| File | Contents |
| --- | --- |
| `context.json` | `party_name`, a list of `core_values` and a dict of `key_policies` (required) |
| `verkiezingsprogramma.txt` | Text from the election programme (optional) |
| `standpunten.txt` | Extra positions as free text (optional) |

`scripts/create_party_data.py` shows how the GroenLinks and VVD folders were
made; running it regenerates their `context.json` files.

## Project structure

```
debate-tool/
├── pyproject.toml
├── scripts/
│   └── create_party_data.py     # creates the party data folders
├── src/debate_tool/
│   ├── cli.py                   # entry point: topic, parties, rounds
│   ├── debate_manager.py        # runs the debate and keeps the transcript
│   ├── parties.py               # loads party data
│   ├── openai_client.py         # OpenAI chat completions (with streaming)
│   ├── agents/
│   │   ├── base_agent.py        # system prompt + conversation history
│   │   ├── debater.py           # Debater and PartyDebater
│   │   └── moderator.py         # the voorzitter
│   └── data/parties/            # one folder per party
└── tests/
```

## Running tests

```bash
pip install -e ".[dev]"
pytest
```

The tests use a fake LLM client, so they need no API key and make no network
calls.

## Credits

Written by Sil Verheye. The party positions in `data/parties` are my own short
summaries of each party's views, not official party texts.

Uses the [OpenAI Python library](https://github.com/openai/openai-python) and
[python-dotenv](https://github.com/theskumar/python-dotenv).

## License

[MIT](LICENSE)
