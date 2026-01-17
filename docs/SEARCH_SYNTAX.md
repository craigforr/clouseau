# Clouseau Search Syntax

## Basic Search

Simple text search across all conversations:

```
hello world
```

## Field-Specific Search

Search within specific fields:

```
user:hello
assistant:goodbye
```

## Operators

### AND (default)
```
hello world  # finds messages with both words
```

### OR
```
hello OR world
```

### NOT
```
hello NOT world
```

### Phrases
```
"exact phrase"
```

## Filters

### Date Range
```
date:2024-01-01..2024-12-31
```

### Session
```
session:abc123
```

### Model
```
model:claude-3
```

## Examples

```
user:"how do I" model:claude-3 date:2024-01-01..
```
