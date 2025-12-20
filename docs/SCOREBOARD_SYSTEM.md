# Scoreboard System Documentation

## Overview
The scoreboard system tracks and persists high scores across game sessions, allowing players to compete for the best scores. Scores are calculated based on tactical performance (avoiding losses) and speed (fast victories earn bonuses).

## Score Calculation

### Formula
**Final Score = Tactical Score + Time Bonus**

Where:
- **Tactical Score** = 100 - (Tactical Penalties)
- **Time Bonus** = Speed-based bonus (0-50 points)

### Tactical Penalties
- **Lost Battle** (attack repelled): -5 points
- **Lost Planet** (conquered by enemy): -10 points
- **Minimum Tactical Score**: 0

### Time Bonuses
Speed matters! Fast, decisive victories are rewarded:
- **Under 60 seconds**: +50 bonus (Perfect speedrun! ⚡)
- **Under 2 minutes**: +30 bonus (Very fast 🚀)
- **Under 3 minutes**: +15 bonus (Fast ⏱️)
- **Under 5 minutes**: +5 bonus (Moderate 🐢)
- **5+ minutes**: No time bonus

### Score Range
- **Maximum Score**: 150 (100 tactical + 50 time bonus)
- **Perfect Game**: 150 points (no losses, under 60 seconds)
- **Defeat**: 0 points (always)
- **Cheater**: "CHEATER" displayed in red

## Components

### 1. `game/scoreboard.py`
**Scoreboard** class manages score persistence and retrieval.

**Methods:**
- `load_scores()`: Loads scores from JSON file
- `save_scores()`: Saves scores to JSON file
- `add_score()`: Adds a new score entry with all game statistics
- `get_top_scores(limit=10)`: Returns top legitimate scores (excludes cheaters)
- `get_all_scores(limit=50)`: Returns all scores including cheaters (cheaters at end)

**Score Entry Format:**
```python
{
    'player_name': str,
    'score': int or "CHEATER",
    'planets_controlled': int,
    'ships_produced': int,
    'battles_won': int,
    'battles_lost': int,
    'victory': bool,
    'is_cheater': bool,
    'timestamp': ISO format string
}
```

### 2. `game/scoreboard_menu.py`
**ScoreboardMenu** class displays the high scores table.

**Features:**
- Displays top 10 scores in a formatted table
- Color coding:
  - **White**: Legitimate victories
  - **Red**: Cheaters (win button pressed)
  - **Gray**: Defeats
- Columns: Rank, Player, Score, Planets, Ships, Won, Lost
- Back button to return to main menu

### 3. Score Calculation in `game/game_state.py`

**Initialization:**
- `self.base_score = 100`: Starting tactical score
- `self.tactical_penalties = 0`: Accumulated penalties
- `self.game_time = 0`: Elapsed time in seconds

**Penalty Tracking:**
Penalties are accumulated in `self.tactical_penalties`:
- Lost battle: +5 penalty
- Lost planet: +10 penalty

**Final Score Calculation:**
The `calculate_final_score()` method computes:
```python
tactical_score = max(0, base_score - tactical_penalties)
time_bonus = calculate_time_bonus(game_time)
final_score = tactical_score + time_bonus
```

**Time Bonus Logic:**
```python
if game_time < 60:    time_bonus = 50
elif game_time < 120:  time_bonus = 30
elif game_time < 180:  time_bonus = 15
elif game_time < 300:  time_bonus = 5
else:                  time_bonus = 0
```

### 4. Integration in `main.py`

**States:**
- Added "scoreboard" state to game state machine
- Scoreboard menu accessible from main menu

**Score Saving:**
- Automatically saves score when game ends (victory or defeat)
- Saves "CHEATER" entry if win button is pressed
- Includes player name from config

## Usage

### For Players
1. From main menu, click "Scoreboard" to view high scores
2. Complete a game to add your score
3. Try to achieve a perfect 100 score!
4. Scores persist between game sessions

### For Developers
```python
# Create scoreboard instance
scoreboard = Scoreboard()

# Add a score
scoreboard.add_score(
    player_name="Alice",
    score=85,
    planets_controlled=5,
    ships_produced=120,
    battles_won=8,
    battles_lost=2,
    victory=True,
    is_cheater=False
)

# Get top scores
top_scores = scoreboard.get_top_scores(limit=10)

# Get all scores including cheaters
all_scores = scoreboard.get_all_scores(limit=50)
```

## File Storage
- Scores saved to: `scoreboard.json`
- Format: JSON array of score entries
- Automatically excluded from git via `.gitignore`

## Strategy Tips for Players
To achieve high scores:
1. **Perfect Score (150)**: Win in under 60 seconds without any losses! ⚡
2. **High Scores (125-149)**: Fast victory (60-120s) with minimal losses
3. **Good Scores (100-124)**: Clean tactical play OR moderate speed
4. **Decent Scores (75-99)**: Some mistakes but solid fundamentals
5. **Low Scores (1-74)**: Many setbacks or very slow victories

**Key Strategies:**
- **Speed Matters**: Every second counts! Fast victories can offset tactical mistakes
- **Minimize Losses**: Each lost battle costs 5 points
- **Protect Planets**: Losing a planet costs 10 points (2x a battle)
- **Use Abilities Wisely**: Shield can prevent costly planet losses
- **Balance Risk vs Speed**: Sometimes an aggressive play for speed is worth a small penalty
- **Know the Thresholds**: 60s, 120s, 180s, and 300s are critical time breakpoints

## Future Enhancements (Ideas)
- Difficulty multipliers (harder AI = higher score potential)
- Map size multipliers (larger maps = higher score potential)
- Online leaderboards
- Score statistics and trends
- Personal best tracking per difficulty/size

