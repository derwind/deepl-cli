# deepl-cli
Universal Command Line Interface for DeepL APIs

## Configuration

Place your DeepL authentication key in `~/.deepl/credentials`:

```ini
[default]
auth_key = YOUR_AUTH_KEY
```

Alternatively, pass the key directly with the `-k` / `--key` option on any command.

---

## CLI Reference

### Global Options

| Option | Description |
|---|---|
| `-k`, `--key AUTH_KEY` | DeepL authentication key (overrides credentials file) |

---

### `translate` — Request Translation

Translate text from a source language to a target language.

```
deepl translate --text TEXT [--source LANGUAGE] [--target LANGUAGE] [--glossary_id GLOSSARY] [-k AUTH_KEY]
```

| Option | Default | Description |
|---|---|---|
| `--text TEXT` | *(required)* | Text to translate |
| `--source LANGUAGE` | `en` | Source language code |
| `--target LANGUAGE` | `ja` | Target language code |
| `--glossary_id GLOSSARY` | `None` | Glossary ID to apply during translation |
| `-k AUTH_KEY` | credentials file | DeepL authentication key |

**Example:**

```sh
deepl translate --text "Hello, world!" --source en --target ja
```

---

### `glossary-language-pairs` — List Language Pairs Supported by Glossaries

List all language pairs that can be used when creating a glossary.

```
deepl glossary-language-pairs [-k AUTH_KEY]
```

**Example:**

```sh
deepl glossary-language-pairs
```

---

### `create-glossary` — Create a Glossary

Create a new glossary with term pairs.

```
deepl create-glossary --name NAME (--entries ENTRIES | --glossary_files FILE [FILE ...]) \
    [--source LANGUAGE] [--target LANGUAGE] [--entries_format FORMAT] [-k AUTH_KEY]
```

| Option | Default | Description |
|---|---|---|
| `--name NAME` | *(required)* | Name of the glossary |
| `--entries ENTRIES` | *(mutually exclusive)* | Term pairs as a CSV string |
| `--glossary_files FILE` | *(mutually exclusive)* | TSV file(s) containing term pairs (repeatable) |
| `--source LANGUAGE` | `en` | Source language code |
| `--target LANGUAGE` | `ja` | Target language code |
| `--entries_format FORMAT` | `csv` | Format of the entries (`csv` or `tsv`) |
| `-k AUTH_KEY` | credentials file | DeepL authentication key |

TSV glossary files use tab-separated columns. Lines beginning with `#` are treated as comments and ignored.

**Example:**

```sh
deepl create-glossary --name "MyGlossary" --glossary_files terms.tsv --source en --target ja
```

---

### `list-glossaries` — List All Glossaries

Retrieve a list of all glossaries associated with the account.

```
deepl list-glossaries [-k AUTH_KEY]
```

**Example:**

```sh
deepl list-glossaries
```

---

### `retrieve-glossary` — Retrieve Glossary Details

Get metadata for a specific glossary by its ID.

```
deepl retrieve-glossary --glossary_id GLOSSARY [-k AUTH_KEY]
```

| Option | Default | Description |
|---|---|---|
| `--glossary_id GLOSSARY` | *(required)* | ID of the glossary |
| `-k AUTH_KEY` | credentials file | DeepL authentication key |

**Example:**

```sh
deepl retrieve-glossary --glossary_id xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

---

### `retrieve-glossary-entries` — Retrieve Glossary Entries

Get the term pairs stored in a specific glossary (returned as TSV).

```
deepl retrieve-glossary-entries --glossary_id GLOSSARY [-k AUTH_KEY]
```

| Option | Default | Description |
|---|---|---|
| `--glossary_id GLOSSARY` | *(required)* | ID of the glossary |
| `-k AUTH_KEY` | credentials file | DeepL authentication key |

**Example:**

```sh
deepl retrieve-glossary-entries --glossary_id xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

---

### `delete-glossary` — Delete a Glossary

Permanently delete a glossary by its ID.

```
deepl delete-glossary --glossary_id GLOSSARY [-k AUTH_KEY]
```

| Option | Default | Description |
|---|---|---|
| `--glossary_id GLOSSARY` | *(required)* | ID of the glossary |
| `-k AUTH_KEY` | credentials file | DeepL authentication key |

**Example:**

```sh
deepl delete-glossary --glossary_id xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

---

## Python API Reference

All functions are available in the `deeplcli.deepl` module.

### `translate`

```python
translate(
    source_lang: str,
    target_lang: str,
    text: str,
    glossary_id: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> Optional[str]
```

Translate `text` from `source_lang` to `target_lang`. Returns the translated string, or `None` on failure.

---

### `glossary_language_pairs`

```python
glossary_language_pairs(auth_key: Optional[str] = None) -> Optional[str]
```

Return a JSON string listing language pairs supported for glossaries.

---

### `create_glossary`

```python
create_glossary(
    source_lang: str,
    target_lang: str,
    name: str,
    entries: Optional[str] = None,
    glossary_files: Optional[List[str]] = None,
    entries_format: str = 'csv',
    auth_key: Optional[str] = None,
) -> Optional[str]
```

Create a glossary. Supply either `entries` (a CSV/TSV string) or `glossary_files` (a list of TSV file paths). Returns a JSON string with the created glossary metadata, or `None` on failure.

---

### `list_glossaries`

```python
list_glossaries(auth_key: Optional[str] = None) -> Optional[str]
```

Return a JSON string listing all glossaries for the account.

---

### `retrieve_glossary`

```python
retrieve_glossary(glossary_id: str, auth_key: Optional[str] = None) -> Optional[str]
```

Return a JSON string with metadata for the specified glossary.

---

### `retrieve_glossary_entries`

```python
retrieve_glossary_entries(glossary_id: str, auth_key: Optional[str] = None) -> Optional[str]
```

Return the entries of the specified glossary as a tab-separated string.

---

### `delete_glossary`

```python
delete_glossary(glossary_id: str, auth_key: Optional[str] = None) -> Optional[str]
```

Delete the specified glossary. Returns an empty string on success, or `None` on failure.

---

### `read_glossaries`

```python
read_glossaries(glossary_files: List[str]) -> str
```

Read one or more TSV glossary files and return a CSV-formatted string of term pairs suitable for use as `entries` in `create_glossary`. Lines beginning with `#` are ignored.
