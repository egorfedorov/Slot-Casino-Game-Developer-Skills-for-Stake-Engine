---
name: game-info-author
description: Create structured game info/rules content for slot games. Invoke when drafting game info sections, symbol payouts, bonus purchase rules, or required disclaimers.
---

# Game Info Author

Use this skill to produce consistent, studio-grade “Game Info” content for slot/casino games, aligned with Stake Engine compliance wording.

## Workflow

1. Capture game summary.
- Theme, core loop, and player goal.
- Required for “Об игре”.

2. Enumerate core features.
- Explain mechanics and states.
- Required for “Функции”.

3. Define symbol and payout rules.
- Provide payout table structure and conditions.
- Required for “Выплаты за символы”.

4. Specify special symbols.
- Wilds, Scatters, Bonus, Multipliers and their behaviors. 
- Required for “Специальные символы”.

5. Describe win methods.
- Lines, ways, clusters, scatter, or hybrid.
- Required for “Способы выигрыша”.

6. Explain bonus purchase if available.
- Price, eligibility, exclusions, and expected feature behavior.
- Required for “Покупка бонусов”.

7. Add general rules and additional info.
- Betting limits, controls, autoplay rules.
- Required for “Общие положения” and “Дополнительная информация”.

8. Append mandatory disclaimer.
- Use the exact disclaimer text provided below.

## Output Contract

Return a single structured block with these exact sections:

1. **Об игре**
2. **Функции**
3. **Выплаты за символы**
4. **Специальные символы**
5. **Способы выигрыша**
6. **Покупка бонусов**
7. **Общие положения**
8. **Дополнительная информация**
9. **General Disclaimer**

## General Disclaimer (Exact Text)

Malfunction voids all wins and plays. A consistent internet connection is required. In the event of a disconnection, reload the game to finish any uncompleted rounds. The expected return is calculated over many plays. The game display is not representative of any physical device and is for illustrative purposes only. Winnings are settled according to the amount received from the Remote Game Server and not from events within the web browser. TM and © 2025 Stake Engine.

## Execution Rules

- Keep all sections concise and player-facing.
- Never contradict math or feature logic.
- If a section is not applicable, state “Not available in this game”.
- Preserve the exact disclaimer text and punctuation.
